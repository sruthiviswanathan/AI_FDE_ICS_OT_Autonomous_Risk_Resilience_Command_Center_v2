from fastapi import FastAPI, HTTPException, Query
from .diagnostics import run_diagnostics
from .core.identity import asset_context, identity_bundle, list_identity_conflicts
from .core.telemetry import quality_summary, timeline

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
