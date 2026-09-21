import pytest

from ot_command.core import telemetry
from ot_command.repository import jsonl
from tests.helpers.golden import get_golden_case


EVAL_004 = get_golden_case("EVAL-004")


def test_eval_004_orders_by_event_time_not_received_time():
    events = [
        {"event_id": "EVT-0000001", "event_time": "2026-10-05T17:48:00", "received_time": "2026-10-05T17:47:35"},
        {"event_id": "EVT-0000002", "event_time": "2026-10-05T17:49:00", "received_time": "2026-10-05T17:50:00"},
    ]
    ordered = telemetry.order_events(events, clock="event_time")
    assert [e["event_id"] for e in ordered] == ["EVT-0000001", "EVT-0000002"]
    assert ordered[0].get("temporal_anomaly") is True or ordered[0].get("uncertainty")


def test_received_time_only_sort_is_forbidden():
    events = [
        {"event_id": "A", "event_time": "2026-10-05T17:48:00", "received_time": "2026-10-05T17:50:00"},
        {"event_id": "B", "event_time": "2026-10-05T17:49:00", "received_time": "2026-10-05T17:47:00"},
    ]
    ordered = telemetry.order_events(events, clock="event_time")
    assert [e["event_id"] for e in ordered] == ["A", "B"]


def test_telemetry_quality_summary_matches_seeded_imperfections():
    summary = telemetry.telemetry_quality_summary()
    assert summary["bad_or_uncertain"] >= 4094
    assert summary["duplicate_packets"] >= 120
    assert summary["unit_mismatches"] >= 47


def test_telemetry_quality_scoped_by_plant():
    plt01 = telemetry.telemetry_quality_summary(plant_id="PLT-01")
    plt10 = telemetry.telemetry_quality_summary(plant_id="PLT-10")
    estate = telemetry.telemetry_quality_summary()
    assert plt01["total_events"] < estate["total_events"]
    assert plt10["total_events"] < estate["total_events"]
    assert plt01["bad_or_uncertain"] != plt10["bad_or_uncertain"]
    assert plt01["scope"]["effective"]["plant_id"] == "PLT-01"


def test_telemetry_quality_falls_back_when_asset_untagged():
    summary = telemetry.telemetry_quality_summary(plant_id="PLT-01", asset_id="OT-00001")
    assert summary["total_events"] > 0
    assert summary["bad_or_uncertain"] > 0
    assert summary["scope"]["scope_note"]
    assert summary["scope"]["effective"]["asset_id"] is None


def test_telemetry_timeline_scoped_by_plant():
    timeline = telemetry.get_timeline(plant_id="PLT-01", limit=20)
    assert timeline["count"] <= 20
    assert timeline["total_count"] > timeline["count"]
    assert all(e["tag_id"].startswith("PLT-01-") for e in timeline["events"])


def test_telemetry_timeline_pagination_walks_beyond_first_window():
    page1 = telemetry.get_timeline(plant_id="PLT-01", limit=50, offset=0)
    page2 = telemetry.get_timeline(plant_id="PLT-01", limit=50, offset=50)
    assert page1["total_count"] > 50
    assert page1["matched_count"] == page1["total_count"]
    ids1 = {e["event_id"] for e in page1["events"]}
    ids2 = {e["event_id"] for e in page2["events"]}
    assert ids1 and ids2
    assert ids1.isdisjoint(ids2)


def test_telemetry_timeline_quality_filter_and_sort():
    filtered = telemetry.get_timeline(plant_id="PLT-01", quality="not_GOOD", limit=25, sort_by="quality", sort_dir="asc")
    assert filtered["matched_count"] <= filtered["total_count"]
    assert filtered["events"]
    assert all(e["quality"] != "GOOD" for e in filtered["events"])
    qualities = [e["quality"] for e in filtered["events"]]
    assert qualities == sorted(qualities)


def test_tag_telemetry_preserves_dual_clock_fields():
    sample = jsonl("data/telemetry/tag_telemetry.jsonl")[:5]
    ordered = telemetry.order_events(sample)
    for row in ordered:
        assert "event_time" in row
        assert "ingest_time" in row or row.get("uncertainty") == "ingest_time_missing"
