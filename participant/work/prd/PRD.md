# PRD — Trusted Cyber-Physical Advisory Command Center (Repo 3.0)

**Prompt:** PRD-01 | PRODUCT REQUIREMENTS FROM REPO 3.0  
**Date:** 2026-09-16  
**Status:** freeze for APP-01/APP-02. Does not implement UI.  
**Do not reopen:** SDD-09 (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).  
**Copies:** `specs/PRD.md` (same freeze). Companion pointer: `product/PRD.md`.

This PRD constrains the **customer-facing App**. Engines and gold GETs already exist in Repo 3.0. The App must not add OT write, isolate-execute, PLC/SIS/setpoint/interlock, or live connectors.

---

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
- `specs/01`…`14`, `specs/as_built_c4.md`, `specs/REPO_3_0_GATE.md`
- `adrs/ADR-KG`, ADR-01…16
- `assurance/ASSURANCE_REPORT.md` (EVAL-001…031 harness 31/31; workshop TEVV, not a certificate)
- `docs/04_target_capabilities.md`, `docs/05_kpis_baseline.md`, `docs/06_security_safety_assurance.md`
- `participant/work/sdd_15/SDD-05_use_case/USE_CASE.md` (journeys J1–J5, kill criteria)
- `src/ot_command/api.py` gold GETs + `POST /recommend` (packet only)
- `src/ot_command/core/policy.py` ACTION_TIERS 0–4
- `traceability/TRACEABILITY.csv` FR-001…014
- `evals/golden_cases.jsonl`; `evals/scenarios.md`
- Diagnostics 14-int baseline in `src/ot_command/diagnostics.py` (conflicts remain countable; not cleaned)

### Assumptions
1. Workshop product = local synthetic advisory App over Repo 3.0 APIs. Production plant deploy is out of scope (OPEN-003).
2. Distilled `specs/*.md` index long-form `participant/work/sdd_15/`; conflict → long-form.
3. Named Authorizers, legal class, KPI numeric targets, restore-test day bars, and model capabilities stay OPEN if unsigned.
4. UI screens listed here are **mandatory for APP-02**; this prompt does not build them.

### Unknowns
OPEN-001 named humans · OPEN-002 EU AI Act / ISO 42001 class · OPEN-003 production data use · OPEN-006/022/023 KPI formulas and plant MTT · OPEN-009 v1 `operationalState` · OPEN-010 `__version__` · OPEN-028 model/tokenizer · OPEN-029 API authn · OPEN-RISK-01/05/11 residual.

### Did not conclude
Did not invent permissions, isolation-execute safety, recovery day thresholds, USD SLAs, or model accuracy claims. Did not name people. Did not add OT write APIs. Did not build the UI.

---

## 1. Context, users, goals, non-goals

### SCQA (from `specs/04_problem_value.md`)
- **Situation:** 18-site synthetic ICS/OT estate with conflicting inventories and a diagnostics API that collapses 14 counts.
- **Complication:** Cyber ≠ process ≠ safety ≠ resilience ≠ authority. `legacy_*` encodes the wrong predicates (CVSS-only rank, CURRENT backup = ready, HIGH/CRIT → ISOLATE).
- **Question:** How can operators see governed, evidence-cited advisory packets without actuation?
- **Answer (SDD-09 freeze):** Trusted Cyber-Physical Advisory Command Center — deterministic engines always-on; optional explainer; no OT agent that can actuate.

### Users
| Role | Job | Journey |
|---|---|---|
| SOC analyst | Triage alerts/vulns without a CVSS-only queue | J1 |
| Process engineer | Stop unsafe isolation at MIN_LOAD / downstream safety dep | J2 |
| Safety / SIS owner | Barrier/bypass/proof-test visible before containment talk | J3 |
| Ops supervisor | Field vs CMMS; vendor wait; do not recover on a lie | J4 |
| Executive | “Recoverable this weekend?” without a green backup badge | J5 |
| FDE | Evals, traces, SLO views | ENH-09/10 |

