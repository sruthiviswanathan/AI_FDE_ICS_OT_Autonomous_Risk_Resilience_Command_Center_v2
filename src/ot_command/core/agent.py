"""Bounded Incident Analyst workflow (FR-012, ADR-07/12/14). Deterministic; LLM optional OFF."""

from __future__ import annotations

import os
import time
from uuid import uuid4

from ot_command.core import authority, containment, identity, recovery, risk, telemetry
from ot_command.core.guardrails import (
    assert_loop_bounded,
    assert_tool_trace_safe,
    detect_prompt_injection,
    refuse_control_action,
)
from ot_command.core.traces import append_trace

PROMPT_REGISTRY = {
    "incident_analyst": {
        "semver": "1.0.0",
        "path": "config/prompts/incident_analyst_v1.md",
        "eval_gate": ["EVAL-014", "EVAL-016", "EVAL-020", "EVAL-021"],
    }
}

MODEL_PIN = {"provider": "none", "model_version": "none", "note": "OPEN-028 placeholder"}

WORKFLOW_DISPLAY_STATES = (
    "Request Validation",
    "Identity Resolution",
    "Risk Correlation",
    "Safety Evaluation",
    "Recovery Evaluation",
    "Authority Evaluation",
    "Recommendation Generation",
    "Human Review",
)

ALLOWED_TOOLS = frozenset(
    {
        "get_identity",
        "get_telemetry_quality",
        "get_contextual_risk",
        "get_safety_conflicts",
        "get_recovery",
        "get_authority_actions",
        "simulate_isolation_consequence",
        "draft_recommendation_packet",
        "cite_untrusted_note",
    }
)


class AgentValidationError(Exception):
    """Missing required envelope fields."""


def _ai_enabled() -> bool:
    return os.environ.get("AI_ENABLED", "0").strip() in {"1", "true", "TRUE", "yes"}


def _count_evidence(payload) -> int:
    if isinstance(payload, dict):
        if "evidence" in payload and isinstance(payload["evidence"], list):
            return len(payload["evidence"])
        return sum(_count_evidence(v) for v in payload.values() if isinstance(v, (dict, list)))
    if isinstance(payload, list):
        return sum(_count_evidence(item) for item in payload)
    return 0


def _confidence(payload: dict | None, default: float = 0.7) -> float:
    if not payload:
        return default
    if "confidence" in payload:
        try:
            return float(payload["confidence"])
        except (TypeError, ValueError):
            return default
    if "uncertainty" in payload and isinstance(payload["uncertainty"], dict):
        return float(payload["uncertainty"].get("confidence", default))
    return default


def _run_state(
    state_name: str,
    fn,
    *,
    tool_calls: list[str],
) -> tuple[dict, object]:
    start = time.perf_counter()
    payload = fn()
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    return (
        {
            "state": state_name,
            "timing_ms": elapsed_ms,
            "evidence_count": _count_evidence(payload),
            "confidence": _confidence(payload if isinstance(payload, dict) else None),
            "tool_calls_used": tool_calls,
        },
        payload,
    )


def validate_request(envelope: dict) -> dict:
    required = ("actor", "purpose", "plant_id", "as_of", "policy_version")
    missing = [field for field in required if not envelope.get(field)]
    if missing:
        raise AgentValidationError(f"missing envelope fields: {missing}")
    injection = None
    if envelope.get("user_prompt"):
        injection = detect_prompt_injection(envelope["user_prompt"])
        if injection["injection_detected"]:
            envelope["_injection_flag"] = True
    return {"valid": True, "missing": missing, "injection_scan": injection}


def simulate_isolation_consequence(*, asset_id: str, plant_id: str) -> dict:
    packet = containment.assess_isolation(severity="HIGH", asset_id=asset_id)
    return {
        "simulation_only": True,
        "asset_id": asset_id,
        "plant_id": plant_id,
        "predicted_process_impact": packet.get("process_impact"),
        "predicted_safety_impact": packet.get("safety_impact"),
        "isolation_recommendation": packet.get("recommendation"),
        "execute": False,
        "note": "Read-only view — no network/PLC API call",
    }


