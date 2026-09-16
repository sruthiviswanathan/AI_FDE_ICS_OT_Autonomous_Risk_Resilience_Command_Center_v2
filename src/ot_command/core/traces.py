"""Append-only decision traces (FR-008, NFR-AUD). Packet is the argument. No hidden CoT."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
TRACE_REL = "data/local/decision_traces.jsonl"
SCHEMA_REL = "contracts/decision_trace.yaml"
TRANSFORM = "enh-10-traces.1"


def trace_path() -> Path:
    return ROOT / TRACE_REL


def append_trace(record: dict[str, Any]) -> dict[str, Any]:
    """Write one JSONL line under data/local/. Never writes data/raw."""
    path = trace_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        **record,
        "persisted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "hidden_cot_as_authority": False,
        "execute_control": False,
        "executed": False,
        "schema": SCHEMA_REL,
        "transform_version": TRANSFORM,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, default=str) + "\n")
    return row


def recent_traces(limit: int = 20) -> list[dict[str, Any]]:
    path = trace_path()
    if not path.exists():
        return []
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    out = []
    for ln in lines[-max(int(limit), 1) :]:
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def trace_count() -> int:
    path = trace_path()
    if not path.exists():
        return 0
    return sum(1 for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip())
