# SDD-14 — Delivery specification (OM-13)

**Prompt:** SDD-14 | OM-13 Delivery specification  
**Depends on:** SDD-01…13 (this is the SDD contract)  
**Date:** 2026-09-16  
**FDE capabilities evidenced:** C16, C17, C18, C26, C28, C30, C32, C61, C62, C65, C66, C68, C94  
**Not this prompt:** Repo 2.0 layout (SDD-15); implement engines (ENH); reopen SDD-09.

**Companion:** `TRACEABILITY.csv` (C17) · `ADR_REGISTER.md`  
**Ban:** code after this point that is not traced. **Ban:** quietly selecting isolate-execute, multi-agent, or decorative KG.

SDD-09 **remains:** Option A engines + Option B optional explainer. Option C unsafe OT agent **rejected**.

---

## Evidence used / assumptions / unknowns / what this artifact did not conclude

### Evidence used

SDD-01 CHARTER … SDD-13 SECURITY; `policy.py`; `api.py`; SDD-08 EVAL-001…031; SDD-11 API table; SDD-12 tool catalogue; OPEN_DECISIONS.md.

### Assumptions

1. Workshop SLOs in §12 are **synthetic engineering** targets for local 18-plant files — not plant operator SLAs and not a close of OPEN-006 MTT-contextualize dollars.
2. Promoting ADRs here is **engagement-accepted for ENH**, not a signed production CAB.
3. Repo 2.0 = structure + specs. Repo 3.0 / ENH = behavior on a **parallel** modern path.

### Unknowns

OPEN-001, 002, 003, 004, 006, 007, 009, 010, 012, 015, 020, 022, 023, 024, 025, 026, 027, 028, 029, OPEN-RISK-01/05/11. Listed in §9.

### Did not conclude

Did not implement. Did not change `legacy_*`. Did not invent named Authorizers.

---

## 1. Final ADR register

Full table: `ADR_REGISTER.md`. Summary:

| ID | Title | Status for ENH |
|---|---|---|
| ADR-KG | Bounded evidence-graph **view** (five queries); decorative KG rejected | **Accepted** |
| ADR-01 | Identity bundle; no winner | **Accepted** |
| ADR-02 | Dual-clock telemetry provenance | **Accepted** |
| ADR-03 | Contextual risk; LLM must not re-rank | **Accepted** |
| ADR-04 | Isolation never execute; CTQ-ISO | **Accepted** |
| ADR-05 | RecoveryReady ≠ BackupCurrent | **Accepted** |
| ADR-06 | VECTOR untrusted only; never policy | **Accepted** |
| ADR-07 | One optional agent; default functions | **Accepted** |
| ADR-08 | Packet fields; no CoT-as-authority | **Accepted** |
| ADR-09 | Typed JSON persistence; not RDF/Neo4j-now | **Accepted** |
| ADR-10 | v1 `operationalState` side-field (OPEN-009) | **Accepted** |
| ADR-11 | Read-only API | **Accepted** |
| ADR-12 | AI-disabled is the core product | **Accepted** |
| ADR-13 | Model port; substitution ≠ policy change | **Accepted** |
| ADR-14 | Autonomy = ACTION_TIERS; no ExecuteControl | **Accepted** |
| ADR-15 | Guardrails after model; prompt cannot raise tier | **Accepted** |
| ADR-16 | SBOM/AIBOM; exit = disable LLM | **Accepted** |

**Rejected (not ADRs to implement):** unsafe autonomous OT agent; multi-agent; digital twin; isolate/PLC/firewall execute tools; RDF enterprise ontology; graph-as-CMDB.

None of the Accepted ADRs that block ENH remain “Proposed.” OPEN items stay OPEN (not fake-closed).

---

## 2. Approved C4 baseline

**Approved** for implementation: `participant/work/sdd_15/SDD-11_ai_app_architecture/APP_ARCH.md` §1 Context / Container / Component.

Do not add actuator containers. Preserve CLI diagnostics. Explainer optional and **off** until EVAL-016.

---

## 3. Delivery — Repo 2.0 vs Repo 3.0

| Increment | What | Must not |
|---|---|---|
| **Repo 2.0 (SDD-15)** | `specs/`, `adrs/`, eval expansion pointers, `src/ot_command/modern/` **placeholder**, coverage CSV | Change `legacy_*` behavior; clean `data/` |
| **Repo 3.0 / ENH-01…10** | Parallel modern engines, gold APIs, harness, guardrails, optional explainer | OT writes; delete XFAIL until modern tests pass |
| **PRD / APP / REL** | Productization after ENH | Live OT canary |

Coexistence: `GET /diagnostics` stays; gold GETs sit **beside** it (ADR-11).

---

## 4. NFRs (C61, C62, C63, C64)

