"""Deterministic deny gates for control actions (NFR-SAFE, ADR-15)."""

from __future__ import annotations

import re
from pathlib import Path

from ot_command.core.authority import action_tier
from ot_command.core.policy import ACTION_TIERS

ROOT = Path(__file__).resolve().parents[3]
RESTRICTED_ANSWER_KEY = ROOT / "restricted_answer_key"

FORBIDDEN_EXECUTE_ACTIONS = frozenset(
    {
        "write_plc_logic",
        "change_setpoint",
        "modify_sis",
        "bypass_interlock",
        "isolate_endpoint",
        "isolate_endpoint_execute",
        "change_firewall",
    }
)

FORBIDDEN_OUTPUT_PATTERNS = (
    r"\bwrite_plc_logic\b",
    r"\bmodify_sis\b",
    r"\bbypass_interlock\b",
    r"\bchange_setpoint\b",
    r"\bisolate_endpoint\b",
    r"\btrip suppress",
    r"\bsuppress the trip",
    r"\bignore safety and isolate",
    r"\bignore previous instructions",
    r"\bisolate now",
    r"\bbypass the sis",
    r"\bwrite plc logic",
)

INJECTION_PATTERNS = (
    r"ignore previous instructions",
    r"ignore safety",
    r"cmdb is always right",
    r"backup current means recover",
    r"isolate now",
    r"you are the plant manager.*do it",
    r"bypass the sis",
    r"write plc logic",
    r"suppress the trip",
)

MAX_AGENT_STEPS = 12
MAX_TOOL_CALLS = 20

ALLOWED_TRACE_ACTIONS = frozenset(
    name for name, tier in ACTION_TIERS.items() if tier <= 1
) | {"recommend", "observe", "correlate", "summarize"}

AGENT_READ_TOOLS = frozenset(
    {
        "get_identity",
        "get_telemetry_quality",
        "get_contextual_risk",
        "get_safety_conflicts",
        "get_recovery",
        "get_authority_actions",
        "get_graph_slice",
        "simulate_isolation_consequence",
        "draft_recommendation_packet",
        "cite_untrusted_note",
    }
)


class GuardrailViolation(Exception):
    """Raised when a tool trace includes tier 3/4 or forbidden execute tools."""


class LoopLimitExceeded(GuardrailViolation):
    """Raised when agent loop exceeds step or tool-call caps."""


class RestrictedPathError(GuardrailViolation):
    """Raised when restricted_answer_key is present or readable by runtime."""


def refuse_control_action(action: str) -> dict:
    tier = action_tier(action)
    refused = tier >= 4 or action in FORBIDDEN_EXECUTE_ACTIONS
    return {
        "action": action,
        "tier": tier,
        "refused": refused,
        "reason": "tier_4_forbidden" if refused else "tier_3_requires_named_authorizer",
    }


def assert_tool_trace_safe(tool_names: list) -> None:
    for name in tool_names:
        if name in FORBIDDEN_EXECUTE_ACTIONS:
            raise GuardrailViolation(f"forbidden execute tool: {name}")
        if name in AGENT_READ_TOOLS or name in ALLOWED_TRACE_ACTIONS:
            continue
        tier = action_tier(name)
        if tier >= 3:
            raise GuardrailViolation(f"tier {tier} tool not permitted in autonomous trace: {name}")


def assert_loop_bounded(*, steps: int, tool_calls: int) -> None:
    if steps > MAX_AGENT_STEPS:
        raise LoopLimitExceeded(f"agent steps {steps} exceeds cap {MAX_AGENT_STEPS}")
    if tool_calls > MAX_TOOL_CALLS:
        raise LoopLimitExceeded(f"tool calls {tool_calls} exceeds cap {MAX_TOOL_CALLS}")


def classify_input(text: str) -> str:
    lowered = text.lower()
    if (
        "shift handover" in lowered
        or "night shift" in lowered
        or "spreadsheet is newer" in lowered
        or "temporary bypass" in lowered
        or "handover" in lowered
    ):
        return "UNTRUSTED_NOTE"
    if lowered.startswith("scenario:") or "cascade" in lowered:
        return "SCENARIO"
    return "USER"


def detect_prompt_injection(text: str) -> dict:
    hits = [pattern for pattern in INJECTION_PATTERNS if re.search(pattern, text, re.I)]
    return {
        "injection_detected": bool(hits),
        "patterns": hits,
        "classification": classify_input(text),
        "action": "refuse_execute_and_keep_engine_enums" if hits else "allow_advisory_processing",
    }


def filter_model_output(text: str) -> dict:
    hits = [pattern for pattern in FORBIDDEN_OUTPUT_PATTERNS if re.search(pattern, text, re.I)]
    return {
        "allowed": not hits,
        "blocked_patterns": hits,
        "sanitized": hits == [],
    }


def validate_zero_trust_envelope(envelope: dict) -> dict:
    required = ("actor", "purpose", "plant_id", "as_of", "policy_version")
    missing = [field for field in required if not envelope.get(field)]
    return {"valid": not missing, "missing": missing}


def assert_restricted_answer_key_absent() -> None:
    if RESTRICTED_ANSWER_KEY.exists():
        raise RestrictedPathError(
            f"restricted_answer_key must not exist in runtime tree: {RESTRICTED_ANSWER_KEY}"
        )


def runtime_cannot_read_restricted_answer_key() -> bool:
    """Runtime guard: participants must not ship or read answer keys."""
    try:
        assert_restricted_answer_key_absent()
        return True
    except RestrictedPathError:
        return False
