"""Deterministic Moonshot forecasts, AI ON captions, twin preview (no LLM, no execute)."""

from fastapi.testclient import TestClient

from ot_command.api import app
from ot_command.core.forecasts import _rank_forecasts, list_forecasts

client = TestClient(app)

ALLOWED_ACTIONS = {"MONITOR", "RECOMMEND_CONTAINMENT_REVIEW", "ABSTAIN"}


def test_forecasts_require_plant_id():
    resp = client.get("/forecasts")
    assert resp.status_code == 422


def test_forecasts_unknown_plant_404():
    resp = client.get("/forecasts?plant_id=PLT-99")
    assert resp.status_code == 404


def test_plt10_cascade_forecasts_abstain_unknown_and_never_execute():
    resp = client.get(
        "/forecasts?plant_id=PLT-10&asset_id=OT-01016&alert_id=ALT-002783&as_of=workshop-static"
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "moonshot"
    assert body["banner"] == "ADVISORY FORECAST — NOT A CONTROL ACTION"
    assert body["execute"] is False
    assert body["plant_id"] == "PLT-10"
    categories = {f["category"] for f in body["forecasts"]}
    assert "VENDOR_SESSION_PLUS_WRITE_ALERT" in categories
    assert "UNKNOWN_PROCESS_CONTEXT" in categories
    assert "SAFETY_BYPASS_AGING" in categories
    for row in body["forecasts"]:
        assert row["execute"] is False
        assert row["recommended_action"] in ALLOWED_ACTIONS
        assert row["action_tier"] <= 1
        assert "isolate_endpoint" not in str(row.get("recommended_action"))
    unknown = next(f for f in body["forecasts"] if f["category"] == "UNKNOWN_PROCESS_CONTEXT")
    assert unknown["recommended_action"] == "ABSTAIN"
    assert "ALT-002783" in unknown["evidence_ids"]
    vendor = next(f for f in body["forecasts"] if f["category"] == "VENDOR_SESSION_PLUS_WRITE_ALERT")
    assert "ALT-002783" in vendor["evidence_ids"]
    assert "RA-00025" in vendor["evidence_ids"]
    assert vendor["recommended_action"] == "ABSTAIN"
    safety_ids = [
        eid
        for f in body["forecasts"]
        if f["category"] == "SAFETY_BYPASS_AGING"
        for eid in f["evidence_ids"]
    ]
    assert "PLT-10-SAFE-07" in safety_ids


def test_identity_conflict_ot_00528_on_plt05():
    resp = client.get("/forecasts?plant_id=PLT-05&asset_id=OT-00528")
    assert resp.status_code == 200
    rows = resp.json()["forecasts"]
    identity = [f for f in rows if f["category"] == "IDENTITY_CONFLICT_REACHABLE"]
    assert identity
    assert identity[0]["asset_id"] == "OT-00528"
    assert identity[0]["recommended_action"] in ALLOWED_ACTIONS
    assert identity[0]["execute"] is False


def test_restore_test_rot_plt01_identity():
    resp = client.get("/forecasts?plant_id=PLT-01")
    assert resp.status_code == 200
    rot = [f for f in resp.json()["forecasts"] if f["category"] == "RESTORE_TEST_ROT"]
    assert rot
    assert any(f.get("component") == "IDENTITY" or "IDENTITY" in f["evidence_ids"][0] for f in rot)


def test_unreachable_cvss9_does_not_rank_above_reachable_open_crit():
    ranked = _rank_forecasts(
        [
            {
                "category": "IDENTITY_CONFLICT_REACHABLE",
                "asset_id": "UNREACH-9",
                "_unreachable_cvss9": True,
                "_reachable_open_crit": False,
            },
            {
                "category": "IDENTITY_CONFLICT_REACHABLE",
                "asset_id": "REACH-OPEN",
                "_unreachable_cvss9": False,
                "_reachable_open_crit": True,
            },
        ]
    )
    assert ranked[0]["asset_id"] == "REACH-OPEN"
    assert ranked[1]["asset_id"] == "UNREACH-9"


def test_explain_template_caption_has_citations():
    resp = client.get("/explain?plant_id=PLT-10&asset_id=OT-01016&alert_id=ALT-002783")
    assert resp.status_code == 200
    body = resp.json()
    assert body["mode"] == "on"
    assert body["engine_authoritative"] is True
    assert body["execute"] is False
    assert body["explainer"] == "template_v1"
    assert 4 <= body["sentence_count"] <= 8
    sentences = [s for s in body["caption"].split(". ") if s.strip()]
    assert 4 <= len(sentences) <= 8
    assert "ALT-002783" in body["evidence_ids"]
    assert any("cyber_alerts.csv" in p or "safety_barriers.csv" in p for p in body["source_files"])
    assert "explainer" not in client.post(
        "/recommend",
        json={
            "actor": "SOC analyst",
            "purpose": "incident triage",
            "plant_id": "PLT-10",
            "asset_id": "OT-01016",
            "alert_id": "ALT-002783",
            "severity": "HIGH",
            "process_context": "UNKNOWN",
        },
    ).json()


def test_twin_cascade_isolate_preview_is_unsafe():
    resp = client.get("/twin/preview?scenario_id=cascade_001&proposed_action=isolate_preview")
    assert resp.status_code == 200
    body = resp.json()
    assert body["lab_result"] == "UNSAFE_ISOLATION"
    assert body["execute"] is False
    assert body["apply_to_plant"] is False
    assert body["create_approval_packet"]["path"] == "/recommend"
    assert body["create_approval_packet"]["execute"] is False


def test_twin_rejects_unknown_action():
    resp = client.get("/twin/preview?scenario_id=cascade_001&proposed_action=write_plc")
    assert resp.status_code == 400


def test_gold_gets_include_forecast_explain_twin():
    routes = {getattr(r, "path", None): getattr(r, "methods", set()) for r in app.routes}
    for path in ("/forecasts", "/explain", "/twin/preview"):
        assert path in routes
        assert "GET" in routes[path]
        assert "POST" not in routes[path]


def test_list_forecasts_engine_direct():
    payload = list_forecasts(plant_id="PLT-10", asset_id="OT-01016", alert_id="ALT-002783")
    assert payload["execute"] is False
    assert all(f["recommended_action"] in ALLOWED_ACTIONS for f in payload["forecasts"])
