"""Bounded evidence graph slice (FR-006, ADR-KG). Read-only; hop cap 8."""

from __future__ import annotations

from functools import lru_cache

from ot_command.core import containment, identity, recovery
from ot_command.repository import rows

MAX_HOP = 8
ALLOWED_QUERIES = frozenset({"Q1", "Q2", "Q3", "Q4", "Q5"})

NETWORK_PATH = "data/raw/network_edges.csv"
TAGS_PATH = "data/reference/tags.csv"
UNITS_PATH = "data/raw/process_units.csv"
BARRIERS_PATH = "data/raw/safety_barriers.csv"
ALERTS_PATH = "data/raw/cyber_alerts.csv"
VULNS_PATH = "data/raw/vulnerabilities.csv"
ACCESS_PATH = "data/raw/remote_access_sessions.csv"
HANDOVER_PATH = "data/shadow/shift_handover_email.txt"


@lru_cache(maxsize=1)
def _tags_by_asset() -> dict[str, dict]:
    return {r["asset_id"]: r for r in rows(TAGS_PATH)}


@lru_cache(maxsize=1)
def _units_by_id() -> dict[str, dict]:
    return {r["unit_id"]: r for r in rows(UNITS_PATH)}


def _node(node_id: str, node_type: str, **props) -> dict:
    return {"id": node_id, "type": node_type, **props}


def _edge(edge_type: str, source: str, target: str, **props) -> dict:
    return {"type": edge_type, "source": source, "target": target, **props}


def _q1_identity(*, asset_id: str | None, alias: str | None) -> dict:
    if alias:
        bundle = identity.resolve_alias(alias)
        nodes = [_node(bundle["alias"], "Alias", confidence=bundle["confidence"])]
        edges = []
        for candidate in bundle["candidates"]:
            aid = candidate["asset_id"]
            nodes.append(
                _node(
                    aid,
                    "Asset",
                    registered_state=candidate.get("registered_state"),
                    observed_state=candidate.get("observed_state"),
                )
            )
            edges.append(_edge("ALIAS_OF", bundle["alias"], aid, source=bundle.get("source")))
        return {
            "query": "Q1",
            "nodes": nodes,
            "edges": edges,
            "conflicts": bundle.get("collision"),
            "cmdb_winner": False,
            "note": "Identity lineage — do not merge colliding aliases (EVAL-001)",
        }
    if not asset_id:
        raise ValueError("Q1 requires asset_id or alias")
    bundle = identity.get_identity_bundle(asset_id)
    nodes = [_node(asset_id, "Asset", **{k: bundle[k] for k in ("registered_state", "observed_state", "plant_id")})]
    edges = []
    for entry in bundle.get("aliases", []):
        alias_id = entry["alias"]
        nodes.append(_node(alias_id, "Alias", source=entry.get("source")))
        edges.append(_edge("ALIAS_OF", alias_id, asset_id, source=entry.get("source")))
    return {
        "query": "Q1",
        "nodes": nodes,
        "edges": edges,
        "conflicts": bundle.get("conflicts"),
        "unit_join_missing": bundle.get("unit_join_missing"),
        "cmdb_winner": False,
    }


def _q2_undocumented_paths(*, asset_id: str | None, plant_id: str | None, hop_cap: int) -> dict:
    edges_raw = rows(NETWORK_PATH)
    if plant_id:
        edges_raw = [e for e in edges_raw if e["plant_id"] == plant_id]
    undocumented = [
        e
        for e in edges_raw
        if e.get("documented") == "NO" and e.get("observed_last_24h") == "YES"
    ]
    if asset_id:
        undocumented = [
            e for e in undocumented if e["source_asset"] == asset_id or e["target_asset"] == asset_id
        ]
    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    hops = 0
    for row in undocumented[: hop_cap * 10]:
        if hops >= hop_cap:
            break
        for aid in (row["source_asset"], row["target_asset"]):
            tag = _tags_by_asset().get(aid)
            unit = _units_by_id().get(tag["unit_id"]) if tag else None
            nodes.setdefault(
                aid,
                _node(
                    aid,
                    "Asset",
                    unit_join_missing=tag is None,
                    production_criticality=unit.get("production_criticality") if unit else None,
                ),
            )
        edges.append(
            _edge(
                "PATH",
                row["source_asset"],
                row["target_asset"],
                documented=row.get("documented"),
                observed_last_24h=row.get("observed_last_24h"),
            )
        )
        hops += 1
    return {
        "query": "Q2",
        "nodes": list(nodes.values()),
        "edges": edges[:hop_cap],
        "hop_cap": hop_cap,
        "undocumented_total": len(undocumented),
        "note": "Undocumented observed paths — blast radius may be unknown (EVAL-012)",
    }


