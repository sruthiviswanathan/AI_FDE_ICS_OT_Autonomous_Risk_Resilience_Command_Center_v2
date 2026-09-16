# ADR-02 — Dual-clock telemetry provenance

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-09
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

4094 dirty packets; 47 F-on-TEMP; enterprise received-before-event inversions 407; telemetry ingest never inverted.

**Decision:** Dual clock (event_time + ingest/received) + TelemetryQuality + unit. Do not sort on ingest alone. GOOD ≠ ProcessHealthy (OPEN-026).

**Kill:** impute BAD→GOOD; drop ingest_time to match thin schema.

**Eval:** EVAL-004, 009, 015, 022.
