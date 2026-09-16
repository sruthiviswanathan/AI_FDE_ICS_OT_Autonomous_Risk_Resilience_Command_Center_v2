from typing import Any

from fastapi import Body, FastAPI, HTTPException, Query
from .diagnostics import run_diagnostics
from .core.identity import asset_context, identity_bundle, list_identity_conflicts
from .core.telemetry import quality_summary, timeline
from .core.risk import rank_all
from .core.containment import recommendation_packet, safety_conflicts
from .core.recovery import plant_recovery
from .core.authority import authority_catalog
from .core.agent import run_recommend
from .core.graph_slice import graph_slice
from .core.ops import cost_per_incident, slo_status

app=FastAPI(title='Synthetic ICS/OT Risk & Resilience API',version='2.0.0')

@app.get('/health')
def health(): return {'status':'ok','mode':'synthetic-read-only'}

@app.get('/diagnostics')
def diagnostics(): return run_diagnostics()

@app.get('/identity/conflicts')
def identity_conflicts():
    return list_identity_conflicts()

@app.get('/assets/{id}/context')
def asset_context_route(id: str):
    try:
        return asset_context(id)
    except KeyError:
        raise HTTPException(status_code=404, detail='unknown asset_id')

@app.get('/assets/{id}/identity')
def asset_identity_route(id: str):
    try:
        return identity_bundle(id)
    except KeyError:
        raise HTTPException(status_code=404, detail='unknown asset_id')

@app.get('/telemetry/quality')
def telemetry_quality():
    return quality_summary()

@app.get('/telemetry/timeline')
def telemetry_timeline(order: str = Query(default='event_time'), tag_id: str | None = None, limit: int = 500):
    return timeline(tag_id=tag_id, order=order, limit=limit)

@app.get('/risk/rank')
def risk_rank(limit: int = Query(default=50, ge=1, le=200)):
    return rank_all(limit=limit)

@app.get('/risk/contextual')
def risk_contextual(limit: int = Query(default=50, ge=1, le=200)):
    return rank_all(limit=limit)

@app.get('/safety/conflicts')
def safety_conflicts_route(limit: int = Query(default=50, ge=1, le=200)):
    return safety_conflicts(limit=limit)

@app.get('/recommendations/{incident_id}')
def recommendation_route(incident_id: str):
    try:
        return recommendation_packet(incident_id)
    except KeyError:
        raise HTTPException(status_code=404, detail='unknown incident_id')

@app.get('/recovery/{plant_id}')
def recovery_plant_route(plant_id: str):
    try:
        return plant_recovery(plant_id)
    except KeyError:
        raise HTTPException(status_code=404, detail='unknown plant_id')

@app.get('/recovery/{site_or_unit}')
def recovery_site_route(site_or_unit: str):
    try:
        return plant_recovery(site_or_unit)
    except KeyError:
        raise HTTPException(status_code=404, detail='unknown site_or_unit')

@app.get('/authority/actions')
def authority_actions_route():
    return authority_catalog()

@app.post('/recommend')
def recommend_route(payload: dict[str, Any] | None = Body(default=None)):
    return run_recommend(payload or {})

@app.get('/graph/slice')
def graph_slice_route(
    plant_id: str | None = None,
    unit_id: str | None = None,
    asset_id: str | None = None,
    hops: int = Query(default=4, ge=1, le=8),
):
    return graph_slice(plant_id=plant_id, unit_id=unit_id, asset_id=asset_id, hops=hops)

@app.get('/ops/slo')
def ops_slo_route():
    return slo_status()

@app.get('/ops/cost-per-incident')
def ops_cost_route():
    return cost_per_incident()
