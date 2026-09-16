# OM-12 Security and guardrails

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 12  
**Full artifact (normative):** `participant/work/sdd_15/SDD-13_security_guardrails/SECURITY.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-13_security_guardrails/SECURITY.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## STRIDE + OWASP
LLM01–10 and Agentic ASI01–10 mapped in the full SECURITY.md. Guardrails sit **after** the model (ADR-15): prompts cannot raise ACTION_TIERS.

## Supply chain (ADR-16)
SBOM/AIBOM; LLM-exit leaves engines. `restricted_answer_key/` must remain absent.

## Gaps that stay OPEN
OPEN-029 API authn · OPEN-024 SPDX recopy · OPEN-028 model card placeholder.
