"""ENH-10 ops telemetry. Recommendation persists a trace. AI-disabled still records policy_gate."""

import os

from tests.helpers.access import field


def test_recommend_persists_decision_trace_when_ai_disabled():
    from ot_command.core.agent import run_recommend
    from ot_command.core.traces import recent_traces, trace_count

    os.environ["AI_ENABLED"] = "0"
    before = trace_count()
    packet = run_recommend({"plant_id": "PLT-01", "action": "recommend"})
    assert field(packet, "executed") is not True
    assert field(packet, "explanation") is None
    assert field(packet, "trace")
    assert (packet.get("trace") or {}).get("policy")
    assert trace_count() >= before + 1
    last = recent_traces(1)[-1]
    assert last.get("policy_gate") or last.get("policy")
    assert last.get("hidden_cot_as_authority") is False
    assert last.get("execute_control") is False


def test_graph_slice_is_hop_capped_and_not_estate_dump():
    from ot_command.core.graph_slice import HOP_CAP, graph_slice

    empty = graph_slice()
    assert empty["whole_graph_dump"] is False
    assert empty["nodes"] == []
    sliced = graph_slice(plant_id="PLT-10", hops=99)
    assert sliced["hops"] == HOP_CAP
    assert sliced["whole_graph_dump"] is False
    assert sliced["imputed_tag_to_unit"] is False
    plants = {n.get("plant_id") for n in sliced["nodes"] if n.get("type") == "process_unit"}
    assert plants <= {"PLT-10"} or not plants


def test_ops_routes_are_get_only_and_gold_graph_exists():
    from ot_command.api import app

    found = {}
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = set(getattr(route, "methods", None) or [])
        if path in {"/graph/slice", "/ops/slo", "/ops/cost-per-incident"}:
            found[path] = methods
    assert "/graph/slice" in found
    for methods in found.values():
        assert "GET" in methods
        assert not (methods & {"POST", "PUT", "PATCH", "DELETE"})


def test_cost_per_incident_does_not_invent_dollar_sla():
    from ot_command.core.ops import cost_per_incident

    row = cost_per_incident()
    assert row["measured_usd"] is None
    assert row["dollar_sla_invented"] is False
    assert row["cvss_only_is_not_a_cost_win"] is True
    assert row["ot_connectors"] == []
