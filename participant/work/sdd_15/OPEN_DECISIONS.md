# OPEN_DECISIONS (append-only)

This file is **append-only**. Later prompts add dated sections. Do not rewrite or delete prior IDs.

UNKNOWN permission is not permission. Missing named authority, threshold, ADR, or legal class stays OPEN.

---

## SDD-01 | OM-1 | 2026-09-15

**Evidence used:** `src/ot_command/core/policy.py`; `docs/06_security_safety_assurance.md`; `docs/05_kpis_baseline.md`; `data/shadow/risk_acceptance_tracker.csv` (180 rows); `contracts/*`; `src/ot_command/__init__.py`; `pyproject.toml`; `data/ot_legacy.db`; `evals/golden_cases.jsonl`; `scenarios/cascade_001.json`.  
**Assumptions:** SDD-01 does not invent people, counsel opinions, or architecture.  
**Unknowns:** listed per ID.  
**Did not conclude:** any of the items below as closed.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-001 | Named human authorities for sponsor, Safety/SIS owner, SOC manager, VP Ops, FDE lead, and every ACTION_TIERS ≥ 3 action | No person names in `policy.py`, `docs/06`, or data. CASCADE-001 has SOC vs process engineer as **roles** only. | Cannot execute consequential recommendations; cannot close HITL RACI as people | Global OT Risk Sponsor (unnamed) |
| OPEN-002 | EU AI Act classification and ISO/IEC 42001 certification status | Methods apply; **no counsel sign-off** and no certificate in repo. Working assumption only: advisory HITL industrial decision support, prohibited from actuation. | Regulatory claims in exec materials | OT-CISO + counsel (not in repo) |
| OPEN-003 | Production (non-workshop) permissible use of each `data/` source | `README.md` permits synthetic local analysis. No plant-operator license for real OT reuse. Operational-truth permission = UNKNOWN for all tables in CHARTER §7. | Any live-plant deployment (out of this repo anyway) | OT-CISO |
| OPEN-004 | Complete ACTION_TIERS vs `docs/06` verb set | Code keys: observe/correlate/summarize/recommend/request_fresh_telemetry/open_ticket/increase_logging/isolate_endpoint/change_remote_access/change_firewall/write_plc_logic/change_setpoint/modify_sis/bypass_interlock. Docs also: enrich, rank evidence, read-only simulation, capture evidence, maintenance-mode. Unknown action defaults to tier 4. | Policy completeness; evals of “permissible autonomous action” (EVAL-006) | FDE + OT-CISO |
| OPEN-005 | Authority when `risk_acceptance_tracker.risk_owner = Unknown` | 41 / 180 rows; e.g. `PLT-15,OT-01094` is Engineering but `PLT-15,OT-00904,Unknown,ACCEPT`. UNKNOWN is not permission. | Risk-acceptance workflow | OT-CISO |
| OPEN-006 | KPI formulas and baselines for unmeasured `docs/05` clocks/cost | BASELINE_PENDING: MTT contextualize; alerts per actionable incident; safety-bypass **aging**; vuln-to-process coverage; restore-test freshness as a KPI; time-to-confidence; time-to-safe-containment; degraded-operation duration; false-positive escalation; decision-evidence completeness; approval latency; AI cost per incident. | SDD-04 baseline dataset completeness | FDE + VP Ops |
| OPEN-007 | Lineage of `data/ot_legacy.db` vs CSV | 6 tables; row counts match CSV; `run_diagnostics()` does not read DB; integrity ok. Independent vs derived = unknown. | SDD-07 lineage | FDE |
| OPEN-008 | Who may authorize isolation in CASCADE-001 / Unit 04 | Handover: “Do not isolate the controller without process engineering review.” SOC recommends isolation at 08:47. No named approver. Software must not execute isolate. | Isolation **execute** remains forbidden; even draft authority is unnamed | VP Ops + Process Eng + Safety (unnamed) |
| OPEN-009 | Canonical telemetry/asset contract | v1 vs v2 field/path split; telemetry schema omits `ingest_time`/`source`/`asset_id` present on `TEL-00000000`. FastAPI implements neither asset API. | SDD-10 contracts; identity API | FDE (no silent pick in SDD-01) |
| OPEN-010 | Canonical package `__version__` | `0.1.0` in `src/ot_command/__init__.py` vs `2.0.0` in `pyproject.toml` / API / manifest. `docs/07` says normalized. | Packaging identity | FDE (do not “clean” in SDD-01) |
| OPEN-011 | `specs/01_mandate.md` at repo root | OM map says SDD-01 produces `specs/01_mandate.md`; capstone SDD-15 **distills** it from this charter. Root spec deferred. | SDD-15 gate | FDE |

