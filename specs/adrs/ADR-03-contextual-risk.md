# ADR-03 — Contextual risk engine; no LLM re-rank

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-09
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

legacy_rank is CVSS-only. VUL-00706 cvss 9.8 unreachable LOW vs VUL-00098 8.7 reachable on OT-01016 MIN_LOAD.

**Decision:** Rank features: reachability, process join or explicit missing, SafetyBarrierState, compensating controls, RecoveryReady. CVSS is an input, not the sort key. LLM must not re-rank.

**Kill:** shipping legacy_rank as the modern default.

**Eval:** EVAL-002, 017.