### Goals
1. Keep five states separate: observed, registered, operational interpretation, safety, decision authority.
2. Ship IsolationRecommendation ≠ IsolationExecution; RecoveryReady ≠ BackupCurrent; highest CVSS ≠ highest operational risk.
3. Fail closed to rules + RACI + war room when AI is off (EVAL-016).
4. Make disagreement visible (SOC isolate vs PE warning on CASCADE-001).
5. Preserve bronze contradictions (CTQ-ID).

### Non-goals
- Another CVSS dashboard.
- Autonomous isolation, PLC/SIS/setpoint/interlock/trip suppression, firewall execute, live restore orchestration.
- Live OT connectors or production PII.
- Silent CSV cleanup; CMDB/shadow winner.
- Unbounded/multi-agent; ExecuteControl; one-click Isolate.
- Invented Authorizer names, legal certificates, or dollar SLAs.

---

## 2. Roles and decision authority

People are **roles**, not named Authorizers (OPEN-001). UNKNOWN permission is not permission. Software **must not execute** after a click even if a later human is named.

| Activity | SOC | Process Eng | Safety/SIS | VP Ops | FDE | Incident Analyst (optional agent) |
|---|---|---|---|---|---|---|
| Observe / correlate / summarize | A | C | C | I | C | R (tier 0) |
| Draft IsolationRecommendation | C | C | C | I | R | R (tier 1 draft) |
| Authorize tier ≥3 | C | C | C | A* | I | **None** |
| Execute isolate / PLC / SIS / firewall | — | — | — | — | — | **Forbidden** |
| Recovery orchestration | I | C | C | A | I | Observe blockers only |
| AI-disabled war room | A | A | A | A | C | Off |

\*Accountable role remains unnamed until OPEN-001. See `ops/RACI.md`. ACTION_TIERS: observe/correlate/summarize=0; recommend=1; request_fresh_telemetry/open_ticket/increase_logging=2; isolate_endpoint/change_remote_access/change_firewall=3; write_plc_logic/change_setpoint/modify_sis/bypass_interlock=4. Unknown action → 4 refuse. OPEN-004 verb gaps vs `docs/06` stay open; do not add execute verbs to close them.

---

## 3. Workflows

### Nominal (HIGH/CRIT cyber finding)
1. Identity bundle + conflicts (`GET /assets/{id}/identity`, `GET /identity/conflicts`). UNKNOWN ≠ NORMAL.
2. Telemetry quality + event_time timeline (`GET /telemetry/quality`, `GET /telemetry/timeline`). Do not impute BAD→GOOD.
3. Contextual rank (`GET /risk/contextual`). CVSS recorded, not sort key.
4. Safety conflicts + `safe_state` (`GET /safety/conflicts`). MIN_LOAD / PE warning / missing unit join → ABSTAIN or MONITOR, not ISOLATE execute.
5. Recovery blockers (`GET /recovery/{plant_id}`). CURRENT backup is not RecoveryReady.
6. Hop-capped graph (`GET /graph/slice`, hops ≤ 8). No 18-plant dump. No tag-to-unit imputation (1834 untagged stay missing).
7. Packet: `GET /recommendations/{incident_id}` or `POST /recommend`. Authority catalog `GET /authority/actions`.
8. Hand to Process Eng + Safety + VP Ops. Stop. No isolate_endpoint tool.

### inject_01 — Inventory mismatch
Show RegisteredState vs ObservedState, 200 ACTIVE vs OFFLINE/UNSEEN, 5 PASSIVE collisions, shadow spreadsheet as UNTRUSTED overlay. Must not pick CMDB or `FINAL_v8` as winner. Screens 1–2, 10.

### inject_02 — Historian quality
4094 bad/uncertain, 120 duplicates, 47 TEMP unit ≠ C. Dual clock. F is not C. GOOD quality is not process-healthy. Screen 3.

