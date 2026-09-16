from pathlib import Path
from typing import Any
import json
import os

from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .diagnostics import run_diagnostics
from .repository import rows
from .core.identity import asset_context, identity_bundle, list_identity_conflicts, search_identity
from .core.telemetry import quality_summary, timeline
from .core.risk import rank_all
from .core.containment import recommendation_packet, safety_conflicts
from .core.recovery import plant_recovery
from .core.authority import authority_catalog
from .core.agent import ai_enabled, run_recommend
from .core.graph_slice import graph_slice
from .core.ops import cost_per_incident, slo_status
from .core.traces import recent_traces


def _apply_dotenv() -> None:
    """Honor repo `.env` for keys the process did not already set. Shell wins."""
    path = Path(__file__).resolve().parents[2] / ".env"
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


_apply_dotenv()

REPO_ROOT = Path(__file__).resolve().parents[2]
UI_ROOT = REPO_ROOT / "apps" / "command_center"
CASCADE_PATH = REPO_ROOT / "scenarios" / "cascade_001.json"

app = FastAPI(title="Synthetic ICS/OT Risk & Resilience API", version="2.0.0")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "synthetic-read-only",
        "ai_enabled": ai_enabled(),
        "explainer": "placeholder" if ai_enabled() else "omitted",
        "explainer_is_authority": False,
        "model_selected": False,
        "live_ot": False,
        "ui": "/ui",
    }


@app.get("/diagnostics")
def diagnostics():
    return run_diagnostics()


@app.get("/identity/conflicts")
def identity_conflicts():
    return list_identity_conflicts()


@app.get("/assets/{id}/context")
def asset_context_route(id: str):
    try:
        return asset_context(id)
    except KeyError:
        raise HTTPException(status_code=404, detail="unknown asset_id")


@app.get("/assets/{id}/identity")
def asset_identity_route(id: str):
    try:
        return identity_bundle(id)
    except KeyError:
        raise HTTPException(status_code=404, detail="unknown asset_id")


@app.get("/telemetry/quality")
def telemetry_quality():
    return quality_summary()


@app.get("/telemetry/timeline")
def telemetry_timeline(order: str = Query(default="event_time"), tag_id: str | None = None, limit: int = 500):
    return timeline(tag_id=tag_id, order=order, limit=limit)


@app.get("/risk/rank")
def risk_rank(limit: int = Query(default=50, ge=1, le=200)):
    return rank_all(limit=limit)


@app.get("/risk/contextual")
def risk_contextual(limit: int = Query(default=50, ge=1, le=200)):
    return rank_all(limit=limit)


@app.get("/safety/conflicts")
def safety_conflicts_route(limit: int = Query(default=50, ge=1, le=200)):
    return safety_conflicts(limit=limit)


@app.get("/recommendations/{incident_id}")
def recommendation_route(incident_id: str):
    try:
        return recommendation_packet(incident_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="unknown incident_id")


@app.get("/recovery/{plant_id}")
def recovery_plant_route(plant_id: str):
    try:
        return plant_recovery(plant_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="unknown plant_id")


@app.get("/recovery/{site_or_unit}")
def recovery_site_route(site_or_unit: str):
    try:
        return plant_recovery(site_or_unit)
    except KeyError:
        raise HTTPException(status_code=404, detail="unknown site_or_unit")


@app.get("/authority/actions")
def authority_actions_route():
    return authority_catalog()


@app.post("/recommend")
def recommend_route(payload: dict[str, Any] | None = Body(default=None)):
    return run_recommend(payload or {})


@app.get("/graph/slice")
def graph_slice_route(
    plant_id: str | None = None,
    unit_id: str | None = None,
    asset_id: str | None = None,
    hops: int = Query(default=4, ge=1, le=8),
):
    return graph_slice(plant_id=plant_id, unit_id=unit_id, asset_id=asset_id, hops=hops)


@app.get("/ops/slo")
def ops_slo_route():
    return slo_status()


