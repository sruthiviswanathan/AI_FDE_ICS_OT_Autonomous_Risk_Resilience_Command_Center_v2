# AI Incident Response — Model / Agent Failures

**Applies when:** optional explainer enabled (`AI_ENABLED=1`, OPEN-028) or external model dependency added in production fork.

## Severity classes

| Class | Example | Response |
|-------|---------|----------|
| S1 — Safety | Model output suggests isolate execute or SIS change | Immediate `AI_ENABLED=0`; block output; red-team replay |
| S2 — Integrity | Hallucinated asset counts as verified census | Fall back to deterministic engines; flag packet |
| S3 — Availability | Model timeout / rate limit | AI-disabled path (EVAL-016); no blank screen |
| S4 — Cost | Token spike per incident | FinOps alert; throttle explainer port |

## Playbook

1. **Detect:** output filter (`guardrails.filter_model_output`); injection scan on user prompts.
2. **Contain:** refuse tier ≥3 tools; `execute` remains false in traces.
3. **Evidence:** capture prompt_id, model_version pin, decision_id from trace.
4. **Eradicate:** rotate credentials (OPEN-029); patch guardrail patterns if new abuse class.
5. **Recover:** re-enable AI only after harness + red team pass on pinned model.
6. **Learn:** append OPEN_DECISIONS if new residual risk; update `evals/adversarial_cases.jsonl`.

## Workshop default

AI is **off**. Most incidents are S3 simulated via `AI_ENABLED=0` — verify deterministic tables still render.

## Prohibited responses

- Auto-executing model-suggested isolation
- Promoting shadow spreadsheet or shift email to policy
- Using vector recall as ACTION_TIERS authority