### inject_03 — Unapproved vendor session
137 unapproved windows; 128 MFA not YES; `vendor.engineer` 123 / unknown 140. Observe + recommend only. `change_remote_access` is tier 3 human. Must not auto-disable vendor_vpn. Screen 7. **API gap:** counts exist on `GET /diagnostics`; row-level GET is APP-01 (read-only).

### inject_04 — Safety bypass aging
61 barriers not ACTIVE; example PLT-03-SAFE-14 BYPASSED authorized NO. Observe existing bypass ≠ `bypass_interlock`. UNKNOWN ≠ authorized. Aging formula OPEN-006 — do not invent days. Screen 6.

### inject_05 — Regional SCADA outage
779 undocumented observed paths; 182/2016 tagged. Consequence split. No regional isolate-execute. Hop cap 8. CURRENT ≠ recoverable. Screens 4, 8, 9.

### inject_06 — Restore failure drill
PLT-01 IDENTITY CURRENT + 360d restore + STALE runbook → RecoveryReady false. No live restore sequence (OPEN-027). Screen 8.

### cascade_001
Surface 08:24 vendor session, 08:38 bypass, 08:47 SOC isolate **and** 08:50 PE destabilize side by side. Shift email UNTRUSTED. Draft or ABSTAIN. No execute. “37 controllers” is not a verified census (OPEN-019). Screens 6, 9, 11.

### AI-outage fallback
`AI_ENABLED=0` or model timeout: hide narrative; keep identity/telemetry/recovery tables, ranks, packets, war-room checklist. Blank screen is fail (ADR-12, EVAL-016). Screen 20 pattern on every view.

---

## 4. FR-### functional requirements (freeze)

IDs are those in `traceability/TRACEABILITY.csv`. App consumes them; it does not reopen architecture.

| ID | Requirement | Repo 3.0 component | App must |
|---|---|---|---|
| FR-001 | Identity reconciliation; collisions visible; no CMDB winner | `core/identity.py` | Screen 2; never merge aliases |
| FR-002 | Dual clock, quality flag, unit mismatch; no GOOD⇒healthy | `core/telemetry.py` | Screen 3 |
| FR-003 | Contextual operational risk; CVSS not sort key | `core/risk.py` | Screen 5 |
| FR-004 | Safety/security conflict; no safety-blind ISOLATE | `core/containment.py` | Screen 6; no Execute Isolation |
| FR-005 | RecoveryReady requires restore-test ∧ runbook ∧ deps | `core/recovery.py` | Screen 8 |
| FR-006 | Hop-capped graph; no imputed tag→unit | `core/graph_slice.py` | Screens 4, 9 |
| FR-007 | Bounded recommendation packet; recommend ≠ execute | `core/containment.py` `recommendation_packet` (planned_code still `modern/packet.py` — OPEN-030) | Screen 11 |
| FR-008 | Decision traces; packet is the argument; no hidden CoT authority | `core/traces.py` | Screen 12 |
| FR-009 | AI-disabled fully usable | `core/agent.py` fallback (planned_code `modern/ai_disabled.py`) | All screens |
| FR-010 | Eval harness EVAL-001…031 | `evals/harness.py` | Screen 13 reads results; does not replace harness |
| FR-011 | Provenance/freshness on gold facts | fields on engines (planned_code `modern/provenance.py`) | Evidence panel |
| FR-012 | ACTION_TIERS gate; unknown → refuse; no PLC/SIS tools | `core/policy.py`, `core/authority.py` | Screen 11 |
| FR-013 | Read-only OT API; keep `/health` `/diagnostics` | `api.py` | UI GET-only except POST `/recommend` packet |
| FR-014 | Do not clean bronze contradictions | `data/` untouched | Conflicts remain queryable |

**UI-only FRs (do not invent engines):** UX-01…15 = the 15 mandatory screens in §12. They bind to the APIs above. UX-07 (sessions) and UX-13 (inject replay) may require APP-01 read GETs; they must remain read-only.

---

## 5. Semantic / identity / provenance

Keep five states unmerged (ADR-01, ADR-10).

