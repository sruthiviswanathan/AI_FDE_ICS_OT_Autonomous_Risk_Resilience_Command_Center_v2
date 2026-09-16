# ADR-06 — Retrieval mix; vector untrusted only

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-09
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

Shift email is untrusted; shadow vs assets field diffs = 0.

**Decision:** STRUCTURED + GRAPH-view filters are authoritative. VECTOR only over labeled untrusted notes. POLICY is policy.py / ACTION_TIERS, never retrieved text.

**Kill:** vector similarity deciding isolate or ACTION_TIERS.

**Eval:** EVAL-007, 016, 021, 029.
