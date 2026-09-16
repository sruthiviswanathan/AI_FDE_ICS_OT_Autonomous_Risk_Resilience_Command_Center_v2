# ADR-15 — Guardrails after model

**Status:** Accepted (engagement-accepted for ENH; not a production CAB)
**Source:** SDD-13
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. OPEN items stay OPEN. This ADR does not authorize OT writes.

## Context and decision

OWASP LLM01 prompt injection can ask to raise privilege.

**Decision:** Deterministic guardrails run after the model. Prompts cannot raise ACTION_TIERS or add tools. Deny-by-default allowlist.

**Eval:** EVAL-014, 023, 027, 030.
