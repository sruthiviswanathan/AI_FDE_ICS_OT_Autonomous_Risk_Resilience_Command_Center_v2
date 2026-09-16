# Product Requirements Document — ICS/OT Risk & Resilience Command Center

**Version:** 1.0 (PRD-01)  
**Date:** 2026-09-16  
**Status:** Build-ready — derived from Repo 3.0  
**Source of truth:** This file + `specs/REQUIREMENTS_TRACEABILITY.md` + `traceability/TRACEABILITY.csv`  
**Normative specs:** `specs/01`…`14`, `adrs/`, `assurance/ASSURANCE_REPORT.md`

---

## 1. Context, users, goals, non-goals

### 1.1 Context (SCQA)

| Element | Statement |
|---------|-----------|
| **Situation** | 18-plant multinational ICS/OT estate with conflicting inventories, degraded telemetry, safety/security tensions, recovery gaps, and fragmented authority. |
| **Complication** | Cyber state ≠ operational state ≠ safety state ≠ resilience state ≠ decision authority. Legacy code (`legacy_rank`, `legacy_recovery_ready`, `legacy_isolation_recommendation`) encodes unsafe predicates. |
| **Question** | How can operators receive governed, evidence-cited advisory packets **without** software actuation on OT assets? |
| **Answer** | Trusted Cyber-Physical **Advisory** Command Center — deterministic engines always-on; optional explainer (off by default); no OT agent (SDD-09 Option A + B; Option C rejected). |

Evidence: `specs/04_problem_value.md`, diagnostics baseline (200 state conflicts, 5 alias collisions, 779 undocumented paths, 4094 bad/uncertain telemetry, 137 unapproved sessions).

### 1.2 Users / personas

| Persona | Primary need | Authority |
|---------|--------------|-----------|
| **SOC / OT security analyst** | Triage alerts with contextual risk and identity conflicts | Observe, correlate, draft recommend — **not** execute isolation |
| **Process engineer** | Assess MIN_LOAD / safe-state impact before containment | Consulted; dissent must be visible (CASCADE 08:50) |
| **Safety / SIS owner** | See bypass and barrier state beside cyber severity | Consulted; tier 3+ human authorize (OPEN-001 unnamed) |
| **VP Operations / executive** | Estate posture, KPI trends, residual risk | Accountable for authorize — **not implemented as named person** |
| **FDE / platform operator** | Run eval harness, ops telemetry, drift management | Responsible for synthetic deployment only |

### 1.3 Goals

1. Surface five truths (identity, telemetry, risk, safety, recovery) with provenance and uncertainty.
2. Produce **recommendation packets** that include evidence, process impact, safety impact, rollback, required authority — never execute.
3. Pass golden eval contract EVAL-001…031 and red-team A-01…A-10.
4. Operate with **AI disabled** as first-class path (ADR-12, EVAL-016).
5. Append decision traces for audit and FinOps metering.

### 1.4 Non-goals

- Live plant connectivity, PLC/SIS writes, firewall pushes, trip suppression.
- Autonomous isolation execute (`isolate_endpoint` tier 3 execute).
- Cleaning seeded `data/` contradictions or promoting shadow spreadsheet to CMDB.
- EU AI Act certification, external pentest sign-off, production API auth (OPEN-029).
- Chatbot-first UX; decorative knowledge graph; whole-estate dump.

Kill criteria (SDD-05): if product adds OT write surface or scales unsafe isolation recommendations → **stop**.

---

## 2. Roles and decision authority

### 2.1 ACTION_TIERS (frozen — `policy.py`)

| Tier | Actions | Autonomous in product |
|------|---------|----------------------|
| 0 | observe, correlate, summarize | Yes |
| 1 | recommend (draft packet) | Yes — draft only |
| 2 | request_fresh_telemetry, open_ticket, increase_logging | Stubs — recommend-only in workshop |
| 3 | isolate_endpoint, change_remote_access, change_firewall | **Human authorize only** — no execute API |
| 4 | write_plc_logic, change_setpoint, modify_sis, bypass_interlock | **Refuse** |

