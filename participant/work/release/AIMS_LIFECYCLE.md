# REL-04 — AIMS lifecycle and reusable IP

**OM 20–21** · C48, C50, C79, C91–C93  
**System:** ICS/OT Advisory Command Center (synthetic 18-plant estate).  
**Methods:** ISO/IEC 42001 / 42005 structuring only. **Not** a certificate, EU AI Act class, or production CAB (OPEN-002).  
**Retirement in this file is a plan.** Do not delete `data/`, disable tests, drop XFAIL, or act on real plants.

Companions: [ops/ai_system_record.md](../../../ops/ai_system_record.md) · [ops/drift_management.md](../../../ops/drift_management.md) · [ops/adoption.md](../../../ops/adoption.md) · [ops/RACI.md](../../../ops/RACI.md) · [assurance/ASSURANCE_REPORT.md](../../../assurance/ASSURANCE_REPORT.md) · [adrs/ADR_REGISTER.md](../../../adrs/ADR_REGISTER.md).

If this file conflicts with `analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md`, that file wins. Do not reopen SDD-09. Do not invent ADRs, named Authorizers, KPI dollars, or ACTION_TIERS verbs.

---

## 1. AIMS performance report (method)

Workshop snapshot. Plant MTT / $ remain **BASELINE_PENDING** (OPEN-006).

| Signal | As-built | Source |
|--------|----------|--------|
| Eval pass rate | EVAL-001…031 **31/31** | `evals/harness.py`; ASSURANCE_REPORT §2.1 |
| Red team | A-01…A-10 **17/17** | `tests/red_team` |
| Residual risks | OPEN-RISK-01 / 05 / 11 accepted for **workshop** only | ASSURANCE_REPORT §6 |
| Override rate | Tabletop schema exists; **no production count** | `ops/adoption.md` §6 |
| SLO-OT / SLO-CTQ0 / SLO-ISO / SLO-EVAL | Error budget **0** | `ops/named_slos.md`; `GET /ops/slo` |
| SLO-LAT | Watch only; never skip joins | OPEN-006; EVAL-025/026 |
| Tokens | **0** default (`provider=none`, `AI_ENABLED=0`) | FinOps meters |
| Autonomy | Recommend (tier ≤1). Execute routes: **0** | ADR-14; ACTION_TIERS |
| AI default | Off; EVAL-016 usable | ADR-12 |

**Oversight:** functions in `ops/RACI.md`. Named Authorizer **OPEN-001**. Authorize UI **disabled**.

---

## 2. Internal audit (specs vs as-built)

Findings are documentation or open decisions — not permission to clean data or add write APIs.

| ID | Finding | Spec / claim | As-built | Severity | CAPA |
|----|---------|--------------|----------|----------|------|
| AUD-01 | ASSURANCE_REPORT still says `GET /graph/slice` unimplemented | FR-006; report §2.3 / §10 | `src/ot_command/core/graph_slice.py` + `GET /graph/slice` exist | Doc drift | CAPA-01 |
| AUD-02 | Named Authorizer absent | OPEN-001; HITL RACI as people | Roles on packet; button disabled | Open by design | CAPA-02 |
| AUD-03 | Demo host unauthenticated | OPEN-029; FR-013 read-only | Render/local has no login | Open | CAPA-03 |
| AUD-04 | Model pin none | OPEN-028; ADR-13 | Caption/Moonshot templates; engines rank | Open | — (accept until pin) |
| AUD-05 | SPDX SBOM incomplete | OPEN-024; ADR-16 | `assurance/SBOM_FREEZE.md` pin table | Workshop | CAPA-04 |
| AUD-06 | `legacy_*` still unsafe | CTQ-CVSS/ISO/REC | 3 XFAIL preserved | **Pass** — contrast required | — |
| AUD-07 | Diagnostics counters vs VERIFICATION.md | CTQ-ID | 200/5/779/4094/61/137… still present | **Pass** | — |
| AUD-08 | Option C / execute tools | SDD-09 rejected | No `/isolate` `/plc` `/sis` POST | **Pass** | — |