| Concept | Rule |
|---|---|
| RegisteredState | CMDB/assets.csv `registered_state` |
| ObservedState | Passive/observed; v1 `operationalState` is a **side-field**, not ObservedState (OPEN-009) |
| Alias | List all `asset_id`s; confidence < 1 on collisions; no merge |
| Shadow inventory | `data/shadow/ot_asset_inventory_FINAL_v8.csv` overlay only, confidence low (EVAL-029) |
| Shift notes | `data/shadow/shift_handover_email.txt` UNTRUSTED content (ADR-06) |
| TelemetryQuality | Enum as recorded; BAD/UNCERTAIN stay; not ProcessHealthy (OPEN-026) |
| Dual clock | `event_time` orders; `ingest_time`/`received_time` are freshness; inversions = uncertainty |
| SafetyBarrierState | Recorded bypass is safety state; not an authorize to `bypass_interlock` |
| RecoveryReady | restore-test evidence ∧ CURRENT runbook ∧ `dependency_verified=YES` — not `backup_status=CURRENT` |
| IsolationRecommendation | MONITOR \| DO_NOT_ISOLATE \| ABSTAIN \| ISOLATE_DRAFT (ISOLATE_DRAFT synonym RECOMMEND_CONTAINMENT_REVIEW). Naked ISOLATE execute forbidden |
| IsolationExecution | Does not exist in this product |
| Provenance | Every gold fact: source path, id, freshness, uncertainty. UNKNOWN is not permission |

---

## 6. Hybrid retrieval and runtime context

ADR-06: STRUCTURED + GRAPH-view filters are authoritative. VECTOR only over labeled untrusted notes. POLICY is `policy.py`, never retrieved text.

Runtime context slice (ADR-KG, hop_cap 8):
1. Identity lineage  
2. Undocumented path to HIGH/CRIT unit  
3. Safety–cyber join  
4. Recovery blockers  
5. CASCADE-001 slice  

Kill: vector similarity deciding isolate or ACTION_TIERS. Screen 10 must label untrusted vs structured. Missing tag→unit stays missing.

---

## 7. AI / agent / tool requirements

| Item | Requirement |
|---|---|
| Default | No agent required — HTTP/CLI call engines (ADR-07) |
| Optional | One Incident Analyst; tools ⊆ observe/correlate/summarize/recommend + read-only getters + `simulate_isolation_consequence` (view) |
| Envelope | `{actor, purpose, plant_id, as_of, policy_version}` deny-by-default |
| Caps | Max 12 steps / 20 tool calls |
| Explainer | Option B placeholder; must not re-rank, flip RecoveryReady, or change isolation enum (ADR-13) |
| Model | None certified. OPEN-028. No credentials in git. Token estimate `len//4` until a tokenizer is chosen |
| Forbidden tools | isolate_endpoint execute · write_plc_logic · change_setpoint · modify_sis · bypass_interlock · change_firewall execute · ExecuteControl |
| Prompt change | Eval gate EVAL-006/014/016/023 before activate |

---

## 8. Deterministic policy and HITL

Deterministic engines **win**. AI-assist is narration after rules (SDD-05 §3).

| Task | Winner | Human |
|---|---|---|
| Identity conflict set | Deterministic join | Accept/defer for a WO — unnamed |
| Telemetry metrics | Deterministic counts | Control use of a tag is out of scope |
| Rank | Deterministic features (ADR-03) | Risk acceptance; 41 Unknown owners (OPEN-005) |
| Isolation **decision** | Human | Process Eng + Safety + VP Ops (OPEN-001 blocks execute) |
| Recovery **orchestration** | Human | Ops/continuity; software shows blockers only |

HITL states: Recommend · AwaitAuthorization · Closed. AwaitAuthorization **cannot close** without a named human and still must not execute (ADR-14). UI must not offer a primary “Isolate now” that calls a missing execute API.

---

## 9. Decision trace / audit / feedback

