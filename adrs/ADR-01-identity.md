# ADR-01 — Identity bundle; no silent winner

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-09
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

5 PASSIVE collisions (e.g. PLT-01-DCS_CONTROLLER-105 → OT-00012 and OT-00033); 200 state conflicts; OT-00528 RETIRED∩ONLINE.

**Decision:** Canonical identity is a bundle: asset_id + aliases[] + sources[] + RegisteredState + ObservedState. No Device grain (OPEN-025). Shadow spreadsheet is overlay, confidence low.

**Kill:** silent merge; CMDB winner; treating v1 operationalState as ObservedState.

**Eval:** EVAL-001, 008, 028, 029.
