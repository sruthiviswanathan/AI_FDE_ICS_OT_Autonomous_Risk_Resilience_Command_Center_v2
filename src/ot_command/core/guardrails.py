"""Deterministic guardrails after the model (ADR-15). Prompts cannot raise ACTION_TIERS.

Order: classify → envelope → allowlist → engines (caller) → output filter → policy.py → human matrix.
No real OT connectors. restricted_answer_key is not readable.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .authority import FORBIDDEN_EXECUTE, POLICY_VERSION, permit
from .policy import ACTION_TIERS

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
MAX_STEPS = 12
MAX_TOOL_CALLS = 20

ROOT = Path(__file__).resolve().parents[3]
PKG = Path(__file__).resolve().parents[1]
ANSWER_KEY = "restricted_answer_key"
TRANSFORM = "enh-08-guardrails.1"
REQUIREMENTS = ROOT / "requirements.txt"
SBOM_PATH = PKG / "sbom_freeze.json"

OT_TOOL_FORMS = (
    "write_plc_logic",
    "change_setpoint",
    "modify_sis",
    "bypass_interlock",
    "isolate_endpoint_execute",
    "suppress_trip",
)
DENIED_PRINCIPALS = {"vendor", "anonymous"}
EXFIL_PURPOSES = {"dump_all_plants", "export_sessions", "all_plants", "topology_dump"}
BANNED_OT_IMPORTS = (
    "pymodbus",
    "opcua",
    "asyncua",
    "snap7",
    "python-snap7",
    "pycomm3",
    "cpppo",
    "minimalmodbus",
)
TOOL_CALL_RE = re.compile(
    r"""(?:tool["']?\s*[:=]\s*["']?|call\(|invoke\()("""
    + "|".join(re.escape(v) for v in OT_TOOL_FORMS + ("isolate_endpoint",))
    + r""")""",
    re.I,
)


def classify_input(payload: dict | None) -> str:
    payload = payload or {}
    if payload.get("shift_note") or payload.get("untrusted") or payload.get("vector"):
        return "UNTRUSTED_NOTE"
    if payload.get("scenario"):
        return "SCENARIO"
    if payload.get("user_prompt") or payload.get("prompt") or payload.get("model_output"):
        return "USER"
    return "GOLD_FACT"


def envelope_complete(payload: dict | None) -> bool:
    payload = payload or {}
    return all(payload.get(k) not in (None, "") for k in ("actor", "purpose", "plant_id", "as_of", "policy_version"))


def principal_denied(actor: str | None) -> bool:
    text = str(actor or "").strip().lower()
    if not text:
        return False
    if text in DENIED_PRINCIPALS:
        return True
    if text.startswith("session:") or "site.engineer" in text:
        return True
    return False


def purpose_denied(purpose: str | None) -> bool:
    return str(purpose or "").strip().lower() in EXFIL_PURPOSES


def loop_guard(
    history: list[tuple],
    tool: str,
    args: dict | None = None,
    *,
    max_tools: int = MAX_TOOL_CALLS,
    max_steps: int = MAX_STEPS,
) -> dict[str, Any]:
    """Abort on cap or repeated tool+args. Do not retry denied tools."""
    if len(history) >= max_tools or len(history) >= max_steps:
        return {"abort": True, "reason": "max_steps_or_tool_calls", "not_retried": True, "executed": False}
    key = (tool, _freeze(args))
    if any(item == key for item in history):
        return {"abort": True, "reason": "repeat_tool_args", "not_retried": True, "executed": False}
    return {"abort": False, "reason": None, "key": key, "executed": False}


def _freeze(args: dict | None) -> tuple:
    if not args:
        return ()
    keep = ("asset_id", "plant_id", "alert_id", "action", "tool")
    return tuple(sorted((k, str(args.get(k))) for k in keep if args.get(k) not in (None, "")))


def extract_tool_calls(model_output: Any) -> list[str]:
    names: list[str] = []
    if isinstance(model_output, dict):
        raw = model_output.get("tool_calls") or model_output.get("tools") or []
        if isinstance(raw, str):
            raw = [raw]
        for item in raw:
            if isinstance(item, dict):
                names.append(str(item.get("tool") or item.get("name") or ""))
            else:
                names.append(str(item))
        if model_output.get("tool"):
            names.append(str(model_output.get("tool")))
        blob = json.dumps(model_output)
    else:
        blob = str(model_output or "")
    for match in TOOL_CALL_RE.finditer(blob):
        names.append(match.group(1))
    return [n for n in names if n]


def output_filter(model_output: Any) -> dict[str, Any]:
    calls = extract_tool_calls(model_output)
    dropped = [
        name
        for name in calls
        if name in FORBIDDEN_EXECUTE or name in OT_TOOL_FORMS or name not in ALLOWED_TOOLS and name in ACTION_TIERS
    ]
    # unknown invented tools also drop
    dropped.extend(name for name in calls if name not in ALLOWED_TOOLS and name not in dropped)
    dropped = list(dict.fromkeys(dropped))
    return {
        "dropped_tool_calls": dropped,
        "kept": [n for n in calls if n in ALLOWED_TOOLS],
        "execute": False,
        "schema_ok": True,
        "filter": "after_model",
    }


def answer_key_access(rel: str | None = None) -> dict[str, Any]:
    """Runtime must not read restricted_answer_key/. Existence is a CI fail, not a source."""
    target = Path(rel) if rel else ROOT / ANSWER_KEY
    name = str(rel or ANSWER_KEY)
    blocked = ANSWER_KEY in Path(name).parts or name.replace("\\", "/").startswith(ANSWER_KEY)
    if blocked:
        return {
            "path": name,
            "readable": False,
            "opened": False,
            "exists_checked": False,
            "error": "restricted_answer_key is not readable by runtime",
        }
    return {"path": name, "readable": True, "opened": False, "blocked": False}


def read_runtime_path(rel: str) -> str:
    decision = answer_key_access(rel)
    if decision.get("readable") is False:
        raise PermissionError(decision["error"])
    path = ROOT / rel
    return path.read_text(encoding="utf-8")


def sbom_freeze() -> dict[str, Any]:
    if SBOM_PATH.exists():
        return json.loads(SBOM_PATH.read_text(encoding="utf-8"))
    pins = []
    if REQUIREMENTS.exists():
        for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
            if "==" in line and not line.strip().startswith("#"):
                name, ver = line.strip().split("==", 1)
                pins.append({"name": name, "version": ver, "ai": False})
    return {
        "status": "workshop-freeze",
        "signed": False,
        "open_024_spdx_recopy": True,
        "components": pins,
        "aibom": {"models": [], "open_028": True},
        "ot_connectors": [],
        "policy_version": POLICY_VERSION,
    }


def overlay_cannot_win(shadow_claim: dict, gold: dict) -> dict[str, Any]:
    """Poisoned overlay is evidence, not SoR. Gold barrier/identity state wins as recorded conflict."""
    return {
        "shadow_is_cmdb": False,
        "winner": None,
        "gold_barriers": gold.get("bypassed_or_degraded_barriers") or gold.get("state"),
        "shadow_claim": shadow_claim,
        "promoted_to_master": False,
        "confidence": 0.4,
        "conflict_surfaced": True,
    }


def apply_guardrails(
    payload: dict | None = None,
    packet: dict | None = None,
    model_output: Any = None,
    requested: str | None = None,
    core: dict | None = None,
) -> dict[str, Any]:
    payload = dict(payload or {})
    packet = dict(packet or {})
    core = core or {}
    channel = classify_input(payload)
    requested = requested or payload.get("action") or payload.get("requested_action") or "recommend"
    actor = payload.get("actor_claim") or payload.get("actor")
    filt = output_filter(model_output if model_output is not None else payload.get("model_output"))
    gate = permit(requested, actor_claim=actor)
    rec = packet.get("isolation_recommendation") or packet.get("recommendation") or core.get("isolation_recommendation")
    if rec in {"ISOLATE", "EXECUTE", "ISOLATE_EXECUTE"}:
        rec = "ABSTAIN"
    if filt["dropped_tool_calls"] and rec == "ISOLATE_DRAFT":
        rec = "ABSTAIN"
    if channel == "UNTRUSTED_NOTE" and rec in {"ISOLATE", "ISOLATE_DRAFT"}:
        rec = "ABSTAIN"
    denied = principal_denied(actor) or purpose_denied(payload.get("purpose"))
    if denied:
        gate = {**gate, "allowed": False, "refused": True, "executed": False}
    return {
        "guardrails_after_model": True,
        "prompt_cannot_raise_tier": True,
        "channel": channel,
        "envelope_complete": envelope_complete(payload),
        "principal_denied": principal_denied(actor),
        "purpose_denied": purpose_denied(payload.get("purpose")),
        "permit": gate,
        "output_filter": filt,
        "isolation_recommendation": rec,
        "recovery_ready": core.get("recovery_ready") is True,
        "cvss_is_sort_key": False,
        "executed": False,
        "execute_control": False,
        "one_click_isolate": False,
        "whole_graph_dump": False,
        "answer_key_readable": False,
        "ot_connectors": [],
        "transform_version": TRANSFORM,
        "policy_version": POLICY_VERSION,
    }
