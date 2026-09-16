import pytest

from ot_command.api import app
from tests.helpers.access import FORBIDDEN_POST_PATHS


def _route_map():
    out = {}
    for route in app.routes:
        methods = getattr(route, "methods", None) or set()
        path = getattr(route, "path", None)
        if path:
            out[path] = methods
    return out


def test_health_and_diagnostics_are_get_only():
    routes = _route_map()
    assert routes["/health"] == {"GET"}
    assert routes["/diagnostics"] == {"GET"}
    assert "POST" not in routes["/health"]
    assert "POST" not in routes["/diagnostics"]


def test_no_forbidden_control_post_routes():
    routes = _route_map()
    post_paths = {p for p, m in routes.items() if "POST" in m}
    for forbidden in FORBIDDEN_POST_PATHS:
        assert forbidden not in post_paths


def test_gold_read_routes_exist_as_get():
    """FR-013 gold GETs — fail until ENH-02…07 wire routes."""
    routes = _route_map()
    required = (
        "/assets/{id}/identity",
        "/telemetry/quality",
        "/risk/contextual",
        "/safety/conflicts",
        "/recovery/{site_or_unit}",
        "/authority/actions",
        "/graph/slice",
    )
    for path in required:
        assert path in routes, f"missing gold GET route: {path}"
        assert "GET" in routes[path]
        assert "POST" not in routes[path]
