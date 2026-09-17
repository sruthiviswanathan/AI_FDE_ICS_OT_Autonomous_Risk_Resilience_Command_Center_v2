"""Product API integration tests (APP-01)."""

import pytest
from fastapi.testclient import TestClient

from ot_command.api import app
from tests.helpers.access import FORBIDDEN_POST_PATHS

client = TestClient(app)


def test_health_payload():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["mode"] == "synthetic-read-only"
    assert body["api_version"] == "3.0.0"
    assert "ai_enabled" not in body


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


def test_recommend_never_executes():
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
    assert "ai_enabled" not in body
    assert "explainer" not in body
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
        "plants",
        "assets",
        "telemetry",
        "vulnerabilities",
        "safety_barriers",
        "recovery_readiness",
        "vendor_sessions",
        "cyber_alerts",
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


def test_estate_by_plant_view():
    resp = client.get("/data/views/estate-by-plant?include_top_alerts=5")
    assert resp.status_code == 200
    body = resp.json()
    assert body["provenance"] == "runtime-derived"
    assert body["plant_count"] == 18
    assert len(body["plants"]) == 18
    assert "methodology" in body
    assert "not_operational_risk_rank" in body["methodology"]

    assert body["total_alerts"] > 0
    assert "asset_status_summary" in body
    summary = body["asset_status_summary"]
    assert summary["total_assets"] > 0
    assert "by_registered_state" in summary
    assert "by_observed_state" in summary

    assert body["methodology"].get("posture_motto")
    layer_keys = {
        "cyber_exposure",
        "process_ops_disagreement",
        "safety_posture",
        "recovery_credibility",
        "evidence_quality",
    }

    plt10 = next(p for p in body["plants"] if p["plant_id"] == "PLT-10")
    assert plt10["counts"]["assets"] > 0
    assert plt10["counts"]["alerts_total"] > 0
    assert plt10["signals"]["elevated"] is True
    assert plt10["signals"]["posture_composite"] in {"red", "amber", "ok"}
    assert set(plt10["posture_layers"].keys()) == layer_keys
    assert plt10["signals"]["posture_composite"] != "ok"
    assert len(plt10["signals"]["elevation_reasons"]) >= 1
    assert "assets_by_observed_state" in plt10
    assert "top_assets_by_alerts" in plt10

    assets = client.get("/plants/PLT-10/assets?limit=5")
    assert assets.status_code == 200
    sample = assets.json()["assets"][0]
    assert "alert_count" in sample


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


def test_list_plants_and_cascade_catalog():
    plants = client.get("/plants")
    assert plants.status_code == 200
    body = plants.json()
    assert body["count"] == 18
    assert body["plants"][0]["plant_id"] == "PLT-01"

    assets = client.get("/plants/PLT-10/assets?limit=500")
    assert assets.status_code == 200
    asset_body = assets.json()
    assert asset_body["plant_id"] == "PLT-10"
    assert asset_body["count"] > 0
    assert all(a.get("plant_id") == "PLT-10" for a in asset_body["assets"])

    missing_plant = client.get("/plants/PLT-999/assets")
    assert missing_plant.status_code == 404

    sample_asset = asset_body["assets"][0]["asset_id"]
    alerts = client.get(f"/assets/{sample_asset}/alerts?limit=50")
    assert alerts.status_code == 200
    alert_body = alerts.json()
    assert alert_body["asset_id"] == sample_asset
    assert alert_body["count"] >= 0

    missing_asset = client.get("/assets/OT-DOES-NOT-EXIST/alerts")
    assert missing_asset.status_code == 404


def test_openapi_matches_registered_routes():
    spec = app.openapi()
    paths = set(spec.get("paths", {}))
    for required in (
        "/health",
        "/plants",
        "/plants/{plant_id}/assets",
        "/assets/{asset_id}/alerts",
        "/data/sources",
        "/data/views/estate-by-plant",
        "/assets/{id}/identity",
        "/risk/contextual",
        "/recommend",
    ):
        assert required in paths


def test_spa_fallback_serves_index_for_client_routes():
    """React Router paths must return index.html on refresh (Render / integrated deploy)."""
    for path in ("/", "/estate", "/incident", "/process", "/recovery"):
        resp = client.get(path)
        assert resp.status_code == 200, path
        assert "text/html" in resp.headers.get("content-type", ""), path
        assert "<!doctype html>" in resp.text.lower(), path

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