**SDD-01 closure rule:** none of OPEN-001…011 is treated as approved permission, threshold, ADR, or architecture.

---

## SDD-02 | OM-2 | 2026-09-15

**Evidence used:** `data/raw/enterprise_events.jsonl` (6500); `data/raw/cyber_alerts.csv` (2800); `data/raw/work_orders.csv` (1250); `data/shadow/shift_handover_email.txt`; `data/shadow/ot_asset_inventory_FINAL_v8.csv` (220); `src/ot_command/legacy/risk.py`; `src/ot_command/api.py`; `docs/03_current_state_architecture.md`.  
**Assumptions:** SDD-01 OPEN items remain open; process mining describes files, not live shifts.  
**Unknowns:** listed per new ID.  
**Did not conclude:** system of record; future architecture; isolation authority.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-012 | Durable case / correlation key for alert → WO → session → barrier → recovery | `correlation_id` empty on **3251 / 6500** enterprise events; max non-empty reuse is 6; no foreign key from `cyber_alerts` to `work_orders` | End-to-end process cycle time; agent “incident object” | FDE + SOC mgr |
| OPEN-013 | Semantic contract for `enterprise_events.event_type` vs `source` | HISTORIAN emits SESSION 122 and WORK_ORDER 88; IAM emits ALARM 109; CMMS is only 118/901 WORK_ORDER events | Enterprise integration design (SDD-10) | FDE |
| OPEN-014 | Work-order clock vs status semantics | 133 CLOSED with empty `closed_at`; 489 not-CLOSED with `closed_at` set; `WO-000018` CLOSED + field ACTIVE + bypass YES + notes awaiting vendor | Maintenance value-stream Measure | Maint/CMMS owner |
| OPEN-015 | Whether shadow spreadsheet is actually newer than CMDB | Handover email claims newer gateway inventory; `ot_asset_inventory_FINAL_v8.csv` vs `assets.csv`: **0** firmware diffs and **0** state-pair diffs on 220 overlapping IDs | Identity reconciliation (SDD-03 L4) | FDE; do not pick a winner |
| OPEN-016 | `docs/03` Purdue-like boxes vs enforceable zones | `zone` is a CSV label (DMZ 377); 779 undocumented observed edges; no firewall policy table | Trust-boundary engineering | OT-CISO |
| OPEN-017 | Meaning of SOC SUPPRESSED on HIGH/CRITICAL | 211 HIGH/CRIT `soc_status=SUPPRESSED` (e.g. `ALT-000040`); not an ACTION_TIERS action; not trip suppression in SIS | Alert-queue vs safety policy | SOC mgr + Safety/SIS |

SDD-01 IDs OPEN-001…011 are **not** closed by SDD-02. Isolation execute remains forbidden. No KG/ADR invented.

---

## SDD-03 | 96-cell forensics | 2026-09-15

**Evidence used:** `scripts/mine_forensics.py`; `matrix.csv` 96 cells; traces OT-00211 / OT-01016 / OT-00528; `tag_telemetry.jsonl` 31224; `safety_barriers.csv`; `recovery_readiness.csv`; `cascade_001.json`.  
**Assumptions:** Tag join is the only asset→unit path (182/2016).  
**Unknowns:** below.  
**Did not conclude:** identity winner; CVSS operational order; isolate; recovery-ready.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-018 | Which plant “Unit 04” in the night-shift handover refers to | `data/shadow/shift_handover_email.txt` has no `plant_id`; `process_units` has U04 on multiple plants; ALT-000425 hits PLT-08-U04 MIN_LOAD but that is **not** proven to be the email’s unit | Unsafe-isolation case binding | Process Eng + Ops |
| OPEN-019 | The CASCADE-001 “37 controllers / 6 unknown firmware” set | `scenarios/cascade_001.json` 08:07; `assets.csv` has no advisory-affected flag; do not invent the 37 IDs | Firmware-campaign identity | FDE + OT-CISO |
| OPEN-020 | Whether 182/2016 tagged assets is the full instrumented set | `tags.csv` unique asset_id=182; 1834 assets cannot be traced to a unit | Estate-wide process consequence | Process Eng |
| OPEN-021 | Which clock is event order: telemetry ingest (never inverted, p50 120s) vs enterprise received (407 inversions) | TEL ingest−event neg=0; EVT-0000001 received before event; handover 20-min historian vs HMI not located as a tagged incident | EVAL-004 implementation | FDE |

