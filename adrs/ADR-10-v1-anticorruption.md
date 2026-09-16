# ADR-10 — v1 operationalState is not ObservedState

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-10
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

asset_api_v1.yaml uses operationalState; v2 uses observed_state; CSV has registered_state + observed_state.

**Decision:** Park v1 operationalState in legacy_v1_operational_state. Do not map it silently to ObservedState (OPEN-009).