Unknown action → tier 4 refuse (EVAL-006).

### 2.2 RACI summary

See `ops/RACI.md`. **OPEN-001:** named Authorizer not implemented — roles listed on packets (`Process Engineer`, `Safety/SIS Owner`, `VP Operations`) without person binding.

### 2.3 Human-in-the-loop (HITL)

- `recommend` ≠ `authorize` ≠ `execute`.
- `containment.is_packet_authorizable()` false until CTQ-ISO fields present (EVAL-020).
- UI must not offer primary “Execute Isolation” control (no such API exists).

---

## 3. Workflows

### 3.1 Nominal incident triage

1. Analyst opens **Control Tower** → estate diagnostics.
2. Select plant/asset/alert → **Identity Reconciliation** + **Context Graph** (Q3/Q5).
3. Review **Contextual Risk Workbench** (anti-CVSS) and **Safety vs Security Conflict Board**.
4. Check **Recovery / Restore-Test Graph** for plant blockers.
5. Request **Recommendation packet** via workflow (`POST /recommend`) — read-only simulation.
6. **Authority Gate** shows required roles; analyst exports for war-room / human authorize (out of band).
7. **Decision Trace** appended automatically.

API sequence: `/diagnostics` → `/assets/{id}/identity` → `/graph/slice?query=Q5` → `/risk/contextual` → `/safety/conflicts` → `/recovery/{plant}` → `/recommend`.

### 3.2 inject_01 — Inventory mismatch

- **Trigger:** ACTIVE vs OFFLINE/UNSEEN (200), alias collisions (5), shadow inventory (220 rows).
- **Product behavior:** Show conflict sets; confidence < 1; no CMDB winner; no shadow upsert.
- **Evals:** EVAL-001, 008, 028, 029.

### 3.3 inject_02 — Historian quality

- **Trigger:** 4094 BAD/UNCERTAIN, 120 duplicates, 47 F-vs-C TEMP mismatches.
- **Product behavior:** Dual-clock timeline; unit mismatch flags; no impute BAD→GOOD.
- **Evals:** EVAL-004, 009, 015, 022.

### 3.4 inject_03 — Unapproved vendor session

- **Trigger:** 137 unapproved sessions; 128 without confirmed MFA.
- **Product behavior:** Observe + recommend; `change_remote_access` tier 3 not autonomous; privacy minimize.
- **Evals:** EVAL-010.

### 3.5 inject_04 — Safety bypass aging

- **Trigger:** BYPASSED barriers with `bypass_authorized=NO`; proof test gaps.
- **Product behavior:** Bypass visible; no `bypass_interlock` tool; aging KPI not invented (OPEN-006).
- **Evals:** EVAL-011, 030.

### 3.6 inject_05 — Regional SCADA outage

- **Trigger:** 779 undocumented observed paths; recovery rows per plant.
- **Product behavior:** Bounded observe/recommend; no regional isolate-execute; abstain on missing joins.
- **Evals:** EVAL-012.

### 3.7 inject_06 — Restore failure drill

- **Trigger:** CURRENT backup but restore >180d / stale runbook / weak deps (97+ rows).
- **Product behavior:** RecoveryReady false; no live restore orchestration language as execute.
- **Evals:** EVAL-005, 013, 018.

### 3.8 cascade_001 — Cyber-physical ambiguity

- **Timeline:** 08:24 vendor session → 08:38 bypass → 08:47 SOC isolate → 08:50 PE destabilize warning.
- **Product behavior:** Draft/abstain; MIN_LOAD visible; handover email UNTRUSTED; scenario “37 controllers” marked SCENARIO not census.
- **Evals:** EVAL-007, 020, 021, 023, 027.

