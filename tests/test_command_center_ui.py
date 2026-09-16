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


def test_ui_and_sessions_are_get_only():
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
