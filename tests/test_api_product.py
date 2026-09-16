"""Product API integration tests (APP-01)."""

import os

import pytest
from fastapi.testclient import TestClient

from ot_command.api import app
from tests.helpers.access import FORBIDDEN_POST_PATHS

client = TestClient(app)


def test_health_includes_ai_disabled_by_default():
    os.environ.pop("AI_ENABLED", None)
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["mode"] == "synthetic-read-only"
    assert body["ai_enabled"] is False
    assert body["api_version"] == "3.0.0"


def test_health_ai_enabled_when_env_set():
    os.environ["AI_ENABLED"] = "1"
    try:
        resp = client.get("/health")
        assert resp.json()["ai_enabled"] is True
    finally:
        os.environ.pop("AI_ENABLED", None)


def test_missing_identity_returns_404():
    resp = client.get("/assets/OT-DOES-NOT-EXIST/identity")
    assert resp.status_code == 404


def test_happy_path_gold_reads():
    identity = client.get("/assets/OT-01016/identity")
    assert identity.status_code == 200
    bundle = identity.json()
    assert bundle["asset_uid"] == "OT-01016"
    assert bundle["cmdb_winner"] is False

    risk = client.get("/risk/contextual?limit=5")
    assert risk.status_code == 200
    rankings = risk.json()["rankings"]
    assert len(rankings) >= 1
    assert "factor_breakdown" in rankings[0]

    recovery = client.get("/recovery/PLT-01")
    assert recovery.status_code == 200
    assert recovery.json()["plant_id"] == "PLT-01"


def test_recommend_ai_disabled_no_execute():
    os.environ.pop("AI_ENABLED", None)
    payload = {
        "actor": "SOC analyst",
        "purpose": "incident triage",
        "plant_id": "PLT-10",
        "asset_id": "OT-01016",
        "alert_id": "ALT-002783",
        "severity": "HIGH",
        "process_context": "UNKNOWN",
    }
    resp = client.post("/recommend", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("ai_enabled") is False
    packet = body.get("recommendation") or {}
    assert packet.get("execute") is False
    assert packet.get("recommendation") not in {"ISOLATE", "EXECUTE"}
    assert body.get("human_review", {}).get("execute") is False


def test_no_forbidden_execute_post_routes():
    routes = {getattr(r, "path", None): getattr(r, "methods", set()) for r in app.routes}
    post_paths = {p for p, m in routes.items() if p and "POST" in m}
    for forbidden in FORBIDDEN_POST_PATHS:
        assert forbidden not in post_paths


def test_data_sources_catalog():
    resp = client.get("/data/sources")
    assert resp.status_code == 200
    body = resp.json()
    keys = {s["source_key"] for s in body["sources"]}
    assert keys == {
        "assets",
        "telemetry",
        "vulnerabilities",
        "safety_barriers",
        "recovery_readiness",
        "vendor_sessions",
    }
    for entry in body["sources"]:
        assert entry["fixture_dependent"] is False
        assert entry["record_count"] > 0
        assert entry["exists"] is True


def test_data_estate_view_derived_at_runtime():
    resp = client.get("/data/views/estate")
    assert resp.status_code == 200
    body = resp.json()
    assert body["provenance"] == "runtime-derived"
    assert body["counts"]["assets"] > 0
    assert body["counts"]["telemetry_events"] > 0
    assert "derived_signals" in body


def test_audit_traces_and_scenario_endpoints():
    traces = client.get("/audit/traces?limit=5")
    assert traces.status_code == 200
    assert "traces" in traces.json()

    catalog = client.get("/scenarios/catalog")
    assert catalog.status_code == 200
    ids = {s["id"] for s in catalog.json()["scenarios"]}
    assert "cascade_001" in ids
    assert "inject_01" in ids
    assert len(ids) >= 9

    scenario = client.get("/scenarios/cascade_001")
    assert scenario.status_code == 200
    body = scenario.json()
    assert body["binding"]["id"] == "cascade_001"
    assert body["timeline_fixture"]["scenario_id"] == "CASCADE-001"

    notes = client.get("/data/shift-notes/untrusted")
    assert notes.status_code == 200
    assert notes.json()["trust"] == "UNTRUSTED"


def test_openapi_matches_registered_routes():
    spec = app.openapi()
    paths = set(spec.get("paths", {}))
    for required in (
        "/health",
        "/data/sources",
        "/assets/{id}/identity",
        "/risk/contextual",
        "/recommend",
    ):
        assert required in paths
