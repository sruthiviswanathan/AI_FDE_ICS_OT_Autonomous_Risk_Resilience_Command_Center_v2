"""Decision trace append-only persistence (FR-008). Workshop local file."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[3]
TRACE_PATH = ROOT / "data" / "local" / "decision_traces.jsonl"
SCHEMA_REF = "contracts/decision_trace.yaml"
TRANSFORM_VERSION = "enh-10-traces.1"


def read_traces(*, limit: int | None = None) -> list[dict]:
    if not TRACE_PATH.exists():
        return []
    rows: list[dict] = []
    with open(TRACE_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    if limit is not None:
        return rows[-limit:]
    return rows


def append_trace(record: dict) -> str:
    decision_id = record.get("decision_id") or str(uuid4())
    row = dict(record)
    row["decision_id"] = decision_id
    row.setdefault("schema", SCHEMA_REF)
    row.setdefault("transform_version", TRANSFORM_VERSION)
    row.setdefault("persisted_at", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    row.setdefault("execute", False)
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACE_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return decision_id