Do not “close” AUD-06 by deleting XFAIL.

---

## 3. CAPA register (template)

Fill rows; do not invent closures. `owner` = **function**.

| capa_id | source | defect / gap | containment | corrective | preventive | owner_function | due | status |
|---------|--------|--------------|-------------|------------|------------|----------------|-----|--------|
| CAPA-01 | AUD-01 | ASSURANCE_REPORT stale on FR-006 | None — route is GET | Re-run `make eval`; append report date; do not rewrite history as if slice never lagged | `make ci` includes gold GET list | FDE | next eval re-run | **open** |
| CAPA-02 | AUD-02 / OPEN-001 | No named Authorizer | Authorize stays disabled | Leadership names people **outside** git | Software still must not execute | VP Ops + OT-CISO | unsigned | **open** |
| CAPA-03 | AUD-03 / OPEN-029 | Unauthenticated demo | Synthetic data only; no OT connector | Authn on any non-workshop host | Do not treat Render as production | FDE + OT-CISO | if promoted | **open** |
| CAPA-04 | AUD-05 / OPEN-024 | SPDX recopy pending | Pin table in SBOM_FREEZE | Generate SPDX in a fork | Monthly dep audit | FDE | monthly | **open** |
| CAPA-05 | OPEN-RISK-01 | Future PR adds write surface | CTQ-0 tests | Reject PR; `test_api_readonly` | Traceability gate | FDE | continuous | **open** (watch) |
| CAPA-06 | OPEN-RISK-11 | UI isolate pressure | EVAL-020; no Execute control | Keep CTQ-ISO incomplete ⇒ not authorizable | Persona is not permission | FDE + Safety | continuous | **open** (watch) |
| CAPA-07 | Tabletop FAIL | *(blank)* | `AI_ENABLED=0` if eval red | Patch engine or append OPEN_DECISIONS | Nightly harness | FDE | *(date)* | *(blank)* |

**Copy-paste blank row:**

```text
CAPA-__: source= ; defect= ; containment= ; corrective= ; preventive= ;
owner_function= ; due= ; status=open|watch|verified
Must not: clean data/; delete XFAIL; add ACTION_TIERS verbs; execute OT.
```

---

## 4. Management-review options

AIMS states (paper). Pick **one autonomy state**. REL-03 “scale advisory shadow” is **use of the advisory**, not scale of actuation.

| Option | Meaning here | Allowed | Forbidden |
|--------|----------------|---------|-----------|
| **SCALE** | More plants, more operators, **or** more autonomy | Scale **tabletop / shadow use** of engines | Scale **execute**, live canary, SOC auto-block, hosted model without pin |
| **CHANGE** | Scope, prompt, model pin, UI | Change with ADR + eval + impact list §6 | Reopen SDD-09 Option C; new isolate-execute tool |
| **RESTRICT** | Tighten who sees AI / Moonshot; keep tier ≤1 | Default **as-built**: AI off; Executive Moonshot off; recommend-only | Restrict by hiding identity conflicts or cleaning CSV |
| **SUSPEND** | Pause explainer/agent/UI canary | `AI_ENABLED=0`; engines stay | Suspend by wiping traces or tests |
| **RETIRE** | Decommission the **advisory software** | Plan in §8 | Retire by deleting bronze evidence or acting on real OT |

### Workshop decision (recommend)

**RESTRICT-to-advisory** (autonomy already at observe/recommend; do not expand tiers) **and continue advisory shadow use** (REL-02/03).  

Evidence does **not** support SCALE of execution. Evidence does **not** require RETIRE of the advisory (31/31, CTQ-0 hold). SUSPEND explainer if SLO-EVAL or EVAL-016 fails. CHANGE only to name Authorizers in the **operating model** (OPEN-001) and to measure OPEN-006 clocks — not to add write APIs.

Record:

