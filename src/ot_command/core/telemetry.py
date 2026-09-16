"""Telemetry dual-clock engine (ADR-02, FR-002). Read-only. GOOD ≠ ProcessHealthy."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Any

from ..repository import jsonl, rows

TELEMETRY_PATH = "data/telemetry/tag_telemetry.jsonl"
TAGS_PATH = "data/reference/tags.csv"
TRANSFORM = "enh-03-telemetry.1"
AS_OF = "2026-09-10T00:00:00Z"
TIMELINE_CAP = 500

_CACHE: dict[str, Any] | None = None


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    text = str(value).replace("Z", "")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _ingest_or_received(event: dict) -> str | None:
    return event.get("ingest_time") or event.get("received_time")


def _clocks(event: dict) -> tuple[datetime | None, datetime | None, str | None]:
    event_dt = _parse_ts(event.get("event_time"))
    ingest_raw = _ingest_or_received(event)
    ingest_dt = _parse_ts(ingest_raw)
    return event_dt, ingest_dt, ingest_raw


def _load() -> dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    tags = {r["tag_id"]: r for r in rows(TAGS_PATH)}
    events = jsonl(TELEMETRY_PATH)
    _CACHE = {"tags": tags, "events": events}
    return _CACHE


def engineering_unit_for(tag_id: str | None) -> str | None:
    if not tag_id:
        return None
    tag = _load()["tags"].get(tag_id)
    if not tag:
        return None
    return tag.get("engineering_unit")


def order_events(events: list[dict]) -> list[dict]:
    """Sort by event_time. Ingest/received is freshness, not order. Flag inversions."""
    enriched = []
    for event in events:
        out = dict(event)
        event_dt, ingest_dt, ingest_raw = _clocks(event)
        out["event_time"] = event.get("event_time")
        if event.get("ingest_time"):
            out["ingest_time"] = event["ingest_time"]
        if event.get("received_time"):
            out["received_time"] = event["received_time"]
        inversion = bool(event_dt and ingest_dt and ingest_dt < event_dt)
        out["inversion"] = inversion
        lag = None
        if event_dt and ingest_dt:
            lag = (ingest_dt - event_dt).total_seconds()
        out["ingest_lag_seconds"] = lag
        out["uncertainty"] = {"clock_inversion": inversion} if inversion else {"clock_inversion": False}
        if ingest_raw is None:
            out["uncertainty"]["clock_completeness"] = "PARTIAL"
        enriched.append((event_dt or datetime.min, out))
    enriched.sort(key=lambda item: item[0])
    return [row for _, row in enriched]


def quality_view(events: list[dict]) -> list[dict]:
    """Keep BAD/UNCERTAIN. Do not impute to GOOD. GOOD is not ProcessHealthy (OPEN-026)."""
    view = []
    for event in events:
        out = dict(event)
        quality = event.get("quality")
        out["quality"] = quality
        out["process_healthy"] = False
        if quality in {"BAD", "UNCERTAIN"}:
            out["usable_for_control"] = False
        view.append(out)
    return view


def unit_mismatch(event: dict, engineering_unit: str | None = None) -> dict:
    """Compare packet unit to tags.engineering_unit. Do not convert. Do not use diagnostics _TEMP==C only."""
    unit = event.get("unit")
    tag_id = event.get("tag_id")
    eng = engineering_unit if engineering_unit is not None else engineering_unit_for(tag_id)
    mismatch = bool(unit and eng and unit != eng)
    quality = event.get("quality")
    usable = not mismatch and quality == "GOOD"
    return {
        "event_id": event.get("event_id"),
        "tag_id": tag_id,
        "unit": unit,
        "engineering_unit": eng,
        "mismatch": mismatch,
        "usable_for_control": False if mismatch else usable,
        "treated_as_celsius": False,
        "converted": False,
        "uncertainty": {"unit_mismatch": mismatch},
    }


def quality_summary(events: list[dict] | None = None) -> dict:
    data = _load()
    rows_in = events if events is not None else data["events"]
    qualities = Counter(r.get("quality") for r in rows_in)
    not_good = sum(v for k, v in qualities.items() if k != "GOOD")
    mismatch_n = 0
    for event in rows_in:
        eng = engineering_unit_for(event.get("tag_id"))
        if eng and event.get("unit") and event.get("unit") != eng:
            mismatch_n += 1
    keys = Counter(
        (r.get("tag_id"), r.get("event_time"), str(r.get("value")), r.get("unit")) for r in rows_in
    )
    duplicates = sum(v - 1 for v in keys.values() if v > 1)
    return {
        "counts": {
            "GOOD": qualities.get("GOOD", 0),
            "BAD": qualities.get("BAD", 0),
            "UNCERTAIN": qualities.get("UNCERTAIN", 0),
            "not_good": not_good,
            "total": len(rows_in),
        },
        "duplicates": duplicates,
        "unit_mismatches_vs_engineering_unit": mismatch_n,
        "process_healthy_inferred": False,
        "imputed_bad_to_good": False,
        "sort_key": "event_time",
        "source_path": TELEMETRY_PATH,
        "note": "BAD/UNCERTAIN retained. Unit check uses tags.engineering_unit, not only *_TEMP==C.",
    }


def timeline(tag_id: str | None = None, order: str = "event_time", limit: int = TIMELINE_CAP) -> dict:
    data = _load()
    selected = data["events"]
    if tag_id:
        selected = [e for e in selected if e.get("tag_id") == tag_id]
    ordered = order_events(selected)
    cap = min(max(int(limit), 1), 2000)
    sliced = quality_view(ordered[:cap])
    for row in sliced:
        eng = engineering_unit_for(row.get("tag_id"))
        if eng:
            mm = unit_mismatch(row, eng)
            row["unit_mismatch"] = mm["mismatch"]
            row["engineering_unit"] = eng
            if mm["mismatch"]:
                row["usable_for_control"] = False
                row["treated_as_celsius"] = False
    return {
        "order": "event_time",
        "requested_order": order,
        "ignored_ingest_sort": order not in {"event_time", None, ""},
        "tag_id": tag_id,
        "returned": len(sliced),
        "available": len(ordered),
        "events": sliced,
    }
