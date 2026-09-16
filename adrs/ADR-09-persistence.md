# ADR-09 — Typed JSON persistence

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-10
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

requirements.txt has no graph DB. Five queries do not require RDF.

**Decision:** Persist gold views as typed JSON/JSONL. Not RDF, not Neo4j-now. Production graph store remains unselected.

**Eval:** EVAL-012 hop cap; NFR-CAP.
