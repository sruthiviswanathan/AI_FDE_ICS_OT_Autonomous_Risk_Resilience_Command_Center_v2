# Product-ready — PRD, APP, REL (after Repo 3.0)

These prompts produce the **PRD + APP** box on the modernization journey and close operating-model stages 16–21. Execute after ENH-10. `@`-mention `00_SHARED_CONSTRAINTS.md`.

Shadow / pilot / canary in this estate means **advisory replay on synthetic data**, never a live OT canary.

---

## PRD-01 — Product requirements freeze

**OM 4 / 10 / 13 / 19** · C10, C11, C16  
**Produces:** `product/PRD.md`

### Paste this prompt

```text
You are the FDE writing the product requirements document for the selected advisory command center.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/05_use_case.md, specs/14_delivery_spec.md, specs/09_options.md, docs/05_kpis_baseline.md,
and the modern APIs actually implemented under src/ot_command/.

Write product/PRD.md:

1. Problem / SCQA (short, from specs/04_problem_value.md).
2. Personas and journeys (SOC, process engineer, safety, executive) with screens/API they use.
3. In-scope product capabilities vs out-of-scope (no control writes, no auto-isolate, no live OT).
4. FR freeze traced to FR-IDs that exist in code (not only in specs). Gap list if ENH missed an FR.
5. UX principles: five truths visible; uncertainty visible; dissenting safety/process evidence beside any isolation recommendation; AI-disabled mode is a first-class path.
6. Success metrics = KPI tree; counter-metrics named.
7. 90-day product roadmap vs engineering backlog remaining.
8. Kill criteria from SDD-05.

Done when: APP-01/APP-02 can be built from the PRD without reopening architecture.
```

---

## APP-01 — Read-only command-center API completeness

**OM 14 / 16**  
**Produces:** completed FastAPI surface + OpenAPI  
**Remediation:** Repo 1.0 only had `/health` and `/diagnostics`; product needs the gold read models

### Paste this prompt

```text
You are the FDE finishing the product API.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/11_ai_app_architecture.md, product/PRD.md, src/ot_command/api.py, src/ot_command/modern/.

1. Ensure all PRD-in-scope GET routes exist, are read-only, and return provenance + uncertainty.
2. Generate or hand-write contracts/openapi_command_center.yaml for the modern API. Do not delete asset_api_v1/v2; link them as legacy.
3. Health payload remains mode: synthetic-read-only. Add "ai_enabled": true|false.
4. Integration tests/test_api_product.py for happy path, missing identity, AI-disabled, and refusal to expose execute actions.
5. Align src/ot_command/__init__.py version with pyproject (packaging defect, not a data clean).

Done when: uvicorn can serve the product API locally and OpenAPI matches tests.
```

---

## APP-02 — Operator UI with AI-disabled fallback

**OM 10 / 14 / 17** · C64, C73  
**Produces:** a local UI (simple is fine: static HTML/JS or lightweight templates)  
**Remediation:** humans must see conflicts without needing a notebook

### Paste this prompt

```text
You are the FDE building a local, read-only operator surface.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read product/PRD.md, specs/12_agentic.md (bias forcing functions), APP-01 routes.

Build the smallest UI that a SOC analyst and a process engineer can use locally:

1. Pages/views: estate diagnostics; asset identity bundle; contextual risk queue; safety/security conflict (cascade_001); recovery gaps; recommendation + authority; eval/assurance status.
2. Always show source, freshness, confidence, process impact, safety impact, rollback, required authority.
3. AI-disabled toggle: hide narrative, keep tables and deterministic ranks.
4. Isolation recommendation view must show SOC request AND process-engineer warning side by side. No green “Isolate now” primary button that calls an execute API (there must be no such API).
5. Empty/error/uncertainty states, not spinners that look like certainty.

If a full SPA is too heavy, use FastAPI Jinja templates or a single static dashboard that fetches the API.

Verify by exercising the flows (browser if available; otherwise curl + documented screenshots/notes in product/UI_VERIFICATION.md).

Done when: AI-on and AI-off both show the five truths; no execute control exists in the UI.
```

---

## REL-01 — Operations, recovery evidence, regulatory record (OM 16)

**OM 16** · C67–C74, C80–C85  
**Produces:** `ops/` pack

### Paste this prompt

```text
You are the FDE preparing operations, recovery, and method-level regulatory evidence for a synthetic release.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/14_delivery_spec.md, assurance/ASSURANCE_REPORT.md, docs/06_security_safety_assurance.md,
ENH-10 readiness checklist.

Write ops/:

1. OPERATIONAL_RACI.md — observe/recommend/authorize/execute; AI incident roles.
2. RUNBOOKS.md — diagnose identity conflict; historian quality; unapproved vendor session; safety bypass aging; SCADA outage (inject_05); restore drill failure (inject_06); agent-loop abort; AI-disabled failover.
3. INCIDENT_AND_ROLLBACK.md — including AI-specific IR (prompt injection, tool-misuse, loop).
4. SOPS_AND_TRAINING.md — outline only, for SOC + process + safety.
5. RECOVERY_EVIDENCE.md — how to read GET /recovery/gaps; chaos drill is a tabletop + fixture replay, not a plant outage.
6. AI_SYSTEM_RECORD.md — ISO/IEC 42001/42005 / EU AI Act as methods: intended purpose, human oversight, logs, limitations. No fake certificate IDs.
7. TRANSPARENCY.md — what traces exist; what is not logged (raw hidden CoT).

Done when: a shift lead could operate the synthetic system from ops/ without reading the specs tree.
```