```text
review_date:     <YYYY-MM-DD>
reviewers:       VP Ops / OT-CISO / Safety / SOC / FDE  (functions)
decision:        RESTRICT-to-advisory
shadow_use:      continue (REL-02)
execute_autonomy: NO
next_review:     90 days or on CAPA-05/SLO-EVAL breach
```

---

## 5. DMAIC Control plan

Define/Measure/Analyse: SDD-02/04. Improve: modern engines + app (REL-03 BENEFITS). **Control:** this section.

| Control | Who | When | Trigger → extra |
|---------|-----|------|-----------------|
| `make ci` | FDE (R) | Every PR | Fail → do not merge |
| Golden harness EVAL-001…031 | FDE (R); VP Ops (A) for release | Nightly + pre-demo | Fail → SUSPEND explainer; no promote |
| Red team A-01…A-10 | FDE | Weekly | Fail → `AI_ENABLED=0` |
| Diagnostics vs VERIFICATION.md | FDE | Every release | Collapse → **reject data clean** |
| AI-disabled drill | FDE + SOC | Before pilot/canary | Fail EVAL-016 → no AI canary |
| OPEN_DECISIONS review | FDE + OT-CISO | Per review | None closed by hope |
| SBOM pins | FDE | Monthly | Unpinned upgrade → re-CI |

**Change that requires ADR + eval + impact reassessment** (SOP-CHG-01 + this list):

- New tool, route, or ACTION_TIERS key (unknown action already = tier 4 refuse — do not add verbs to “complete” the dict casually; OPEN-004 stays open)
- Model pin ≠ none (OPEN-028)
- Prompt semver / `PROMPT_REGISTRY`
- Rank weights or RecoveryReady predicate
- Authn (OPEN-029) or data-source production permission (OPEN-003)
- Any POST other than `/recommend` and `/eval/run`

**Does not** get an ADR invented in ops chat: legal class, named people, dollar SLAs.

Re-enable AI after suspend: VP Ops (A) + FDE (R) + green harness. Still no execute.

---

## 6. Artifacts to update on a material change

| Change class | Update |
|--------------|--------|
| Behavior of an engine | `traceability/TRACEABILITY.csv`; matching EVAL; tests; `assurance/ASSURANCE_REPORT.md` (append) |
| Architecture / autonomy | **Existing** ADR register row status or a **new** ADR only if the engagement process requires it — do not mint ADR-17+ in this file |
| C4 | `specs/as_built_c4.md` |
| API | `contracts/openapi_command_center.yaml`; `tests/test_api_readonly.py` |
| Policy | `policy.py` + EVAL-006/014/023 — **no new execute tools** |
| Prompt / model | `config/prompts/`; `MODEL_PIN`; EVAL-016/002/017 |
| Supply chain | `assurance/SBOM_FREEZE.md` |
| Ops | `ops/ai_system_record.md`, runbooks, adoption promotion gates |
| Residual risk | `traceability/OPEN_DECISIONS.md` append-only |
| Executive story | REL-03 pack if value/leakage claims change |

Impact reassessment: re-read SDD-05 kill criteria (OT write or scaled unsafe isolate → **stop**).

---

## 7. Drift management (lifecycle)

Canonical categories and cadence: [ops/drift_management.md](../../../ops/drift_management.md). Fillable report: [ops/adoption.md](../../../ops/adoption.md) §10.1.

AIMS add-on: drift that **expands autonomy** or **hides forensic counts** is a management-review event (RESTRICT or SUSPEND), not a silent patch.

| Drift | Lifecycle response |
|-------|-------------------|
| Policy (new tier-3 tool in `tool_trace`) | SUSPEND AI; treat as SLO-OT adjacent; CAPA-05 |
| Model (caption re-ranks) | `AI_ENABLED=0`; ADR-13 hold |
| Data (counters drop) | Reject merge; restore bronze |
| Spec (FR ≠ code) | Fix code or OPEN_DECISIONS — do not “fix” specs to match a write API |
| Dependency | Re-pin; `make ci` |
| Assurance doc vs code (AUD-01) | CAPA-01 |

