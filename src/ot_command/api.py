from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .core import agent, authority, containment, graph_slice, identity, ops, recovery, risk, telemetry
from .core.agent import AgentValidationError
from .diagnostics import run_diagnostics

app = FastAPI(title="Synthetic ICS/OT Risk & Resilience API", version="2.0.0")


@app.get("/health")
def health():
    return {"status": "ok", "mode": "synthetic-read-only"}


@app.get("/diagnostics")
def diagnostics():
    return run_diagnostics()


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


@app.get("/recovery/{site_or_unit}")
def recovery_view(site_or_unit: str):
    plant_id = site_or_unit.split("-")[0] if "-" in site_or_unit else site_or_unit
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


