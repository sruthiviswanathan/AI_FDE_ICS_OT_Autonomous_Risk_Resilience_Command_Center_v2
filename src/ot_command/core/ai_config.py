"""AI feature flag — shared by API health and agent workflow (ADR-12)."""

from __future__ import annotations

import os


def ai_enabled() -> bool:
    return os.environ.get("AI_ENABLED", "0").strip() in {"1", "true", "TRUE", "yes"}
