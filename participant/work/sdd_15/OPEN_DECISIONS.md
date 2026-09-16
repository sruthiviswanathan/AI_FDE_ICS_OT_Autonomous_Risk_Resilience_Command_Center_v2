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
