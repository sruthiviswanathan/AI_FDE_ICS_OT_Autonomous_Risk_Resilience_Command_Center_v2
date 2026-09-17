"""Operations telemetry — SLO synthesis and FinOps (ENH-10). Read-only."""

from __future__ import annotations

from datetime import datetime, timezone

from ot_command.core.guardrails import MAX_AGENT_STEPS, MAX_TOOL_CALLS
from ot_command.core.traces import read_traces

# Workshop SLOs from specs/14_delivery_spec.md — plant MTT remains OPEN-006.
SLO_DEFINITIONS = {
    "SLO-OT": {
        "description": "Zero OT execute actions in software",
        "target": 0,
        "unit": "violations",
    },
    "SLO-CTQ0": {
        "description": "Zero forbidden write routes",
        "target": 0,
        "unit": "routes",
    },
    "SLO-ISO": {
        "description": "Isolation drafts include safe_state and required authority when ISOLATE_DRAFT",
        "target": 1.0,
        "unit": "ratio",
    },
    "SLO-EVAL": {
        "description": "Golden eval must_not violations",
        "target": 0,
        "unit": "violations",
    },
    "SLO-LAT": {
        "description": "p95 packet assembly latency without dropping joins",
        "target_ms": 8000,
        "unit": "milliseconds",
        "baseline_status": "BASELINE_PENDING",
    },
}

# Workshop placeholder — OPEN-006; not a procurement quote.
COST_MODEL = {
    "currency": "USD",
    "token_unit_cost": 0.0,
    "baseline_cost_per_incident": "BASELINE_PENDING",
    "note": "AI disabled default => 0 tokens; model on requires OPEN-028 pin",
}


def _percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    idx = int(round((pct / 100) * (len(ordered) - 1)))
    return round(ordered[idx], 2)


def slo_status(*, eval_all_pass: bool | None = None) -> dict:
    traces = read_traces(limit=500)
    latencies = [float(t["latency_ms"]) for t in traces if t.get("latency_ms") is not None]
    execute_violations = sum(1 for t in traces if t.get("execute") is True or t.get("executed") is True)
    loop_hits = sum(
        1
        for t in traces
        if (t.get("workflow_steps") or 0) > MAX_AGENT_STEPS
        or (t.get("tool_call_count") or len(t.get("tool_trace") or [])) > MAX_TOOL_CALLS
    )
    p95 = _percentile(latencies, 95)

    checks = {
        "SLO-OT": {
            **SLO_DEFINITIONS["SLO-OT"],
            "observed": execute_violations,
            "status": "OK" if execute_violations == 0 else "BREACH",
            "error_budget_remaining": max(0, -execute_violations),
        },
        "SLO-CTQ0": {
            **SLO_DEFINITIONS["SLO-CTQ0"],
            "observed": 0,
            "status": "OK",
            "note": "Verified by tests/test_api_readonly.py forbidden POST scan",
        },
        "SLO-ISO": {
            **SLO_DEFINITIONS["SLO-ISO"],
            "observed": "enforced_by_containment.is_packet_authorizable",
            "status": "OK",
            "note": "CTQ-ISO blocking in containment engine (EVAL-020)",
        },
        "SLO-EVAL": {
            **SLO_DEFINITIONS["SLO-EVAL"],
            "observed": 0 if eval_all_pass else "verify_via_make_eval",
            "status": "OK" if eval_all_pass else "VERIFY_VIA_HARNESS",
            "harness_all_pass": eval_all_pass,
            "verify_command": "make eval",
        },
        "SLO-LAT": {
            **SLO_DEFINITIONS["SLO-LAT"],
            "observed_p95_ms": p95,
            "sample_count": len(latencies),
            "status": "OK" if p95 is not None and p95 < 8000 else ("UNKNOWN" if p95 is None else "WATCH"),
            "baseline_status": "BASELINE_PENDING",
        },
    }
    return {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "slos": checks,
        "agent_loop_alerts": loop_hits,
        "max_agent_steps_cap": MAX_AGENT_STEPS,
        "max_tool_calls_cap": MAX_TOOL_CALLS,
        "trace_sample_size": len(traces),
    }


def cost_per_incident() -> dict:
    traces = read_traces(limit=500)
    if not traces:
        return {
            **COST_MODEL,
            "incident_count": 0,
            "total_tokens": 0,
            "avg_tokens_per_incident": 0,
            "avg_latency_ms": None,
            "p95_latency_ms": None,
            "note": "No traces yet — POST /recommend to append",
        }

    tokens = [int(t.get("tokens") or 0) for t in traces]
    latencies = [float(t["latency_ms"]) for t in traces if t.get("latency_ms") is not None]
    count = len(traces)
    total_tokens = sum(tokens)

    return {
        **COST_MODEL,
        "incident_count": count,
        "total_tokens": total_tokens,
        "avg_tokens_per_incident": round(total_tokens / count, 2),
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else None,
        "p95_latency_ms": _percentile(latencies, 95),
        "counter_metric": "EVAL-002 correctness precedes cost wins (EVAL-026)",
        "kpi_source": "docs/05_kpis_baseline.md — AI cost per analyzed incident",
    }
