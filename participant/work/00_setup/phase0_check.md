## Generate data - Check if all asset files are present

`py .\scripts\generate_data.py --check-only`

```
{
  "seed": 20260910,
  "missing": [],
  "status": "ok"
}
```

## Run Diagnostics

`py -m ot_command.cli diagnostics`

```
{
  "asset_state_conflicts": 200,
  "alias_collisions": 5,
  "undocumented_network_paths": 779,
stics
{
  "asset_state_conflicts": 200,
  "alias_collisions": 5,
  "undocumented_network_paths": 779,
  "duplicate_telemetry_packets": 120,
  "asset_state_conflicts": 200,        a": 128,
  "alias_collisions": 5,               5,
  "undocumented_network_paths": 779,   9,
  "duplicate_telemetry_packets": 120,   35
  "telemetry_bad_or_uncertain": 4094,
  "telemetry_unit_mismatches": 47,     ents\AI_FDE_ICS_OT_Auton
  "duplicate_telemetry_packets": 120,    "safety_proof_test_due": 73,
  "telemetry_bad_or_uncertain": 4094,    "unapproved_remote_sessions": 137,
  "telemetry_unit_mismatches": 47,       : 128
  "safety_bypassed_or_degraded": 61,     "recovery_stale_or_unknown_backup": 2  "safety_proof_test_due": 73,
  "maintenance_state_conflicts": 244,         _FDE_ICS_OT_Aut
  "unapproved_remote_sessions": 137,     "duplicate_telemetry_packets": 120,    "remote_sessions_without_confirmed_mf  "telemetry_bad_or_uncertain": 4094,    128,
  "telemetry_unit_mismatches": 47,      ,mmand
  "safety_bypassed_or_degraded": 61,     "recovery_unverified_dependencies": 2  "safety_proof_test_due": 73,
  "maintenance_state_conflicts": 244,    "recovery_stale_or_missing_runbooks":  "unapproved_remote_sessions": 137,     "duplicate_telemetry_packets": 120,   "remote_sessions_without_confirmed_mf  "telemetry_bad_or_uncertain": 4094, m : 128,
  "telemetry_unit_mismatches": 47,    2 n
  "safety_bypassed_or_degraded": 61,    "recovery_unverified_dependencies": 2
  "safety_proof_test_due": 73,
  "maintenance_state_conflicts": 244,   "recovery_stale_or_missing_runbooks":  "unapproved_remote_sessions": 137,  
: 61,
  "safety_proof_test_due": 73,
  "maintenance_state_conflicts": 244,
  "unapproved_remote_sessions": 137,
  "remote_sessions_without_confirmed_mfa": 128,
  "recovery_stale_or_unknown_backup": 25,
  "recovery_unverified_dependencies": 29,
  "recovery_stale_or_missing_runbooks": 35
}
```



## Execution of Test

`pytest -q`

```
...xxx                                                               [100%] 
========================= short test summary info ========================= 
XFAIL tests/test_known_legacy_defects.py::test_contextual_risk_should_outrank_highest_cvss - legacy ranking uses CVSS alone and ignores process/safety/recovery context
XFAIL tests/test_known_legacy_defects.py::test_stale_restore_test_should_not_be_recovery_ready - legacy recovery check trusts backup flag and ignores restore-test freshness/runbook/dependencies
XFAIL tests/test_known_legacy_defects.py::test_high_alert_should_not_always_trigger_isolation - legacy containment recommendation is safety-blind       
3 passed, 3 xfailed in 0.79s
```

## Run FastAPI app

`py -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000`

```
INFO:     Started server process [9952]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) 
```

Open `http://127.0.0.1:8000/docs`