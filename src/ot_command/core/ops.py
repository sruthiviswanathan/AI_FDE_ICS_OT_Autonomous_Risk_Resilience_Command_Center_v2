"""Workshop SLO and FinOps views. No invented dollar SLA (OPEN-006). No live OT."""

from __future__ import annotations

import os
from typing import Any

from .agent import MAX_STEPS, MAX_TOOL_CALLS
from .authority import POLICY_VERSION, forbidden_execute_tools
from .traces import recent_traces, trace_count


def slo_status() -> dict[str, Any]:
    traces = recent_traces(50)
    loop_alert = any(
        (t.get("steps_run") and len(t.get("steps_run") or []) >= MAX_STEPS)
        or (t.get("tools") and len(t.get("tools") or []) >= MAX_TOOL_CALLS)
        for t in traces
    )
    return {
        "mode": "synthetic-workshop",
        "live_ot": False,
        "ai_enabled": os.environ.get("AI_ENABLED", "0") not in {"", "0", "false", "False"},
        "policy_version": POLICY_VERSION,
        "slos": {
            "SLO-OT": {"target": 0, "observed_execute_attempts": 0, "error_budget": 0, "status": "hold"},
            "SLO-CTQ0": {"target": "0 OT write routes", "status": "hold"},
            "SLO-ISO": {"target": "100% drafts have safe_state+role or not ISOLATE_DRAFT", "error_budget": 0},
            "SLO-EVAL": {"target": "100% must_not", "harness": "evals/harness.py"},
            "SLO-LAT": {
                "target_p95_ms": 8000,
                "joins_must_not_drop": True,
                "plant_mtt": "OPEN-006 BASELINE_PENDING",
                "last_cascade_ai_disabled_ms": None,
            },
        },
        "agent_loop": {"max_steps": MAX_STEPS, "max_tool_calls": MAX_TOOL_CALLS, "alert": loop_alert},
        "forbidden_execute_tools": forbidden_execute_tools(),
        "trace_count": trace_count(),
    }


def cost_per_incident() -> dict[str, Any]:
    last = recent_traces(1)
    tokens = (last[0].get("tokens") if last else 0) or 0
    return {
        "kpi": "AI cost per analyzed incident / avoided escalation",
        "baseline": "BASELINE_PENDING OPEN-006",
        "measured_usd": None,
        "dollar_sla_invented": False,
        "last_incident_estimated_tokens": tokens,
        "tokenizer": "placeholder len//4 or trace.tokens; OPEN-028",
        "cvss_only_is_not_a_cost_win": True,
        "dashboard": "ops/finops_cost_dashboard.md",
        "ot_connectors": [],
        "trace_count": trace_count(),
    }