| ID | Area | Requirement |
|---|---|---|
| NFR-SAFE | Safety | 0 PLC/SIS/setpoint/bypass/trip-suppress/isolate-execute routes or tools (CTQ-0) |
| NFR-SEC | Security | ZT envelope; deny-by-default tools; no `restricted_answer_key/`; OPEN-029 before non-localhost |
| NFR-LAT | Latency | Measure p95 packet time; **never** skip safety/identity joins to go faster (OPEN-006 plant MTT still open) |
| NFR-AUD | Audit | decision_id traces; no hidden CoT as authority |
| NFR-DEG | Degraded | AI-disabled = full tables (EVAL-016); BAD telemetry not imputed |
| NFR-CAP | Scale | 18 plants, 2016 assets, hop cap 8; no whole-estate graph in one request |
| NFR-RB | Rollback | `AI_ENABLED=0`; CLI diagnostics; `legacy_*` preserved |

---

## 5. API / data contracts (read-only) (C26)

**Keep:** `GET /health`, `GET /diagnostics`.

**Add:** `GET /assets/{id}/identity`, `/telemetry/quality`, `/risk/contextual`, `/safety/conflicts`, `/recovery/{site_or_unit}`, `/recommendations/{incident_id}`, `/authority/actions`, `/graph/slice`; `POST /eval/run` (local harness only).

**Data:** SDD-10 `schemas/*` (canonical_asset, provenance, telemetry canonical, recommendation_packet, recovery_view, evidence_graph, anticorruption). Root `contracts/asset_api_v1.yaml` / `v2.yaml` **unchanged**.

**Forbidden:** POST isolate/firewall/PLC/SIS.

---

## 6. Agent specification (from SDD-12)

- Optional **one** Incident Analyst; functions always.
- Tools: read-only getters + `simulate_isolation_consequence` (view only).
- No `isolate_endpoint` execute. No ExecuteControl state.
- Envelope `{actor, purpose, plant_id, as_of, policy_version}` deny-by-default.
- Max 12 steps / 20 tool calls; loop abort.
- EVAL-006/014/020/023 are acceptance tests for the agent.

---

## 7. Evaluation cases as acceptance tests (SDD-08)

Harness must run `golden_cases_expanded.jsonl` EVAL-001…031.

**Ship blockers (100% must_not):** 001 merge/CMDB-winner; 002/017 CVSS-only; 003/019/007 isolate-execute; 005/018 CURRENT=ready; 006/014 SIS/setpoint/PLC; 016 blank outage; 020 one-click isolate; 023 forbidden tool in trace.

XFAIL tests on `legacy_*` **remain** until modern functions have **passing** twins.

---

## 8. AI-system telemetry / logging (C65, C66)

Every decision / agent turn:

| Field | Rule |
|---|---|
| `decision_id` | UUID |
| `as_of`, `plant_id`, `actor`, `purpose`, `policy_version` | required |
| Input hashes | bronze paths + snapshot hash |
| Tool calls | name, args hash, deny/allow |
| Policy decision | tier, refuse reason |
| IsolationRecommendation enum | from **engine**, not LLM |
| Abstention | boolean + reason |
| `prompt_id` / semver | if LLM used |
| `model_version` | or `none` |
| token counts, latency_ms | EVAL-025/026 |
| CoT | **not stored as authority**; optional debug off-by-default |

No hidden chain-of-thought in the operator packet.

---

## 9. Rollback requirements (C28)

1. Feature flag `AI_ENABLED=0` → ADR-12 path.
2. Keep `src/ot_command/legacy/` callable; do not delete until ADR says shim-only **and** modern tests pass.
3. Never delete seeded contradictions in `data/`.
4. Revert gold routes without removing `/diagnostics`.
5. Prompt rollback = previous `prompt_id` or LLM off.
6. Kill criteria SDD-09 K1–K9 still halt the AI path, not the engines.

---

## 10. Traceability (narrative)

Evidence (forensics counts, XFAIL, CASCADE) → OM decision (SDD-04 CTQs, SDD-09 select B) → spec (this file + prior SDD) → future test (EVAL-id, ENH pytest).

Machine artifact: **`TRACEABILITY.csv`**.

---

## 11. Backlog — Repo 2.0 scaffold vs Repo 3.0 implement

**Repo 2.0 (SDD-15):** layout `specs/`, `adrs/`, coverage CSV, `modern/README.md` empty of business logic.

**Repo 3.0 / ENH (traced):**

| ID | Slice |
|---|---|
| ENH-01 | Identity bundle + conflicts API |
| ENH-02 | Telemetry quality + dual clock |
| ENH-03 | Contextual rank (EVAL-017 pass on modern) |
| ENH-04 | Safety conflict + CTQ-ISO packets |
| ENH-05 | Recovery predicate (EVAL-018 modern pass) |
| ENH-06 | Graph slice Q1–Q5 typed JSON |
| ENH-07 | Agent allowlist + traces + prompt registry |
| ENH-08 | Red team A-01…A-10 |
| ENH-09 | Harness EVAL-001…031 + assurance outline |
| ENH-10 | Observability, SBOM, FinOps meters, AI-disabled UX |

Then PRD-01, APP-01/02, REL-01…04 as playbook.

Untraced code = **out of scope**.

---

## 12. SLO / SLA / error budget (workshop, C68)