OPEN-001…017 remain open. SDD-03 does not close them. Isolation execute remains forbidden. No solution implemented.

---

## SDD-04 | OM-3 | 2026-09-15

**Evidence used:** `docs/05_kpis_baseline.md`; `VERIFICATION.md`; SDD-03 cells; SDD-02 W1–W11.  
**Assumptions:** Workshop CTQs in SCQA §7 are prompt-specified, not sponsor-signed.  
**Unknowns:** below.  
**Did not conclude:** architecture; legal class; dollar baseline.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-022 | Official formula and threshold for “stale configuration rate” | `docs/05` names the KPI; `assets.backup_age_days` p50=211 and >90d = 1581/2016 is a **proxy only**; 90 days is not in docs/05 | After-intervention configuration KPI | FDE + Maint/CMMS |
| OPEN-023 | Workshop CTQ numeric improve targets (disagreement 9.92%, dirty telemetry 13.11%) | SDD-04 sets **visibility and forbidden-path** CTQs only; rate reductions without hiding aliases are not sponsor-signed | 12-month KPI contracts | OT-CISO + VP Ops |

OPEN-001…021 remain open. OPEN-006 still covers clocks, actionable-incident definition, and AI cost (BASELINE_PENDING). No technology selected. Moonshot is not autonomous isolation.

---

## SDD-05 | OM-4 | 2026-09-15

**Evidence used:** SDD-04 SCQA; `docs/06`; `policy.py`; `LICENSE.txt`; `requirements.txt`; EVAL-001…006.  
**Assumptions:** Working class = industrial safety-related HITL decision support, no actuation.  
**Unknowns:** below.  
**Did not conclude:** certified EU AI Act class; production license opinion; AI control approval.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-002 | *(restated, not closed)* EU AI Act legal class and ISO/IEC 42001 certification | Working assumption recorded in USE_CASE.md §9; **no counsel sign-off** | Any customer-facing “high-risk system” claim | OT-CISO + counsel (not in repo) |
| OPEN-024 | Production licensing/IP/SBOM and real-person data lawful basis | `LICENSE.txt` is workshop-only; FastAPI/Pydantic/pytest licenses not recopied; `api.py` has no authn; real IAM/session data would be personal data | Production deploy (already out of this repo) | Legal + FDE |

**Qualification:** advisory use case **GO** with mandatory non-AI fallback. AI for consequential OT control remains **NO-GO**. OPEN-001 still blocks named-human execute.

---

## SDD-06 | OM-5 | 2026-09-16

**Evidence used:** `data/raw/assets.csv` (no `device` column); `data/telemetry/tag_telemetry.jsonl` (`quality` only); `docs/06`; `policy.py`; SDD-06 DOMAIN.md.  
**Assumptions:** Bounded contexts are language/ownership, not a datastore choice.  
**Unknowns:** below.  
**Did not conclude:** system of record; KG; ACTION_TIERS completion (still OPEN-004).

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-025 | Canonical grain for informal “device” | No `device` column in `assets.csv` or related raw files. Speech refers to physical boxes; data grain is `asset_id` + `asset_type`. | Any API or schema named Device | FDE + OT-CISO (inventory) |
| OPEN-026 | Canonical field for process “healthy” | No `healthy` column. `quality=GOOD`, `registered_state=ACTIVE`, and `safety_barriers.state=ACTIVE` are **not** interchangeable with process health. | Any health KPI or dashboard tile labeled “healthy” without a new named measure | VP Ops + Process Eng |

OPEN-001 (named Authorize), OPEN-004 (docs/06 verbs vs ACTION_TIERS), OPEN-009 (v1 `operationalState` vs v2 `observed_state`) remain open and still block collapsing those terms. Glossary in DOMAIN.md defines remaining overloaded speech (`status`, `critical`, `CURRENT`, `isolate`, `identity`, Recommend vs Authorize).

