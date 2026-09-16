from pathlib import Path
import csv
import json
import os

ROOT = Path(__file__).resolve().parents[2]


def _root() -> Path:
    override = os.environ.get("OT_DATA_ROOT")
    return Path(override) if override else ROOT


def rows(rel: str) -> list[dict]:
    with open(_root() / rel, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def jsonl(rel: str) -> list[dict]:
    with open(_root() / rel, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]
