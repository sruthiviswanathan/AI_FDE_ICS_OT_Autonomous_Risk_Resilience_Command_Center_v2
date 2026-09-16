"""ACTION_TIERS catalog and autonomous permission (FR-012, ADR-14)."""

from ot_command.core.policy import ACTION_TIERS


def action_tier(action: str) -> int:
    return ACTION_TIERS.get(action, 4)


def is_autonomous_permitted(action: str) -> bool:
    return action_tier(action) == 0


def list_tier0_actions() -> list:
    return sorted(action for action, tier in ACTION_TIERS.items() if tier == 0)


def catalog() -> dict:
    return {
        "policy_version": "policy.py:ACTION_TIERS",
        "unknown_action_default_tier": 4,
        "actions": [
            {"action": name, "tier": tier, "autonomous": tier == 0}
            for name, tier in sorted(ACTION_TIERS.items(), key=lambda x: (x[1], x[0]))
        ],
        "refuse_tier4": sorted(
            name for name, tier in ACTION_TIERS.items() if tier >= 4
        ),
        "human_authorize_tier3": sorted(
            name for name, tier in ACTION_TIERS.items() if tier == 3
        ),
        "note": "Tier ≥3 is not license to execute in this API (OPEN-001)",
    }