---

## SDD-07 | OM-6 | 2026-09-16

**Evidence used:** `data/manifest.json`; `repository.py`; `diagnostics.py`; `api.py`; `scripts/generate_data.py` (no sqlite write); sqlite vs CSV set-equality on 6 tables; `contracts/telemetry_event_schema.json`; shadow inventory vs assets field diffs = 0; `LICENSE.txt`.  
**Assumptions:** Workshop forensics allowed; operational-truth still UNKNOWN. Restore-test day threshold not chosen.  
**Unknowns:** below.  
**Did not conclude:** system of record; production access; RecoveryReady SLA days.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-007 | *(restated, not closed)* sqlite refresh / mastership vs CSV | Six tables **set-equal** to matching CSVs (profile 2026-09-16). `generate_data.py` does not write `data/ot_legacy.db`. `run_diagnostics()` does not read it. Content replica is observed; **ETL/refresh still undocumented**. Not a second master. | Treating DB as SoR or deleting it | FDE |
| OPEN-027 | Independent restore-test / backup-blob evidence | `recovery_readiness.csv` has `last_restore_test_days` only. No backup files, restore logs, or success/fail artifact. Cannot verify RecoveryReady without trusting the integer. | DR attestation; EVAL-005 beyond flag logic | VP Ops + FDE |

OPEN-003 (production reuse), OPEN-009 (contracts vs records), OPEN-012 (correlation_id), OPEN-015 (shadow vs CMDB), OPEN-020 (untagged assets), OPEN-022 / OPEN-006 (restore-test SLA days), OPEN-024 (session PII in production) remain open. Shadow spreadsheet is **not** a new CMDB. Shift email is **untrusted content**.

---

## SDD-08 | OM-7 | 2026-09-16

**Evidence used:** `evals/golden_cases.jsonl`; `tests/test_known_legacy_defects.py`; `scenarios/cascade_001.json`; inject_01…06 titles; `docs/06`; `policy.py`; SDD-03 traces; SDD-05 fallback.  
**Assumptions:** Cases are a failing-closed contract; harness not implemented. Inject bodies are titles only — fixtures bind to estate records.  
**Unknowns:** below.  
**Did not conclude:** legal class; named Authorizer; latency/cost SLAs; OPEN-RISK acceptance.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-006 | *(restated)* Latency and AI-cost acceptance numbers | `docs/05` BASELINE_PENDING; EVAL-025/026 specify meters only | Declaring a ms or $/incident pass bar | FDE + VP Ops |
| OPEN-RISK-01 | Accept residual that a later change adds a write surface | CTQ-0 holds on `api.py` today; eval cannot bind future PRs by itself | Continuous CTQ-0 in CI | FDE + OT-CISO |
| OPEN-RISK-05 | Accept that a complete packet can still be wrongly authorized | C47 automation bias; CASCADE 08:47 | Isolation **execute** remains out of software; human still fallible | Safety + VP Ops |
| OPEN-RISK-11 | Accept that advisory UI may increase isolate pressure vs paper war-room | EVAL-020 specifies no one-click; residual over-trust | Production UX | OT-CISO + Safety |

OPEN-001 still blocks named-human Authorize records. OPEN-002 still blocks any “high-risk system” claim. EVAL-001…006 stubs are expanded in `golden_cases_expanded.jsonl` but **not executed**.

---

## SDD-09 | OM-8 | 2026-09-16

**Evidence used:** SDD-03 collisions/CVSS/CURRENT/ISOLATE; SDD-05 B+C; SDD-08 EVAL map; `docs/04`; `requirements.txt` (no LLM/graph SDK).  
**Assumptions:** Workshop build = extend this repo. TCO is FDE-weeks / relative tokens, not a quote.  
**Unknowns:** below.  
**Did not conclude:** graph store engine (SDD-10); LLM vendor; digital twin.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-028 | LLM provider / local vs hosted | Selected solution requires a **port** and AI-disabled path (EVAL-016). No model in Repo 1.0. Hosted pick is not required to implement Option A engines. | Default-on explainer | FDE (do not pick in SDD-09) |