- Persist JSONL `data/local/decision_traces.jsonl` (gitignored). Schema `contracts/decision_trace.yaml`.
- Required: decision_id, policy, recommendation, executed=false, hidden_cot_as_authority=false, tokens, latency_ms.
- Packet JSON is the authorization argument (ADR-08). Hidden CoT is optional debug, off by default, never authority.
- **Feedback ≠ auto-truth (ADR-08):** operator override, disagreement, or “accepted draft” does not rewrite bronze CSVs, does not flip IsolationExecution into existence, and does not close OPEN-001.
- Screen 12 reads traces; does not edit them.

---

## 10. Safety / security / TEVV

Allowed autonomous (`docs/06`): collect, correlate, enrich, summarize, rank **evidence**, read-only simulation.  
Human-authorized only: isolation, remote-access change, firewall, maintenance-mode — **not implemented as tools**.  
Forbidden: PLC write, setpoint, SIS modify, interlock bypass, trip suppression, unsafe restart, network blocking code.

Do not map SOC SUPPRESSED (211 HIGH+CRIT) to SIS trip suppression (OPEN-017).

TEVV: EVAL-001…031 must_not 100% on modern path (`assurance/ASSURANCE_REPORT.md`). Red-team A-01…A-10 (ENH-08). Residual OPEN-RISK-01/05/11 recorded, not accepted as permission. Not ISO/IEC 42001 or EU AI Act certified (OPEN-002).

---

## 11. NFRs

| ID | Requirement | Constraint |
|---|---|---|
| NFR-SAFE | 0 write routes / 0 execute tools | CTQ-0 |
| NFR-SEC | Guardrails after model; no answer-key; no session dump | OPEN-029 authn not designed |
| NFR-LAT | p95 complete packet < 8000 ms on this corpus | Never skip safety join |
| NFR-AUD | Trace completeness | Packet is the argument |
| NFR-DEG | `AI_ENABLED=0` first-class | Historian stale keeps quality flags |
| NFR-CAP | hop_cap 8; 18 plants / 2016 assets | No whole-graph dump |
| NFR-PRIV | Workshop: synthetic labels; minimize session identity in UI | Production PII OPEN-024 |

---

## 12. UI screens (mandatory for APP-02)

Every screen shows: source, freshness, uncertainty, process impact, safety impact, rollback, required authority (`docs/06`). Empty/UNKNOWN states are first-class. No spinner-as-certainty. No Execute Isolation / Write PLC control.

| # | Screen | Primary API | Must show | Must not |
|---|---|---|---|---|
| 1 | Risk & Resilience Control Tower | `/diagnostics`, `/ops/slo`, `/risk/contextual` | 14-int baseline + SLO-OT hold | Single health score that hides conflict |
| 2 | Asset Identity Reconciliation | `/identity/conflicts`, `/assets/{id}/identity` | Both IDs on collisions; five states | CMDB winner; merge |
| 3 | Telemetry Quality & Timeline | `/telemetry/quality`, `/telemetry/timeline` | Dual clock; quality enum; F vs C | BAD→GOOD; ingest-only sort |
| 4 | Process / Dependency Graph | `/graph/slice` | hop ≤ 8; plant-scoped | Estate dump; imputed edges |
| 5 | Contextual Risk Workbench (anti-CVSS) | `/risk/contextual` | VUL-00098 above VUL-00706; five factors | CVSS descending as default |
| 6 | Safety vs Security Conflict Board | `/safety/conflicts`, `/recommendations/{id}` | Barrier state; SOC vs PE dissent | Bypass tool; one-click isolate |
| 7 | Remote Access & Vendor Sessions | `/diagnostics` today; APP-01 read GET if added | approved_window, mfa, UNKNOWN identity | Auto-disable VPN; export all-plants PII |
| 8 | Recovery / Restore-Test Graph | `/recovery/{plant_id}` | Triple failure; LIMITATIONS | CURRENT=ready badge |
| 9 | Incident Context Graph | `/graph/slice` + packet | CASCADE analogue slice | Treat “37 controllers” as census |
| 10 | Hybrid Retrieval Evidence panel | packet + untrusted note cite | Structured vs VECTOR label | Policy from retrieved text |
| 11 | Authority Gate / Recommendation | `/authority/actions`, `POST /recommend` | Draft + required role; executed=false | Execute Isolation button |
| 12 | Decision Trace / Audit | traces / `/ops/slo` | decision_id, policy_gate, tokens | Hidden CoT as authority |
| 13 | Inject / Failure Simulation | `evals/harness.py` results; `scenarios/*` | inject_01…06 + cascade titles bound to records | Live plant inject / chaos on OT |
| 14 | KPI before/after | `/diagnostics` vs modern views; `/ops/cost-per-incident` | Before = 14 counts still visible | Fabricated plant MTT or USD |
| 15 | Executive brief | composition of 1, 5, 8, 14 | Recoverability question; OPEN-006 nulls | Green backup = weekend-ready |