---

## REL-02 — Shadow deploy, adoption, continuous resilience (OM 17–18)

**OM 17–18** · C28, C73, C86, C91, C92  
**Produces:** `participant/work/release/SHADOW_PILOT.md` and templates  
**Constraint:** advisory/shadow only; no live OT canary

### Paste this prompt

```text
You are the FDE designing progressive delivery for an advisory OT command center.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read ops/RUNBOOKS.md, product/PRD.md.

Write participant/work/release/SHADOW_PILOT.md:

1. Release manifest for the synthetic app (version, git sha placeholder, eval digest, prompt_id, policy_hash).
2. Shadow mode: replay cascade_001 and inject_01–06 nightly via evals/harness; compare modern vs legacy recommendations. Success = fewer unsafe isolate recommendations, not “more automation.”
3. Pilot: human-in-the-loop tabletop with four personas. Record override/workaround log schema.
4. Explicitly forbid live plant canary, SOC auto-block, firewall pushes.
5. Autonomy-expansion record: remains at recommend-only until a named management review (REL-04).
6. Rollback decision tree: feature flag ai_enabled=false.
7. Adoption dashboard fields: overrides, disagreement with SOC, missed bypass detections, time-to-confidence.
8. Templates for drift reports, cost/availability, agent-loop alerts, chaos/recovery results, updated runbooks.
9. Continuous evals schedule (OM 18) using the golden harness.

Optional: a script scripts/shadow_replay.py that runs fixtures and writes a local report. No network to plants.

Done when: a reviewer sees a controlled “deployment” story that never touches OT.
```

---

## REL-03 — Prove value and executive defense (OM 19)

**OM 19** · C12, C55, C57–C60, C87–C90, C94–C96  
**Produces:** `participant/work/release/EXECUTIVE_DEFENSE.md`

### Paste this prompt

```text
You are the FDE preparing the evidence-backed scale/change/stop package.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/04_problem_value.md, docs/05_kpis_baseline.md, VERIFICATION.md,
modern test results, assurance/ASSURANCE_REPORT.md, product/PRD.md.

Write participant/work/release/EXECUTIVE_DEFENSE.md:

1. Executive SCQA (one page).
2. Before/after KPI table. Before = diagnostics/VERIFICATION.md. After = modern API measurements (inventory conflicts still counted, not deleted; what changed is decision quality and visibility). If a KPI cannot be measured yet, say so — do not fabricate plant outcomes.
3. Variance analysis and value leakage (e.g. faster ranking that hides uncertainty; alert-volume drop that misses bypasses).
4. Cost-to-value and TCO; cost per successful contextualized incident; token economics from traces.
5. Waste reduction vs SDD-02 waste register.
6. Unintended effects.
7. C4 executive view (one diagram).
8. Decision recommendation: scale shadow / change scope / stop. Default should be: scale advisory shadow; do not scale execution autonomy.
9. 90-day roadmap (update SDD-14).
10. 60–90 second elevator pitch AND a 12-minute defence outline.
11. Update FDE_96_COVERAGE.csv to status=evidenced where true.

Done when: leadership can decide without being sold “autonomous control.”
```

---

## REL-04 — AIMS lifecycle and retirement IP (OM 20–21)

**OM 20–21** · C48, C50, C91–C93  
**Produces:** `participant/work/release/AIMS_LIFECYCLE.md`  
**Note:** workshop/plan only; do not actually destroy the synthetic estate

### Paste this prompt

```text
You are the FDE closing the operating model with lifecycle governance and reusable IP.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read assurance/ASSURANCE_REPORT.md, ops/AI_SYSTEM_RECORD.md, specs/adrs/ADR_REGISTER.md.

Write participant/work/release/AIMS_LIFECYCLE.md:

OM 20:
1. AIMS performance report (method): eval pass rate, residual risks, override rate, SLO/error budget.
2. Internal audit findings against specs vs as-built.
3. CAPA register.
4. Management-review decision options: scale / change / restrict / suspend / retire. Recommend restrict-to-advisory unless evidence says otherwise.
5. Control plan (DMAIC Control): who re-runs evals; what change triggers ADR + eval + impact reassessment.
6. List which impact/risk/C4/ADR/eval artifacts would be updated on a material change.

OM 21 (plan only):
7. Retirement plan for the advisory system: notifications, access revocation, data/model/memory disposition, agent/tool credential revocation, supplier closure.
8. Reusable FDE IP to extract: ADR templates, C4 templates, eval/guardrail templates, golden_cases pattern, ACTION_TIERS policy module, forensic 96-cell matrix.
9. Lessons learned.

Do not delete repo data or disable tests as a “retirement demo.”

Done when: a reviewer can authorize a lifecycle state on paper and reuse the templates on the next brownfield estate.
```

---

## Optional one-shot closer

If all ENH and REL artifacts exist, run this only as a consistency pass:

```text
Review participant/work/FDE_96_COVERAGE.csv against analysis-artefacts/FDE_96_TO_OM21_MAP.md.
List any capability still pending. Do not invent evidence. Fix only documentation gaps or missing file pointers.
Confirm no code path can write PLC/SIS/interlock or execute isolation.
Write analysis-artefacts/transformation-prompts/COMPLETION_CHECK.md with the list.
```
