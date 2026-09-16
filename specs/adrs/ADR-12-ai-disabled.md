# ADR-12 — AI-disabled is core

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-11
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

SDD-05 mandatory non-AI fallback. Blank screen on LLM down fails the system.

**Decision:** AI_ENABLED=0 (or model timeout) still shows identity/telemetry/recovery tables and refuses control. Engines do not require an LLM.

**Eval:** EVAL-016.
