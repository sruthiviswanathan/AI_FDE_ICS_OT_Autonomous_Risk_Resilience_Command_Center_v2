import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .core import agent, authority, containment, data_layer, graph_slice, identity, ops, recovery, risk, telemetry
from .core.agent import AgentValidationError
from .core.traces import read_traces
from .diagnostics import run_diagnostics

ROOT = Path(__file__).resolve().parents[2]
UI_DIST = ROOT / "apps" / "command_center" / "dist"

app = FastAPI(
    title="ICS/OT Command Center API",
    version="3.0.0",
    description="Read-only product API for the operator command center. Legacy contracts: contracts/asset_api_v1.yaml, contracts/asset_api_v2.yaml.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173", "http://127.0.0.1:8000"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "synthetic-read-only",
        "api_version": "3.0.0",
    }


@app.get("/diagnostics")
def diagnostics():
    return run_diagnostics()


@app.get("/data/sources")
def data_sources():
    """Canonical estate sources loaded at runtime (APP-01)."""
    return data_layer.sources_catalog()


@app.get("/data/views/estate")
def data_estate_view():
    """Live derived estate summary — not acceptance-test fixtures."""
    return data_layer.estate_derived_view()


@app.get("/data/views/estate-by-plant")
def data_estate_by_plant(include_top_alerts: int = 3, severity_min: str | None = None):
    """Per-plant estate aggregates for Home dashboard (inventory signals, not risk rank)."""
    return data_layer.estate_by_plant_view(
        include_top_alerts=include_top_alerts,
        severity_min=severity_min,
    )


@app.get("/data/views/vendor-sessions")
def data_vendor_sessions(limit: int = 50):
    """Vendor/remote access sessions with anomaly flags."""
    anomalies = data_layer.derived_vendor_session_anomalies()
    return {
        "count": len(anomalies),
        "limit": limit,
        "sessions": anomalies[:limit],
        "source_path": data_layer.source_path("vendor_sessions"),
        "note": "UNKNOWN identity / unapproved window / MFA gaps flagged; not permission to block live.",
    }


@app.get("/plants")
def list_plants():
    plants = data_layer.list_plants()
    return {"count": len(plants), "plants": plants}


@app.get("/plants/{plant_id}/assets")
def list_plant_assets(plant_id: str, limit: int = 100, q: str | None = None):
    if plant_id not in data_layer.derived_plants_by_id():
        raise HTTPException(status_code=404, detail=f"plant {plant_id} not found")
    cap = min(max(limit, 1), 500)
    assets = data_layer.list_assets_for_plant(plant_id, limit=cap, q=q)
    return {"plant_id": plant_id, "count": len(assets), "limit": cap, "assets": assets}


@app.get("/assets/{asset_id}/alerts")
def list_asset_alerts(asset_id: str, limit: int = 50, severity: str | None = None):
    if asset_id not in data_layer.derived_assets_by_id():
        raise HTTPException(status_code=404, detail=f"asset {asset_id} not found")
    cap = min(max(limit, 1), 200)
    alerts = data_layer.list_alerts_for_asset(asset_id, limit=cap, severity=severity)
    return {"asset_id": asset_id, "count": len(alerts), "limit": cap, "alerts": alerts}


@app.get("/assets/{id}/identity")
def asset_identity(id: str):
    try:
        return identity.get_identity_bundle(id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"asset {id} not found in any source")


@app.get("/identity/conflicts")
def identity_conflicts():
    return identity.list_identity_conflicts()


@app.get("/telemetry/quality")
def telemetry_quality():
    return telemetry.telemetry_quality_summary()


@app.get("/telemetry/timeline")
def telemetry_timeline(tag_id: str | None = None, order: str = "event_time"):
    if order != "event_time":
        raise HTTPException(status_code=400, detail="only order=event_time is supported")
    return telemetry.get_timeline(tag_id=tag_id, order=order)


@app.get("/risk/contextual")
def risk_contextual(limit: int = 20):
    return risk.rank_corpus(limit=limit)


@app.get("/safety/conflicts")
def safety_conflicts(plant_id: str | None = None):
    return containment.list_safety_conflicts(plant_id=plant_id)


def _plant_id_from_site_or_unit(site_or_unit: str) -> str:
    """Map plant id (PLT-01) or unit id (PLT-10-U06) to recovery plant grain."""
    parts = site_or_unit.split("-")
    if len(parts) >= 2 and parts[0] == "PLT":
        return f"{parts[0]}-{parts[1]}"
    return site_or_unit


@app.get("/recovery/{site_or_unit}")
def recovery_view(site_or_unit: str):
    plant_id = _plant_id_from_site_or_unit(site_or_unit)
    try:
        return recovery.get_plant_recovery_view(plant_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"recovery view not found for {site_or_unit}")


@app.get("/authority/actions")
def authority_actions():
    return authority.catalog()


