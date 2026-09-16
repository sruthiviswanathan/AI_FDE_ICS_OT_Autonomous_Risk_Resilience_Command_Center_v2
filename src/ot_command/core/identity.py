"""Identity reconciliation (FR-001, ADR-01). Read-only; no CMDB winner."""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache

from ot_command.repository import rows

ASSETS_PATH = "data/raw/assets.csv"
ALIASES_PATH = "data/raw/asset_aliases.csv"
SHADOW_PATH = "data/shadow/ot_asset_inventory_FINAL_v8.csv"
TAGS_PATH = "data/reference/tags.csv"


def _provenance(source_path: str, record_id: str) -> dict:
    claim = "shadow" if "shadow" in source_path else "registered"
    return {
        "source_path": source_path,
        "record_id": record_id,
        "grain": "asset_id",
        "claim_type": claim,
        "freshness": "workshop-static",
    }


@lru_cache(maxsize=1)
def _assets_by_id() -> dict[str, dict]:
    return {r["asset_id"]: r for r in rows(ASSETS_PATH)}


@lru_cache(maxsize=1)
def _shadow_by_id() -> dict[str, dict]:
    return {r["asset_id"]: r for r in rows(SHADOW_PATH)}


@lru_cache(maxsize=1)
def _tagged_assets() -> set[str]:
    return {r["asset_id"] for r in rows(TAGS_PATH)}


@lru_cache(maxsize=1)
def _alias_rows() -> list[dict]:
    return rows(ALIASES_PATH)


@lru_cache(maxsize=1)
def _alias_index() -> dict[str, list[dict]]:
    idx: dict[str, list[dict]] = defaultdict(list)
    for row in _alias_rows():
        idx[row["alias"]].append(row)
    return dict(idx)


@lru_cache(maxsize=1)
def _aliases_by_asset() -> dict[str, list[dict]]:
    by_asset: dict[str, list[dict]] = defaultdict(list)
    for row in _alias_rows():
        by_asset[row["asset_id"]].append(
            {
                "source": row["source"],
                "alias": row["alias"],
                "provenance": _provenance(ALIASES_PATH, row["asset_id"]),
            }
        )
    return dict(by_asset)


def _state_conflict(registered: str, observed: str) -> bool:
    return registered == "ACTIVE" and observed in {"OFFLINE", "UNSEEN"}


def _alias_collision_asset_ids(alias: str) -> set[str]:
    return {r["asset_id"] for r in _alias_index().get(alias, [])}


def _build_conflicts(asset_id: str, registered: str, observed: str) -> list[dict]:
    conflicts: list[dict] = []
    if _state_conflict(registered, observed):
        conflicts.append(
            {
                "conflict_id": f"{asset_id}-REG-OBS",
                "type": "REGISTERED_VS_OBSERVED",
                "left_value": registered,
                "right_value": observed,
                "rule_id": "BR-01",
            }
        )
    seen_aliases: set[str] = set()
    for entry in _aliases_by_asset().get(asset_id, []):
        alias = entry["alias"]
        if alias in seen_aliases:
            continue
        seen_aliases.add(alias)
        peers = sorted(_alias_collision_asset_ids(alias) - {asset_id})
        if peers:
            conflicts.append(
                {
                    "conflict_id": f"{asset_id}-ALIAS-{alias}",
                    "type": "ALIAS_COLLISION",
                    "left_value": asset_id,
                    "right_value": peers,
                    "rule_id": "ADR-01",
                }
            )
    return conflicts


