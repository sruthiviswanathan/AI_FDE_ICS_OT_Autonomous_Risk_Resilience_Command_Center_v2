"""APP-02 command-room UI. No Execute Isolation / Write PLC controls."""

from pathlib import Path
import re

from ot_command.api import app, health, sessions_route

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "apps" / "command_center"
FORBIDDEN_LABELS = (
    "Execute Isolation",
    "Isolate now",
    "Isolate endpoint",
    "Write PLC",
    "Change setpoint",
    "Modify SIS",
    "Bypass interlock",
    "Suppress trip",
)


def _buttons_and_links(text: str) -> list[str]:
    labels = re.findall(r"<button[^>]*>(.*?)</button>", text, flags=re.I | re.S)
    labels += re.findall(r"<a[^>]*>(.*?)</a>", text, flags=re.I | re.S)
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip() for t in labels]


def test_ui_files_exist_and_fifteen_screens_named():
    html = (UI / "index.html").read_text(encoding="utf-8")
    assert "OT Risk" in html or "Command Room" in html
    for i in range(1, 16):
        assert f'data-screen="{i}"' in html
    assert (UI / "static" / "app.css").exists()
    assert (UI / "static" / "app.js").exists()
    assert (UI / "fixtures" / "command_center_fixtures.json").exists()
    assert (UI / "SCENARIO_BINDINGS.md").exists()
    assert (UI / "fixtures" / "scenario_bindings.json").exists()
    html = (UI / "index.html").read_text(encoding="utf-8")
    assert 'id="scenario-rail"' in html


def test_no_execute_isolation_or_write_plc_controls():
    html = (UI / "index.html").read_text(encoding="utf-8")
    js = (UI / "static" / "app.js").read_text(encoding="utf-8")
    for label in FORBIDDEN_LABELS:
        for blob in _buttons_and_links(html):
            assert label.lower() not in blob.lower(), blob
        assert f">{label}<" not in html
    assert "executeIsolation" not in js
    assert "writePlc(" not in js


def test_ai_disabled_is_default_path_in_markup():
    html = (UI / "index.html").read_text(encoding="utf-8")
    js = (UI / "static" / "app.js").read_text(encoding="utf-8")
    assert "AI-disabled" in html
    assert "el(\"ai-toggle\").checked = false" in js or 'ai-toggle").checked = false' in js
    assert "EVAL-016" in html


def test_retrieval_mix_labels_present():
    html = (UI / "index.html").read_text(encoding="utf-8")
    for lab in ("STRUCTURED", "GRAPH", "VECTOR", "POLICY", "MEMORY"):
        assert lab in html
    assert "UNTRUSTED" in html


def test_health_exposes_ai_enabled_and_ui_path():
    payload = health()
    assert payload["mode"] == "synthetic-read-only"
    assert payload["live_ot"] is False
    assert "ai_enabled" in payload
    assert payload["ui"] == "/ui"


def test_sessions_route_is_observe_only():
    payload = sessions_route(plant_id="PLT-10", limit=5)
    assert payload["change_remote_access_execute"] is False
    assert payload["auto_disable_vendor_vpn"] is False
    assert payload["all_plants_export"] is False
    assert payload["unknown_is_not_approval"] is True


def test_scenario_bindings_do_not_hide_conflicts_or_invent_execute():
    import json

    data = json.loads((UI / "fixtures" / "scenario_bindings.json").read_text(encoding="utf-8"))
    assert data["hide_conflicts"] is False
    assert data["beautify_demo"] is False
    assert data["live_ot"] is False
    ids = {s["id"] for s in data["scenarios"]}
    for required in ("EVAL-001", "EVAL-002", "EVAL-003", "EVAL-004", "EVAL-005", "EVAL-006", "inject_01", "inject_06", "cascade_001", "EVAL-016"):
        assert required in ids
    for s in data["scenarios"]:
        assert s["conflicts_remain_visible"] is True
        assert "Execute Isolation" not in (s.get("expected_badges") or [])
    js = (UI / "static" / "app.js").read_text(encoding="utf-8")
    assert "applyScenario" in js
    assert "hide_conflicts=false" in js


def test_scenario_bindings_use_estate_ids():
    import json

    data = json.loads((UI / "fixtures" / "scenario_bindings.json").read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in data["scenarios"]}
    assert by_id["EVAL-001"]["asset_ids"] == ["OT-00012", "OT-00033"]
    assert by_id["EVAL-003"]["alert_id"] == "ALT-002783"
    assert by_id["EVAL-005"]["plant_id"] == "PLT-01"
    assert "37 as verified census" in by_id["cascade_001"]["must_not_badges"]

    found = {}
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = set(getattr(route, "methods", None) or [])
        if path in {"/ui", "/access/sessions", "/ops/traces"}:
            found[path] = methods
    assert "/ui" in found
    assert "/access/sessions" in found
    for methods in found.values():
        assert "GET" in methods
        assert not (methods & {"POST", "PUT", "PATCH", "DELETE"})