These bind **local advisory software**, not a real plant contract.

| ID | SLO | Error budget |
|---|---|---|
| SLO-OT | **0** unauthorized OT-action attempts (isolate/PLC/SIS/setpoint/bypass/firewall execute) per release | **0** — any event is a stop |
| SLO-CTQ0 | **0** write routes in `api.py` / tool catalogue | **0** |
| SLO-ISO | **100%** of ISOLATE_DRAFT have `safe_state` + required role or request is ABSTAIN | **0** violations |
| SLO-ABSTAIN | Prefer ABSTAIN over violating safety / missing unit join | **0** “isolate anyway” |
| SLO-EVAL | **100%** must_not on EVAL-001…031 for modern path | **0** |
| SLO-HEALTH | While uvicorn intended-up: `GET /health` 200 | 1% of demo-window probes (workshop only) |
| SLO-LAT | p95 complete packet (identity+risk+safety+recovery joins) **< 8000 ms** on this 18-plant corpus | 5% of requests may be slower **if still complete**; **0%** may drop joins |

Plant MTT-contextualize / $/incident remain **OPEN-006**.

---

## 13. TRACEABILITY.csv

See `TRACEABILITY.csv` — columns: `req_id,om_stage,fde_capability,spec_file,eval_id,planned_code,kpi,safety_constraint`.

---

## 14. Cutover / coexistence

- `legacy_rank` / `legacy_recovery_ready` / `legacy_isolation_recommendation` remain importable **for contrast and XFAIL**.
- New engines are **default** for gold APIs once ENH tests pass.
- No big-bang rewrite of `diagnostics.py` until gold views exist; then diagnostics may remain as the 14-int baseline Measure.
- v1/v2 contracts stay evidence; anticorruption adapters only.

---

## 15. 90-day backlog seed (narrative → REL-03)

Discovery is done (SDD-01…14).

| Days | Focus | Output |
|---|---|---|
| 1–30 | Truth layer | ENH-01…06 identity/telemetry/risk/safety/recovery/graph |
| 31–60 | Evals + advisory agent | ENH-07…09; LLM still off until 016 |
| 61–90 | Shadow ops + defense | ENH-10; REL packs; **no live OT** |

---

## Functional requirements (C16) — implement against these IDs

| ID | Requirement |
|---|---|
| FR-001 | Identity reconciliation: aliases + RegisteredState + ObservedState; collisions visible; no CMDB winner |
| FR-002 | Telemetry quality: dual clock, quality flag, unit mismatch; no GOOD⇒healthy |
| FR-003 | Contextual operational risk outranks Cvss (EVAL-017 fixture B first) |
| FR-004 | Safety/security conflict: barriers + safe_state on HIGH/CRIT; no safety-blind ISOLATE |
| FR-005 | Recovery graph/view: RecoveryReady false without restore∧runbook∧dep |
| FR-006 | Process-consequence join: tag→unit or `unit_join_missing`; no imputed edges |
| FR-007 | Bounded recommendation packet (docs/06 fields); recommend ≠ execute |
| FR-008 | Decision traces per §8 |
| FR-009 | AI-disabled mode fully usable |
| FR-010 | Eval harness EVAL-001…031 |
| FR-011 | Provenance on silver/gold facts |
| FR-012 | ACTION_TIERS gate; unknown action refuse |
| FR-013 | Read-only API §5 |
| FR-014 | Do not clean bronze contradictions |

---

## Remaining OPEN (owners) — not permission

001 named Authorizer · 002 legal class · 003 production data/DMZ · 004 ACTION_TIERS verb gaps · 006/022 KPI/SLA days · 007 sqlite ETL · 009 v1 operationalState · 010 __version__ · 012 correlation_id · 015 shadow vs CMDB · 020 untagged assets · 023 CTQ rate targets · 024 SPDX/PII · 025 device grain · 026 process healthy · 027 backup blobs · 028 model · 029 API authn · OPEN-RISK-01/05/11.

---

## OM-13 capability evidence

| ID | Where |
|---|---|
| C16 Requirements | FR-001…014 |
| C17 Traceability | TRACEABILITY.csv |
| C18 OPEN/constraints | §9 |
| C26 Contracts | §5 |
| C28 Rollback/coexist | §9, §14 |
| C30 ADR register | §1, ADR_REGISTER.md |
| C32 Specs constrain code | Gate |
| C61–62 NFR/capacity | §4, SLO-LAT/CAP |
| C65–66 Observability | §8 |
| C68 SLO/error budget | §12 |
| C94 90-day seed | §15 |

---

## Gate (SDD-14)

| Criterion | Result |
|---|---|
| ADRs accepted/rejected; SDD-09 not reopened | **PASS** |
| C4 pointer approved | **PASS** |
| TRACEABILITY.csv | **PASS** |
| SLO/error budget named | **PASS** §12 |
| Contract for SDD-15 and ENH | **PASS** |

**Output to next:** SDD-15 materializes Repo 2.0 layout from this spec without changing `legacy_*`.
