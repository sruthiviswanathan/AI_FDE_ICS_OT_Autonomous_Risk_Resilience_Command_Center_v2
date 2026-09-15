"""SDD-03 forensic mining. Read-only. Does not clean data or call OT."""
from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]


def rows(rel: str) -> list[dict]:
    with (ROOT / rel).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def jsonl(rel: str) -> list[dict]:
    with (ROOT / rel).open(encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def parse(ts: str):
    return datetime.fromisoformat(ts) if ts else None


def main() -> None:
    out_dir = Path(__file__).resolve().parents[1]
    findings: dict = {}

    assets = rows("data/raw/assets.csv")
    aliases = rows("data/raw/asset_aliases.csv")
    edges = rows("data/raw/network_edges.csv")
    tags = rows("data/reference/tags.csv")
    units = rows("data/raw/process_units.csv")
    deps = rows("data/raw/process_dependencies.csv")
    vulns = rows("data/raw/vulnerabilities.csv")
    safety = rows("data/raw/safety_barriers.csv")
    work = rows("data/raw/work_orders.csv")
    access = rows("data/raw/remote_access_sessions.csv")
    rec = rows("data/raw/recovery_readiness.csv")
    alerts = rows("data/raw/cyber_alerts.csv")
    plants = rows("data/reference/plants.csv")
    vendors = rows("data/reference/vendors.csv")
    shadow = rows("data/shadow/ot_asset_inventory_FINAL_v8.csv")
    tracker = rows("data/shadow/risk_acceptance_tracker.csv")
    tele = jsonl("data/telemetry/tag_telemetry.jsonl")
    events = jsonl("data/raw/enterprise_events.jsonl")

    a_by = {a["asset_id"]: a for a in assets}
    u_by = {u["unit_id"]: u for u in units}
    tags_by_asset: dict[str, list] = defaultdict(list)
    for t in tags:
        tags_by_asset[t["asset_id"]].append(t)

    # --- L4 identity ---
    alias_by = Counter(x["alias"] for x in aliases)
    collisions = [k for k, v in alias_by.items() if v > 1]
    collision_rows = [x for x in aliases if x["alias"] in set(collisions)]
    src_per_asset = Counter()
    for x in aliases:
        src_per_asset[x["asset_id"]] += 1
    state_conf = [
        a
        for a in assets
        if a["registered_state"] == "ACTIVE" and a["observed_state"] in {"OFFLINE", "UNSEEN"}
    ]
    findings["identity"] = {
        "n_assets": len(assets),
        "n_aliases": len(aliases),
        "alias_sources": dict(Counter(x["source"] for x in aliases)),
        "collisions": collisions,
        "collision_rows": collision_rows[:20],
        "owner": dict(Counter(a["owner"] for a in assets)),
        "registered": dict(Counter(a["registered_state"] for a in assets)),
        "observed": dict(Counter(a["observed_state"] for a in assets)),
        "state_conflicts_n": len(state_conf),
        "state_conflict_ids": [a["asset_id"] for a in state_conf[:8]],
        "firmware_unique": len({a["firmware"] for a in assets}),
        "shadow_n": len(shadow),
        "shadow_not_in_assets": sorted({s["asset_id"] for s in shadow} - set(a_by)),
        "backup_age_days_p50": statistics.median(int(a["backup_age_days"]) for a in assets),
        "backup_age_gt_90": sum(int(a["backup_age_days"]) > 90 for a in assets),
    }
    sh_fw = 0
    sh_obs = 0
    for s in shadow:
        a = a_by[s["asset_id"]]
        if a["firmware"] != s["firmware"]:
            sh_fw += 1
        if a["observed_state"] != s["observed_state"]:
            sh_obs += 1
    findings["identity"]["shadow_firmware_diff"] = sh_fw
    findings["identity"]["shadow_observed_diff"] = sh_obs

    # --- L2 topology ---
    findings["topology"] = {
        "asset_type": dict(Counter(a["asset_type"] for a in assets)),
        "zone": dict(Counter(a["zone"] for a in assets)),
        "protocol": dict(Counter(a["protocol"] for a in assets)),
        "edges_n": len(edges),
        "undocumented_observed": sum(
            e["documented"] == "NO" and e["observed_last_24h"] == "YES" for e in edges
        ),
        "approved_unknown": sum(e["approved_path"] == "UNKNOWN" for e in edges),
        "approved_no_observed_yes": sum(
            e["approved_path"] == "NO" and e["observed_last_24h"] == "YES" for e in edges
        ),
        "edge_protocol": dict(Counter(e["protocol"] for e in edges)),
        "self_loops": sum(e["source_asset"] == e["target_asset"] for e in edges),
        "assets_as_src_or_tgt": len(
            {e["source_asset"] for e in edges} | {e["target_asset"] for e in edges}
        ),
    }
    edge_nodes = {e["source_asset"] for e in edges} | {e["target_asset"] for e in edges}
    findings["topology"]["assets_not_on_any_edge"] = len(set(a_by) - edge_nodes)

    # --- L3 telemetry ---
    quality = Counter(x["quality"] for x in tele)
    sources = Counter(x.get("source") for x in tele)
    units_c = Counter(x["unit"] for x in tele)
    keys = Counter((x["tag_id"], x["event_time"], str(x["value"]), x["unit"]) for x in tele)
    dup_extra = sum(v - 1 for v in keys.values() if v > 1)
    temp_bad = [x for x in tele if x["tag_id"].endswith("_TEMP") and x["unit"] != "C"]
    lags = []
    neg = 0
    missing_ingest = 0
    order_invert_tags = 0
    by_tag: dict[str, list] = defaultdict(list)
    for x in tele:
        et, it = parse(x["event_time"]), parse(x.get("ingest_time") or "")
        if et is None or it is None:
            missing_ingest += 1
            continue
        d = (it - et).total_seconds()
        lags.append(d)
        if d < 0:
            neg += 1
        by_tag[x["tag_id"]].append(x)
    # event_time order vs ingest_time order disagreements per tag (sample)
    invert_examples = []
    for tag, xs in by_tag.items():
        ev_order = [x["event_id"] for x in sorted(xs, key=lambda z: z["event_time"])]
        in_order = [x["event_id"] for x in sorted(xs, key=lambda z: z.get("ingest_time") or z["event_time"])]
        if ev_order != in_order:
            order_invert_tags += 1
            if len(invert_examples) < 3:
                invert_examples.append({"tag_id": tag, "n": len(xs)})
    tag_ids_tele = {x["tag_id"] for x in tele}
    tag_ids_ref = {t["tag_id"] for t in tags}
    findings["telemetry"] = {
        "n": len(tele),
        "quality": dict(quality),
        "source": dict(sources),
        "unit": dict(units_c),
        "dup_extra": dup_extra,
        "dup_groups": sum(1 for v in keys.values() if v > 1),
        "temp_unit_mismatch": len(temp_bad),
        "temp_unit_mismatch_units": dict(Counter(x["unit"] for x in temp_bad)),
        "temp_examples": [
            {"event_id": x["event_id"], "tag_id": x["tag_id"], "unit": x["unit"]} for x in temp_bad[:5]
        ],
        "lag_n": len(lags),
        "lag_neg": neg,
        "lag_min": min(lags) if lags else None,
        "lag_p50": statistics.median(lags) if lags else None,
        "lag_p90": sorted(lags)[int(0.9 * len(lags))] if lags else None,
        "lag_max": max(lags) if lags else None,
        "lag_gt_60": sum(d > 60 for d in lags),
        "lag_gt_300": sum(d > 300 for d in lags),
        "missing_ingest": missing_ingest,
        "order_invert_tags": order_invert_tags,
        "invert_examples": invert_examples,
        "tags_in_tele_not_ref": len(tag_ids_tele - tag_ids_ref),
        "tags_in_ref_not_tele": len(tag_ids_ref - tag_ids_tele),
        "asset_id_in_tele": sum(1 for x in tele if "asset_id" in x),
        "schema_required_missing_from_schema": ["ingest_time", "source", "asset_id"],
        "historian_enabled_no": sum(t["historian_enabled"] != "YES" for t in tags),
    }

    # --- L5 process ---
    findings["process"] = {
        "units_n": len(units),
        "unit_type": dict(Counter(u["unit_type"] for u in units)),
        "production_criticality": dict(Counter(u["production_criticality"] for u in units)),
        "safe_state": dict(Counter(u["safe_state"] for u in units)),
        "manual_mode": dict(Counter(u["manual_mode_supported"] for u in units)),
        "deps_n": len(deps),
        "dep_type": dict(Counter(d["dependency_type"] for d in deps)),
        "dep_documented_no": sum(d["documented"] == "NO" for d in deps),
        "dep_critical_yes": sum(d["critical"] == "YES" for d in deps),
        "dep_critical_undocumented": sum(d["critical"] == "YES" and d["documented"] == "NO" for d in deps),
        "assets_with_tag": sum(1 for a in assets if a["asset_id"] in tags_by_asset),
        "assets_without_tag": sum(1 for a in assets if a["asset_id"] not in tags_by_asset),
        "min_load_units": [u["unit_id"] for u in units if u["safe_state"] == "MIN_LOAD"][:12],
    }

    # --- L6 cyber ---
    findings["cyber"] = {
        "vuln_n": len(vulns),
        "severity": dict(Counter(v["severity"] for v in vulns)),
        "status": dict(Counter(v["status"] for v in vulns)),
        "reachable": dict(Counter(v["network_reachable"] for v in vulns)),
        "control": dict(Counter(v["compensating_control"] for v in vulns)),
        "exploitability": dict(Counter(v["exploitability"] for v in vulns)),
        "cvss_ge_9": sum(float(v["cvss"]) >= 9 for v in vulns),
        "cvss_ge_9_reachable_no": sum(float(v["cvss"]) >= 9 and v["network_reachable"] == "NO" for v in vulns),
        "cvss_ge_9_reachable_unknown": sum(
            float(v["cvss"]) >= 9 and v["network_reachable"] == "UNKNOWN" for v in vulns
        ),
        "open_high_crit": sum(v["status"] == "OPEN" and v["severity"] in {"HIGH", "CRITICAL"} for v in vulns),
        "alerts_n": len(alerts),
        "alert_type": dict(Counter(a["type"] for a in alerts)),
        "alert_sev": dict(Counter(a["severity"] for a in alerts)),
        "soc_status": dict(Counter(a["soc_status"] for a in alerts)),
        "process_context": dict(Counter(a["process_context"] for a in alerts)),
        "high_crit": sum(a["severity"] in {"HIGH", "CRITICAL"} for a in alerts),
        "high_crit_unknown_ctx": sum(
            a["severity"] in {"HIGH", "CRITICAL"} and a["process_context"] == "UNKNOWN" for a in alerts
        ),
        "access_n": len(access),
        "method": dict(Counter(x["method"] for x in access)),
        "identity": dict(Counter(x["identity"] for x in access)),
        "approved": dict(Counter(x["approved_window"] for x in access)),
        "mfa": dict(Counter(x["mfa"] for x in access)),
    }

    # anti-CVSS candidates: high cvss unreachable LOW asset vs lower cvss reachable CRITICAL asset
    anti = []
    for v in vulns:
        a = a_by.get(v["asset_id"])
        if not a:
            continue
        tlist = tags_by_asset.get(v["asset_id"], [])
        unit_ids = list({t["unit_id"] for t in tlist})
        unit_meta = [u_by[u] for u in unit_ids if u in u_by]
        anti.append(
            {
                "finding_id": v["finding_id"],
                "asset_id": v["asset_id"],
                "cvss": float(v["cvss"]),
                "severity": v["severity"],
                "reachable": v["network_reachable"],
                "control": v["compensating_control"],
                "status": v["status"],
                "asset_crit": a["criticality"],
                "asset_type": a["asset_type"],
                "observed": a["observed_state"],
                "plant_id": a["plant_id"],
                "units": unit_ids,
                "unit_prod": [u["production_criticality"] for u in unit_meta],
                "safe_state": [u["safe_state"] for u in unit_meta],
            }
        )
    high_low = [
        x
        for x in anti
        if x["cvss"] >= 9.0 and x["reachable"] == "NO" and x["asset_crit"] == "LOW"
    ]
    mid_crit = [
        x
        for x in anti
        if x["cvss"] <= 7.0
        and x["reachable"] == "YES"
        and x["asset_crit"] == "CRITICAL"
        and x["status"] == "OPEN"
    ]
    findings["anti_cvss"] = {
        "high_cvss_unreachable_low_asset_n": len(high_low),
        "high_cvss_unreachable_low_examples": high_low[:5],
        "lower_cvss_reachable_critical_open_n": len(mid_crit),
        "lower_cvss_reachable_critical_examples": mid_crit[:5],
    }

    # --- L7 safety ---
    findings["safety"] = {
        "n": len(safety),
        "state": dict(Counter(s["state"] for s in safety)),
        "proof": dict(Counter(s["proof_test_status"] for s in safety)),
        "bypass_auth": dict(Counter(s["bypass_authorized"] for s in safety)),
        "barrier_type": dict(Counter(s["barrier_type"] for s in safety)),
        "bypassed_unauth": [
            s
            for s in safety
            if s["state"] == "BYPASSED" and s["bypass_authorized"] in {"NO", "UNKNOWN"}
        ][:8],
        "sis_not_active": [
            s for s in safety if s["barrier_type"] == "SIS_TRIP" and s["state"] != "ACTIVE"
        ],
        "units_with_nonactive_barrier": sorted(
            {s["unit_id"] for s in safety if s["state"] != "ACTIVE"}
        ),
    }

    # unsafe isolation: HIGH/CRIT alert, unit MIN_LOAD or barrier not ACTIVE
    min_load = {u["unit_id"] for u in units if u["safe_state"] == "MIN_LOAD"}
    unsafe_units = {s["unit_id"] for s in safety if s["state"] != "ACTIVE"} | min_load
    unsafe_alerts = []
    for al in alerts:
        if al["severity"] not in {"HIGH", "CRITICAL"}:
            continue
        tlist = tags_by_asset.get(al["asset_id"], [])
        unit_ids = {t["unit_id"] for t in tlist}
        hit = unit_ids & unsafe_units
        if not hit:
            continue
        a = a_by.get(al["asset_id"], {})
        unsafe_alerts.append(
            {
                "alert_id": al["alert_id"],
                "asset_id": al["asset_id"],
                "severity": al["severity"],
                "type": al["type"],
                "process_context": al["process_context"],
                "soc_status": al["soc_status"],
                "units": sorted(hit),
                "safe_state": [u_by[u]["safe_state"] for u in hit if u in u_by],
                "asset_type": a.get("asset_type"),
                "plant_id": al["plant_id"],
            }
        )
    findings["unsafe_isolation"] = {
        "n": len(unsafe_alerts),
        "examples": unsafe_alerts[:8],
        "min_load_and_highcrit_alert_n": sum(
            any(u in min_load for u in x["units"]) for x in unsafe_alerts
        ),
    }

    # --- L8 ops ---
    findings["ops"] = {
        "wo_n": len(work),
        "cmms": dict(Counter(w["cmms_status"] for w in work)),
        "field": dict(Counter(w["field_status"] for w in work)),
        "type": dict(Counter(w["type"] for w in work)),
        "bypass_yes": sum(w["temporary_bypass"] == "YES" for w in work),
        "notes": dict(Counter(w["notes"] for w in work)),
        "closed_not_rts": sum(
            w["cmms_status"] == "CLOSED" and w["field_status"] != "RETURNED_TO_SERVICE" for w in work
        ),
        "closed_no_closed_at": sum(w["cmms_status"] == "CLOSED" and not w["closed_at"] for w in work),
        "open_queue": sum(w["cmms_status"] in {"OPEN", "IN_PROGRESS", "DEFERRED"} for w in work),
    }

    # --- L9 enterprise ---
    corr_empty = sum(1 for e in events if not e.get("correlation_id"))
    lags_e = []
    neg_e = 0
    for e in events:
        d = (parse(e["received_time"]) - parse(e["event_time"])).total_seconds()
        lags_e.append(d)
        if d < 0:
            neg_e += 1
    findings["enterprise"] = {
        "events_n": len(events),
        "source": dict(Counter(e["source"] for e in events)),
        "event_type": dict(Counter(e["event_type"] for e in events)),
        "payload_state": dict(Counter(e["payload_state"] for e in events)),
        "corr_empty": corr_empty,
        "lag_neg": neg_e,
        "lag_p50": statistics.median(lags_e),
        "vendors": [
            {"id": v["vendor_id"], "name": v["name"], "remote": v["remote_access"], "sla": v["support_sla_hours"]}
            for v in vendors
        ],
        "plants_n": len(plants),
        "regions": dict(Counter(p["region"] for p in plants)),
        "tracker_n": len(tracker),
        "tracker_decision": dict(Counter(t["decision"] for t in tracker)),
        "tracker_owner": dict(Counter(t["risk_owner"] for t in tracker)),
        "tracker_expired_before_20260915": sum(t["expiry"] < "2026-09-15" for t in tracker),
        "tracker_accept_unknown": sum(
            t["decision"] == "ACCEPT" and t["risk_owner"] == "Unknown" for t in tracker
        ),
    }

    # --- L10 recovery ---
    current_lie = [
        r
        for r in rec
        if r["backup_status"] == "CURRENT"
        and (
            int(r["last_restore_test_days"]) > 90
            or r["runbook_status"] != "CURRENT"
            or r["dependency_verified"] != "YES"
        )
    ]
    findings["recovery"] = {
        "n": len(rec),
        "backup": dict(Counter(r["backup_status"] for r in rec)),
        "runbook": dict(Counter(r["runbook_status"] for r in rec)),
        "dep": dict(Counter(r["dependency_verified"] for r in rec)),
        "fallback": dict(Counter(r["manual_fallback"] for r in rec)),
        "component": dict(Counter(r["component"] for r in rec)),
        "restore_p50": statistics.median(int(r["last_restore_test_days"]) for r in rec),
        "restore_gt_180": sum(int(r["last_restore_test_days"]) > 180 for r in rec),
        "current_but_weak_n": len(current_lie),
        "current_but_weak_examples": current_lie[:8],
        "legacy_would_ready": sum(r["backup_status"] == "CURRENT" for r in rec),
    }

    # --- three traces: tagged CRITICAL/HIGH unit assets with deps + safety + vuln/alert ---
    dep_down = defaultdict(list)
    for d in deps:
        dep_down[d["upstream_unit"]].append(d)
    traces = []
    for a in assets:
        tlist = tags_by_asset.get(a["asset_id"], [])
        if not tlist:
            continue
        uid = tlist[0]["unit_id"]
        u = u_by.get(uid)
        if not u:
            continue
        bars = [s for s in safety if s["unit_id"] == uid]
        vs = [v for v in vulns if v["asset_id"] == a["asset_id"]]
        als = [al for al in alerts if al["asset_id"] == a["asset_id"]]
        downs = dep_down.get(uid, [])
        plant = next((p for p in plants if p["plant_id"] == a["plant_id"]), {})
        traces.append(
            {
                "asset_id": a["asset_id"],
                "asset_type": a["asset_type"],
                "criticality": a["criticality"],
                "registered_state": a["registered_state"],
                "observed_state": a["observed_state"],
                "firmware": a["firmware"],
                "zone": a["zone"],
                "protocol": a["protocol"],
                "plant_id": a["plant_id"],
                "plant_type": plant.get("plant_type"),
                "plant_crit": plant.get("criticality"),
                "unit_id": uid,
                "unit_type": u["unit_type"],
                "unit_prod": u["production_criticality"],
                "safe_state": u["safe_state"],
                "manual_mode": u["manual_mode_supported"],
                "downstream": downs,
                "barriers": [
                    {
                        "barrier_id": b["barrier_id"],
                        "type": b["barrier_type"],
                        "state": b["state"],
                        "proof": b["proof_test_status"],
                        "bypass_authorized": b["bypass_authorized"],
                    }
                    for b in bars
                ],
                "vulns": [
                    {
                        "finding_id": v["finding_id"],
                        "cvss": v["cvss"],
                        "reachable": v["network_reachable"],
                        "status": v["status"],
                    }
                    for v in vs[:6]
                ],
                "alerts_n": len(als),
                "alerts_highcrit": sum(al["severity"] in {"HIGH", "CRITICAL"} for al in als),
            }
        )

    def score_trace(t):
        return (
            int(t["criticality"] == "CRITICAL")
            + int(t["unit_prod"] in {"CRITICAL", "HIGH"})
            + int(any(b["state"] != "ACTIVE" for b in t["barriers"]))
            + int(t["safe_state"] == "MIN_LOAD")
            + int(bool(t["downstream"]))
            + int(t["registered_state"] != t["observed_state"] and t["observed_state"] in {"OFFLINE", "UNSEEN", "ONLINE"})
            + min(len(t["vulns"]), 2)
        )

    traces_sorted = sorted(traces, key=score_trace, reverse=True)
    # pick diverse: MIN_LOAD+barrier, identity conflict, high cvss unreachable
    pick = []
    used_plants = set()
    for t in traces_sorted:
        if t["plant_id"] in used_plants:
            continue
        if t["safe_state"] == "MIN_LOAD" and any(b["state"] != "ACTIVE" for b in t["barriers"]):
            pick.append(t)
            used_plants.add(t["plant_id"])
            if len(pick) == 1:
                break
    for t in traces_sorted:
        if t["asset_id"] in {p["asset_id"] for p in pick}:
            continue
        if t["registered_state"] == "ACTIVE" and t["observed_state"] in {"OFFLINE", "UNSEEN"} and t["downstream"]:
            pick.append(t)
            if len(pick) == 2:
                break
    for t in traces_sorted:
        if t["asset_id"] in {p["asset_id"] for p in pick}:
            continue
        if t["vulns"] and t["unit_prod"] in {"CRITICAL", "HIGH"}:
            pick.append(t)
            if len(pick) == 3:
                break
    while len(pick) < 3 and traces_sorted:
        t = traces_sorted[len(pick)]
        if t["asset_id"] not in {p["asset_id"] for p in pick}:
            pick.append(t)
    findings["traces"] = pick[:3]

    # firmware uniqueness / volatility
    fw_by_type = defaultdict(set)
    for a in assets:
        fw_by_type[a["asset_type"]].add(a["firmware"])
    findings["firmware_versions_by_type"] = {k: len(v) for k, v in fw_by_type.items()}

    dest = out_dir / "scripts" / "_findings.json"
    dest.write_text(json.dumps(findings, indent=2, default=str), encoding="utf-8")
    print("wrote", dest)
    print("collisions", collisions)
    print("traces", [t["asset_id"] for t in findings["traces"]])
    print("anti high_low", findings["anti_cvss"]["high_cvss_unreachable_low_asset_n"])
    print("anti mid_crit", findings["anti_cvss"]["lower_cvss_reachable_critical_open_n"])
    print("unsafe_iso", findings["unsafe_isolation"]["n"])
    print("current_lie", findings["recovery"]["current_but_weak_n"])
    print("tele lag_p50", findings["telemetry"]["lag_p50"], "neg", findings["telemetry"]["lag_neg"])
    print("order_invert_tags", findings["telemetry"]["order_invert_tags"])


if __name__ == "__main__":
    main()
