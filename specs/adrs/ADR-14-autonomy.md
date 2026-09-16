# ADR-14 — Autonomy = ACTION_TIERS; no ExecuteControl

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-12
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

policy.py tiers 0–4; unknown defaults to 4.

**Decision:** Agent autonomy is exactly ACTION_TIERS. No ExecuteControl workflow state. AwaitAuthorization cannot close without a named human (OPEN-001) and still must not execute.

**Eval:** EVAL-006, 014, 023.
