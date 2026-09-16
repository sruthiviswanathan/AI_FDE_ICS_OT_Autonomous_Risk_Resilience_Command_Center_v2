"""Authority gate (ADR-14, FR-012). Autonomy is ACTION_TIERS. No ExecuteControl.

Unknown action is tier 4 refuse. Self-asserted role is not Authorize (OPEN-001).
"""

from __future__ import annotations

from typing import Any

from .policy import ACTION_TIERS, requires_human_approval

POLICY_VERSION = "policy.py:ACTION_TIERS"
TRANSFORM = "enh-07-authority.1"

FORBIDDEN_EXECUTE = (
    "write_plc_logic",
    "change_setpoint",
    "modify_sis",
    "bypass_interlock",
    "isolate_endpoint",
    "isolate_endpoint_execute",
    "change_firewall",
    "change_remote_access",
    "suppress_trip",
)

TIER0 = {"observe", "correlate", "summarize"}


def forbidden_execute_tools() -> list[str]:
    return list(FORBIDDEN_EXECUTE)


def _tier(action: str) -> int:
    return int(ACTION_TIERS.get(action, 4))


def permit(action: str, actor_claim: str | None = None) -> dict[str, Any]:
    """Deny-by-default permit. Never sets executed. Actor claim cannot raise a tier."""
    name = str(action or "")
    tier = _tier(name)
    known = name in ACTION_TIERS
    execute_forbidden = name in FORBIDDEN_EXECUTE or tier >= 3 or not known
    autonomous = known and tier == 0
    draft = known and tier in {1, 2}
    allowed = autonomous or (known and tier == 1)
    refused = not allowed
    return {
        "action": name,
        "allowed": allowed,
        "refused": refused,
        "executed": False,
        "tier": tier,
        "draft": draft,
        "autonomous": autonomous,
        "known_verb": known,
        "requires_human_approval": requires_human_approval(name) if known else True,
        "authorizable": False,
        "actor_claim": actor_claim,
        "actor_claim_is_authorizer": False,
        "open_001": True,
        "would_write_if_connected": False,
        "mapped_from_soc_status": False,
        "execute_control": False,
        "execute_forbidden": execute_forbidden,
        "tool_calls": [],
        "bounded_autonomy": True,
        "approval": "AwaitAuthorization cannot close without a named human (OPEN-001); still no execute",
        "audit": True,
        "policy_version": POLICY_VERSION,
        "transform_version": TRANSFORM,
        "stub_not_implemented": known and tier == 2,
    }


def authority_catalog() -> dict[str, Any]:
    actions = []
    for name, tier in ACTION_TIERS.items():
        decision = permit(name)
        actions.append(
            {
                "action": name,
                "tier": tier,
                "autonomous": decision["autonomous"],
                "draft_only": decision["draft"],
                "allowed_execute": False,
                "execute_forbidden": decision["execute_forbidden"],
                "stub_not_implemented": decision["stub_not_implemented"],
            }
        )
    actions.append(
        {
            "action": "unknown",
            "tier": 4,
            "autonomous": False,
            "draft_only": False,
            "allowed_execute": False,
            "execute_forbidden": True,
            "note": "ACTION_TIERS.get(action, 4)",
        }
    )
    return {
        "policy_version": POLICY_VERSION,
        "execute_control": False,
        "one_click_isolate": False,
        "open_001_named_authorizer": True,
        "bounded_autonomy": True,
        "approval": True,
        "audit": True,
        "actions": actions,
        "forbidden_execute_tools": forbidden_execute_tools(),
        "must_not": ["SIS change", "setpoint write", "write_plc_logic", "bypass_interlock", "modify_sis"],
    }