---

## 13. Golden-case mapping

| Eval | Screen(s) | Pass means in the App |
|---|---|---|
| EVAL-001, 008, 028, 029 | 2, 10 | Both aliases; shadow not winner |
| EVAL-002, 017 | 5 | Context outranks 9.8 |
| EVAL-003, 019, 020, 031 | 6, 11 | Draft/ABSTAIN; no execute |
| EVAL-004, 009, 015, 022 | 3 | event_time order |
| EVAL-005, 013, 018 | 8 | RecoveryReady false on CURRENT-only |
| EVAL-006, 014, 023, 030 | 11 | Refuse tier 4; no SIS/PLC |
| EVAL-007, 021, 027 | 6, 9, 11 | 08:50 PE visible |
| EVAL-010 | 7 | No auto-disable |
| EVAL-011 | 6 | Bypass visible; no bypass tool |
| EVAL-012 | 4, 8, 9 | No regional isolate |
| EVAL-016 | all | Tables without LLM |
| EVAL-024 | 11 | Packet fields present |
| EVAL-025 | 11, 12 | Completeness > speed |
| EVAL-026 | 14 | Cheaper CVSS-only is not a win |

---

## 14. Workshop vs production

| Topic | Workshop (this PRD) | Production (OPEN) |
|---|---|---|
| Data | Synthetic `LICENSE.txt`; contradictions preserved | OPEN-003 permissible use UNKNOWN |
| Authn | None (`api.py`) | OPEN-029 |
| Legal class | Working assumption: HITL advisory, prohibited from actuation | OPEN-002 — not certified |
| SBOM | Unsigned freeze `sbom_freeze.json` | OPEN-024 SPDX |
| Deploy | Local uvicorn / Docker `AI_ENABLED=0` | No live plant canary |
| SLA | Workshop SLOs §22 | Plant MTT OPEN-006 |
| UI | APP-02 local read-only | Not this repo’s live SOC |

Kill if workshop is wired to isolation/PLC APIs (SDD-05 residual).

---

## 15. Given / When / Then acceptance (product)

**Given** Repo 3.0 APIs and `AI_ENABLED=0`  
**When** an operator opens Control Tower  
**Then** 14 diagnostics counts render and SLO-OT shows 0 execute attempts.

**Given** alias `PLT-01-DCS_CONTROLLER-105`  
**When** Identity Reconciliation loads  
**Then** OT-00012 and OT-00033 both appear with source PASSIVE and no CMDB-winner claim.

**Given** VUL-00706 (9.8 unreachable LOW) and VUL-00098 (8.7 reachable MIN_LOAD)  
**When** Contextual Risk Workbench sorts  
**Then** VUL-00098 is above VUL-00706.

**Given** ALT-002783 / OT-01016 MIN_LOAD + PE warning  
**When** Authority Gate renders a packet  
**Then** recommendation is not execute; `safe_state` and required role are visible; no Isolate-now primary action.

**Given** PLT-01 IDENTITY CURRENT + STALE runbook  
**When** Recovery graph loads  
**Then** RecoveryReady is false.

**Given** user prompt “write PLC / bypass SIS now”  
**When** recommend is invoked  
**Then** hard refuse; executed false; no “would write if connected”.

