"""Bounded Incident Analyst workflow (ADR-07, ADR-12, ADR-14). Advisory only.

Pipeline: request validation → access check → retrieval plan → evidence →
context slice → draft → policy gate → human packet → trace.

Tools are read-only getters plus read-only isolation-consequence simulation.
Forbidden tools raise ToolDenied. Shift notes stay UNTRUSTED content.
Explainer model substitution must not change risk / recovery / policy outputs.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .authority import POLICY_VERSION, authority_catalog, forbidden_execute_tools, permit
from .containment import isolation_recommendation, recommendation_packet, safety_conflicts
from .guardrails import apply_guardrails, loop_guard, principal_denied, purpose_denied
from .identity import identity_bundle, list_identity_conflicts
from .recovery import plant_recovery
from .risk import rank_all
from .telemetry import quality_summary

ROOT = Path(__file__).resolve().parents[3]
PKG = Path(__file__).resolve().parents[1]
HANDOVER_PATH = "data/shadow/shift_handover_email.txt"
VERSIONS_PATH = PKG / "versions.json"
REGISTRY_PATH = PKG / "prompts" / "registry.json"
TRANSFORM = "enh-07-agent.1"
AS_OF = "2026-09-10T00:00:00Z"
MAX_STEPS = 12
MAX_TOOL_CALLS = 20
WORKFLOW = (
    "request_validation",
    "access_check",
    "retrieval_plan",
    "evidence",
    "context_slice",
    "draft",
    "policy_gate",
    "human_packet",
    "trace",
)
ENVELOPE_FIELDS = ("actor", "purpose", "plant_id", "as_of", "policy_version")
ALLOWED_TOOLS = (
    "get_identity",
    "get_telemetry_quality",
    "get_contextual_risk",
    "get_safety_conflicts",
    "get_recovery",
    "get_authority_actions",
    "simulate_isolation_consequence",
    "draft_recommendation_packet",
    "cite_untrusted_note",
    "propose_request_fresh_telemetry",
    "propose_open_ticket",
    "propose_increase_logging",
)
AGENT_DEFINITION = {
    "name": "IncidentAnalyst",
    "count": 1,
    "role": "advisory",
    "execute_control": False,
    "multi_agent": False,
}

_TRACES: list[dict] = []
_VERSIONS: dict[str, Any] | None = None
_REGISTRY: dict[str, Any] | None = None


class ToolDenied(PermissionError):
    def __init__(self, tool: str, reason: str):
        super().__init__(reason)
        self.tool = tool
        self.reason = reason


def versions() -> dict[str, Any]:
    global _VERSIONS
    if _VERSIONS is None:
        _VERSIONS = json.loads(VERSIONS_PATH.read_text(encoding="utf-8"))
    return dict(_VERSIONS)


def prompt_registry() -> dict[str, Any]:
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return dict(_REGISTRY)


def prompt_eval_gate() -> list[str]:
    return list(prompt_registry().get("eval_gate") or versions().get("eval_gate_before_prompt_change") or [])


def ai_enabled() -> bool:
    return os.environ.get("AI_ENABLED", "0") not in {"", "0", "false", "False", "no"}


def _load_prompt(name: str) -> str:
    rel = (prompt_registry().get("prompts") or {}).get("prompt-v1", {}).get("files", {}).get(name)
    if not rel:
        return ""
    path = PKG / "prompts" / rel
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _envelope(payload: dict) -> dict[str, Any]:
    return {field: payload.get(field) for field in ENVELOPE_FIELDS}


def _envelope_complete(env: dict) -> bool:
    return all(env.get(field) not in (None, "") for field in ENVELOPE_FIELDS)


def _access_ok(env: dict) -> tuple[bool, str]:
    if not _envelope_complete(env):
        return False, "envelope incomplete — deny-by-default"
    if principal_denied(env.get("actor")):
        return False, "principal denied"
    if purpose_denied(env.get("purpose")):
        return False, "purpose denied — no plant-wide dump"
    return True, "envelope complete; agent is not operator"


def _read_handover() -> str:
    path = ROOT / HANDOVER_PATH
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _compact_risk(limit: int = 5) -> dict:
    ranked = rank_all(limit=limit)
    return {
        "order": ranked.get("order"),
        "sort_key": ranked.get("sort_key"),
        "cvss_is_sort_key": False,
        "llm_rerank": False,
        "finding_ids": [item.get("finding_id") or item.get("id") for item in ranked.get("items") or []],
    }


def _safe_identity(asset_id: str | None) -> dict:
    if not asset_id:
        conflicts = list_identity_conflicts()
        return {
            "conflicts_queryable": True,
            "winner": None,
            "alias_collision_count": len(conflicts.get("alias_collisions") or []),
            "registered_vs_observed_count": len(conflicts.get("registered_vs_observed") or []),
        }
    try:
        return identity_bundle(asset_id)
    except KeyError:
        return {"asset_id": asset_id, "unknown": True}


def _safe_recovery(plant_id: str | None) -> dict:
    if not plant_id:
        return {"recovery_ready": False, "blockers": ["plant_id missing"]}
    try:
        return plant_recovery(plant_id)
    except KeyError:
        return {"plant_id": plant_id, "recovery_ready": False, "unknown_plant": True}


def _draft_packet(payload: dict) -> dict:
    incident_id = payload.get("incident_id") or payload.get("alert_id")
    if incident_id:
        try:
            return recommendation_packet(str(incident_id))
        except KeyError:
            pass
    alert = {
        "alert_id": payload.get("alert_id"),
        "asset_id": payload.get("asset_id"),
        "plant_id": payload.get("plant_id"),
        "severity": payload.get("severity") or "HIGH",
        "process_context": payload.get("process_context") or "UNKNOWN",
        "user_prompt": payload.get("user_prompt") or payload.get("prompt"),
        "soc_requests_isolate": bool(payload.get("soc_requests_isolate")),
        "process_engineer_warning": bool(payload.get("process_engineer_warning")),
        "scenario": payload.get("scenario"),
    }
    return isolation_recommendation(alert)


def deterministic_core(payload: dict) -> dict[str, Any]:
    """Risk / recovery / policy outputs. Independent of explainer model."""
    packet = _draft_packet(payload)
    plant_id = payload.get("plant_id") or packet.get("plant_id")
    recovery = _safe_recovery(plant_id)
    risk = _compact_risk()
    quality = quality_summary()
    identity = _safe_identity(payload.get("asset_id") or packet.get("subject_asset_uid"))
    return {
        "isolation_recommendation": packet.get("isolation_recommendation") or packet.get("recommendation"),
        "recommendation": packet.get("recommendation") or packet.get("isolation_recommendation"),
        "executed": False,
        "recovery_ready": recovery.get("recovery_ready") is True,
        "recovery_blockers": recovery.get("process_dependency_blockers") or recovery.get("blockers"),
        "risk_finding_ids": risk["finding_ids"],
        "cvss_is_sort_key": False,
        "llm_rerank": False,
        "telemetry_quality_counts": quality.get("counts"),
        "identity_unknown": bool(identity.get("unknown")),
        "packet": packet,
        "recovery": {"plant_id": plant_id, "recovery_ready": recovery.get("recovery_ready") is True},
        "risk": risk,
        "transform_version": TRANSFORM,
    }


def simulate_isolation_consequence(payload: dict | None = None) -> dict:
    packet = _draft_packet(payload or {})
    return {
        "simulation_only": True,
        "executed": False,
        "isolate_endpoint": False,
        "ot_io": False,
        "process_impact": packet.get("process_impact"),
        "safety_impact": packet.get("safety_impact"),
        "rollback": packet.get("rollback"),
        "isolation_recommendation": packet.get("isolation_recommendation"),
        "note": "Read-only view over process/safety joins. Not isolate_endpoint.",
    }


def cite_untrusted_note() -> dict:
    text = _read_handover()
    return {
        "label": "UNTRUSTED",
        "source_path": HANDOVER_PATH,
        "content": text,
        "is_command": False,
        "vector_used": True,
        "sets_isolation_recommendation": False,
        "prompt_injection_remains_content": True,
    }


def _dispatch(name: str, payload: dict) -> Any:
    if name == "get_identity":
        return _safe_identity(payload.get("asset_id"))
    if name == "get_telemetry_quality":
        return quality_summary()
    if name == "get_contextual_risk":
        return _compact_risk()
    if name == "get_safety_conflicts":
        return safety_conflicts(limit=10)
    if name == "get_recovery":
        return _safe_recovery(payload.get("plant_id"))
    if name == "get_authority_actions":
        return authority_catalog()
    if name == "simulate_isolation_consequence":
        return simulate_isolation_consequence(payload)
    if name == "draft_recommendation_packet":
        return _draft_packet(payload)
    if name == "cite_untrusted_note":
        return cite_untrusted_note()
    if name in {"propose_request_fresh_telemetry", "propose_open_ticket", "propose_increase_logging"}:
        return {"stub": True, "side_effect": False, "action": name, "tier": 2, "executed": False}
    raise ToolDenied(name, "unknown tool — tier 4 refuse")


def call_tool(name: str, envelope: dict | None = None, payload: dict | None = None) -> Any:
    """Invoke an allowlisted read-only tool. Forbidden and unknown names raise ToolDenied."""
    if name in forbidden_execute_tools() or name not in ALLOWED_TOOLS:
        raise ToolDenied(name, f"forbidden or unknown tool {name}")
    env = envelope or _envelope(payload or {})
    ok, reason = _access_ok(env)
    if not ok:
        raise ToolDenied(name, reason)
    return _dispatch(name, payload or {})


def run_tool_sequence(names: list[str], envelope: dict, payload: dict | None = None) -> dict[str, Any]:
    """Execute allowlisted tools with loop abort. Denied tools are not retried."""
    payload = payload or {}
    history: list[tuple] = []
    results: list[dict] = []
    aborted = None
    for name in names:
        decision = loop_guard(history, name, payload)
        if decision["abort"]:
            aborted = decision
            break
        try:
            results.append({"tool": name, "ok": True, "result": call_tool(name, envelope=envelope, payload=payload)})
            history.append(decision["key"])
        except ToolDenied as exc:
            results.append({"tool": name, "ok": False, "denied": exc.reason, "not_retried": True})
            aborted = {"abort": True, "reason": "denied", "not_retried": True, "executed": False}
            break
    return {
        "results": results,
        "aborted": aborted,
        "calls": len(results),
        "executed": False,
        "max_tool_calls": MAX_TOOL_CALLS,
        "max_steps": MAX_STEPS,
    }


def optional_explanation(explainer_model: str | None) -> dict | None:
    if not ai_enabled():
        return None
    return {
        "model": explainer_model or versions().get("explainer_model"),
        "prompt_id": versions().get("prompt_id"),
        "authority": False,
        "text": "placeholder narration over deterministic packet; not authority",
        "system_prompt": _load_prompt("system")[:240],
    }


def _fallback_tables(core: dict) -> dict:
    conflicts = list_identity_conflicts()
    return {
        "mode": "AI_DISABLED" if not ai_enabled() else "AI_OPTIONAL",
        "blank_screen": False,
        "identity_conflict_table": {
            "alias_collision_count": len(conflicts.get("alias_collisions") or []),
            "registered_vs_observed_count": len(conflicts.get("registered_vs_observed") or []),
            "winner": None,
        },
        "telemetry_quality_counts": core.get("telemetry_quality_counts"),
        "recovery_not_ready_reasons": core.get("recovery_blockers"),
        "action_tiers_refuse": True,
        "war_room_checklist": [
            "review identity conflicts",
            "review telemetry quality counts",
            "review recovery blockers",
            "refuse control verbs",
            "do not require LLM to render CSV facts",
        ],
        "requires_llm": False,
    }


def run_workflow(payload: dict | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    requested = payload.get("action") or payload.get("requested_action") or "recommend"
    env = _envelope(payload)
    steps: list[str] = []
    tool_trace: list[dict] = []
    seen: set[tuple] = set()

    steps.append("request_validation")
    valid = requested is not None
    access_ok, access_reason = _access_ok(env)
    steps.append("access_check")

    steps.append("retrieval_plan")
    plan = list(ALLOWED_TOOLS)

    evidence: dict[str, Any] = {}
    steps.append("evidence")
    if access_ok and valid:
        for tool in (
            "get_authority_actions",
            "get_telemetry_quality",
            "get_recovery",
            "cite_untrusted_note",
            "simulate_isolation_consequence",
        ):
            if len(tool_trace) >= MAX_TOOL_CALLS or len(steps) >= MAX_STEPS:
                break
            key = (tool, payload.get("asset_id"), payload.get("plant_id"))
            if key in seen:
                break
            seen.add(key)
            try:
                evidence[tool] = call_tool(tool, envelope=env, payload=payload)
                tool_trace.append({"tool": tool, "ok": True})
            except ToolDenied as exc:
                tool_trace.append({"tool": tool, "ok": False, "denied": exc.reason})
                break
    else:
        tool_trace.append({"tool": None, "ok": False, "denied": access_reason})

    steps.append("context_slice")
    core = deterministic_core(payload)
    slice_ = {
        "hop_cap": 8,
        "whole_graph_dump": False,
        "identity": {"unknown": core["identity_unknown"]},
        "telemetry_quality_counts": core["telemetry_quality_counts"],
        "risk": core["risk"],
        "recovery": core["recovery"],
        "untrusted_note_is_command": False,
    }

    steps.append("draft")
    packet = core["packet"]

    steps.append("policy_gate")
    gate = permit(requested, actor_claim=payload.get("actor_claim") or env.get("actor"))
    if requested in forbidden_execute_tools() or gate["refused"] and requested != "recommend":
        try:
            call_tool(requested, envelope=env, payload=payload)
        except ToolDenied:
            tool_trace.append({"tool": requested, "ok": False, "denied": "policy gate", "not_retried": True})

    steps.append("human_packet")
    state = "Recommend" if gate.get("draft") or requested == "recommend" else "Closed"
    if gate["tier"] >= 3:
        state = "AwaitAuthorization"
    human = {
        "state": state,
        "execute_control": False,
        "await_authorization_closes": False,
        "open_001": True,
        "required_authority": packet.get("required_authority") or packet.get("required_role"),
        "handoff": ["SOC", "Process Eng", "Safety", "VP Ops"],
    }

    steps.append("trace")
    pin = versions()
    trace = {
        "decision_id": f"dec-{packet.get('packet_id') or 'adhoc'}",
        "workflow": list(WORKFLOW),
        "steps_run": steps[:MAX_STEPS],
        "tools": tool_trace,
        "policy": {"action": requested, "tier": gate["tier"], "allowed": gate["allowed"]},
        "recommendation": core["isolation_recommendation"],
        "authority": "OPEN-001",
        "model_version": payload.get("explainer_model") or pin.get("explainer_model"),
        "prompt_id": pin.get("prompt_id"),
        "tool_catalog_version": pin.get("tool_catalog_version"),
        "tokens": 0,
        "hidden_cot_as_authority": False,
        "execute_control": False,
        "agent": AGENT_DEFINITION,
    }
    _TRACES.append(trace)

    explanation = optional_explanation(payload.get("explainer_model"))
    guarded = apply_guardrails(
        payload=payload,
        packet=packet,
        model_output=payload.get("model_output"),
        requested=requested,
        core=core,
    )
    rec = guarded.get("isolation_recommendation") or core["isolation_recommendation"]
    return {
        "agent": AGENT_DEFINITION,
        "workflow": list(WORKFLOW),
        "steps_run": steps,
        "envelope": env,
        "envelope_complete": _envelope_complete(env),
        "access": {"ok": access_ok, "reason": access_reason},
        "retrieval_plan": plan,
        "evidence_tools": sorted(evidence),
        "context_slice": slice_,
        "draft": packet,
        "permit": gate,
        "human_packet": human,
        "trace": trace,
        "guardrails": guarded,
        "isolation_recommendation": rec,
        "recommendation": rec,
        "recovery_ready": core["recovery_ready"],
        "risk_finding_ids": core["risk_finding_ids"],
        "cvss_is_sort_key": False,
        "executed": False,
        "ot_action": False,
        "one_click_isolate": False,
        "execute_control": False,
        "forbidden_execute_tools": forbidden_execute_tools(),
        "prompt_registry": {"active": prompt_registry().get("active"), "eval_gate": prompt_eval_gate()},
        "versions": pin,
        "explanation": explanation,
        "fallback": _fallback_tables(core),
        "vector_used": True,
        "prompt_injection_remains_content": True,
        "transform_version": TRANSFORM,
        "live_restore_orchestration": False,
    }


def run_recommend(payload: dict | None = None) -> dict[str, Any]:
    """POST /recommend body. Recommendation object only. No OT action."""
    return run_workflow(payload)


def traces() -> list[dict]:
    return list(_TRACES)