@app.get("/ops/cost-per-incident")
def ops_cost_route():
    return cost_per_incident()


@app.get("/ops/traces")
def ops_traces_route(limit: int = Query(default=20, ge=1, le=100)):
    return {
        "hidden_cot_as_authority": False,
        "execute_control": False,
        "items": recent_traces(limit),
        "source_path": "data/local/decision_traces.jsonl",
    }


@app.get("/lookup")
def lookup_route(q: str = Query(default=""), limit: int = Query(default=12, ge=1, le=20)):
    """Bounded identity lookup. Not an estate dump. No CMDB winner."""
    payload = search_identity(q, limit=limit)
    extra: list[dict[str, Any]] = []
    needle = (q or "").strip().upper()
    if len(needle) >= 2 and payload["returned"] < limit:
        for rec in rows("data/raw/cyber_alerts.csv"):
            if needle in (rec.get("alert_id") or "").upper() or needle in (rec.get("asset_id") or "").upper():
                extra.append(
                    {
                        "kind": "alert",
                        "id": rec.get("alert_id"),
                        "asset_ids": [rec.get("asset_id")] if rec.get("asset_id") else [],
                        "plant_ids": [rec.get("plant_id")] if rec.get("plant_id") else [],
                        "severity": rec.get("severity"),
                        "soc_status": rec.get("soc_status"),
                        "winner": None,
                    }
                )
            if payload["returned"] + len(extra) >= limit:
                break
        if payload["returned"] + len(extra) < limit:
            for rec in rows("data/raw/vulnerabilities.csv"):
                if needle in (rec.get("finding_id") or "").upper():
                    extra.append(
                        {
                            "kind": "finding",
                            "id": rec.get("finding_id"),
                            "asset_ids": [rec.get("asset_id")] if rec.get("asset_id") else [],
                            "plant_ids": [],
                            "cvss": rec.get("cvss"),
                            "network_reachable": rec.get("network_reachable"),
                            "winner": None,
                        }
                    )
                if payload["returned"] + len(extra) >= limit:
                    break
        if payload["returned"] + len(extra) < limit:
            for rec in rows("data/reference/tags.csv"):
                if needle in (rec.get("tag_id") or "").upper() or needle in (rec.get("asset_id") or "").upper():
                    extra.append(
                        {
                            "kind": "tag",
                            "id": rec.get("tag_id"),
                            "asset_ids": [rec.get("asset_id")] if rec.get("asset_id") else [],
                            "plant_ids": [],
                            "unit_id": rec.get("unit_id"),
                            "winner": None,
                        }
                    )
                if payload["returned"] + len(extra) >= limit:
                    break
        if payload["returned"] + len(extra) < limit:
            for rec in rows("data/reference/plants.csv"):
                if needle in (rec.get("plant_id") or "").upper():
                    extra.append(
                        {
                            "kind": "plant",
                            "id": rec.get("plant_id"),
                            "asset_ids": [],
                            "plant_ids": [rec.get("plant_id")],
                            "winner": None,
                        }
                    )
                if payload["returned"] + len(extra) >= limit:
                    break
    hits = list(payload.get("hits") or []) + extra
    return {
        **payload,
        "hits": hits[:limit],
        "returned": min(len(hits), limit),
        "estate_dump": False,
        "all_plants_export": False,
        "live_ot": False,
    }


