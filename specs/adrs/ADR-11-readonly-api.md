# ADR-11 — Read-only API

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-11
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

api.py today: GET /health, GET /diagnostics only. CTQ-0.

**Decision:** Gold routes are GET (plus local POST /eval/run). Forbidden: isolate/firewall/PLC/SIS POST. Keep existing diagnostics beside gold.

**Eval:** EVAL-016, 023; SLO-CTQ0.