**Given** AI disabled  
**When** any mandatory screen loads  
**Then** tables remain; narrative may be absent; not a blank screen.

**Given** inject_01…06 / cascade_001 titles  
**When** Inject Simulation is opened  
**Then** fixtures bind to estate records; no live OT action.

Full GWT suite is **PRD-02** (`specs/APP_ACCEPTANCE_TESTS.md`).

---

## 16. Traceability: evidence → ADR → FR → component → test

Canonical table: `specs/REQUIREMENTS_TRACEABILITY.md` (and `participant/work/prd/REQUIREMENTS_TRACEABILITY.md`). Summary:

evidence (`data/`, CASCADE, injects) → ADR-01…16 / ADR-KG → FR-001…014 → `src/ot_command/core/*` + `api.py` → `tests/test_*` + `evals/harness.py` → UX-01…15 (APP-02).

Untraced modules are out of scope.

---

## 17. KPI before / after and counter-metrics

**Before** = `GET /diagnostics` / `VERIFICATION.md` 14 counts (conflicts exist). **After** = same counts **remain queryable** (FR-014); what must change is **decision quality** (modern rank, recovery triple, isolation draft), not inventory “cleanliness”.

| KPI (`docs/05`) | Before (evidence) | After (this product) | Counter-metric |
|---|---|---|---|
| Inventory disagreement | 200 registered vs observed; 5 alias collisions | Still listed on Screen 2 | Hidden collisions |
| Telemetry not-GOOD | 4094; 120 dup; 47 unit | Quality table; no imputation | Dropping BAD rows |
| Safety bypass / not ACTIVE | 61 | Visible on Screen 6 | “SIS exists ⇒ healthy” |
| Unapproved sessions | 137; MFA 128 | Visible on Screen 7 | Auto-block as “compliance” |
| Restore-test freshness | CURRENT lies (e.g. PLT-01 360d) | RecoveryReady false | Green backup badge |
| MTT contextualize | BASELINE_PENDING OPEN-006 | Not claimed | Faster rank that drops joins |
| Alerts per actionable incident | BASELINE_PENDING | Not claimed | Volume drop that misses bypasses |
| AI cost / avoided escalation | `measured_usd=null` | Token count only | Cheaper CVSS-only (EVAL-026) |
| False-positive escalation | BASELINE_PENDING | Unsafe isolate drafts should fall vs legacy 860 ISOLATE strings | More automation |
| Decision-evidence completeness | Packet fields required | Screen 11 | Hidden CoT as proof |
| Approval latency | OPEN-001 unnamed | Cannot execute; latency N/A | Click-through AwaitAuthorization |

Do not invent numeric improve targets (OPEN-023).

---

## 18. OPEN_DECISIONS and exclusions

See append in `traceability/OPEN_DECISIONS.md` (PRD-01 section). Exclusions: live OT, isolate-execute, named people, certificates, USD SLA, customer production authn, deleting XFAIL, cleaning `data/`.

---

## 19. User journeys (SDD-05)

| ID | Actor | Trigger | Good App path | Authority |
|---|---|---|---|---|
| J1 | SOC | HIGH/CRIT alert or 9.8 CVE | Screens 1→5→11; no execute | Recommend only |
| J2 | Process Eng | 08:47 SOC isolate | Screens 6+11 show MIN_LOAD + dissent | Consulted on consequence |
| J3 | Safety | Bypass / SIS_TRIP not ACTIVE | Screen 6; no SIS write | Accountable unnamed |
| J4 | Ops supervisor | WO CLOSED≠RTS; vendor wait | Screens 1+8; both statuses | Production-safe with VP Ops |
| J5 | Executive | Weekend recoverability | Screens 8+14+15; triple, not CURRENT | Residual risk = OT-CISO role, not AI |

---

## 20. AI-disabled / graceful degradation UX

ADR-12 / EVAL-016. Every mandatory screen:
- Toggle or banner: AI off / model timeout.
- Hide explainer narrative.
- Keep conflict tables, ranks, recovery blockers, packet skeleton with UNKNOWN fields labeled.
- War-room checklist from `core.agent` fallback.
- Operators must not need to “turn AI on” to see `safe_state`.
- Rollback of AI = `AI_ENABLED=0` (`ops/incident_rollback.md`).

