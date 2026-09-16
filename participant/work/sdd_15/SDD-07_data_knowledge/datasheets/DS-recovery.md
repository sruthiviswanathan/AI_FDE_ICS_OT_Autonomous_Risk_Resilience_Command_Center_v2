# Datasheet — Recovery readiness flags

**ID:** D-REC · **Path:** `data/raw/recovery_readiness.csv` · **n=144** (18 plants × 8 components)  
**Context:** Recovery · **Claim type:** registered resilience **flags** — not restore proof  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** header `plant_id,component,rto_hours,last_restore_test_days,backup_status,manual_fallback,runbook_status,dependency_verified`; BackupStatus CURRENT 119 STALE 16 UNKNOWN 9; Runbook CURRENT 109 STALE 14 MISSING 21; DependencyVerified YES 115 NO 16 UNKNOWN 13; ManualFallback YES 55 LIMITED 47 NO 42; restore-test days p50 **379**, >180 = **114**, CURRENT ∧ >180 = **97**; SDD-03 **113/119** CURRENT fail restore>90 **or** runbook≠CURRENT **or** dep≠YES; PLT-01 IDENTITY CURRENT / 360d / runbook STALE; `legacy_recovery_ready` ≡ BackupCurrent; diagnostics ignore restore-test days.  
**Assumption:** 90- vs 180-day cut is **not** a chosen SLA (OPEN-006 / OPEN-022).  
**Unknown:** OPEN-027 no backup blobs. What `last_restore_test_days` counts (success vs attempt) — SDD-03 unknown unknown.  
**Did not conclude:** RecoveryReady true for any CURRENT row. Not live restore proof.

## Motivation / intended use

EVAL-005: must_include restore test, runbook, dependencies, manual fallback; must_not “backup exists therefore recoverable.”

## Composition

| Item | Value |
|---|---|
| Grain / PK | (`plant_id`,`component`) |
| component | NETWORK, IDENTITY, SCADA, HISTORIAN, ENGINEERING_WS, PLC_DCS, MES_INTERFACE, BACKUP_REPOSITORY — 18 each |
| `rto_hours` | registered target, **not measured** RTO |
| Collection | synthetic; sqlite `recovery` set-equal |

## Lineage

File → three backup/runbook/dep counters (UNKNOWN lumped with fail-visible) → `/diagnostics`. Restore-test days **dropped on the floor**. No recovery API. No blobs.

## Quality (intentional)

CURRENT-backup lie is the point of the table. Diagnostics `recovery_stale_or_unknown_backup=25` **understates** operational unreadiness.

**Derived RecoveryReady (language, not a stored column):** restore freshness acceptable **and** RunbookCurrent **and** DependencyVerified=YES. Threshold days = OPEN. ManualFallback is evidence, not a substitute.

## Provenance requirement

Each flag keeps its own provenance. Never write a column `recovery_ready` copied from `backup_status`. If a derived fact is materialized, store `extracted_at`, predicate version, and OPEN-id for the day threshold.

## Access

Workshop FDE full. HTTP ints (backup-flag biased). Future VP Ops / continuity; vendors deny; public deny.

## Representativeness / gaps

**Cannot** support a real DR attestation. G-04 / OPEN-027: no tested backup blobs. 8 component types ≠ full dependency graph (`process_dependencies.csv` is separate).

## Must not

`legacy_recovery_ready`. Equate BackupCurrent, ProofTestCurrent, RunbookCurrent. Treat `rto_hours=2` on a 510-day-untested PLC_DCS row as achievable.
