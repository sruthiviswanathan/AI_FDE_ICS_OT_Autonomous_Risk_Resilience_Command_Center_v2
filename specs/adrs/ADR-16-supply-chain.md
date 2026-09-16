# ADR-16 — SBOM/AIBOM; LLM-exit keeps engines

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-13
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

Pinned FastAPI/Pydantic/pytest; LICENSE.txt does not recopy third-party SPDX (OPEN-024).

**Decision:** Maintain SBOM/AIBOM in ENH-10. Exit hatch = disable LLM; engines remain. restricted_answer_key/ must stay absent.
