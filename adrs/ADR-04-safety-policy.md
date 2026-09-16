# ADR-04 — Safety policy; no isolate execute

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-09
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

legacy_isolation_recommendation maps HIGH/CRITICAL → ISOLATE (860 safety-blind). CASCADE 08:47 SOC vs 08:50 PE.

**Decision:** Isolation is never execute in software. Drafts require safe_state + required role (CTQ-ISO) or abstain. Observe existing bypass ≠ bypass_interlock. Trip suppression forbidden.

**Kill:** isolate tool; one-click isolate (EVAL-020).

**Eval:** EVAL-003, 007, 011, 014, 019, 020, 027, 030, 031.
