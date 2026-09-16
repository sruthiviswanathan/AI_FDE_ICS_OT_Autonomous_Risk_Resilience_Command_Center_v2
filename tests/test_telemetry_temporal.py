"""Target-state telemetry / dual-clock tests (ADR-02). Fail until ot_command.core.telemetry exists."""

from tests.helpers.access import field
from tests.helpers.golden import golden_case


def test_eval_004_orders_by_event_time_and_flags_inversion():
    from ot_command.core.telemetry import order_events

    events = [
        {
            "event_id": "EVT-0000001",
            "event_time": "2026-10-05T17:48:00",
            "received_time": "2026-10-05T17:47:35",
        },
        {
            "event_id": "EVT-LATER",
            "event_time": "2026-10-05T17:49:00",
            "received_time": "2026-10-05T17:46:00",
        },
    ]
    ordered = order_events(events)
    ids = [field(e, "event_id") for e in ordered]
    assert ids == ["EVT-0000001", "EVT-LATER"]
    first = ordered[0]
    assert field(first, "event_time")
    assert field(first, "received_time") or field(first, "ingest_time")
    assert field(first, "inversion") or field(first, "uncertainty")


def test_eval_015_event_time_order_invariant_under_ingest_shuffle():
    from ot_command.core.telemetry import order_events

    base = [
        {"event_id": "A", "event_time": "2026-10-01T00:00:10", "ingest_time": "2026-10-01T00:02:00", "tag_id": "PLT-01-U01_TEMP"},
        {"event_id": "B", "event_time": "2026-10-01T00:00:20", "ingest_time": "2026-10-01T00:01:00", "tag_id": "PLT-01-U01_TEMP"},
        {"event_id": "C", "event_time": "2026-10-01T00:00:30", "ingest_time": "2026-10-01T00:04:00", "tag_id": "PLT-01-U01_TEMP"},
    ]
    shuffled = [
        {**base[0], "ingest_time": "2026-10-01T00:09:00"},
        {**base[1], "ingest_time": "2026-10-01T00:00:01"},
        {**base[2], "ingest_time": "2026-10-01T00:00:02"},
    ]
    pre = [field(e, "event_id") for e in order_events(base)]
    post = [field(e, "event_id") for e in order_events(shuffled)]
    assert pre == post == ["A", "B", "C"]


def test_eval_009_does_not_impute_bad_to_good():
    from ot_command.core.telemetry import quality_view

    events = [
        {"event_id": "TEL-BAD", "quality": "BAD", "value": 1},
        {"event_id": "TEL-UNC", "quality": "UNCERTAIN", "value": 2},
        {"event_id": "TEL-GOOD", "quality": "GOOD", "value": 3},
    ]
    view = quality_view(events)
    by_id = {field(e, "event_id"): e for e in view}
    assert field(by_id["TEL-BAD"], "quality") == "BAD"
    assert field(by_id["TEL-UNC"], "quality") == "UNCERTAIN"
    assert field(by_id["TEL-GOOD"], "process_healthy") is not True


def test_eval_022_flags_fahrenheit_on_celsius_temp_tag():
    fx = golden_case("EVAL-022")["fixture"]
    from ot_command.core.telemetry import unit_mismatch

    result = unit_mismatch(
        {"event_id": fx["event_id"], "tag_id": fx["tag_id"], "unit": fx["unit"]},
        engineering_unit="C",
    )
    assert field(result, "mismatch") is True
    assert fx["unit"] in str(field(result, "unit") or fx["unit"])
    assert field(result, "usable_for_control") is not True
    assert field(result, "treated_as_celsius") is not True


def test_enh03_telemetry_routes_are_get_only():
    from ot_command.api import app

    found = {}
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = set(getattr(route, "methods", None) or [])
        if path in {"/telemetry/quality", "/telemetry/timeline"}:
            found[path] = methods
    assert "/telemetry/quality" in found
    assert "/telemetry/timeline" in found
    for methods in found.values():
        assert "GET" in methods
        assert not (methods & {"POST", "PUT", "PATCH", "DELETE"})
