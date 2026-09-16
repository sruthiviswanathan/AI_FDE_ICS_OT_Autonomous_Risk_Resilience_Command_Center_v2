# ADR-05 — RecoveryReady ≠ BackupCurrent

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-09
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

legacy_recovery_ready is true iff backup CURRENT. 113/119 CURRENT rows fail restore/runbook/deps. PLT-01 IDENTITY restore 360d STALE.

**Decision:** RecoveryReady requires restore-test evidence AND runbook current AND dependency verified. Absence ⇒ false. No live restore orchestration.

**Kill:** CURRENT=ready.

**Eval:** EVAL-005, 013, 018.