**Closed by this prompt (workshop, Proposed ADRs — not sponsor-signed production ADRs):** Option C unsafe agent **rejected**; autonomous isolation **NO**; multi-agent **not selected**; decorative KG **rejected**; bounded evidence-graph **view** **CONDITIONAL YES** (ADR-KG). OPEN-006 still covers token $/incident numbers.

---

## SDD-10 | OM-9 | 2026-09-16

**Evidence used:** SDD-06 terms; SDD-09 ADR-KG five queries; `contracts/asset_api_v1.yaml` / `v2.yaml`; `contracts/telemetry_event_schema.json`; `requirements.txt` (no graph DB).  
**Assumptions:** Workshop persistence = typed JSON views; root brownfield contracts stay.  
**Unknowns:** below.  
**Did not conclude:** production graph DB; OWL ontology; mapping of v1 `operationalState`.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-009 | *(restated, not closed)* v1 `operationalState` vs CSV/v2 states | Anticorruption parks v1 in `legacy_v1_operational_state` (ADR-10). Still no documented plant mapping. | Treating v1 as ObservedState | FDE |

**Closed in workshop (Proposed ADR-09):** persistence = typed JSON graph/JSONL, not RDF, not Neo4j-now. Vector remains optional untrusted memory and **must not** set isolation or ACTION_TIERS.

---

## SDD-11 | OM-10 | 2026-09-16

**Evidence used:** `api.py` two GETs; SDD-09/10; CASCADE-001; SDD-08 EVAL-016.  
**Assumptions:** LLM off until EVAL-016; workshop = local venv/Docker.  
**Unknowns:** OPEN-003 production DMZ; OPEN-006 p95 SLA; OPEN-028 provider; OPEN-001 people.  
**Did not conclude:** implemented routes; UI; model pick.

No new OPEN id. **Proposed ADR-11** read-only API; **ADR-12** AI-disabled as the product core; **ADR-13** explainer port must not mutate ACTION_TIERS or isolation/recovery predicates.

---

## SDD-12 | OM-11 | 2026-09-16

**Evidence used:** `policy.py`; SDD-09 ADR-07; SDD-11; EVAL-006/014/020/023; CASCADE-001 08:47 as input.  
**Assumptions:** One Incident Analyst optional; engines always; tier 2 stubs recommend-only.  
**Unknowns:** OPEN-001 Authorize people; OPEN-004 verbs still absent from ACTION_TIERS (no extra tools invented).  
**Did not conclude:** implemented agent loop.

No new OPEN id. **Proposed ADR-14** autonomy pin to ACTION_TIERS. Multi-agent still **not selected**. `isolate_endpoint` execute is **not a tool**. AwaitAuthorization cannot close without a named human (OPEN-001) and still must not execute.

---

## SDD-13 | OM-12 | 2026-09-16

**Evidence used:** `api.py` (no authn); `requirements.txt` pins; `LICENSE.txt`; SDD-12 allowlist; OWASP LLM Top 10 2026; OWASP Agentic ASI 2026; docs/07 answer-key absent.  
**Assumptions:** Guardrails are code after the model (ADR-15). Model card is placeholder.  
**Unknowns:** below.  
**Did not conclude:** signed SBOM; counsel opinion; implemented authn.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-028 | *(restated)* Model/provider + model card | No weights in Repo 1.0; SECURITY.md card is placeholder | Default-on explainer | FDE |
| OPEN-024 | *(restated)* SPDX recopy / production SBOM + session PII | LICENSE.txt does not recopy FastAPI/Pydantic/pytest licenses | Production supply-chain pack | Legal + FDE |
| OPEN-029 | Authentication on FastAPI before non-localhost | `api.py` has no authn (ASI03 workshop gap) | Bind beyond loopback; plant-scoped IAM | FDE + OT-CISO |

**Proposed ADR-15:** guardrails deterministic, non-bypassable by prompts. **ADR-16:** SBOM/AIBOM + exit = AI-disabled engines. `restricted_answer_key/` must remain absent.

---

## SDD-14 | OM-13 | 2026-09-16

**Evidence used:** SDD-01…13; ADR-KG and ADR-01…16; SDD-08 EVAL-001…031; `policy.py`; `api.py`.  
**Assumptions:** ADR promotion is engagement-accepted for ENH, not a production CAB. Workshop SLOs are engineering targets, not a close of OPEN-006 plant MTT.  
**Unknowns:** OPEN-001…029 as listed in DELIVERY_SPEC §9 — **none closed by freeze**.  
**Did not conclude:** implemented engines; named Authorizer; legal class.