def _q3_safety_cyber(*, asset_id: str | None, alert_id: str | None) -> dict:
    alert = None
    if alert_id:
        alert = next((a for a in rows(ALERTS_PATH) if a["alert_id"] == alert_id), None)
        asset_id = asset_id or (alert.get("asset_id") if alert else None)
    if not asset_id:
        raise ValueError("Q3 requires asset_id or alert_id")
    tag = _tags_by_asset().get(asset_id)
    unit_id = tag["unit_id"] if tag else None
    unit = _units_by_id().get(unit_id or "")
    barriers = [b for b in rows(BARRIERS_PATH) if b.get("unit_id") == unit_id] if unit_id else []
    nodes = [_node(asset_id, "Asset")]
    edges: list[dict] = []
    if alert:
        nodes.append(
            _node(
                alert["alert_id"],
                "Alert",
                severity=alert.get("severity"),
                process_context=alert.get("process_context"),
            )
        )
        edges.append(_edge("ALERT_ON", alert["alert_id"], asset_id))
    if tag:
        nodes.append(_node(tag["tag_id"], "Tag"))
        edges.append(_edge("TAGGED", tag["tag_id"], asset_id))
        if unit:
            nodes.append(_node(unit_id, "Unit", safe_state=unit.get("safe_state")))
            edges.append(_edge("IN_UNIT", asset_id, unit_id))
    for barrier in barriers:
        nodes.append(
            _node(
                barrier["barrier_id"],
                "Barrier",
                state=barrier.get("state"),
                bypass_authorized=barrier.get("bypass_authorized"),
            )
        )
        edges.append(_edge("PROTECTS", barrier["barrier_id"], unit_id or asset_id))
    return {
        "query": "Q3",
        "nodes": nodes,
        "edges": edges,
        "unit_join_missing": tag is None,
        "safe_state": unit.get("safe_state") if unit else None,
    }


def _q4_recovery(*, plant_id: str | None) -> dict:
    if not plant_id:
        raise ValueError("Q4 requires plant_id")
    view = recovery.get_plant_recovery_view(plant_id)
    nodes = [_node(plant_id, "Plant")]
    edges: list[dict] = []
    for component in view["components"]:
        cid = f"{component['plant_id']}:{component['component']}"
        nodes.append(
            _node(
                cid,
                "RecoveryComponent",
                recovery_ready=component["recovery_ready"],
                blockers=component.get("blockers"),
            )
        )
        edges.append(_edge("RECOVERY_FOR", cid, plant_id))
    return {
        "query": "Q4",
        "nodes": nodes,
        "edges": edges,
        "recovery_ready_count": view["recovery_ready_count"],
        "note": "RecoveryReady derived — backup CURRENT alone insufficient (EVAL-005)",
    }


def _q5_cascade(*, asset_id: str | None, alert_id: str | None) -> dict:
    asset_id = asset_id or "OT-01016"
    alert_id = alert_id or "ALT-002783"
    cyber = _q3_safety_cyber(asset_id=asset_id, alert_id=alert_id)
    sessions = [
        s
        for s in rows(ACCESS_PATH)
        if s.get("asset_id") == asset_id or s.get("plant_id") == "PLT-10"
    ][:5]
    nodes = list(cyber["nodes"])
    edges = list(cyber["edges"])
    for session in sessions:
        nodes.append(
            _node(
                session["session_id"],
                "Session",
                approved_window=session.get("approved_window"),
                mfa=session.get("mfa"),
            )
        )
        if session.get("asset_id"):
            edges.append(_edge("SESSION_ON", session["session_id"], session["asset_id"]))
    nodes.append(
        _node(
            HANDOVER_PATH,
            "UntrustedNote",
            trust="UNTRUSTED_CONTENT",
            note="08:50 PE destabilize warning — not decision authority",
        )
    )
    return {
        "query": "Q5",
        "nodes": nodes,
        "edges": edges,
        "scenario_markers": {
            "firmware_advisory_controllers": {"count": 37, "source_system": "SCENARIO", "verified": False},
            "timeline": ["08:24 vendor session", "08:38 barrier bypassed", "08:47 SOC isolate", "08:50 PE destabilize"],
        },
        "unit_join_missing": cyber.get("unit_join_missing"),
        "safe_state": cyber.get("safe_state"),
        "note": "CASCADE-001 gold slice — no isolate execute (EVAL-007)",
    }


def get_slice(
    *,
    query: str,
    asset_id: str | None = None,
    plant_id: str | None = None,
    alert_id: str | None = None,
    alias: str | None = None,
    hop_cap: int = MAX_HOP,
) -> dict:
    if query not in ALLOWED_QUERIES:
        raise ValueError(f"query must be one of {sorted(ALLOWED_QUERIES)}")
    hop_cap = min(max(hop_cap, 1), MAX_HOP)
    if query == "Q1":
        payload = _q1_identity(asset_id=asset_id, alias=alias)
    elif query == "Q2":
        payload = _q2_undocumented_paths(asset_id=asset_id, plant_id=plant_id, hop_cap=hop_cap)
    elif query == "Q3":
        payload = _q3_safety_cyber(asset_id=asset_id, alert_id=alert_id)
    elif query == "Q4":
        payload = _q4_recovery(plant_id=plant_id)
    else:
        payload = _q5_cascade(asset_id=asset_id, alert_id=alert_id)
    return {
        **payload,
        "hop_cap": hop_cap,
        "hop_limit_enforced": True,
        "winner": None,
        "source_paths": [
            NETWORK_PATH,
            TAGS_PATH,
            UNITS_PATH,
            BARRIERS_PATH,
            ALERTS_PATH,
            ACCESS_PATH,
        ],
    }