def run_incident_workflow(envelope: dict) -> dict:
    workflow_start = time.perf_counter()
    decision_id = str(uuid4())
    tool_trace: list[str] = []
    workflow_states: list[dict] = []

    def track(tool: str) -> None:
        if tool not in ALLOWED_TOOLS and tool not in {"observe", "correlate", "summarize", "recommend"}:
            refuse = refuse_control_action(tool)
            if refuse["refused"]:
                raise AgentValidationError(f"forbidden tool: {tool}")
        tool_trace.append(tool)

    # 1 Request Validation
    state, validation = _run_state(
        "Request Validation",
        lambda: validate_request(envelope),
        tool_calls=[],
    )
    workflow_states.append(state)

    asset_id = envelope.get("asset_id")
    alert_id = envelope.get("alert_id")
    plant_id = envelope["plant_id"]

    # 2 Identity Resolution
    track("get_identity")
    state, identity_bundle = _run_state(
        "Identity Resolution",
        lambda: identity.get_identity_bundle(asset_id) if asset_id else {"note": "asset_id not supplied"},
        tool_calls=["get_identity"],
    )
    workflow_states.append(state)

    # 3 Risk Correlation
    track("get_contextual_risk")
    state, risk_view = _run_state(
        "Risk Correlation",
        lambda: risk.rank_corpus(limit=5),
        tool_calls=["get_contextual_risk"],
    )
    workflow_states.append(state)

    # 4 Safety Evaluation
    track("get_safety_conflicts")
    if asset_id:
        track("simulate_isolation_consequence")
    state, safety_view = _run_state(
        "Safety Evaluation",
        lambda: {
            "conflicts": containment.list_safety_conflicts(plant_id=plant_id),
            "isolation_simulation": simulate_isolation_consequence(asset_id=asset_id, plant_id=plant_id)
            if asset_id
            else None,
        },
        tool_calls=["get_safety_conflicts"] + (["simulate_isolation_consequence"] if asset_id else []),
    )
    workflow_states.append(state)

    # 5 Recovery Evaluation
    track("get_recovery")
    state, recovery_view = _run_state(
        "Recovery Evaluation",
        lambda: recovery.get_plant_recovery_view(plant_id),
        tool_calls=["get_recovery"],
    )
    workflow_states.append(state)

    # 6 Authority Evaluation
    track("get_authority_actions")
    state, authority_view = _run_state(
        "Authority Evaluation",
        lambda: authority.catalog(),
        tool_calls=["get_authority_actions"],
    )
    workflow_states.append(state)

    # 7 Recommendation Generation
    track("draft_recommendation_packet")
    state, recommendation = _run_state(
        "Recommendation Generation",
        lambda: containment.assess_isolation(
            severity=envelope.get("severity", "HIGH"),
            asset_id=asset_id,
            alert_id=alert_id,
            process_context=envelope.get("process_context"),
        ),
        tool_calls=["draft_recommendation_packet"],
    )
    workflow_states.append(state)

    # 8 Human Review
    state, review = _run_state(
        "Human Review",
        lambda: {
            "status": "AwaitAuthorization",
            "required_authority": recommendation.get("required_authority"),
            "execute": False,
            "named_authorizer": "OPEN-001",
            "ai_enabled": _ai_enabled(),
            "manual_fallback": "Engines render tables when AI_ENABLED=0 (ADR-12)",
        },
        tool_calls=[],
    )
    workflow_states.append(state)

    assert_tool_trace_safe(tool_trace)
    assert_loop_bounded(steps=len(workflow_states), tool_calls=len(tool_trace))

    result = {
        "decision_id": decision_id,
        "agent": "IncidentAnalyst",
        "prompt_id": "incident_analyst",
        "prompt_semver": PROMPT_REGISTRY["incident_analyst"]["semver"],
        "model_pin": MODEL_PIN,
        "policy_version": envelope["policy_version"],
        "workflow_states": workflow_states,
        "tool_trace": tool_trace,
        "recommendation": recommendation,
        "identity_bundle": identity_bundle if asset_id else None,
        "risk_preview": risk_view,
        "recovery_preview": recovery_view,
        "authority_preview": authority_view,
        "human_review": review,
        "ai_enabled": _ai_enabled(),
        "explainer": None if not _ai_enabled() else {"status": "optional_off_by_default"},
    }

    elapsed_ms = round((time.perf_counter() - workflow_start) * 1000, 2)
    append_trace(
        {
            "decision_id": decision_id,
            "actor": envelope["actor"],
            "purpose": envelope["purpose"],
            "plant_id": plant_id,
            "tool_trace": tool_trace,
            "recommendation": recommendation.get("recommendation"),
            "execute": False,
            "tokens": 0 if not _ai_enabled() else None,
            "latency_ms": elapsed_ms,
            "ai_enabled": _ai_enabled(),
            "workflow_steps": len(workflow_states),
            "tool_call_count": len(tool_trace),
            "policy_gate": {
                "action": "recommend",
                "tier": 1,
                "allowed": True,
                "authorizable": containment.is_packet_authorizable(recommendation),
                "open_001": True,
                "policy_version": envelope["policy_version"],
            },
            "model_version": MODEL_PIN.get("model_version"),
            "prompt_id": "incident_analyst",
        }
    )
    return result


def manual_fallback_tables() -> dict:
    """AI-disabled path (EVAL-016): deterministic tables without LLM."""
    return {
        "identity_conflicts": identity.list_identity_conflicts(),
        "telemetry_quality": telemetry.telemetry_quality_summary(),
        "recovery_plt_01": recovery.get_plant_recovery_view("PLT-01"),
        "authority": authority.catalog(),
        "ai_enabled": False,
    }
