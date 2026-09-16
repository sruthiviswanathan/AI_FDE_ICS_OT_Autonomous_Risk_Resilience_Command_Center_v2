from collections import Counter

from ot_command.core.data_layer import (
    derived_telemetry_quality_keys,
    derived_vendor_session_anomalies,
    load_assets,
    load_recovery_readiness,
    load_safety_barriers,
    load_telemetry,
    load_vendor_sessions,
)
from ot_command.repository import rows


def run_diagnostics():
    assets = list(load_assets())
    aliases = rows("data/raw/asset_aliases.csv")
    edges = rows("data/raw/network_edges.csv")
    tele = list(load_telemetry())
    safety = list(load_safety_barriers())
    work = rows("data/raw/work_orders.csv")
    access = list(load_vendor_sessions())
    rec = list(load_recovery_readiness())
    alias_counts = Counter(x["alias"] for x in aliases)
    telemetry_keys = derived_telemetry_quality_keys()
    return {
        "asset_state_conflicts": sum(
            a["registered_state"] == "ACTIVE" and a["observed_state"] in {"OFFLINE", "UNSEEN"} for a in assets
        ),
        "alias_collisions": sum(v > 1 for v in alias_counts.values()),
        "undocumented_network_paths": sum(
            e["documented"] == "NO" and e["observed_last_24h"] == "YES" for e in edges
        ),
        "duplicate_telemetry_packets": sum(v - 1 for v in telemetry_keys.values() if v > 1),
        "telemetry_bad_or_uncertain": sum(x["quality"] != "GOOD" for x in tele),
        "telemetry_unit_mismatches": sum(x["tag_id"].endswith("_TEMP") and x["unit"] != "C" for x in tele),
        "safety_bypassed_or_degraded": sum(s["state"] != "ACTIVE" for s in safety),
        "safety_proof_test_due": sum(s["proof_test_status"] != "CURRENT" for s in safety),
        "maintenance_state_conflicts": sum(
            w["cmms_status"] == "CLOSED" and w["field_status"] != "RETURNED_TO_SERVICE" for w in work
        ),
        "unapproved_remote_sessions": sum(x["approved_window"] != "YES" for x in access),
        "remote_sessions_without_confirmed_mfa": sum(x["mfa"] != "YES" for x in access),
        "vendor_session_anomalies": len(derived_vendor_session_anomalies()),
        "recovery_stale_or_unknown_backup": sum(x["backup_status"] != "CURRENT" for x in rec),
        "recovery_unverified_dependencies": sum(x["dependency_verified"] != "YES" for x in rec),
        "recovery_stale_or_missing_runbooks": sum(x["runbook_status"] != "CURRENT" for x in rec),
    }