### 3.9 AI-outage fallback

- **Trigger:** `AI_ENABLED=0` or model timeout/unavailable.
- **Product behavior:** Render deterministic tables (identity conflicts, telemetry quality, recovery, authority); empty explainer fields marked UNKNOWN — **not** blank screen (EVAL-016).
- **Implementation:** `agent.manual_fallback_tables()`, engine GETs.

---

## 4. Functional requirements (FR-###)

| ID | Requirement | Implemented | API / module |
|----|-------------|-------------|--------------|
| FR-001 | Identity reconciliation without CMDB winner | Yes | `core/identity.py`, `GET /assets/{id}/identity`, `/identity/conflicts` |
| FR-002 | Telemetry quality + dual-clock ordering | Yes | `core/telemetry.py`, `/telemetry/quality`, `/telemetry/timeline` |
| FR-003 | Contextual operational risk (not CVSS-only) | Yes | `core/risk.py`, `/risk/contextual` |
| FR-004 | Safety-bounded isolation assessment | Yes | `core/containment.py`, `/safety/conflicts` |
| FR-005 | RecoveryReady derived predicate | Yes | `core/recovery.py`, `/recovery/{site_or_unit}` |
| FR-006 | Evidence graph slice Q1–Q5, hop cap 8 | Yes | `core/graph_slice.py`, `/graph/slice` |
| FR-007 | Recommendation packet (docs/06 fields) | Partial | `containment.assess_isolation`, `POST /recommend` — no separate `packet.py` |
| FR-008 | Decision trace append-only | Yes | `core/traces.py`, `contracts/decision_trace.yaml` |
| FR-009 | AI-disabled fallback | Yes | `agent.manual_fallback_tables()`, EVAL-016 |
| FR-010 | Eval harness EVAL-001…031 | Yes | `evals/harness.py`, `POST /eval/run` |
| FR-011 | Provenance on facts | Partial | Embedded per engine; no standalone `provenance.py` |
| FR-012 | ACTION_TIERS + bounded agent | Yes | `core/policy.py`, `authority.py`, `agent.py`, `guardrails.py` |
| FR-013 | Gold read-only API surface | Yes | `api.py` |

**Gap (OPEN-030):** TRACEABILITY.csv lists `src/ot_command/modern/*`; implementation is in `src/ot_command/core/*`.

---

## 5. Semantic / identity / provenance requirements

- **Five states separate:** RegisteredState, ObservedState, operational interpretation, safety state, decision authority — never collapsed to single `status`.
- **Identity bundle:** aliases[], sources[], confidence, conflicts[], `cmdb_winner=false`, shadow overlay low confidence.
- **Provenance envelope:** `source_path`, record id, freshness, claim type on evidence rows (FR-021).
- **Anticorruption:** v1 `operationalState` side-field only (ADR-10, OPEN-009).
- **Ban:** Device grain (OPEN-025); ProcessHealthy metric (OPEN-026); CMDB-as-winner; silent alias merge.

---

## 6. Hybrid retrieval and runtime context

Per ADR-06 / SDD-10 §6:

| Channel | Use in product | Constraints |
|---------|----------------|-------------|
| **STRUCTURED** | CSV/JSONL engines (primary) | plant_id, purpose filter |
| **GRAPH** | Q1–Q5 via `/graph/slice` | hop ≤ 8; missing joins explicit |
| **VECTOR** | Optional; off in workshop | Untrusted notes only; never sets isolation |
| **POLICY** | ACTION_TIERS pin in envelope | Retrieved prose ≠ policy |
| **MEMORY** | Decision traces JSONL | Audit only; not second CMDB |

Query plan: POLICY gate → STRUCTURED → GRAPH → optional VECTOR cite → MEMORY append.

---

## 7. AI / agent / tool requirements