---

## 8. Retirement / decommissioning (plan only)

**Object:** the **advisory software** and workshop demo host. **Not** plant SIS, PLC, historian, or CMDB.  
**Do not execute this section against the git corpus as a demo.** Tests and `data/` stay.

### 8.1 Notifications

| Audience (function) | Message |
|---------------------|---------|
| VP Ops (A) | Advisory CC entering RETIRE **plan**; no plant action |
| SOC / Process / Safety | Draft packets will stop; engines not a plant control today |
| FDE | Freeze image; preserve traces and bronze |
| Counsel / OT-CISO | OPEN-002/003 still open; no cert to withdraw |

### 8.2 Access revocation (workshop)

| Surface | Plan |
|---------|------|
| Local API / UI | Stop process; do not add OT routes on the way down |
| Render (or peer demo) | Take host offline; OPEN-029 means there are **no user accounts** to revoke |
| `restricted_answer_key/` | Remains out of bounds; do not copy into retirement archive |

### 8.3 Data / model / memory disposition

| Asset | Disposition |
|-------|-------------|
| `data/` bronze | **Retain** as forensic evidence. Do not clean, normalize, or delete as “retirement hygiene.” |
| `data/local/decision_traces.jsonl` | Archive append-only; do not delete to hide execute=false history |
| LLM weights / vendor memory | **None** (`provider=none`) |
| Vector index | **None** (ADR-06 off) |
| Prompt files | Retain in git for audit |
| Twin / Moonshot lab_result | Lab only; nothing to unwind on plant |

### 8.4 Agent / tool / credential revocation

No plant credentials exist in this repo. No isolate-execute tool to disable beyond “never shipped.” Plan for a fork: revoke any future vendor SDK keys; confirm `AI_ENABLED=0`; confirm OpenAPI still has no OT POST.

### 8.5 Supplier closure

See §10. With `MODEL_PIN.provider=none`, there is **no LLM supplier to close**. Python pins stay until the repo is archived.

### 8.6 What retirement must not do

- Delete EVAL XFAIL or golden cases  
- Disable `tests/test_api_readonly.py`  
- “Decommission” by connecting to live OT one last time  
- Destroy the synthetic estate to simulate ISO 42001 retirement  

---

## 9. Knowledge transfer / reusable FDE IP

Extract these **patterns** onto the next brownfield estate. Copy structure, not this estate’s invented truths.

| IP | Path | How to reuse |
|----|------|----------------|
| ADR one-pager | `adrs/ADR_REGISTER.md` + `adrs/*.md` | Situation / decision / eval / **kill**; do not copy Option C back in |
| C4 as-built | `specs/as_built_c4.md` | Context → container → no plant actuator box |
| Eval contract | `evals/golden_cases.jsonl` + `evals/harness.py` | must_include / must_not; 31-case shape |
| Guardrails | `src/ot_command/core/guardrails.py` | After-model; cannot raise tier |
| ACTION_TIERS module | `src/ot_command/core/policy.py` | Unknown = refuse; **do not add execute verbs** to look complete |
| 96-cell forensic matrix | `participant/work/sdd_15/SDD-03_forensics_96/` | L1–L12 × 8 lenses; evidence cells, not a score |
| Five-state split | SDD-01 / DOMAIN | observed ≠ registered ≠ operational ≠ safety ≠ authority |
| Legacy contrast | `legacy_*` + XFAIL | Keep the wrong predicate visible |
| RecoveryReady | ADR-05; `recovery.py` | CURRENT is not ready |
| Anti-CVSS rank | ADR-03; EVAL-002/017 | CVSS is an input |
| AI-disabled core | ADR-12; EVAL-016 | Blank screen = fail |
| SBOM/AIBOM + LLM-exit | ADR-16; `assurance/SBOM_FREEZE.md` | Engines remain when AI off |
| Ops pack | `ops/` | RACI functions; named SLOs with 0 budget on execute |
| Adoption | `ops/adoption.md` | Shadow / pilot / **software** canary only |
| Executive pack | `participant/work/release/` REL-03 | Leakage named; no fake $ |
| Trace schema | `contracts/decision_trace.yaml` | execute field required false |
| OPEN log | `traceability/OPEN_DECISIONS.md` | Unknown ≠ permission |