No new OPEN id. **ADR-KG and ADR-01…16 Accepted** for ENH. SDD-09 Option C / isolate-execute / multi-agent / decorative KG remain **rejected**. TRACEABILITY.csv is the C17 contract: untraced code is out of scope.

---

## SDD-15 | Repo 2.0 layout | 2026-09-16

**Evidence used:** playbook SDD-15; `FDE_96_TO_OM21_MAP.md`; SDD-01…14 worktree; `evals/golden_cases.jsonl` expanded to EVAL-001…031; `scripts/check_sdd_gates.py`; `src/ot_command/__init__.py` still `0.1.0`; `api.py` still two GETs.  
**Assumptions:** Distilled specs index long-form artifacts. `pending` coverage is not `missing`. Packaging version left as evidence.  
**Unknowns:** OPEN-001…010, 012…029, OPEN-RISK-01/05/11.  
**Did not conclude:** modern engines; LLM provider; named Authorizer.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-011 | Canonical root `specs/01_mandate.md` | **Closed this prompt:** `specs/01_mandate.md` exists (distilled from CHARTER.md). Prior SDD-01 row remains as history. | SDD-15 gate | FDE |
| OPEN-010 | *(restated, not closed)* Canonical package `__version__` | `__init__.py` left at `0.1.0` vs pyproject `2.0.0`. Optional packaging alignment was not taken. | Packaging identity | FDE |

No new OPEN id. ENH remediations queued. Isolation execute remains forbidden. `legacy_*` unchanged.

---

## ENH-01 | OM-14 | 2026-09-16

**Evidence used:** `specs/14_delivery_spec.md`; `specs/08_evals_risks.md`; `evals/golden_cases.jsonl` (31 cases); `tests/test_known_legacy_defects.py`; `traceability/TRACEABILITY.csv` (planned_code `modern/`); capstone ENH-01 (`ot_command.core.*`); `data/raw/asset_aliases.csv` (alias `PLT-01-DCS_CONTROLLER-105` → OT-00012 + OT-00033); diagnostics counters via VERIFICATION.md.  
**Assumptions:** Stubs raise `NotImplementedError` until ENH-02+; test helpers are not production code.  
**Unknowns:** OPEN-001…010, 012…029, OPEN-RISK-01/05/11 unchanged.  
**Did not conclude:** implemented engines; gold API routes; named Authorizer; legal class.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-030 | Canonical module path: `core.*` vs `modern/*` in TRACEABILITY.csv | Capstone ENH-01 tests target `src/ot_command/core/*.py`; TRACEABILITY.csv rows still say `src/ot_command/modern/*.py` (48 rows). Both are stubs/placeholders; no second ADR. | Coverage CSV path accuracy; as-built C4 labels | FDE |

No other new OPEN id. Legacy XFAIL preserved (3). New core tests fail closed on `NotImplementedError`. Isolation execute remains forbidden. `data/` not cleaned.

---

## ENH-02 | OM-14 | 2026-09-16

**Evidence used:** `specs/10_information_architecture.md`; `adrs/ADR-01-identity.md`; `data/raw/assets.csv` (n=2016); `data/raw/asset_aliases.csv` (5 collision aliases, e.g. `PLT-01-DCS_CONTROLLER-105` → OT-00012 + OT-00033); `data/shadow/ot_asset_inventory_FINAL_v8.csv` (n=220, 0 shadow-only ids); `data/reference/tags.csv` (182 tagged assets); diagnostics: alias_collisions=5, asset_state_conflicts=200; EVAL-001 golden fixture.  
**Assumptions:** Shadow overlay confidence=0.3; alias collision confidence=0.4 per SDD-11 snapshot SNAP-IDENTITY-001. v1 `operationalState` remains unmapped side-field (OPEN-009).  
**Unknowns:** OPEN-001…010, 012…029, OPEN-RISK-01/05/11, OPEN-030 unchanged.  
**Did not conclude:** risk/telemetry engines; named Authorizer; shadow spreadsheet promoted to CMDB.

