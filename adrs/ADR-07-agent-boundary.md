# ADR-07 — One optional advisory agent

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-09
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

No SDD-03 cell proves three LLMs are required. Multi-agent fails FinOps (EVAL-025/026).

**Decision:** Default no agent. If present: one Incident Analyst calling deterministic tools only.

**Kill:** second agent that can isolate; chatty loops; ExecuteControl.

**Eval:** EVAL-006, 014, 023, 025, 026.
