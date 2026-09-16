"""Identity bundle engine (ADR-01, ADR-10, FR-001). Read-only. No CMDB winner."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from ..repository import rows

ASSETS_PATH = "data/raw/assets.csv"
ALIASES_PATH = "data/raw/asset_aliases.csv"
SHADOW_PATH = "data/shadow/ot_asset_inventory_FINAL_v8.csv"
TAGS_PATH = "data/reference/tags.csv"
TRANSFORM = "enh-02-identity.1"
AS_OF = "2026-09-10T00:00:00Z"

_CACHE: dict[str, Any] | None = None


def _prov(source_system: str, source_path: str, confidence: float) -> dict:
    return {
        "source_system": source_system,
        "source_path": source_path,
        "extracted_at": AS_OF,
        "transform_version": TRANSFORM,
        "confidence": confidence,
        "clock_completeness": "PARTIAL",
        "quality_flag": "NA",
    }


def _state_disagreement(registered: str, observed: str) -> bool:
    if registered == "RETIRED" and observed == "ONLINE":
        return True
    if registered == "ACTIVE" and observed in {"OFFLINE", "UNSEEN"}:
        return True
    return False


def _load() -> dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    assets = {r["asset_id"]: r for r in rows(ASSETS_PATH)}
    aliases = rows(ALIASES_PATH)
    by_alias: dict[str, list[dict]] = defaultdict(list)
    by_asset_aliases: dict[str, list[dict]] = defaultdict(list)
    for row in aliases:
        by_alias[row["alias"]].append(row)
        by_asset_aliases[row["asset_id"]].append(row)
    shadow_rows = rows(SHADOW_PATH)
    shadow = {r["asset_id"]: r for r in shadow_rows}
    tagged = {r["asset_id"] for r in rows(TAGS_PATH)}
    _CACHE = {
        "assets": assets,
        "by_alias": by_alias,
        "by_asset_aliases": by_asset_aliases,
        "shadow": shadow,
        "shadow_n": len(shadow_rows),
        "tagged": tagged,
    }
    return _CACHE


def _collision_aliases() -> dict[str, list[dict]]:
    data = _load()
    out = {}
    for alias, recs in data["by_alias"].items():
        ids = {r["asset_id"] for r in recs}
        if len(ids) > 1:
            out[alias] = recs
    return out


def _confidence(*parts: float) -> float:
    return min(parts) if parts else 1.0


def shadow_overlay_status() -> dict:
    data = _load()
    return {
        "row_count": data["shadow_n"],
        "is_cmdb": False,
        "promoted_to_master": False,
        "confidence": 0.4,
        "source_path": SHADOW_PATH,
        "source_system": "SHADOW_SPREADSHEET",
        "note": "Evidence overlay only. OPEN-015. Shift email is untrusted.",
        "provenance": _prov("SHADOW_SPREADSHEET", SHADOW_PATH, 0.4),
    }


def reconcile_alias(alias: str) -> dict:
    data = _load()
    recs = list(data["by_alias"].get(alias, []))
    asset_ids = []
    seen = set()
    for rec in recs:
        aid = rec["asset_id"]
        if aid not in seen:
            seen.add(aid)
            asset_ids.append(aid)
    sources = [rec["source"] for rec in recs]
    collision = len(asset_ids) > 1
    conf = 0.5 if collision else (1.0 if asset_ids else 0.0)
    conflicts = []
    if collision:
        conflicts.append(
            {
                "conflict_id": f"ALIAS_COLLISION:{alias}",
                "type": "ALIAS_COLLISION",
                "left_value": asset_ids[0],
                "right_value": asset_ids[1:],
                "rule_id": "ADR-01",
            }
        )
    return {
        "alias": alias,
        "asset_ids": asset_ids,
        "sources": sources,
        "aliases": [
            {
                "source": rec["source"],
                "alias": rec["alias"],
                "asset_id": rec["asset_id"],
                "provenance": _prov(rec["source"], ALIASES_PATH, conf),
            }
            for rec in recs
        ],
        "identities": [
            {"asset_id": aid, "alias": alias, "source": "PASSIVE" if "PASSIVE" in sources else sources[0] if sources else None}
            for aid in asset_ids
        ],
        "confidence": conf,
        "winner": None,
        "canonical_source": None,
        "conflicts": conflicts,
        "provenance": _prov("ENGINE", "ot_command.core.identity.reconcile_alias", conf),
    }


def identity_bundle(asset_id: str) -> dict:
    data = _load()
    row = data["assets"].get(asset_id)
    if row is None:
        raise KeyError(asset_id)
    registered = row["registered_state"]
    observed = row["observed_state"]
    alias_rows = data["by_asset_aliases"].get(asset_id, [])
    collisions_for_asset = []
    coll_map = _collision_aliases()
    for rec in alias_rows:
        if rec["alias"] in coll_map:
            collisions_for_asset.append(rec["alias"])
    conflicts: list[dict] = []
    confs: list[float] = []
    if _state_disagreement(registered, observed):
        conflicts.append(
            {
                "conflict_id": f"REGISTERED_VS_OBSERVED:{asset_id}",
                "type": "REGISTERED_VS_OBSERVED",
                "left_value": registered,
                "right_value": observed,
                "rule_id": "ADR-01",
            }
        )
        confs.append(0.5)
    for alias in collisions_for_asset:
        ids = sorted({r["asset_id"] for r in coll_map[alias]})
        conflicts.append(
            {
                "conflict_id": f"ALIAS_COLLISION:{alias}",
                "type": "ALIAS_COLLISION",
                "left_value": ids[0],
                "right_value": ids[1:],
                "rule_id": "ADR-01",
            }
        )
        confs.append(0.5)
    shadow_row = data["shadow"].get(asset_id)
    shadow_overlay = None
    if shadow_row is not None:
        confs.append(0.4)
        diffs = {
            k: {"assets": row.get(k), "shadow": shadow_row.get(k)}
            for k in row
            if row.get(k) != shadow_row.get(k)
        }
        shadow_overlay = {
            "source_system": "SHADOW_SPREADSHEET",
            "confidence": 0.4,
            "is_cmdb": False,
            "promoted_to_master": False,
            "field_diffs": diffs,
        }
        conflicts.append(
            {
                "conflict_id": f"SHADOW_VS_ASSETS:{asset_id}",
                "type": "SHADOW_VS_ASSETS",
                "left_value": "assets.csv",
                "right_value": SHADOW_PATH,
                "rule_id": "ADR-01",
            }
        )
    conflicts.append(
        {
            "conflict_id": f"V1_OPERATIONALSTATE_UNMAPPED:{asset_id}",
            "type": "V1_OPERATIONALSTATE_UNMAPPED",
            "left_value": "operationalState",
            "right_value": None,
            "rule_id": "ADR-10",
        }
    )
    conf = _confidence(*confs) if confs else 1.0
    tagged = asset_id in data["tagged"]
    return {
        "asset_uid": asset_id,
        "asset_id": asset_id,
        "plant_id": row["plant_id"],
        "asset_type": row["asset_type"],
        "registered_state": registered,
        "observed_state": observed,
        "operational_interpretation": None,
        "firmware_declared": row["firmware"],
        "firmware_observed": "UNKNOWN",
        "asset_criticality": row["criticality"],
        "zone": row["zone"],
        "owner": row["owner"],
        "aliases": [
            {
                "source": a["source"],
                "alias": a["alias"],
                "asset_id": a["asset_id"],
                "provenance": _prov(a["source"], ALIASES_PATH, conf),
            }
            for a in alias_rows
        ],
        "shadow_overlay": shadow_overlay,
        "unit_join_missing": not tagged,
        "conflicts": conflicts,
        "confidence": conf,
        "winner": None,
        "canonical_source": None,
        "legacy_v1_operational_state": None,
        "observations": _observations(row),
        "provenance": _prov("ENGINE", "ot_command.core.identity.identity_bundle", conf),
    }


def _observations(row: dict) -> dict:
    """v1/v2/CSV names stay separate. operationalState is not ObservedState (OPEN-009)."""
    return {
        "v1": {
            "path": "/assets/{id}",
            "assetId": row["asset_id"],
            "fwVersion": row["firmware"],
            "operationalState": None,
            "unmapped": True,
            "open_decision": "OPEN-009",
        },
        "v2": {
            "path": "/ot-assets/{asset_id}",
            "asset_id": row["asset_id"],
            "firmware": row["firmware"],
            "observed_state": row["observed_state"],
        },
        "csv": {
            "path": ASSETS_PATH,
            "registered_state": row["registered_state"],
            "observed_state": row["observed_state"],
            "firmware": row["firmware"],
        },
    }


def asset_context(asset_id: str) -> dict:
    bundle = identity_bundle(asset_id)
    return bundle


def list_identity_conflicts() -> dict:
    data = _load()
    alias_collisions = []
    for alias, recs in sorted(_collision_aliases().items()):
        ids = sorted({r["asset_id"] for r in recs})
        alias_collisions.append(
            {
                "alias": alias,
                "asset_ids": ids,
                "sources": [r["source"] for r in recs],
                "confidence": 0.5,
                "winner": None,
            }
        )
    registered_vs_observed = []
    for aid, row in data["assets"].items():
        if _state_disagreement(row["registered_state"], row["observed_state"]):
            registered_vs_observed.append(
                {
                    "asset_id": aid,
                    "registered_state": row["registered_state"],
                    "observed_state": row["observed_state"],
                }
            )
    return {
        "alias_collisions": alias_collisions,
        "registered_vs_observed": registered_vs_observed,
        "shadow": shadow_overlay_status(),
        "winner": None,
        "canonical_source": None,
    }