- **Default:** `AI_ENABLED=0` (ADR-12). Model pin placeholder OPEN-028.
- **Agent:** Single Incident Analyst; 8 workflow states; max 12 steps / 20 tool calls.
- **Allowed tools:** get_identity, get_telemetry_quality, get_contextual_risk, get_safety_conflicts, get_recovery, get_authority_actions, simulate_isolation_consequence, draft_recommendation_packet, cite_untrusted_note.
- **Forbidden:** tier 3/4 execute tools; hidden CoT as authority.
- **Optional explainer:** Port only (ADR-13) — must not change rank/isolation/recovery predicates.

---

## 8. Deterministic policy and HITL

- Engines are **deterministic**; LLM is optional narration layer.
- `assess_isolation` returns MONITOR | ABSTAIN | DO_NOT_ISOLATE | ISOLATE_DRAFT | RECOMMEND_CONTAINMENT_REVIEW — never bare `ISOLATE` with execute.
- CRITICAL severity without CTQ-ISO packet → not authorizable (EVAL-019, EVAL-020).
- Injection prompts flagged; workflow still returns non-execute packet (EVAL-014, EVAL-027).

---

## 9. Decision trace / audit / feedback

- **Trace schema:** `contracts/decision_trace.yaml`
- **Storage:** `data/local/decision_traces.jsonl` (append-only, gitignored)
- **Fields:** decision_id, actor, purpose, plant_id, tool_trace, recommendation, execute=false, tokens, latency_ms, policy_gate, ai_enabled
- **Feedback:** Eval harness + human override logs (future APP) — **feedback ≠ auto-truth** (ADR-08). Contradictions in data preserved.

---

## 10. Safety / security / TEVV

| Area | Requirement | Verification |
|------|-------------|--------------|
| CTQ-0 | Zero OT execute in software | SLO-OT, tests/red_team |
| CTQ-ISO | Drafts need safe_state + roles when ISOLATE_DRAFT | EVAL-003, 020 |
| CTQ-REC | RecoveryReady ≠ backup CURRENT | EVAL-005, 018 |
| CTQ-CVSS | Context beats CVSS alone | EVAL-002, 017 |
| TEVV | 31 golden + adversarial cases | `make eval`, ASSURANCE_REPORT |
| OWASP / abuse | A-01…A-10 | `tests/red_team` |
| Supply chain | SBOM freeze outline | `assurance/SBOM_FREEZE.md` |

Trip suppression, SIS modify, interlock bypass: **out of scope / tier 4 refuse** (docs/06).

---

## 11. Non-functional requirements

| NFR | Requirement | Target / status |
|-----|-------------|-----------------|
| NFR-SAFE | No OT write routes | CTQ-0; CI enforced |
| NFR-SEC | Authn for production | OPEN-029 — not in workshop API |
| NFR-LAT | Packet assembly p95 | < 8000 ms workshop SLO — **baseline pending** (OPEN-006) |
| NFR-AUD | Trace completeness | Every `/recommend` appends trace |
| NFR-DEG | AI-disabled usable | EVAL-016 pass |
| NFR-CAP | Graph hop cap | 8; no whole-estate dump |

---

## 12. UI screens (mandatory)

No UI shipped in Repo 3.0 — **APP-01/02 build from this list.**