def resolve_alias(alias: str) -> dict:
    rows_for_alias = _alias_index().get(alias, [])
    asset_ids = sorted({r["asset_id"] for r in rows_for_alias})
    is_collision = len(asset_ids) > 1
    sources = sorted({r["source"] for r in rows_for_alias})
    primary_source = "PASSIVE" if "PASSIVE" in sources else (sources[0] if sources else None)

    evidence = [
        {
            "source_path": ALIASES_PATH,
            "record_id": row["asset_id"],
            "field": "alias",
            "value": alias,
            "source": row["source"],
        }
        for row in rows_for_alias
    ]

    candidates = []
    assets = _assets_by_id()
    shadow = _shadow_by_id()
    for aid in asset_ids:
        asset = assets.get(aid) or shadow.get(aid)
        row_sources = sorted({r["source"] for r in rows_for_alias if r["asset_id"] == aid})
        candidates.append(
            {
                "asset_id": aid,
                "sources": row_sources,
                "registered_state": asset.get("registered_state") if asset else None,
                "observed_state": asset.get("observed_state") if asset else None,
            }
        )

    confidence = 0.4 if is_collision else (0.75 if asset_ids else 0.0)

    return {
        "alias": alias,
        "source": primary_source,
        "confidence": confidence,
        "evidence": evidence,
        "candidates": candidates,
        "merged": False,
        "cmdb_winner": False,
        "collision": is_collision,
    }


def get_identity_bundle(asset_id: str) -> dict:
    assets = _assets_by_id()
    shadow = _shadow_by_id()
    record = assets.get(asset_id)
    shadow_record = shadow.get(asset_id)
    if not record and not shadow_record:
        raise KeyError(asset_id)

    base = dict(record or shadow_record)
    primary_path = ASSETS_PATH if record else SHADOW_PATH

    shadow_overlay = None
    if shadow_record:
        shadow_overlay = {
            "source": "shadow",
            "source_path": SHADOW_PATH,
            "confidence": 0.3,
            "note": "shadow spreadsheet is competing evidence only; not CMDB winner",
        }
        if record:
            diffs = {
                k: {"assets": record.get(k), "shadow": shadow_record.get(k)}
                for k in record
                if record.get(k) != shadow_record.get(k)
            }
            if diffs:
                shadow_overlay["field_diffs"] = diffs

    registered = base["registered_state"]
    observed = base["observed_state"]
    conflicts = _build_conflicts(asset_id, registered, observed)

    return {
        "asset_uid": asset_id,
        "plant_id": base.get("plant_id"),
        "asset_type": base.get("asset_type"),
        "registered_state": registered,
        "observed_state": observed,
        "firmware_declared": base.get("firmware"),
        "firmware_observed": "UNKNOWN",
        "asset_criticality": base.get("criticality"),
        "zone": base.get("zone"),
        "owner": base.get("owner"),
        "aliases": _aliases_by_asset().get(asset_id, []),
        "shadow_overlay": shadow_overlay,
        "unit_join_missing": asset_id not in _tagged_assets(),
        "conflicts": conflicts,
        "state_conflict": _state_conflict(registered, observed),
        "provenance": _provenance(primary_path, asset_id),
        "legacy_v1_operational_state": None,
        "cmdb_winner": False,
        "merged": False,
    }


def list_identity_conflicts() -> dict:
    assets = rows(ASSETS_PATH)
    alias_counts = Counter(r["alias"] for r in _alias_rows())
    alias_collisions = sum(1 for count in alias_counts.values() if count > 1)
    asset_state_conflicts = sum(
        1
        for a in assets
        if a["registered_state"] == "ACTIVE" and a["observed_state"] in {"OFFLINE", "UNSEEN"}
    )
    collision_aliases = sorted(alias for alias, count in alias_counts.items() if count > 1)
    return {
        "alias_collisions": alias_collisions,
        "asset_state_conflicts": asset_state_conflicts,
        "collision_aliases": collision_aliases,
        "winner": None,
    }


def v1_field_observation(asset_id: str) -> dict:
    """Map canonical bundle to v1 contract fields — observations, not SoR."""
    bundle = get_identity_bundle(asset_id)
    return {
        "assetId": bundle["asset_uid"],
        "fwVersion": bundle["firmware_declared"],
        "operationalState": bundle["legacy_v1_operational_state"],
        "_note": "operationalState is side-field only; not ObservedState (OPEN-009, ADR-10)",
    }


def v2_field_observation(asset_id: str) -> dict:
    """Map canonical bundle to v2 contract fields — observations, not SoR."""
    bundle = get_identity_bundle(asset_id)
    return {
        "asset_id": bundle["asset_uid"],
        "firmware": bundle["firmware_declared"],
        "observed_state": bundle["observed_state"],
    }
