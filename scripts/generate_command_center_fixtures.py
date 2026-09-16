"""Slice real synthetic CSVs into a demo fixture. No invented fields.

Reads DictReader / JSONL rows by known EVAL/inject IDs and first matching
estate filters. Writes apps/command_center/fixtures/command_center_fixtures.json.
Does not rewrite data/raw or data/shadow.
"""
from __future__ import annotations

import json
from pathlib import Path

from ot_command.repository import jsonl, rows

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "apps/command_center/fixtures/command_center_fixtures.json"
SHIFT = ROOT / "data/shadow/shift_handover_email.txt"


def _by(table: list[dict], key: str, value: str) -> list[dict]:
    return [dict(r) for r in table if r.get(key) == value]


def _first(table: list[dict], pred) -> dict | None:
    for r in table:
        if pred(r):
            return dict(r)
    return None


def build() -> dict:
    assets = rows("data/raw/assets.csv")
    aliases = rows("data/raw/asset_aliases.csv")
    edges = rows("data/raw/network_edges.csv")
    vulns = rows("data/raw/vulnerabilities.csv")
    barriers = rows("data/raw/safety_barriers.csv")
    sessions = rows("data/raw/remote_access_sessions.csv")
    recovery = rows("data/raw/recovery_readiness.csv")
    alerts = rows("data/raw/cyber_alerts.csv")
    units = rows("data/raw/process_units.csv")
    deps = rows("data/raw/process_dependencies.csv")
    shadow = rows("data/shadow/ot_asset_inventory_FINAL_v8.csv")
    tele = jsonl("data/telemetry/tag_telemetry.jsonl")
    events = jsonl("data/raw/enterprise_events.jsonl")

    alias_ids = ["OT-00012", "OT-00033"]
    identity_assets = [dict(r) for r in assets if r["asset_id"] in alias_ids or r["asset_id"] == "OT-00528"]
    identity_aliases = [dict(r) for r in aliases if r["asset_id"] in alias_ids or r.get("alias") == "PLT-01-DCS_CONTROLLER-105"]
    collide = [dict(r) for r in aliases if r.get("alias", "").startswith("COLLIDE-")][:10]
    shadow_hits = [dict(r) for r in shadow if r["asset_id"] in {a["asset_id"] for a in identity_assets}]
    shadow_sample = [dict(r) for r in shadow[:3]]

    undocumented = [
        dict(r)
        for r in edges
        if r.get("documented") == "NO" and r.get("observed_last_24h") == "YES"
    ][:8]

    bad_named = _first(tele, lambda r: r.get("event_id") == "TEL-00000288")
    bad_quality = [dict(r) for r in tele if r.get("quality") in {"BAD", "UNCERTAIN"}][:6]
    unit_mismatch = [dict(r) for r in tele if str(r.get("tag_id", "")).endswith("_TEMP") and r.get("unit") != "C"][:4]
    bad_telemetry = []
    seen = set()
    for r in ([bad_named] if bad_named else []) + bad_quality + unit_mismatch:
        eid = r.get("event_id")
        if eid in seen:
            continue
        seen.add(eid)
        bad_telemetry.append(r)

    evt1 = _first(events, lambda r: r.get("event_id") == "EVT-0000001")

    vuln_pair = [dict(r) for r in vulns if r["finding_id"] in {"VUL-00706", "VUL-00098"}]
    vuln_assets = [dict(r) for r in assets if r["asset_id"] in {"OT-00654", "OT-01016"}]
    unit_u06 = _by(units, "unit_id", "PLT-10-U06")
    unit_u07 = _by(units, "unit_id", "PLT-10-U07")
    dep_u06 = [
        dict(r)
        for r in deps
        if r.get("upstream_unit") in {"PLT-10-U06", "PLT-10-U07"}
        or r.get("downstream_unit") in {"PLT-10-U06", "PLT-10-U07"}
    ]
    barrier_cascade = _by(barriers, "barrier_id", "PLT-10-SAFE-07")
    barrier_aging = _by(barriers, "barrier_id", "PLT-03-SAFE-14")
    alert = _by(alerts, "alert_id", "ALT-002783")

    unapproved = [
        dict(r)
        for r in sessions
        if r.get("approved_window") != "YES"
    ][:6]
    no_mfa = [dict(r) for r in sessions if r.get("mfa") != "YES"][:4]
    sessions_out = []
    seen_s = set()
    for r in unapproved + no_mfa:
        sid = r.get("session_id")
        if sid in seen_s:
            continue
        seen_s.add(sid)
        sessions_out.append(r)

    stale = [
        dict(r)
        for r in recovery
        if r.get("plant_id") == "PLT-01" and r.get("component") == "IDENTITY"
    ]
    if not stale:
        stale = [dict(r) for r in recovery if r.get("backup_status") == "CURRENT" and r.get("runbook_status") == "STALE"][:3]

    shift_text = SHIFT.read_text(encoding="utf-8")

    return {
        "schema": "command_center_fixtures.v1",
        "mode": "synthetic-read-only",
        "live_ot": False,
        "invented_fields": False,
        "sources": [
            "data/raw/assets.csv",
            "data/raw/asset_aliases.csv",
            "data/raw/network_edges.csv",
            "data/raw/vulnerabilities.csv",
            "data/raw/safety_barriers.csv",
            "data/raw/remote_access_sessions.csv",
            "data/raw/recovery_readiness.csv",
            "data/raw/cyber_alerts.csv",
            "data/raw/process_units.csv",
            "data/raw/process_dependencies.csv",
            "data/raw/enterprise_events.jsonl",
            "data/telemetry/tag_telemetry.jsonl",
            "data/shadow/ot_asset_inventory_FINAL_v8.csv",
            "data/shadow/shift_handover_email.txt",
        ],
        "rule": "Every object is an exact source row or the exact shift-email file. No invented fields or IDs.",
        "identity_conflicts": {
            "eval": "EVAL-001",
            "inject": "inject_01",
            "aliases": identity_aliases,
            "collide_alias_sample": collide,
            "assets": identity_assets,
            "shadow_overlay": shadow_hits,
            "shadow_overlay_sample": shadow_sample,
            "shadow_is_winner": False,
            "cmdb_is_winner": False,
        },
        "undocumented_paths": {
            "inject": "inject_05",
            "filter": "documented=NO AND observed_last_24h=YES",
            "rows": undocumented,
        },
        "bad_telemetry": {
            "eval": "EVAL-004",
            "inject": "inject_02",
            "rows": bad_telemetry,
            "enterprise_clock_inversion": evt1,
        },
        "anti_cvss_pair": {
            "eval": "EVAL-002",
            "vulnerabilities": vuln_pair,
            "assets": vuln_assets,
            "units": unit_u06 + unit_u07,
            "dependencies": dep_u06,
            "alert": alert,
            "cvss_is_sort_key": False,
        },
        "bypassed_barrier": {
            "eval": "EVAL-003",
            "inject": "inject_04",
            "rows": barrier_cascade + barrier_aging,
        },
        "unapproved_vendor_session": {
            "eval": "EVAL-010",
            "inject": "inject_03",
            "rows": sessions_out,
            "unknown_is_not_approval": True,
        },
        "stale_restore": {
            "eval": "EVAL-005",
            "inject": "inject_06",
            "rows": stale,
            "backup_current_is_not_recovery_ready": True,
        },
        "untrusted_shift_text": {
            "path": "data/shadow/shift_handover_email.txt",
            "trust": "UNTRUSTED",
            "is_command": False,
            "text": shift_text,
        },
        "forbidden_ui": {
            "execute_isolation": False,
            "write_plc": False,
            "ot_connectors": [],
        },
    }


def main() -> None:
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("WROTE", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