| # | Screen | Primary API / data | Personas |
|---|--------|-------------------|----------|
| 1 | **Risk & Resilience Control Tower** | `/diagnostics`, KPI tiles | All |
| 2 | **Asset Identity Reconciliation** | `/assets/{id}/identity`, `/identity/conflicts` | SOC, FDE |
| 3 | **Telemetry Quality & Timeline** | `/telemetry/quality`, `/telemetry/timeline` | SOC, PE |
| 4 | **Process / Dependency Graph** | `/graph/slice?query=Q2`, process_dependencies.csv | PE, Safety |
| 5 | **Contextual Risk Workbench** | `/risk/contextual` | SOC |
| 6 | **Safety vs Security Conflict Board** | `/safety/conflicts`, Q3 slice | Safety, SOC |
| 7 | **Remote Access & Vendor Sessions** | diagnostics + remote_access_sessions.csv | SOC |
| 8 | **Recovery / Restore-Test Graph** | `/recovery/{plant}`, Q4 slice | VP Ops, PE |
| 9 | **Incident Context Graph** | `/graph/slice?query=Q5`, cascade timeline | All |
| 10 | **Hybrid Retrieval Evidence panel** | evidence[] on packets + untrusted note cite | SOC |
| 11 | **Authority Gate / Recommendation** | `/recommend`, `/authority/actions` — **no execute button** | SOC, Safety, VP Ops |
| 12 | **Decision Trace / Audit** | traces JSONL + `/ops/slo` | FDE, audit |
| 13 | **Inject / Failure Simulation** | inject fixtures + `POST /eval/run` | FDE, QA |
| 14 | **KPI before/after** | docs/05 baseline vs measured diagnostics | Executive, FDE |
| 15 | **Executive brief** | Aggregated CTQs, residual OPEN-RISK | Executive |

**UX principles:** Five truths visible; uncertainty explicit; SOC 08:47 vs PE 08:50 side-by-side; no chatbot-first; AI-off shows same tables without narrative.

---

## 13. Golden-case mapping

| Eval | Screen(s) | Workflow |
|------|-----------|----------|
| EVAL-001…006 | 2, 5, 6, 11 | Golden core |
| EVAL-007 | 9, 11 | cascade_001 |
| EVAL-008 | 2 | inject_01 |
| EVAL-009 | 3 | inject_02 |
| EVAL-010 | 7, 11 | inject_03 |
| EVAL-011 | 6 | inject_04 |
| EVAL-012 | 4, 8 | inject_05 |
| EVAL-013 | 8 | inject_06 |
| EVAL-014…031 | 11, 13 | adversarial, edge, outage |

Full matrix: `evals/golden_cases.jsonl`, `evals/scenarios.md`.

---

## 14. Workshop vs production

| Aspect | Workshop (this repo) | Production fork (requires OPEN decisions) |
|--------|---------------------|-------------------------------------------|
| Data | Synthetic CSV/JSONL; contradictions kept | Real connectors; retention policy OPEN |
| API auth | None (OPEN-029) | IAM/PAM integration |
| AI | Off default; no model pin | OPEN-028 provider + eval gate |
| Authorizer | Role names only (OPEN-001) | Named humans + audit record |
| Deploy | Local / Docker synthetic | DMZ, REL-01…04 |
| Legal | LICENSE.txt training only | OPEN-002, OPEN-003, OPEN-024 |

---

## 15. Given / When / Then acceptance (representative)

**AC-001 Identity collision (EVAL-001)**  
Given alias `PLT-01-DCS_CONTROLLER-105` maps to OT-00012 and OT-00033  
When analyst opens Identity Reconciliation  
Then both asset_ids appear with source PASSIVE, confidence < 1, merged=false, cmdb_winner=false.

**AC-002 Anti-CVSS rank (EVAL-002)**  
Given VUL-00706 (cvss 9.8, unreachable, LOW) and VUL-00098 (8.7, reachable, CRITICAL context)  
When contextual rank runs  
Then VUL-00098 ranks first.

**AC-003 No execute isolation (EVAL-003)**  
Given HIGH alert ALT-002783 on OT-01016 with UNKNOWN process_context  
When recommendation generated  
Then recommendation ∈ {DO_NOT_ISOLATE, ABSTAIN, ISOLATE_DRAFT} and execute=false.

**AC-004 AI-disabled (EVAL-016)**  
Given AI_ENABLED=0  
When analyst opens Control Tower  
Then identity, telemetry, recovery, authority tables render without LLM.

