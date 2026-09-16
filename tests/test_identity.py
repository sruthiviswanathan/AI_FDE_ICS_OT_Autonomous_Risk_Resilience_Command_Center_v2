"""Target-state identity tests (ADR-01). Fail until ot_command.core.identity exists."""

from tests.helpers.access import as_id_set, field
from tests.helpers.golden import golden_case


def test_eval_001_alias_collision_lists_both_ids_and_no_cmdb_winner():
    case = golden_case("EVAL-001")
    fx = case["fixture"]
    from ot_command.core.identity import reconcile_alias

    bundle = reconcile_alias(fx["alias"])
    ids = as_id_set(bundle)
    assert set(fx["asset_ids"]) <= ids
    assert field(bundle, "confidence") < 1
    assert field(bundle, "winner") in (None, "", False)
    sources = field(bundle, "sources") or [
        field(a, "source") for a in (field(bundle, "aliases") or [])
    ]
    assert "PASSIVE" in sources
    assert field(bundle, "canonical_source") != "CMDB"


def test_eval_028_keeps_retired_and_online():
    fx = golden_case("EVAL-028")["fixture"]
    from ot_command.core.identity import identity_bundle

    bundle = identity_bundle(fx["asset_id"])
    assert field(bundle, "registered_state") == "RETIRED"
    assert field(bundle, "observed_state") == "ONLINE"
    assert field(bundle, "confidence") < 1
    assert field(bundle, "winner") in (None, "", False)


def test_eval_029_shadow_spreadsheet_is_not_cmdb():
    fx = golden_case("EVAL-029")["fixture"]
    from ot_command.core.identity import shadow_overlay_status

    overlay = shadow_overlay_status()
    assert field(overlay, "row_count") == fx["shadow_n"]
    assert field(overlay, "is_cmdb") is False
    assert field(overlay, "promoted_to_master") is False
    conf = field(overlay, "confidence")
    assert conf is not None and conf < 1


def test_eval_008_does_not_delete_colliding_aliases():
    from ot_command.core.identity import reconcile_alias

    bundle = reconcile_alias("PLT-01-DCS_CONTROLLER-105")
    assert len(as_id_set(bundle)) >= 2


def test_adr10_v1_operational_state_is_not_observed_state():
    from ot_command.core.identity import identity_bundle

    bundle = identity_bundle("OT-01016")
    observed = field(bundle, "observed_state")
    parked = field(bundle, "legacy_v1_operational_state")
    assert observed != "operationalState"
    if parked is not None:
        assert parked != observed or field(bundle, "observed_state") in {
            "ONLINE",
            "OFFLINE",
            "UNSEEN",
            "INTERMITTENT",
        }
    observations = field(bundle, "observations") or {}
    v1 = field(observations, "v1") or {}
    assert field(v1, "operationalState") != observed
    assert field(v1, "operationalState") in (None, "")
    v2 = field(observations, "v2") or {}
    assert field(v2, "observed_state") == observed


def test_enh02_identity_routes_are_get_only():
    from ot_command.api import app

    found = {}
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = set(getattr(route, "methods", None) or [])
        if path in {"/identity/conflicts", "/assets/{id}/context", "/assets/{id}/identity"}:
            found[path] = methods
    assert "/identity/conflicts" in found
    assert "/assets/{id}/context" in found
    assert "/assets/{id}/identity" in found
    for path, methods in found.items():
        assert "GET" in methods
        assert not (methods & {"POST", "PUT", "PATCH", "DELETE"})

