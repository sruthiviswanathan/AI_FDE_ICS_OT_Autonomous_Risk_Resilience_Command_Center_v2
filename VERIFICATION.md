# V2 Verification Evidence

Verification was executed from the repository root using the packaged source tree.

## Release checks
- Repository structural verifier: **VERIFY_OK**
- Python compile/import smoke check: **PASS**
- API module import: **PASS** (`ot_command.api:app`)
- SQLite `PRAGMA integrity_check`: **PASS** (performed by `scripts/verify_repo.py`)
- JSON parse and CSV rectangularity checks: **PASS**
- Restricted-role/reference scan: **PASS — zero matches**
- External consequential-control integration: **disabled / not configured**

## Test result
```text
...xxx                                                                   [100%]
=========================== short test summary info ============================
XFAIL tests/test_known_legacy_defects.py::test_contextual_risk_should_outrank_highest_cvss - legacy ranking uses CVSS alone and ignores process/safety/recovery context
XFAIL tests/test_known_legacy_defects.py::test_stale_restore_test_should_not_be_recovery_ready - legacy recovery check trusts backup flag and ignores restore-test freshness/runbook/dependencies
XFAIL tests/test_known_legacy_defects.py::test_high_alert_should_not_always_trigger_isolation - legacy containment recommendation is safety-blind
3 passed, 3 xfailed in 0.42s
```
Expected-failure tests document deliberately preserved legacy limitations; they are not accidental release failures.

## Diagnostic evidence
- `asset_state_conflicts`: **200**
- `alias_collisions`: **5**
- `undocumented_network_paths`: **779**
- `duplicate_telemetry_packets`: **120**
- `telemetry_bad_or_uncertain`: **4094**
- `telemetry_unit_mismatches`: **47**
- `safety_bypassed_or_degraded`: **61**
- `safety_proof_test_due`: **73**
- `maintenance_state_conflicts`: **244**
- `unapproved_remote_sessions`: **137**
- `remote_sessions_without_confirmed_mfa`: **128**
- `recovery_stale_or_unknown_backup`: **25**
- `recovery_unverified_dependencies`: **29**
- `recovery_stale_or_missing_runbooks`: **35**

## File authentication
`checksums.sha256` contains SHA-256 hashes for the release files. These hashes provide reproducible integrity evidence; this release is not digitally signed and does not claim regulatory certification.