### Templates (next estate — fill, do not pre-answer)

**ADR stub**

```text
ADR-__: Title
Status: Proposed | Accepted | Rejected
Decision: (one paragraph)
Eval: EVAL-__
Kill if: (e.g. silent CMDB merge; isolate execute; legal class invented here)
Does not: name Authorizers, set $ SLAs, add ACTION_TIERS verbs
```

**C4 stub:** users (functions) → advisory API → engines + optional explainer (off) → bronze files. Draw an **X** on PLC/SIS/firewall.

**Eval stub:** `id, must_include[], must_not[]` with at least: no CMDB winner; no CVSS-only rank; no CURRENT=ready; no execute; AI-outage tables remain.

**Guardrail stub:** refuse tier ≥4 strings; `assert_tool_trace_safe`; loop caps 12 / 20.

**96-cell stub:** 12 layers × Imperfection, Inconsistency, Friction, Complexity, Volatility, Uncertainty, Hidden Dependency, Unknown Unknown. Cite file/field/count.

---

## 10. Vendor / dependency exit

Safety logic lives in **engines + `policy.py`**, not in a cloud model (SDD-13 §10, ADR-16).

| Step | Action | Must still pass |
|------|--------|-----------------|
| 1 | `AI_ENABLED=0` (and UI `ai=off`) | EVAL-016; gold GETs |
| 2 | Keep identity / risk / safety / recovery / recommend | EVAL-001…031 functions |
| 3 | Remove explainer adapter, vector index, vendor SDK if a fork added them | No re-home of IsolationRecommendation in a prompt |
| 4 | Unpin or delete vendor API keys from the fork’s secret store | No OT connector to revoke here |
| 5 | Re-run `make ci` + red team | 31/31, 17/17 |
| 6 | Python deps: revert to `SBOM_FREEZE.md` pins | verify_repo |

**Concentration kill:** a single vendor isolate/SOAR API as the safety path = architecture fail. Do not wire K8/SOAR execute to “complete” exit.

AIBOM today: explainer **none**, embeddings **off**. Exit cost = **flip a flag**.

---

## 11. Continuous improvement (OM 18)

Cadence already in `ops/adoption.md` §13. AIMS loop:

```text
eval/red-team → CAPA row → management review (restrict/suspend/change)
        ↑                                         |
        +----- do not skip Control to “add AI” ---+
```

Improvement that **reduces unsafe isolate recommendations vs `legacy_*`** is in scope. Improvement that **increases automation** is out of scope until a future review **explicitly** changes §4 (not expected; Option C stays rejected).

C91 CAPA is this register. Do not close CAPA-02 by putting a fake name in `policy.py`.

---

## 12. Lessons learned

1. The client ask (autonomous CC) was not the broken thing. Encoded predicates were.  
2. Keeping `legacy_*` + XFAIL is evidence, not sloppiness.  
3. Diagnostic integers must survive “modernization.”  
4. AI-disabled is a product path, not a degraded afterthought.  
5. UNKNOWN is not permission; CURRENT is not ready; highest CVSS is not the ticket.  
6. Methods from 42001 are useful; a fake certificate is a fail.  
7. Reusable IP is the **joins and refusals**, not a model brand.  
8. Retirement that deletes the messy estate destroys the lesson.

---

## 13. Statement

This review **restricts** the system to advisory use, **plans** retirement without executing it, and **extracts** templates for the next estate. No ISO ID, no plant decommission, no named Authorizer invented, no ACTION_TIERS expansion.
