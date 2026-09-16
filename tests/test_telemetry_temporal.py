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


def test_tag_telemetry_preserves_dual_clock_fields():
    sample = jsonl("data/telemetry/tag_telemetry.jsonl")[:5]
    ordered = telemetry.order_events(sample)
    for row in ordered:
        assert "event_time" in row
        assert "ingest_time" in row or row.get("uncertainty") == "ingest_time_missing"
