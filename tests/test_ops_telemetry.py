"""ENH-10 ops telemetry — decision traces, SLO, FinOps."""

import json
from pathlib import Path

from ot_command.core import agent, ops
from ot_command.core.traces import TRACE_PATH, read_traces

ROOT = Path(__file__).resolve().parents[1]


def _envelope(**overrides):
    base = {
        "actor": "SOC analyst",
        "purpose": "ops telemetry test",
        "plant_id": "PLT-10",
        "as_of": "workshop-static",
        "policy_version": "policy.py:ACTION_TIERS",
        "asset_id": "OT-01016",
        "alert_id": "ALT-002783",
        "severity": "HIGH",
        "process_context": "UNKNOWN",
    }
    base.update(overrides)
    return base


def test_recommendation_writes_enriched_trace(tmp_path, monkeypatch):
    trace_file = tmp_path / "decision_traces.jsonl"
    monkeypatch.setattr("ot_command.core.traces.TRACE_PATH", trace_file)

    result = agent.run_incident_workflow(_envelope())
    assert result["recommendation"]["execute"] is False

    traces = read_traces()
    assert len(traces) == 1
    row = traces[0]
    assert row["decision_id"] == result["decision_id"]
    assert row["execute"] is False
    assert row.get("latency_ms") is not None
    assert row.get("tokens") == 0
    assert row.get("schema") == "contracts/decision_trace.yaml"
    assert row.get("policy_gate", {}).get("authorizable") is False


def test_ai_disabled_trace_includes_policy_gate(tmp_path, monkeypatch):
    trace_file = tmp_path / "decision_traces.jsonl"
    monkeypatch.setattr("ot_command.core.traces.TRACE_PATH", trace_file)
    agent.run_incident_workflow(_envelope())
    row = read_traces()[0]
    gate = row["policy_gate"]
    assert gate["action"] == "recommend"
    assert gate["tier"] == 1
    assert gate["open_001"] is True


def test_ops_slo_synthesizes_from_traces():
    report = ops.slo_status(eval_all_pass=True)
    assert "slos" in report
    assert report["slos"]["SLO-OT"]["status"] == "OK"
    assert report["max_agent_steps_cap"] == 12


def test_cost_per_incident_meters_tokens_and_latency():
    report = ops.cost_per_incident()
    assert "incident_count" in report
    assert "avg_tokens_per_incident" in report
    assert report["counter_metric"]


def test_decision_trace_schema_file_exists():
    schema = ROOT / "contracts" / "decision_trace.yaml"
    assert schema.exists()
    text = schema.read_text(encoding="utf-8")
    assert "decision_id" in text
    assert "execute" in text
