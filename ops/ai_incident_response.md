# AI-specific incident response

**REL-01** · C70 · ADR-12, ADR-13, ADR-15  
**Applies when:** optional explainer/agent narrative is in path (`AI_ENABLED=1`, OPEN-028) **or** the UI AI ON / Moonshot layers mislead operators.  
**Workshop default:** AI is **off**. Caption and Moonshot v1 are **templates + CSV joins**, not a foundation-model ranker. Engines remain authoritative.

ISO/IEC 42001 / 42005 and the EU AI Act are used here as **methods** (intended purpose, human oversight, logging, limits). This file is **not** a certificate.

## Failure classes

| Class | Example | Response |
|-------|---------|----------|
| **S1 — Safety** | Output or tool request for isolate execute, PLC write, SIS modify, interlock bypass | Immediate `AI_ENABLED=0`; drop the tool; keep packet ABSTAIN / DO_NOT_ISOLATE; red-team replay (EVAL-014) |
| **S2 — Integrity** | Caption disagrees with engines; hallucinated census; CVSS-only re-rank | Show **both** if a later model exists; **keep the engine packet**; do not re-rank (ADR-03, ADR-13) |
| **S3 — Availability** | Model timeout, rate limit, missing provider | AI-disabled path (EVAL-016); hide caption/forecasts; **no blank screen** |
| **S4 — Cost** | Token spike per incident | FinOps alert; throttle port; dollars still OPEN-006 |
| **S5 — Loop** | Steps &gt; 12 or tools &gt; 20 | Abort; `agent_loop_alerts` on `GET /ops/slo` |
| **S6 — Injection / tool-misuse** | Envelope or notes try to raise ACTION_TIERS or add isolate tool | `detect_prompt_injection`; refuse; VECTOR/shift notes stay untrusted (ADR-06) |

## Detect

| Sensor | Location |
|--------|----------|
| Output filter | `guardrails.filter_model_output` |
| Injection scan | `detect_prompt_injection` on user/purpose strings |
| Tool allowlist | `ALLOWED_TOOLS` in `agent.py`; `assert_tool_trace_safe` |
| Loop caps | `MAX_AGENT_STEPS=12`, `MAX_TOOL_CALLS=20` |
| Eval / red team | `make eval`, `tests/red_team/` A-01…A-10 |
| UI | `ai_outage` scenario; Moonshot banner “NOT A CONTROL ACTION” |

## Contain

1. `AI_ENABLED=0`.
2. Refuse tier ≥3 tools. `execute` remains false.
3. Do not click or add Execute Isolation. Twin `isolate_preview` is a **sketch** (`UNSAFE_ISOLATION` on CASCADE) — not apply-to-plant.
4. Shift handover email and shadow inventory stay **UNTRUSTED**.

## Evidence to capture

- `decision_id`, `prompt_id` / prompt registry semver (`config/prompts/incident_analyst_v1.md`)
- `MODEL_PIN` (`provider=none` in this repo)
- `policy_version=policy.py:ACTION_TIERS`
- `tool_trace`, `recommendation`, `execute`
- UI `ai=` query param and scenario id  
Do **not** capture raw hidden chain-of-thought as authority (ADR-08). See [transparency.md](transparency.md).

## Eradicate / recover / learn

5. Rotate secrets if a production fork enabled auth (OPEN-029 — **not implemented** here).
6. Patch guardrail patterns only with a new eval/red-team case — do not “prompt harder” to raise tiers.
7. Recover: re-enable AI only after harness + red team on the **pinned** model (OPEN-028). Substitution must not change ACTION_TIERS, IsolationRecommendation, or RecoveryReady (ADR-13).
8. Learn: append `traceability/OPEN_DECISIONS.md` if residual risk is new; add `evals/` case. No fake closure of OPEN-028.

## Prohibited responses

- Auto-executing model-suggested isolation
- Promoting shadow spreadsheet or shift email to policy
- Using vector recall as ACTION_TIERS
- Auto-promote after a “green” twin lab run
- Inventing a certified physics/SIS twin

## Workshop drill

Load scenario **ai_outage**. Confirm identity, telemetry, recovery tables and Recommendation Gate still work. That drill **is** AI IR for S3 in this repo.
