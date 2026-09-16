"""Route and action surface checks for read-only / deny-by-default gates."""

FORBIDDEN_POST_PATHS = (
    "/isolate",
    "/firewall",
    "/plc",
    "/sis",
    "/setpoint",
    "/bypass",
)

EXPECTED_GOLD_GET_PATHS = (
    "/assets/{id}/identity",
    "/telemetry/quality",
    "/risk/contextual",
    "/safety/conflicts",
    "/recovery/{site_or_unit}",
    "/recommendations/{incident_id}",
    "/authority/actions",
    "/graph/slice",
)