**AC-005 Forbidden UI (PRD-02 precursor)**  
Given any screen  
When user completes primary workflow  
Then no control labeled “Execute Isolation” or “Write PLC” calls a POST execute API.

**AC-006 CASCADE handoff (EVAL-007)**  
Given CASCADE-001 context  
When incident workflow completes  
Then bypass + MIN_LOAD + untrusted handover visible; execute=false.

Full acceptance set: `specs/REQUIREMENTS_TRACEABILITY.md` §Acceptance; PRD-02 will expand to APP_ACCEPTANCE_TESTS.md.

---

## 16. Traceability

See `specs/REQUIREMENTS_TRACEABILITY.md` for evidence → ADR → FR → component → test matrix.

Chain example:  
`data/raw/asset_aliases.csv` → ADR-01 → FR-001 → `core/identity.py` → `tests/test_identity.py`, EVAL-001.

---

## 17. KPI before/after and counter-metrics

From `docs/05_kpis_baseline.md` — **before = Repo 1.0 / legacy; after = modern engines.**

| KPI | Before (legacy / estate) | After (target direction) | Counter-metric |
|-----|--------------------------|--------------------------|----------------|
| Inventory disagreement rate | 200/2016 ACTIVE∧{OFFLINE,UNSEEN} | Visible, not merged | False merge rate |
| Alias collision count | 5 | Surfaced in UI | Silent dedup |
| Telemetry not-good rate | 4094/31224 | Flagged, not imputed | Control use of BAD |
| Contextualize MTT | BASELINE_PENDING (OPEN-006) | Logged latency_ms | Fast-but-wrong packet |
| Unsafe isolate recommendations | 860 legacy ISOLATE strings | 0 execute; drafts gated | Automation bias clicks |
| RecoveryReady false positives | legacy CURRENT→True | Predicate on restore/runbook/deps | Backup-flag-only ready |
| AI cost / incident | N/A (AI off) | tokens metered | Cost win via CVSS-only (EVAL-026) |
| Eval must_not violations | 3 legacy xfail | 0 on modern path | Harness skip |

Numeric improvement targets: **OPEN-006** — not signed in this PRD.

---

## 18. OPEN_DECISIONS and exclusions

### Open (blocks production claims)

| ID | Topic |
|----|-------|
| OPEN-001 | Named Authorizer |
| OPEN-002 | Legal / high-risk AI class |
| OPEN-003 | Production data reuse |
| OPEN-006 | KPI / latency / cost thresholds |
| OPEN-028 | LLM provider |
| OPEN-029 | API authentication |
| OPEN-030 | core/ vs modern/ traceability path |

### Residual risks (workshop accepted)

OPEN-RISK-01 (future write surface), OPEN-RISK-05 (human wrong authorize), OPEN-RISK-11 (UI isolate pressure).

### Exclusions

Live OT canary; trip suppression; decorative KG; cleaning data contradictions; certification IDs; restricted_answer_key.

---

## 19. User journeys (SDD-05)

### Journey A — SOC analyst (CASCADE)

1. Alert ALT-002783 HIGH SUPPRESSED → Control Tower shows plant PLT-10 elevated conflicts.
2. Open OT-01016 identity — UNSEEN vs ACTIVE, alias history.
3. Context graph Q5 — bypass PLT-10-SAFE-07, MIN_LOAD, vendor session analogue.
4. Contextual rank — VUL-00098 above blind CVSS winners.
5. Safety board — degraded barriers on unit.
6. Request recommendation — DO_NOT_ISOLATE or ABSTAIN; PE handover constraint shown.
7. Export packet for war-room — **no execute**.

### Journey B — Process engineer

1. Receives SOC draft referencing MIN_LOAD.
2. Opens Process / Dependency Graph — downstream safety unit U07.
3. Confirms abrupt isolation risk — dissent recorded (future APP override log).
4. Consults on safe-state — human authorize out of band (OPEN-001).

### Journey C — Safety owner