@app.get("/case/slice")
def case_slice_route(
    plant_id: str | None = None,
    asset_id: str | None = None,
    alert_id: str | None = None,
    unit_id: str | None = None,
    tag_id: str | None = None,
    hops: int = Query(default=4, ge=1, le=8),
):
    """Session-local case view. OPEN-012 durable correlation stays open. Not an estate dump."""
    try:
        hops_n = int(hops)
    except (TypeError, ValueError):
        hops_n = 4
    hops_n = min(max(hops_n, 1), 8)
    identity = None
    if asset_id:
        try:
            identity = identity_bundle(asset_id)
            plant_id = plant_id or identity.get("plant_id")
        except KeyError:
            raise HTTPException(status_code=404, detail="unknown asset_id")
    graph = None
    if plant_id or unit_id or asset_id:
        graph = graph_slice(plant_id=plant_id, unit_id=unit_id, asset_id=asset_id, hops=hops_n)
    recovery = None
    if plant_id:
        try:
            recovery = plant_recovery(plant_id)
        except KeyError:
            recovery = None
    packet = None
    if alert_id:
        try:
            packet = recommendation_packet(alert_id)
        except KeyError:
            packet = None
    tel = None
    if tag_id:
        tel = timeline(tag_id=tag_id, order="event_time", limit=12)
    cascade = None
    analogue = bool(
        alert_id == "ALT-002783"
        or asset_id == "OT-01016"
        or (plant_id == "PLT-10" and not alert_id and not asset_id)
    )
    if analogue and CASCADE_PATH.is_file():
        raw = json.loads(CASCADE_PATH.read_text(encoding="utf-8"))
        cascade = {
            "scenario_id": raw.get("scenario_id"),
            "title": raw.get("title"),
            "timeline": raw.get("timeline") or [],
            "verified_census": False,
            "open_019": True,
            "note": "Analogue timeline. 37 controllers is not a verified census (OPEN-019).",
        }
    return {
        "plant_id": plant_id,
        "asset_id": asset_id,
        "alert_id": alert_id,
        "unit_id": unit_id,
        "tag_id": tag_id,
        "correlation_id": None,
        "open_012": True,
        "winner": None,
        "live_ot": False,
        "estate_dump": False,
        "identity": identity,
        "graph": graph,
        "recovery": recovery,
        "packet": packet,
        "telemetry_timeline": tel,
        "cascade_analogue": cascade,
        "source_path": "composed gold views — bronze files unchanged",
    }


@app.get("/access/sessions")
def sessions_route(
    plant_id: str | None = None,
    identity: str | None = None,
    asset_id: str | None = None,
    limit: int = Query(default=20, ge=1, le=50),
):
    """Read-only session slice. Not change_remote_access. Not an all-plants dump (EVAL-010)."""
    recs = rows("data/raw/remote_access_sessions.csv")
    scoped = [r for r in recs if r.get("plant_id") == plant_id] if plant_id else recs
    if identity:
        scoped = [r for r in scoped if (r.get("identity") or "") == identity]
    if asset_id:
        scoped = [r for r in scoped if r.get("asset_id") == asset_id]
    unapproved = [r for r in scoped if r.get("approved_window") != "YES"]
    cap = min(int(limit), 20 if not plant_id else int(limit))
    sample = unapproved[:cap]
    return {
        "plant_id": plant_id,
        "identity": identity,
        "asset_id": asset_id,
        "all_plants_export": False,
        "unknown_is_not_approval": True,
        "change_remote_access_execute": False,
        "auto_disable_vendor_vpn": False,
        "returned": len(sample),
        "unapproved_in_scope": len(unapproved),
        "rows": sample,
        "source_path": "data/raw/remote_access_sessions.csv",
    }


_UI_SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OT Risk &amp; Resilience Command Room</title>
  <link rel="stylesheet" href="/ui/static/app.css">
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/ui/static/app.js"></script>
</body>
</html>
"""


@app.get("/ui")
@app.get("/ui/")
def ui_index():
    index = UI_ROOT / "index.html"
    bundle = UI_ROOT / "static" / "app.js"
    if not index.exists() or not bundle.exists():
        raise HTTPException(status_code=404, detail="command center UI missing")
    return HTMLResponse(_UI_SHELL, headers={"Cache-Control": "no-store"})


if (UI_ROOT / "static").is_dir():
    app.mount("/ui/static", StaticFiles(directory=str(UI_ROOT / "static")), name="ui-static")
if (UI_ROOT / "fixtures").is_dir():
    app.mount("/ui/fixtures", StaticFiles(directory=str(UI_ROOT / "fixtures")), name="ui-fixtures")
