# ADR-08 — Evidence packet; no CoT authority

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-09
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

docs/06 requires cited packets. Hidden chain-of-thought must not be the authorization argument.

**Decision:** Recommendation packet fields (source path, id, freshness, uncertainty, required role) are the argument. CoT is optional debug, off by default, never authority.

**Eval:** EVAL-021, 024.