No new OPEN id. `assets.csv` and shadow not rewritten. Gold route `/assets/{id}/identity` + `/identity/conflicts` added (read-only). Legacy XFAIL preserved. Risk engine still stubbed.

---

## ENH-03 | OM-14 | 2026-09-16

**Evidence used:** `data/telemetry/tag_telemetry.jsonl` (n=31224); `data/reference/tags.csv` (engineering_unit); ADR-02; EVAL-004 fixture (EVT-0000001 received before event); diagnostics-aligned counts: bad_or_uncertain=4094, duplicate_packets=120, unit_mismatches=47 (tags.csv join); ingest−event negative count=0 on tag telemetry.  
**Assumptions:** `order=event_time` only; received_time treated as ingest analogue for enterprise-style rows. GOOD ≠ ProcessHealthy (OPEN-026).  
**Unknowns:** OPEN-001…010, 012…029, OPEN-RISK-01/05/11, OPEN-030 unchanged.  
**Did not conclude:** risk/safety/recovery engines; enterprise_events.jsonl timeline API; imputing BAD→GOOD.

No new OPEN id. `tag_telemetry.jsonl` not rewritten. Legacy XFAIL preserved. Risk engine still stubbed.

---

## ENH-04 | OM-14 | 2026-09-16

**Evidence used:** `data/raw/vulnerabilities.csv` (n=1100); EVAL-002 fixtures VUL-00706 (cvss 9.8, reachable NO, asset OT-00654 LOW) vs VUL-00098 (cvss 8.7, reachable YES, OT-01016 HIGH, barrier BYPASSED); EVAL-017 A/B fixture; ADR-03; `legacy_rank` unchanged in `legacy/risk.py`.  
**Assumptions:** Weights are workshop-explainable, not OPEN-006 dollar thresholds. Asset enrichment when `criticality` omitted. CVSS weighted as input (×2), not sole sort key.  
**Unknowns:** OPEN-001…010, 012…029, OPEN-RISK-01/05/11, OPEN-030 unchanged.  
**Did not conclude:** safety/containment engine; full RecoveryReady predicate (ENH-06); LLM re-rank (forbidden).

No new OPEN id. `legacy_rank` XFAIL preserved. Gold GET `/risk/contextual` added (read-only).

---

## ENH-05 | OM-14 | 2026-09-16

**Evidence used:** EVAL-003 fixture OT-01016 / ALT-002783 / PLT-10-U06 MIN_LOAD / PLT-10-SAFE-07 BYPASSED bypass_authorized NO; EVAL-019 CRITICAL-only; EVAL-031 UNKNOWN process_context; ADR-04; `policy.py` isolate_endpoint tier 3; handover email constraint (untrusted); 860 legacy safety-blind isolations cited in ADR-04.  
**Assumptions:** `required_authority` lists roles only (OPEN-001 unnamed people). ISOLATE_DRAFT requires explicit `asset_id` + unit join safe_state. Alert-only queries abstain on UNKNOWN process_context.  
**Unknowns:** OPEN-001…010, 012…029, OPEN-RISK-01/05/11, OPEN-030 unchanged.  
**Did not conclude:** recovery engine; isolate execute; named Authorizer; trip suppression (forbidden).

No new OPEN id. `legacy_isolation_recommendation` XFAIL preserved. Gold GET `/safety/conflicts` added. `execute` always false.

---

## ENH-06 | OM-14 | 2026-09-16

**Evidence used:** `data/raw/recovery_readiness.csv` (144 rows / 18 plants); EVAL-005 PLT-01 IDENTITY (backup CURRENT, restore 360d, runbook STALE, manual_fallback LIMITED); EVAL-018 CURRENT-only; ADR-05 (113/119 CURRENT rows fail restore/runbook/deps); workshop restore-test threshold **180d** (not a close of OPEN-006/022 plant SLA).  
**Assumptions:** `recovery_ready` requires backup CURRENT + restore ≤180d + runbook CURRENT + dependency YES + manual_fallback YES. Missing fields ⇒ false.  
**Unknowns:** OPEN-001…010, 012…029, OPEN-RISK-01/05/11, OPEN-030 unchanged.  
**Did not conclude:** live restore orchestration; backup blob verification (OPEN-027); authority/agent engines.

