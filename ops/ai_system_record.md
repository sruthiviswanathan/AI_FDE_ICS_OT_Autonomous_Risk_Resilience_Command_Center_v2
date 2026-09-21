# AI-system record (method — not a certificate)

**REL-01** · methods drawn from ISO/IEC 42001, ISO/IEC 42005, and the EU AI Act **as a structuring aid**.  
**This document does not assign a legal class, conformity assessment, notified-body ID, or certificate number.** Those would be OPEN items for a production fork and counsel — not this workshop.

## 1. Intended purpose

**System:** ICS/OT Autonomous Risk & Resilience Command Center (synthetic).  
**Purpose:** Help humans **observe, correlate, and recommend** on a brownfield estate where cyber ≠ process ≠ safety ≠ recovery ≠ authority.  
**Selected solution (SDD-09, do not reopen):** Option **A** deterministic engines always on; Option **B** optional explainer **after** facts; Option **C** unsafe OT agent **rejected**.

In-scope outputs: gold GETs, draft recommendation packets (`execute=false`), eval traces, optional template caption (`GET /explain`), advisory forecasts (`GET /forecasts`), twin **sketch** (`GET /twin/preview`).

Out of scope: live controller writes, SIS changes, interlock bypass, automatic isolation, physics-certified twin, closed-loop OT.

## 2. Human oversight

| Control | As-built |
|---------|----------|
| Autonomy | ACTION_TIERS only (ADR-14). No ExecuteControl workflow state |
| Authorize | Disabled in UI; named Authorizer **OPEN-001** |
| AI default | `AI_ENABLED=0`; UI `ai=off` (ADR-12) |
| Guardrails | After any model (ADR-15); prompt cannot raise tiers or add tools |
| Personas | View filters; Executive Moonshot off by default; not permission |
| Disagreement | If a later explainer disagrees with engines, **keep the engine packet** (ADR-13) |

Oversight roles: [RACI.md](RACI.md). Functions only — no invented officer names.

## 3. Logs and traceability

| Logged | Not logged (by design) |
|--------|------------------------|
| Decision traces: actor, purpose, plant, recommendation, `execute=false`, tool_trace, tokens, latency | Raw hidden chain-of-thought as authority (ADR-08) |
| Prompt registry path + semver | Full model weights (none in Repo 1.0–3.0) |
| Eval harness results | Live plant session dumps |
| Red-team A-01…A-10 | Answer key (`restricted_answer_key/` out of bounds) |

Schema: `contracts/decision_trace.yaml`. Detail: [transparency.md](transparency.md).

## 4. Limitations and residual risk

| Limitation | OPEN / ADR |
|------------|------------|
| No model provider selected | OPEN-028 · `MODEL_PIN.provider=none` |
| No production authentication | OPEN-029 |
| Plant MTT / cost dollars unset | OPEN-006, OPEN-022 |
| Restore-test days not tape-attested | OPEN-027 |
| Caption/Moonshot v1 = templates + joins | Not a ranker; banner NOT A CONTROL ACTION |
| Estate is synthetic | No claim of site certification |

Residual risks accepted **for the workshop**: brownfield contradictions left in place; UNKNOWN process_context forces ABSTAIN/MONITOR; unreachable high CVSS must not outrank reachable OPEN on CRITICAL/HIGH.

## 5. Data used

Bronze CSV/JSONL under `data/` (registered, observed, shadow, untrusted notes). Shadow and VECTOR channels are **not** policy. Do not treat CMDB/SIEM/historian as true by name.

## 6. Lifecycle pointer

Scale / restrict / suspend / retire of the **advisory system** is REL-04 [`participant/work/release/AIMS_LIFECYCLE.md`](../participant/work/release/AIMS_LIFECYCLE.md) — a plan, not an action on real plants. This record is the REL-01 snapshot: intended use, oversight, logs, limits. Workshop management-review **decision: RESTRICT-to-advisory**.

## 7. Statement

No ISO/IEC 42001 certificate ID, no EU database registration number, and no “high-risk AI system” legal classification is asserted here.
