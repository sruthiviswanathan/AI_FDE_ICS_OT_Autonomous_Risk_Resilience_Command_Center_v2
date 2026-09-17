"""Telemetry quality and dual-clock ordering (FR-002, ADR-02). Read-only."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from functools import lru_cache

from ot_command.core.data_layer import load_telemetry, source_path
from ot_command.repository import rows

TELEMETRY_PATH = source_path("telemetry")
TAGS_PATH = "data/reference/tags.csv"


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


def _ingest_clock(event: dict) -> str | None:
    return event.get("ingest_time") or event.get("received_time")


@lru_cache(maxsize=1)
def _tag_engineering_units() -> dict[str, str]:
    return {r["tag_id"]: r["engineering_unit"] for r in rows(TAGS_PATH)}


@lru_cache(maxsize=1)
def _all_telemetry() -> tuple[dict, ...]:
    return load_telemetry()


def _enrich_event(event: dict) -> dict:
    row = dict(event)
    ingest = _ingest_clock(row)
    event_time = row.get("event_time")
    engineering_unit = _tag_engineering_units().get(row.get("tag_id", ""))
    if engineering_unit:
        row["engineering_unit"] = engineering_unit
        row["unit_mismatch"] = row.get("unit") != engineering_unit
    else:
        row["unit_mismatch"] = False

    if not row.get("ingest_time") and not row.get("received_time"):
        row["uncertainty"] = "ingest_time_missing"
    elif event_time and ingest:
        event_dt = _parse_ts(event_time)
        ingest_dt = _parse_ts(ingest)
        if event_dt and ingest_dt:
            lag = (ingest_dt - event_dt).total_seconds()
            row["ingest_lag_seconds"] = lag
            if lag < 0:
                row["temporal_anomaly"] = True
                row["uncertainty"] = row.get("uncertainty") or "ingest_before_event"
    return row


def order_events(events: list, *, clock: str = "event_time") -> list:
    if clock != "event_time":
        raise ValueError("only event_time ordering is permitted; received/ingest alone is forbidden")

    enriched = [_enrich_event(e) for e in events]
    return sorted(enriched, key=lambda e: e.get("event_time") or "")


def flag_temporal_anomalies(events: list) -> list:
    return [e for e in order_events(events) if e.get("temporal_anomaly") or e.get("uncertainty")]


def _filter_events(
    events: list[dict],
    *,
    plant_id: str | None = None,
    asset_id: str | None = None,
    tag_id: str | None = None,
) -> list[dict]:
    out = events
    if tag_id:
        out = [e for e in out if e.get("tag_id") == tag_id]
    if plant_id:
        prefix = f"{plant_id}-"
        out = [e for e in out if str(e.get("tag_id", "")).startswith(prefix)]
    if asset_id:
        out = [e for e in out if e.get("asset_id") == asset_id]
    return out


def _duplicate_packets(events: list[dict]) -> int:
    keys = Counter((x["tag_id"], x["event_time"], str(x["value"]), x["unit"]) for x in events)
    return sum(v - 1 for v in keys.values() if v > 1)


def _tagged_assets_for_plant(plant_id: str) -> set[str]:
    prefix = f"{plant_id}-"
    return {x["asset_id"] for x in _all_telemetry() if str(x.get("tag_id", "")).startswith(prefix)}


def _scoped_events(
    *,
    plant_id: str | None = None,
    asset_id: str | None = None,
    tag_id: str | None = None,
) -> tuple[list[dict], dict]:
    """Resolve telemetry scope. Most CMDB assets have no historian tags — fall back plant-wide."""
    all_events = list(_all_telemetry())
    scope: dict = {
        "requested": {"plant_id": plant_id, "asset_id": asset_id, "tag_id": tag_id},
        "effective": {"plant_id": plant_id, "asset_id": asset_id, "tag_id": tag_id},
        "scope_note": None,
        "tagged_assets_in_plant": len(_tagged_assets_for_plant(plant_id)) if plant_id else None,
    }
    if tag_id:
        return _filter_events(all_events, tag_id=tag_id), scope

    tele = _filter_events(all_events, plant_id=plant_id, asset_id=asset_id)
    if asset_id and not tele and plant_id:
        tagged = _tagged_assets_for_plant(plant_id)
        tele = _filter_events(all_events, plant_id=plant_id)
        scope["effective"]["asset_id"] = None
        scope["scope_note"] = (
            f"Asset {asset_id} has no historian tags "
            f"({len(tagged)} tagged assets in {plant_id}); showing plant scope."
        )
    return tele, scope


def telemetry_quality_summary(*, plant_id: str | None = None, asset_id: str | None = None) -> dict:
    tele, scope = _scoped_events(plant_id=plant_id, asset_id=asset_id)
    tags = _tag_engineering_units()
    unit_mismatches = sum(
        1 for x in tele if tags.get(x["tag_id"]) and x["unit"] != tags[x["tag_id"]]
    )
    ingest_lags = []
    for x in tele:
        ingest = _ingest_clock(x)
        if x.get("event_time") and ingest:
            event_dt = _parse_ts(x["event_time"])
            ingest_dt = _parse_ts(ingest)
            if event_dt and ingest_dt:
                ingest_lags.append((ingest_dt - event_dt).total_seconds())

    return {
        "bad_or_uncertain": sum(1 for x in tele if x["quality"] != "GOOD"),
        "duplicate_packets": _duplicate_packets(tele),
        "unit_mismatches": unit_mismatches,
        "total_events": len(tele),
        "scope": scope,
        "ingest_lag_seconds": {
            "p50": sorted(ingest_lags)[len(ingest_lags) // 2] if ingest_lags else None,
            "max": max(ingest_lags) if ingest_lags else None,
            "negative_count": sum(1 for lag in ingest_lags if lag < 0),
        },
        "quality_by_flag": dict(Counter(x["quality"] for x in tele)),
        "source_path": TELEMETRY_PATH,
        "note": "GOOD quality is not ProcessHealthy (OPEN-026); do not impute BAD to GOOD",
    }


def get_timeline(
    *,
    tag_id: str | None = None,
    plant_id: str | None = None,
    asset_id: str | None = None,
    order: str = "event_time",
    limit: int | None = None,
) -> dict:
    events, scope = _scoped_events(plant_id=plant_id, asset_id=asset_id, tag_id=tag_id)
    ordered = order_events(events, clock=order)
    if limit is not None and limit > 0:
        ordered = ordered[:limit]
    return {
        "scope": scope,
        "order": order,
        "count": len(ordered),
        "events": ordered,
    }