No new OPEN id. `legacy_recovery_ready` XFAIL preserved. Gold GET `/recovery/{site_or_unit}` added. CSV not rewritten.

---

## ENH-07 | OM-14 | 2026-09-16

**Evidence used:** SDD-12 AGENTIC.md; EVAL-006/014/023; ADR-07/12/14; `policy.py` ACTION_TIERS; CASCADE-001 handoff constraint; playbook workflow display states (8); `config/prompts/incident_analyst_v1.md` registry.  
**Assumptions:** Single Incident Analyst agent; AI_ENABLED=0 default; POST `/recommend` returns packet only (no OT action); tool trace tier ≤1; prompt/model pins are placeholders (OPEN-028).  
**Unknowns:** OPEN-001 named Authorizer; OPEN-004 verb gaps; OPEN-028 model provider.  
**Did not conclude:** graph slice GET (later ENH); multi-agent; LLM explainer on by default.

No new OPEN id. Forbidden tools raise/deny. Workflow states emit timing_ms, evidence_count, confidence, tool_calls_used. Traces append to `data/local/decision_traces.jsonl`.

---

## ENH-08 | OM-14–15 | 2026-09-16

**Evidence used:** SDD-13 SECURITY.md A-01…A-10; `tests/red_team/test_redteam_agent.py` (14 cases); `evals/adversarial_cases.jsonl` (7 rows); `assurance/OWASP_MAPPING.md`; `assurance/SBOM_FREEZE.md`; guardrails caps steps=12 tools=20; verify_repo checks restricted_answer_key absent.  
**Assumptions:** Red team is local synthetic only — no OT protocol attacks. Workshop CI via Makefile + `.github/workflows/ci.yml`.  
**Unknowns:** OPEN-024 full SPDX; OPEN-029 API authn; OPEN-028 model card.  
**Did not conclude:** external pentest; certification; real OT connectors.

No new OPEN id. Attacks fail closed. `restricted_answer_key/` must remain absent. Legacy XFAIL preserved for A-07 contrast.

---

## ENH-09 | OM-15 | 2026-09-16

**Evidence used:** `evals/harness.py` executed 31/31 PASS; `tests/test_eval_golden.py`; `assurance/ASSURANCE_REPORT.md`; red-team 17/17; EVAL-007 CASCADE-001 latency ~132 ms / 0 tokens; guardrails extended for EVAL-014/030 patterns; `containment.is_packet_authorizable` (EVAL-020); `POST /eval/run` local only.  
**Assumptions:** Harness checks modern engines deterministically — not a production LLM eval. Latency/token numbers are workshop measurements; OPEN-006 thresholds still unset.  
**Unknowns:** OPEN-001…010, 012…029, OPEN-RISK-01/05/11, OPEN-030 unchanged.  
**Did not conclude:** external pentest; certification; graph slice GET (FR-006 still missing — pytest route test fails until implemented).

No new OPEN id. Golden harness **executed** (SDD-08 assumption “harness not implemented” superseded for Repo 2.0). Legacy XFAIL preserved. `GET /graph/slice` remains out of scope for ENH-09.

---

## ENH-10 | OM-16 | 2026-09-16

**Evidence used:** `specs/REPO_3_0_GATE.md`; `ops/*.md` pack; `specs/as_built_c4.md`; `core/ops.py` + `GET /ops/slo`, `/ops/cost-per-incident`; `core/graph_slice.py` + `GET /graph/slice`; `contracts/decision_trace.yaml`; enriched `traces.py` (tokens, latency_ms, policy_gate); `tests/test_ops_telemetry.py`; Dockerfile `AI_ENABLED=0` + HEALTHCHECK; `pyproject.toml` 3.0.0.  
**Assumptions:** Synthetic advisory service only. FinOps meters present; dollar thresholds remain OPEN-006. SLO-LAT p95 logged from traces — not a production SLA sign-off.  
**Unknowns:** OPEN-001…010, 012…029, OPEN-RISK-01/05/11, OPEN-030 unchanged.  
**Did not conclude:** live plant deploy; production auth (OPEN-029); LLM vendor (OPEN-028); customer UI (PRD-01).

No new OPEN id. Repo 3.0 gate declares **PRD + App ready**. Legacy XFAIL preserved. `data/` contradictions not cleaned. Decision traces gitignored at runtime path.