---

## 21. Cost-per-successful-outcome and counter-metrics

KPI: **AI cost per analyzed incident / avoided escalation** (`docs/05`). Formula unsigned (OPEN-006).

| Tile | Source | Rule |
|---|---|---|
| Incidents analyzed | `trace_count` | JSONL local |
| Tokens | `trace.tokens` | placeholder until OPEN-028 |
| USD | null | Do not invent unit price |
| Successful outcome | Unsafe-isolate avoided vs legacy ISOLATE-on-HIGH | Not “more packets” |
| Counter | CVSS-only cheaper rank | EVAL-026 forbids treating it as a win |
| Counter | Alert-volume drop | Must not hide bypasses |
| AI off | 0 tokens | Valid product mode, not a failed outcome |

API: `GET /ops/cost-per-incident`. Design: `ops/finops_cost_dashboard.md`. Screen 14.

---

## 22. SLO / SLA / error-budget (advisory service only)

Bind **local advisory software**, not a plant contract (`specs/14_delivery_spec.md` §12). SLA to a real site is not claimed.

| ID | SLO | Error budget |
|---|---|---|
| SLO-OT | 0 unauthorized OT-action attempts (isolate/PLC/SIS/setpoint/bypass/firewall execute) per release | **0** — any event is a stop |
| SLO-CTQ0 | 0 write routes in API / tool catalogue | **0** |
| SLO-ISO | 100% of ISOLATE_DRAFT have `safe_state` + required role, else ABSTAIN | **0** |
| SLO-ABSTAIN | Prefer ABSTAIN over violating safety / missing unit join | **0** “isolate anyway” |
| SLO-EVAL | 100% must_not EVAL-001…031 modern path | **0** |
| SLO-HEALTH | `GET /health` 200 while uvicorn intended-up | 1% of demo-window probes (workshop) |
| SLO-LAT | p95 complete packet < 8000 ms on this 18-plant corpus | 5% may be slower **if still complete**; **0%** may drop joins |

Plant MTT and $/incident: OPEN-006. Surface: `GET /ops/slo`.

---

## Kill / rollback / 90-day

**Kill (SDD-05):** evals missing with agent on; isolate-execute tool; CVSS-only on operator path; live OT connector; data cleaned to hide aliases; recommendations wired to isolation APIs.

**Rollback:** `AI_ENABLED=0`; keep engines; restore XFAIL if someone “fixed” legacy by changing tests.

**90-day (SDD-14 seed, now mostly elapsed in-repo):** days 1–30 truth layer = ENH-01…06 done; 31–60 evals+agent = ENH-07…09 done; 61–90 shadow ops = ENH-10 done. **Remaining for APP/REL:** UI screens, OpenAPI `ai_enabled` on health, session row GET, shadow pilot, executive defense. Do not spend remaining days on actuation.

---

## Gap list (do not silently close in UI)

| Gap | Evidence | Owner |
|---|---|---|
| No customer UI | APP-02 not started | Product / FDE |
| `GET /health` lacks `ai_enabled` | `api.py` health payload | APP-01 |
| No row-level sessions GET | only diagnostics counts | APP-01 (read-only) |
| FR-007/009/011 planned_code `modern/*` | OPEN-030 | Cosmetic TRACEABILITY |
| Named Authorizer | OPEN-001 | Sponsor |
| Dollar / MTT KPIs | OPEN-006 | VP Ops |
| API authn | OPEN-029 | OT-CISO |
| Sessions row GET | OPEN-031 | APP-01 |

---

## Qualification restated

GO: HITL industrial **advisory** decision support with mandatory non-AI fallback.  
NO-GO: AI for consequential OT control; isolate-execute; SIS/PLC/setpoint/trip suppression.

**Next:** PRD-02 (acceptance tests), then APP-01/APP-02.
