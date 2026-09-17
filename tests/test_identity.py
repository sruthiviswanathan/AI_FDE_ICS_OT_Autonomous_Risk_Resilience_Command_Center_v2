import pytest

from ot_command.core import identity
from tests.helpers.golden import get_golden_case


EVAL_001 = get_golden_case("EVAL-001")


def test_eval_001_alias_collision_lists_both_assets_without_merge():
    alias = EVAL_001["fixture"]["alias"]
    bundle = identity.resolve_alias(alias)
    asset_ids = {c["asset_id"] for c in bundle["candidates"]}
    assert asset_ids == set(EVAL_001["fixture"]["asset_ids"])
    assert bundle.get("merged") is not True
    assert bundle.get("cmdb_winner") is not True


def test_eval_001_must_include_evidence_source_confidence():
    alias = EVAL_001["fixture"]["alias"]
    bundle = identity.resolve_alias(alias)
    for key in ("evidence", "source", "confidence"):
        assert key in bundle
    assert bundle["confidence"] < 1.0


def test_active_offline_state_conflict_visible():
    bundle = identity.get_identity_bundle("OT-00012")
    assert bundle["registered_state"] == "ACTIVE"
    assert bundle["observed_state"] in {"OFFLINE", "UNSEEN", "ONLINE"}
    assert bundle.get("state_conflict") is True or "conflicts" in bundle


def test_list_identity_conflicts_matches_diagnostics_order_of_magnitude():
    summary = identity.list_identity_conflicts()
    assert summary["alias_collisions"] >= 5
    assert summary["asset_state_conflicts"] >= 200
    assert summary["conflict_count"] >= summary["asset_state_conflicts"]


def test_list_identity_conflicts_scoped_by_plant():
    estate = identity.list_identity_conflicts()
    plt01 = identity.list_identity_conflicts(plant_id="PLT-01")
    plt02 = identity.list_identity_conflicts(plant_id="PLT-02")

    assert plt01["plant_id"] == "PLT-01"
    assert plt01["asset_state_conflicts"] < estate["asset_state_conflicts"]
    assert plt01["alias_collisions"] <= estate["alias_collisions"]
    assert plt01["conflict_count"] == len(plt01["conflicts"])
    assert all(row["plant_id"] == "PLT-01" for row in plt01["conflicts"])
    state_row = next(r for r in plt01["conflicts"] if r["type"] == "REGISTERED_VS_OBSERVED")
    assert state_row["registered_state"] == "ACTIVE"
    assert state_row["observed_state"] in {"OFFLINE", "UNSEEN"}
    assert plt01["asset_state_conflicts"] != plt02["asset_state_conflicts"] or plt01["plant_id"] != plt02["plant_id"]