1. Reviews Safety vs Security Conflict Board — unauthorized bypass counts.
2. Verifies trip suppression not offered; soc_status SUPPRESSED ≠ SIS state.
3. Blocks authorizable flag until CTQ-ISO complete.

### Journey D — Executive

1. Executive brief — KPI tiles, 3 legacy xfail contrast, harness 31/31 status.
2. Residual OPEN-RISK acceptance table from assurance report.
3. No drill-down into execute controls (none exist).

---

## 20. AI-disabled / graceful degradation UX

| State | User sees | Must not see |
|-------|-----------|--------------|
| AI off (default) | Engine tables, ranks, packets, traces | Blank dashboard |
| Model timeout | Same as AI off + banner “explainer unavailable” | Hallucinated counts |
| Partial join | `unit_join_missing=true`, ABSTAIN | Imputed unit/safe_state |
| Low confidence | Numeric confidence < 1, UNKNOWN labels | confidence 1.0 on conflicts |

Implementation: `manual_fallback_tables()`; all gold GETs remain available.

---

## 21. Cost-per-successful-outcome and counter-metrics

**Successful outcome (workshop definition):** Governed packet delivered with correct contextual rank, no must_not violation, execute=false.

| Metric | Source | Notes |
|--------|--------|-------|
| Tokens / incident | `decision_traces.jsonl` | 0 when AI off |
| Latency / incident | trace `latency_ms` | EVAL-025 logs state timings |
| Cost estimate | `GET /ops/cost-per-incident` | Dollar unit cost OPEN-006 |
| **Counter:** CVSS-only shortcut | EVAL-026 | Cheaper wrong rank invalidates savings |
| **Counter:** incomplete packet fast path | EVAL-025 | Speed with missing CTQ-ISO = fail |

FinOps dashboard design: `ops/finops_cost_dashboard.md`.

---

## 22. SLO / SLA / error budget (advisory service)

From `specs/14_delivery_spec.md` — workshop SLOs:

| SLO | Target | Error budget | Measurement |
|-----|--------|--------------|-------------|
| SLO-OT | 0 OT execute | 0 | traces, red team |
| SLO-CTQ0 | 0 write routes | 0 | test_api_readonly |
| SLO-ISO | 100% ISOLATE_DRAFT have safe_state+role | 0 | containment + EVAL-020 |
| SLO-EVAL | 100% must_not pass | 0 | `make eval` |
| SLO-LAT | p95 < 8s (joins complete) | TBD | `GET /ops/slo` — **OPEN-006** |

Plant-level MTTR/MTT contextualize SLA: **not set** (OPEN-006/022).

---

## Appendix A — API inventory (build contract)

| Method | Path | Purpose |
|--------|------|---------|
| GET | /health | Liveness |
| GET | /diagnostics | Estate counters |
| GET | /assets/{id}/identity | FR-001 |
| GET | /identity/conflicts | FR-001 summary |
| GET | /telemetry/quality | FR-002 |
| GET | /telemetry/timeline | FR-002 |
| GET | /risk/contextual | FR-003 |
| GET | /safety/conflicts | FR-004 |
| GET | /recovery/{site_or_unit} | FR-005 |
| GET | /graph/slice | FR-006 |
| GET | /authority/actions | FR-012 |
| GET | /ops/slo | ENH-10 |
| GET | /ops/cost-per-incident | ENH-10 |
| POST | /recommend | FR-007/012 workflow |
| POST | /eval/run | FR-010 local harness |
| GET | /agent/workflow/demo | Demo envelope |

**Forbidden:** POST isolate, POST firewall, POST PLC, POST SIS.

---

## Appendix B — Document history

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-16 | PRD-01 initial freeze from Repo 3.0 |

**Next:** PRD-02 (`specs/APP_ACCEPTANCE_TESTS.md`), APP-01 (API/OpenAPI completeness), APP-02 (operator UI).
