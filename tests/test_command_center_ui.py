"""APP-02 command-room UI (React). No Execute Isolation / Write PLC controls."""

from pathlib import Path
import re

from ot_command.api import app, health, sessions_route

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "apps" / "command_center"
SRC = UI / "src"
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


def _src() -> str:
    parts = []
    for path in sorted(SRC.rglob("*")):
        if path.suffix in {".js", ".jsx", ".css", ".html"}:
            parts.append(path.read_text(encoding="utf-8"))
    parts.append((UI / "index.html").read_text(encoding="utf-8"))
    return "\n".join(parts)


def _buttons_and_links(text: str) -> list[str]:
    labels = re.findall(r"<button[^>]*>(.*?)</button>", text, flags=re.I | re.S)
    labels += re.findall(r"<button[^>]*>\s*\{[^}]*\}\s*</button>", text, flags=re.I | re.S)
    labels += re.findall(r"<a[^>]*>(.*?)</a>", text, flags=re.I | re.S)
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip() for t in labels]


def test_ui_files_exist_and_fifteen_screens_named():
    html = (UI / "index.html").read_text(encoding="utf-8")
    src = _src()
    assert "OT Risk" in html or "Command Room" in html
    assert 'id="root"' in html
    assert (UI / "src" / "App.jsx").exists()
    assert (UI / "src" / "main.jsx").exists()
    assert (UI / "package.json").exists()
    assert (UI / "vite.config.js").exists()
    assert (UI / "fixtures" / "command_center_fixtures.json").exists()
    assert (UI / "SCENARIO_BINDINGS.md").exists()
    assert (UI / "fixtures" / "scenario_bindings.json").exists()
    for i in range(1, 16):
        assert f'data-screen="{i}"' in src
    assert 'id="scenario-rail"' in src
    assert 'id="packet-status"' in src
    assert 'id="case-search"' in src
    assert 'id="role-btns"' in src
    assert 'id="graph-canvas"' in src
    assert 'id="incident-timeline"' in src
    assert 'id="hitl-queue"' in src
    assert "from \"react\"" in src or "from 'react'" in src
    assert "/src/main.jsx" in html


def test_no_execute_isolation_or_write_plc_controls():
    src = _src()
    for label in FORBIDDEN_LABELS:
        for blob in _buttons_and_links(src):
            assert label.lower() not in blob.lower(), blob
        assert f">{label}<" not in src
    assert "executeIsolation" not in src
    assert "writePlc(" not in src


def test_ai_disabled_is_default_path_in_markup():
    src = _src()
    assert "placeholder explainer omitted" in src.lower() or "Placeholder explainer omitted" in src
    assert 'id="ai-toggle"' in src
    assert "useState(false)" in src
    assert "EVAL-016" in src


def test_retrieval_mix_labels_present():
    src = _src()
    for lab in ("STRUCTURED", "GRAPH", "VECTOR", "POLICY", "MEMORY"):
        assert lab in src
    assert "UNTRUSTED" in src


def test_health_exposes_ai_enabled_and_ui_path():
    payload = health()
    assert payload["mode"] == "synthetic-read-only"
    assert payload["live_ot"] is False
    assert "ai_enabled" in payload
    assert payload["explainer_is_authority"] is False
    assert payload["model_selected"] is False
    assert payload["ui"] == "/ui"


def test_sessions_route_is_observe_only():
    payload = sessions_route(plant_id="PLT-10", limit=5)
    assert payload["change_remote_access_execute"] is False
    assert payload["auto_disable_vendor_vpn"] is False
    assert payload["all_plants_export"] is False
    assert payload["unknown_is_not_approval"] is True


def test_lookup_is_bounded_and_does_not_pick_a_winner():
    from ot_command.core.identity import search_identity
    from ot_command.api import lookup_route, case_slice_route

    empty = search_identity("x")
    assert empty["estate_dump"] is False
    assert empty["hits"] == []
    bundle = search_identity("PLT-01-DCS_CONTROLLER-105")
    assert bundle["winner"] is None
    assert bundle["estate_dump"] is False
    ids = []
    for hit in bundle["hits"]:
        ids.extend(hit.get("asset_ids") or [])
    assert "OT-00012" in ids
    assert "OT-00033" in ids
    payload = lookup_route(q="ALT-002783", limit=12)
    assert payload["estate_dump"] is False
    assert payload["all_plants_export"] is False
    kinds = {h["kind"] for h in payload["hits"]}
    assert "alert" in kinds
    slice_ = case_slice_route(plant_id="PLT-10", asset_id="OT-01016", alert_id="ALT-002783")
    assert slice_["estate_dump"] is False
    assert slice_["winner"] is None
    assert slice_["live_ot"] is False
    assert slice_["open_012"] is True
    assert slice_["identity"]["winner"] is None
    assert slice_["cascade_analogue"]["verified_census"] is False


def test_sessions_identity_filter_is_observe_only():
    payload = sessions_route(plant_id="PLT-10", identity="unknown", limit=5)
    assert payload["change_remote_access_execute"] is False
    assert payload["auto_disable_vendor_vpn"] is False
    assert payload["unknown_is_not_approval"] is True
    assert payload["identity"] == "unknown"
    for row in payload["rows"]:
        assert row.get("identity") == "unknown"


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
    src = _src()
    assert "applyScenario" in src
    assert "hide_conflicts=false" in src
    assert "function graphSvg(" in src
    assert "function hitlQueue(" in src
    assert "runLookup" in src
    assert "AwaitAuthorization" in src
    assert "Execute Isolation" not in src


def test_ui_renders_records_not_pretty_json():
    src = _src()
    css = (UI / "src" / "app.css").read_text(encoding="utf-8")
    assert "JSON.stringify(obj, null, 2)" not in src
    assert "function record(" in src
    assert "function sloCard(" in src
    assert ".facts" in css
    assert "Execute Isolation" not in src


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
        if path in {"/ui", "/access/sessions", "/ops/traces", "/lookup", "/case/slice"}:
            found[path] = methods
    assert "/ui" in found
    assert "/access/sessions" in found
    assert "/lookup" in found
    assert "/case/slice" in found
    for methods in found.values():
        assert "GET" in methods
        assert not (methods & {"POST", "PUT", "PATCH", "DELETE"})