@app.get("/graph/slice")
def graph_slice_view(
    query: str = "Q5",
    asset_id: str | None = None,
    plant_id: str | None = None,
    alert_id: str | None = None,
    alias: str | None = None,
    hop_cap: int = 8,
):
    if hop_cap > 8:
        raise HTTPException(status_code=400, detail="hop_cap max 8")
    try:
        return graph_slice.get_slice(
            query=query,
            asset_id=asset_id,
            plant_id=plant_id,
            alert_id=alert_id,
            alias=alias,
            hop_cap=hop_cap,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/ops/slo")
def ops_slo():
    return ops.slo_status()


@app.get("/ops/cost-per-incident")
def ops_cost_per_incident():
    return ops.cost_per_incident()


class RecommendRequest(BaseModel):
    actor: str
    purpose: str
    plant_id: str
    as_of: str = "workshop-static"
    policy_version: str = "policy.py:ACTION_TIERS"
    asset_id: str | None = None
    alert_id: str | None = None
    severity: str | None = None
    process_context: str | None = None


@app.post("/recommend")
def recommend(request: RecommendRequest):
    try:
        return agent.run_incident_workflow(request.model_dump())
    except AgentValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


class EvalRunRequest(BaseModel):
    case_ids: list[str] | None = Field(default=None, description="Optional subset; default all EVAL-001…031")


@app.post("/eval/run")
def eval_run(request: EvalRunRequest | None = None):
    """Local harness only — runs golden eval cases (ENH-09). No OT I/O."""
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from evals.harness import run_all

    case_ids = request.case_ids if request else None
    return run_all(case_ids=case_ids)


@app.get("/audit/traces")
def audit_traces(limit: int = 50):
    """Decision trace list for audit screen (APP-02)."""
    traces = read_traces(limit=limit)
    return {"count": len(traces), "limit": limit, "traces": traces}


BINDINGS_PATH = ROOT / "apps" / "command_center" / "scenario_bindings.json"


def _load_scenario_bindings() -> dict:
    if not BINDINGS_PATH.is_file():
        raise HTTPException(status_code=404, detail="scenario bindings not found")
    return json.loads(BINDINGS_PATH.read_text(encoding="utf-8"))


@app.get("/scenarios/catalog")
def scenario_catalog():
    """APP-03 golden scenario rail — plant/asset/alert and expected badges."""
    return _load_scenario_bindings()


@app.get("/scenarios/{scenario_id}")
def get_scenario(scenario_id: str):
    """Scenario binding plus optional timeline JSON fixture."""
    catalog = _load_scenario_bindings()
    binding = next((s for s in catalog.get("scenarios", []) if s["id"] == scenario_id), None)
    if binding is None:
        raise HTTPException(status_code=404, detail=f"scenario {scenario_id} not found")
    payload: dict = {"binding": binding}
    timeline_path = ROOT / "scenarios" / f"{scenario_id}.json"
    if timeline_path.is_file():
        payload["timeline_fixture"] = json.loads(timeline_path.read_text(encoding="utf-8"))
    return payload


@app.get("/data/shift-notes/untrusted")
def shift_notes_untrusted():
    """Untrusted shift handover — never treated as authoritative."""
    path = ROOT / "data" / "shadow" / "shift_handover_email.txt"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="shift notes not found")
    return {
        "source_path": "data/shadow/shift_handover_email.txt",
        "trust": "UNTRUSTED",
        "content": path.read_text(encoding="utf-8"),
        "note": "Shift notes are operator narrative only — not permission to act.",
    }


@app.get("/agent/workflow/demo")
def agent_workflow_demo():
    """Expose workflow state shape for UI / EVAL-016 (deterministic demo envelope)."""
    envelope = {
        "actor": "SOC analyst",
        "purpose": "incident triage demo",
        "plant_id": "PLT-10",
        "as_of": "workshop-static",
        "policy_version": "policy.py:ACTION_TIERS",
        "asset_id": "OT-01016",
        "alert_id": "ALT-002783",
        "severity": "HIGH",
        "process_context": "UNKNOWN",
    }
    return agent.run_incident_workflow(envelope)


def _register_spa_fallback(ui_dist: Path) -> None:
    """Serve built UI assets and index.html for React Router deep links."""
    index_html = ui_dist.resolve()
    index_file = index_html / "index.html"
    if not index_file.is_file():
        return

    @app.get("/{spa_path:path}", include_in_schema=False)
    async def spa_fallback(spa_path: str = "") -> FileResponse:
        if spa_path:
            asset = (index_html / spa_path).resolve()
            try:
                asset.relative_to(index_html)
            except ValueError as exc:
                raise HTTPException(status_code=404, detail="Not Found") from exc
            if asset.is_file():
                return FileResponse(asset)
        return FileResponse(index_file)


if UI_DIST.is_dir():
    _register_spa_fallback(UI_DIST)


