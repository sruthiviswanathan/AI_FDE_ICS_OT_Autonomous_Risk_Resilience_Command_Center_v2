"""Read-only API contract (ADR-11, FR-013). No TestClient / extra deps.

Gold GET assertions fail until routes exist. Write-route scan may pass today (CTQ-0).
"""

from ot_command.api import app

WRITE = {"POST", "PUT", "PATCH", "DELETE"}
FORBIDDEN_PATH_TOKENS = (
    "isolate",
    "plc",
    "setpoint",
    "sis",
    "interlock",
    "firewall",
    "bypass",
    "suppress_trip",
    "write_plc",
)
GOLD_GETS = (
    "/assets/{id}/identity",
    "/telemetry/quality",
    "/risk/contextual",
    "/safety/conflicts",
    "/recovery/{site_or_unit}",
    "/recommendations/{incident_id}",
    "/authority/actions",
    "/graph/slice",
)


def _routes():
    out = []
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = set(getattr(route, "methods", None) or [])
        if path:
            out.append((path, methods))
    return out


def test_baseline_health_and_diagnostics_remain():
    paths = {p for p, _ in _routes()}
    assert "/health" in paths
    assert "/diagnostics" in paths


def test_no_ot_write_or_isolate_execute_routes():
    offenders = []
    for path, methods in _routes():
        writes = methods & WRITE
        if not writes:
            continue
        low = path.lower()
        if any(tok in low for tok in FORBIDDEN_PATH_TOKENS):
            offenders.append((path, sorted(writes)))
    assert offenders == []


def test_gold_read_routes_from_delivery_spec_exist():
    paths = {p for p, methods in _routes() if "GET" in methods}
    missing = [expected for expected in GOLD_GETS if expected not in paths]
    assert missing == [], f"gold GET missing: {missing}"
