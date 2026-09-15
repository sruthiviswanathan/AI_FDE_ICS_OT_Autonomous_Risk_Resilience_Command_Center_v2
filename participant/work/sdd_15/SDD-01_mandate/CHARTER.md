# SDD-01 — Engagement charter, mandate, and field-evidence register

**Prompt:** SDD-01 | OM-1 Mandate and field immersion  
**Repo:** AI_FDE_ICS_OT_Autonomous_Risk_Resilience_Command_Center_v2 (Repo 1.0 brownfield)  
**Date:** 2026-09-15  
**FDE capabilities evidenced here (OM 1 homes only):** C01, C02, C46, C48, C50, C80, C81  
**Not this prompt:** L1–L12 × 8 forensic cells (SDD-03). No target architecture.

---

## Evidence used / assumptions / unknowns / what this artifact did not conclude

### Evidence used (file, field, count or id)

| Source | What was read | Quantified fact used |
|---|---|---|
| `data/manifest.json` | `counts`, `seed`, `files`, `notes`, `repo_version` | seed `20260910`; 18 plants; 2016 assets; 6048 aliases; 3780 edges; 216 units; 198 process deps; 864 tags; 31224 telemetry; 1100 vulns; 450 barriers; 1250 WOs; 700 remote sessions; 2800 alerts; 144 recovery; 6500 enterprise events; `repo_version` `2.0.0`; notes = synthetic + deliberate inconsistencies |
| `VERIFICATION.md` | Diagnostic evidence block | 200 / 5 / 779 / 120 / 4094 / 47 / 61 / 73 / 244 / 137 / 128 / 25 / 29 / 35; pytest 3 passed, 3 xfailed |
| `src/ot_command/diagnostics.py` | Heuristic keys | Same 14 keys; `UNKNOWN` treated as non-compliant in several sums |
| `data/raw/assets.csv` | `registered_state`, `observed_state`, `owner` | 2016 rows; 200 ACTIVE and observed in {OFFLINE,UNSEEN}; `owner=Unknown` 343/2016 |
| `data/raw/asset_aliases.csv` | `source` | 6048 rows; 2016 CMDB + 2016 PASSIVE + 2016 CMMS |
| `data/raw/network_edges.csv` | `documented`, `observed_last_24h`, `approved_path` | 3780 rows; undocumented and observed-24h = 779 (VERIFICATION) |
| `data/telemetry/tag_telemetry.jsonl` | keys vs contract | 31224 events; keys include `ingest_time`, `source`, `asset_id` |
| `contracts/telemetry_event_schema.json` | `required` / `properties` | required = event_id, tag_id, event_time, value, unit, quality; no ingest_time / source / asset_id |
| `contracts/asset_api_v1.yaml`, `contracts/asset_api_v2.yaml` | path + field comments | v1 `/assets/{id}` assetId/fwVersion/operationalState; v2 `/ot-assets/{asset_id}` asset_id/firmware/observed_state |
| `src/ot_command/core/policy.py` | `ACTION_TIERS`, `requires_human_approval` | tiers 0–4; unknown action defaults to 4; approval if tier >= 3 |
| `src/ot_command/legacy/risk.py` | `legacy_rank`, `legacy_recovery_ready`, `legacy_isolation_recommendation` | CVSS sort; backup flag; HIGH/CRITICAL to ISOLATE |
| `src/ot_command/api.py` | routes | `/health`, `/diagnostics` only; FastAPI version 2.0.0 |
| `src/ot_command/__init__.py` | `__version__` | `0.1.0` (conflicts with pyproject 2.0.0) |
| `pyproject.toml` | `[project].version` | `2.0.0` |
| `docs/01_domain_context.md` | estate + goal | 18 sites, five regions; goal is not automate control |
| `docs/05_kpis_baseline.md` | 18 named KPIs | catalogue only; no numeric targets in that file |
| `docs/06_security_safety_assurance.md` | allowed / restricted behavior | collect–simulate allowed; PLC/SIS/interlock/trip/unsafe restart out of scope |
| `docs/03_current_state_architecture.md` | landscape sketch | documented Purdue-like stack + parallel undocumented paths |
| `README.md` | safety | synthetic; no real equipment; API read-only |
| `AGENTS.md` | engagement rules | five states; no live OT writes; evals before agents; `restricted_answer_key/` out of bounds |
| `participant/CHALLENGE_BRIEF.md` | inherited program | leadership wants autonomous command center; no trusted cyber-physical truth |
| `analysis-artefacts/problem-explained/BUSINESS_PROBLEM_PAINPOINTS_SCOPE.md` | in/out scope | copied as scope boundary; counts match VERIFICATION.md |
| `data/shadow/shift_handover_email.txt` | Unit 04 notes | spreadsheet newer than CMDB; do not isolate without process engineering |
| `data/shadow/risk_acceptance_tracker.csv` | `risk_owner`, `decision` | 180 rows; owner Unknown 41; ACCEPT 71 / MITIGATE 58 / DEFER 51 |
| `data/shadow/ot_asset_inventory_FINAL_v8.csv` | identity overlay | 220 rows; all 220 `asset_id` also in `assets.csv` |
| `data/ot_legacy.db` | SQLite copy | 6 tables; row counts match CSV; PRAGMA integrity_check=ok |
| `data/reference/plants.csv` | region/type | 18 plants; regions APAC, EU, LATAM, MEA, NA; plant ids are `PLT-nn` |
| `evals/golden_cases.jsonl` | EVAL-001 to EVAL-006 | 6 stub cases; not executed by pytest |
| `scenarios/cascade_001.json` | CASCADE-001 | SOC isolation vs process-engineer warning; no named human approver |
| `tests/test_baseline.py`, `tests/test_known_legacy_defects.py` | pass vs xfail | 3 pass / 3 xfail (strict) |
| `analysis-artefacts/FDE_96_TO_OM21_MAP.md` | OM 1 capability homes | C01, C02, C46, C48, C50, C80, C81 |

`restricted_answer_key/` was not opened.

### Assumptions

1. This chat executes **SDD-01 / OM-1** after Phase 0 freeze. Artifacts stay under `participant/work/sdd_15/` until SDD-15 distills `specs/01_mandate.md`.
2. Workshop analysis of synthetic files is allowed by `README.md` + `data/manifest.json` notes. That is **not** permission to treat any named system as operational truth.
3. Role titles in this charter are **role-real, person-unnamed**. No human name in `src/`, `data/`, `docs/06`, or `policy.py` is an approver of record.
4. ISO/IEC 42001 / 42005 / EU AI Act are **methods**. No certification is claimed.
5. `VERIFICATION.md` counts are the before-intervention diagnostic snapshot unless a later prompt re-measures from the same files.

### Unknowns

1. Named sponsor, named Safety/SIS owner, named SOC manager, named FDE lead — **not in repo**.
2. Production (non-workshop) lawful basis, licensing, and plant-operator permission for each dataset.
3. EU AI Act legal class signed by counsel.
4. Whether `data/ot_legacy.db` is a derived copy or an independent registered store (schema matches CSV; lineage not documented).
5. KPI time metrics (contextualize, confidence, containment, approval latency, AI cost) — **no clocks in product code**.
6. Who may accept risk when `risk_acceptance_tracker.risk_owner = Unknown` (41/180).
7. `ACTION_TIERS` keys vs `docs/06` verbs (`enrich`, `rank evidence`, `capture evidence`, `maintenance-mode`) — incomplete map.

### What this artifact did not conclude

- Did not choose a winning inventory (CMDB vs PASSIVE vs CMMS vs shadow spreadsheet).
- Did not rank operational risk; did not use CVSS as a priority order.
- Did not declare recovery ready; did not treat `backup_status=CURRENT` as readiness.
- Did not design KG, RAG, digital twin, agents, or a target C4.
- Did not authorize isolation, remote-access change, firewall change, or any tier >= 3 action.
- Did not clean or rewrite `data/` contradictions.
- Did not implement product code.

**Gate self-check:** no source whose **operational-truth permission is UNKNOWN** is treated as permitted truth. No target architecture is specified below.

---

## 1. Engagement charter (C01 consulting judgement)

Leadership inherited a multinational ICS/OT risk program and asked for an **autonomous risk and resilience command center**. The estate already emits many dashboards. The FDE judgement is that the blocking problem is **no trusted cyber-physical truth**, not missing visualization.

**Client ask (stated):** global autonomous command center (`participant/CHALLENGE_BRIEF.md`; `docs/01_domain_context.md`).

**FDE mandate (this engagement):** trustworthy, safety-bounded, authority-aware **decision support** across 18 synthetic plants — collect, correlate, enrich, summarize, rank evidence, and run read-only simulation (`docs/06_security_safety_assurance.md`). Not plant control. Not another dashboard. Not unbounded agents.

**Estate grain (manifest, not a plant census of the real world):** 18 plants times 5 regions (`APAC, EU, LATAM, MEA, NA` in `data/reference/plants.csv`); 2016 assets; mixed PLC/DCS/SCADA/HMI/historian/SIS/CMMS/SOC/vendor access as **labels in files**, not as live connectors.

**Five states stay separate for the whole engagement:**

| State | Working definition in this repo | Example field / artifact |
|---|---|---|
| Observed | What a sensor, session, or edge saw | `assets.observed_state`; `network_edges.observed_last_24h`; telemetry `quality` |
| Registered | What an inventory/CMMS/API stored | `assets.registered_state`; `work_orders.cmms_status`; asset API v1 `operationalState` |
| Operational interpretation | What operations/shift/process context claims | `cyber_alerts.process_context`; `data/shadow/shift_handover_email.txt` |
| Safety | Barrier/SIS/proof-test/bypass recorded state | `safety_barriers.state`, `proof_test_status`, `bypass_authorized` |
| Decision authority | Who may act, at which ACTION_TIERS | `policy.py`; `docs/06`; `risk_acceptance_tracker.risk_owner` |

**Forensic tension (do not collapse):** cyber state is not operational state is not safety state is not resilience state (`README.md`).

**Hard bounds:** no live OT connection; no PLC writes; no setpoint changes; no SIS changes; no interlock bypass; no trip suppression; no unsafe isolation or restart (`docs/06`; `AGENTS.md`; `.cursor/rules/ot-fde.mdc`).

---

## 2. ISO/IEC 42001-style scope (C46, C50) — method, not a certificate

This section applies AIMS **scope language** to the synthetic workshop system. It is **not** an ISO/IEC 42001 certification, not an EU AI Act legal opinion, and not a production AIMS.

| Scope element | Statement | Evidence / limit |
|---|---|---|
| AI system (workshop) | Read-only FastAPI + CLI diagnostics + CSV/JSONL/SQLite corpus + stub evals | `src/ot_command/api.py` (2 GET routes); `cli.py` (`diagnostics` only) |
| Purpose | Advisory cyber-physical decision support: make disagreement visible; do not actuate | `docs/01_domain_context.md`; `docs/06` |
| Intended use class (working assumption) | Human-in-the-loop industrial **advisory** system; prohibited from control actuation | Working assumption → OPEN-002 |
| Operating environment now | Local synthetic workshop (`README.md`); seed `20260910` | Not a plant DCS |
| Operating environment later | Future real plant — **not in scope of this mandate** | OPEN-003 |
| Intended users | OT-CISO / Global OT Risk Sponsor, VP Operations, Site Process Engineering, Safety/SIS owner, SOC manager, Maintenance/CMMS, Vendor Access owner, FDE lead, plant operators (as affected users) | Titles proposed; **no named people** → OPEN-001 |
| In scope (AI/system behavior) | Collect, correlate, enrich, summarize, rank evidence, read-only simulation | `docs/06` |
| In scope (engagement work) | Brownfield forensics, contextual risk **design**, safety/security conflict handling **design**, recovery graph **design**, bounded-autonomy **model**, TEVV, KPI before/after, 90-day roadmap | BUSINESS_PROBLEM_PAINPOINTS_SCOPE.md §3; CHALLENGE_BRIEF.md |
| Out of scope (always) | Live OT; PLC logic write; setpoint; SIS modify; interlock bypass; trip suppression; unsafe restart; automatic isolation; network blocking code | `docs/06`; `README.md` |
| Out of scope (method) | Silent data cleanup; CVSS-only operational ranking; backup_status CURRENT implies recoverable; `restricted_answer_key/`; agents before evals; architecture chosen without SDD-09 | `AGENTS.md`; `00_SHARED_CONSTRAINTS.md` |
| Data boundary | Files under `data/`, `contracts/`, `src/`, `tests/`, `evals/`, `scenarios/` listed in §7 | Production reuse UNKNOWN |
| Oversight | Consequential actions (tier >= 3) require named human authority; none named yet | `policy.py`; OPEN-001 |
| Prohibited AI uses (this estate) | Autonomous isolation; control-loop AI; SIS/setpoint/interlock agents | `docs/06`; EVAL-003 / EVAL-006 stubs |

**Responsible AI context (C46):** recommendations must expose evidence, source, freshness, uncertainty, process impact, safety impact, rollback, required authority (`docs/06`). Automation-bias risk is in-scope as a harm: SOC may over-trust a CRITICAL / ISOLATE banner (`legacy_isolation_recommendation`; CASCADE-001 08:47).

---

## 3. Outcome statement (measurable against `docs/05_kpis_baseline.md`)

**Success before any architecture is chosen:** the program can **see and refuse** untrusted cyber-physical claims, and can **measure** disagreement, telemetry quality, unsafe-recommendation avoidance, and recovery-evidence gaps — without actuating the plant.

Quantify first. Thresholds are **not** invented here (SDD-04 / SDD-08). `BASELINE_PENDING` means the KPI is named in `docs/05` but not computed by `run_diagnostics()` and has no time-series in product code.

| KPI (`docs/05`) | Formula used now | Population | Current snapshot | Limitation |
|---|---|---|---|---|
| Asset inventory disagreement rate | registered_state=ACTIVE AND observed_state in {OFFLINE,UNSEEN} / 2016 | `data/raw/assets.csv` n=2016 | **200 / 2016 = 9.92%** | Only this conflict pair; aliases/shadow not in the rate |
| Unknown/unowned asset rate | owner=Unknown / 2016 | `assets.owner` | **343 / 2016 = 17.01%** | Empty owner = 0; Unknown is a label, not proven unowned |
| Telemetry bad/uncertain quality rate | quality != GOOD / 31224 | `tag_telemetry.jsonl` | **4094 / 31224 = 13.11%** | Duplicates 120 and TEMP unit!=C 47 are extra defects |
| Stale configuration rate | Not defined in diagnostics | firmware / `backup_age_days` exist | **BASELINE_PENDING** | No catalogue formula |
| Mean time to contextualize an OT alert | Not in code | 2800 alerts | **BASELINE_PENDING** | No join to process/safety in API |
| Alerts per actionable incident | 2800 alerts; “actionable” undefined | `cyber_alerts.csv` | **OPEN-006** | 1735/2800 process_context=UNKNOWN (62.0%) |
| Safety-bypass aging | Count bypassed/degraded; duration not in file | `safety_barriers.csv` n=450 | Count **61** (35 DEGRADED + 26 BYPASSED); aging **BASELINE_PENDING** | bypass_authorized=UNKNOWN 157/450 |
| Vulnerability-to-process-impact coverage | No unit join on `vulnerabilities.csv` | 1100 findings; 2800 alerts | **Not covered as a computed rate** | network_reachable=UNKNOWN 344/1100 |
| Remote-session approval compliance | approved_window=YES / 700 | `remote_access_sessions.csv` | **563 / 700 = 80.4%**; non-YES **137** | UNKNOWN 76 counted as non-compliant by diagnostics |
| Restore-test freshness | `last_restore_test_days` exists; unused by `legacy_recovery_ready` and unused by diagnostics | 144 recovery rows | **Field present; KPI BASELINE_PENDING** | Legacy uses `backup_status` only |
| Recovery runbook completeness | runbook_status=CURRENT / 144 | `recovery_readiness.csv` | **109 / 144 = 75.7%**; non-CURRENT **35** | CURRENT is not tested |
| Time to cyber-physical incident confidence | Not in code | — | **BASELINE_PENDING** | |
| Time to safe containment recommendation | Not in code | — | **BASELINE_PENDING** | Isolation path is safety-blind today |
| Degraded-operation duration | Not in code | — | **BASELINE_PENDING** | |
| False-positive escalation rate | Not in code | — | **BASELINE_PENDING** | |
| Decision evidence completeness | Not in code | — | **BASELINE_PENDING** | `docs/06` requires fields the API does not emit |
| Human approval latency for consequential actions | Not in code | — | **BASELINE_PENDING** | No named approver |
| AI cost per analyzed incident / avoided escalation | Not in code | — | **BASELINE_PENDING** | No FinOps meter |

**Outcome in one sentence:** before autonomy, the estate must make the 200 identity-state conflicts, 4094 dirty telemetry records, 61 degraded/bypassed barriers, 244 CMMS/field splits, 137 unapproved sessions, and 35 incomplete runbooks **visible and non-executable as plant control** — and must stop ranking by CVSS alone and isolating on HIGH/CRITICAL alone.

---

## 4. Sponsor / owner roles (C81) — titles only; people OPEN

No person name appears in `policy.py`, `docs/06`, or the data files as an engagement sponsor. Titles below are **proposed RACI actors**. Every cell that needs a named human is OPEN-001.

| Role (playbook + transformation prompt) | Named in repo? | Proposed accountability (workshop) |
|---|---|---|
| Global OT Risk Sponsor / OT-CISO | No | Accountable for risk acceptance policy and residual-risk posture |
| VP Operations / Plant Operations | No | Accountable for production-safe response; consulted on isolation drafts |
| Site Process Engineering | No (CASCADE-001 has a role warning only) | Accountable for process-consequence of containment drafts |
| Safety / SIS owner | No | Accountable for barrier state, proof-test, bypass authorization |
| SOC manager | No | Responsible for alert triage; **not** sole authority to isolate |
| Maintenance / CMMS owner | No | Accountable for work-order vs field-status reconciliation process |
| Vendor Access owner | No | Accountable for remote-session approval/MFA evidence |
| FDE lead | No (this charter is the FDE work product) | Responsible for evidence register, eval gates, spec traceability |
| Plant operators | Affected users; not named | Consulted; receptors of wrong isolation |
| Nearby community / environment | Not in data; named as safety receptors in prompt | Informed residual-risk stakeholders — **not a data table** |

`data/shadow/risk_acceptance_tracker.csv` uses `risk_owner` in {Plant Manager 48, OT Security 47, Engineering 44, Unknown 41}. Those are **tracker labels**, not engagement sponsors, and **Unknown is not permission** (OPEN-005).

---

## 5. Governance RACI (C48, C80, C81)

### 5.1 ACTION_TIERS as coded (`src/ot_command/core/policy.py`)

| Tier | Actions in code | requires_human_approval |
|---|---|---|
| 0 | observe, correlate, summarize | False |
| 1 | recommend | False |
| 2 | request_fresh_telemetry, open_ticket, increase_logging | False |
| 3 | isolate_endpoint, change_remote_access, change_firewall | **True** |
| 4 | write_plc_logic, change_setpoint, modify_sis, bypass_interlock | **True** |
| default | any action not in the dict | **True** (`.get(action, 4)`) |

`docs/06` additionally names enrich, rank evidence, read-only simulation (allowed autonomous) and capture evidence (reversible) and maintenance-mode transitions (human-authorized). Those strings are **not** keys in `ACTION_TIERS` (OPEN-004). Isolation recommendation in `legacy_isolation_recommendation` does **not** call `requires_human_approval`.

### 5.2 Decision-rights RACI (workshop roles; people unnamed)

R = Responsible, A = Accountable, C = Consulted, I = Informed. **No cell grants live OT permission.**

| Decision / artifact | FDE | SOC mgr | Process Eng | Safety/SIS | VP Ops | OT-CISO | Vendor Access | Maint/CMMS |
|---|---|---|---|---|---|---|---|---|
| Evidence register / source reliability | A/R | C | C | C | I | A (policy) | C | C |
| Treat a file as operational truth | — | — | — | — | — | A | — | — |
| Isolation **draft** (recommend only) | R (spec/eval) | R (draft) | **A/C** | **C** | A (plant) | I | I | C |
| Isolation **execute** | Forbidden in this repo | Must not execute in software | Must stop unsafe isolate | Must stop if barrier degraded | Human only if ever authorized outside repo | A residual risk | I | C |
| Risk acceptance / DEFER / ACCEPT | I | C | C | C | C | **A** | I | C |
| Eval gates before any agent | **A/R** | C | C | C | I | A (go/no-go) | I | I |
| Model / prompt / policy change | R | I | C | C | I | A | I | I |
| Tier 0 observe/correlate/summarize | R (tooling) | R | I | I | I | I | I | I |
| Tier 1 recommend | R (quality) | R | C | C | I | I | I | I |
| Tier 2 reversible (ticket, logging, fresh telemetry) | R (design) | R | C | I | I | I | C | C |
| Tier 3 consequential (isolate, remote access, firewall) | Spec only | C | **C** | **C** | **A** with Safety | A (policy) | C | I |
| Tier 4 control write / SIS / interlock | **Forbidden** | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden |

UNKNOWN permission is recorded as OPEN, not as an “I” that implies consent.

---

## 6. Stakeholder and affected-groups map (C02)

### 6.1 Direct users and operators of truth fragments

| Group | Job in this estate (evidence) | Failure if over-trusted | What “good” looks like (mandate-level, not architecture) |
|---|---|---|---|
| SOC analysts | 2800 alerts; 199 CRITICAL; `legacy_rank` by CVSS | Automation bias: CRITICAL banner leads to isolate (`legacy_isolation_recommendation`; CASCADE-001 08:47) | See reachability, process, safety, recovery before escalate |
| Process engineers | CASCADE-001 08:50 warning; `process_units.safe_state` in {RECIRCULATE 60, STOPPED 59, MIN_LOAD 54, ISOLATED 43} | Ignored by isolation rule | Isolation drafts show `safe_state` + required role |
| Safety / SIS owner | 450 barriers; 61 not ACTIVE; 73 proof not CURRENT; bypass_authorized=UNKNOWN 157 | Security treats barriers as healthy | Barrier state is a first-class input, not a footnote |
| Operations supervisors / operators | Shift email Unit 04; `work_orders` 244 CLOSED not RTS | Paper-closed risk while unit near min stable load | Field status visible next to CMMS |
| Maintenance / CMMS | 1250 WOs; cmms/field split | Planners close work that is not returned | Conflict count stays visible (do not “clean”) |
| Vendors | `vendors.csv` n=10; remote methods jump_host / vendor_vpn; 137 sessions not approved_window=YES; 128 MFA not YES; identity unknown 140/700 | Undocumented path treated as approved | Session evidence is not permission |
| OT Security / SOC manager | owner=OT Security 349 assets; tracker OT Security 47 | CVSS queue is not plant risk | Contextual rank required by EVAL-002 stub |
| Regional / plant leadership | 18 PLT-nn; operator BusinessUnit-* | Dashboard count as success | KPIs in §3 |
| FDE / assurance | evals stubs EVAL-001 to 006; 3 XFAIL product defects | Shipping agents on XFAIL logic | Tests/evals before automation |
| Community / environment | Not a table; prompt-required safety receptors | Isolation or trip that releases/stops protection | Residual-risk stakeholder; no actuation from this system |

### 6.2 Affected-group / harm sketch (not a legal impact assessment — that is SDD-05)

| Harm class | Example already in repo | Receptor |
|---|---|---|
| Cyber | 779 undocumented and observed paths; 137 unapproved sessions | SOC, vendors, plants |
| Process | Isolation vs MIN_LOAD / Unit 04 handover | Operators, production |
| Safety | 61 barriers not ACTIVE while SOC may still isolate | People on site; environment as receptor |
| Resilience | 25 non-CURRENT backups; 29 unverified deps; 35 runbook gaps; `legacy_recovery_ready` trusts CURRENT | Continuity owners |
| Authority | No named approver; 41 tracker rows risk_owner=Unknown | OT-CISO, Safety, Ops |

---

## 7. Field-evidence register

**Rule:** `permitted_use_operational_truth = UNKNOWN` unless a cited doc grants it. **None of the data files is granted operational-truth permission.**  
**Workshop forensics** of synthetic records is allowed by `README.md` (fictional, local, no real equipment) and `data/manifest.json` `notes`.  
**Live OT control** is FORBIDDEN by `docs/06_security_safety_assurance.md`.

Claim types: **observed** / **registered** / **shadow** / **reference** / **code** / **eval**.

| Path | Grain | Claim type | Reliability as record existence | Limitation | Operational-truth permission | Workshop forensics |
|---|---|---|---|---|---|---|
| `data/manifest.json` | 1 manifest; 18 count keys | reference | HIGH | Counts are seed metadata, not a live census | UNKNOWN | YES (notes) |
| `data/reference/plants.csv` | 18 rows; PLT-01 to PLT-18 | reference | HIGH | Countries Country-1 to Country-10; fictional | UNKNOWN | YES |
| `data/reference/vendors.csv` | 10 rows | reference | HIGH | remote_access is a label, not a live VPN | UNKNOWN | YES |
| `data/reference/tags.csv` | 864 rows | reference | HIGH | historian_enabled is a flag, not historian proof | UNKNOWN | YES |
| `data/raw/assets.csv` | 2016 rows | registered + observed in the same row | HIGH as file; LOW as single truth | 200 ACTIVE vs OFFLINE/UNSEEN; 343 owner Unknown | UNKNOWN | YES |
| `data/raw/asset_aliases.csv` | 6048 rows; 3 sources times 2016 | registered (CMDB/CMMS) + observed-like (PASSIVE) | HIGH as file | 5 alias collisions (VERIFICATION); name is not identity | UNKNOWN | YES |
| `data/raw/network_edges.csv` | 3780 rows | observed and registered path flags | HIGH as file | 779 undocumented and observed_last_24h=YES; approved_path=UNKNOWN 240 | UNKNOWN | YES |
| `data/raw/process_units.csv` | 216 rows | registered process | HIGH as file | safe_state is a label; not a live SIS | UNKNOWN | YES |
| `data/raw/process_dependencies.csv` | 198 rows | registered / partial undocumented | HIGH as file | documented=NO 51/198 | UNKNOWN | YES |
| `data/raw/vulnerabilities.csv` | 1100 rows; e.g. VUL-00001 | registered cyber finding | HIGH as file | CVSS present; no process-unit field; reachable UNKNOWN 344 | UNKNOWN | YES |
| `data/raw/safety_barriers.csv` | 450 rows; e.g. PLT-01-SAFE-01 | safety (recorded) | HIGH as file | 61 not ACTIVE; 73 proof not CURRENT; bypass_authorized UNKNOWN 157 | UNKNOWN | YES |
| `data/raw/work_orders.csv` | 1250 rows; e.g. WO-000001 | registered (cmms_status) + operational (field_status) | HIGH as file | 244 CLOSED and field not RETURNED_TO_SERVICE | UNKNOWN | YES |
| `data/raw/remote_access_sessions.csv` | 700 rows; e.g. RA-00001 | observed session + registered approval flags | HIGH as file | approved_window UNKNOWN 76; mfa UNKNOWN 72; identity unknown 140 | UNKNOWN | YES |
| `data/raw/recovery_readiness.csv` | 144 rows | registered resilience flags | HIGH as file | CURRENT backup is not restore-tested; diagnostics ignore last_restore_test_days | UNKNOWN | YES |
| `data/raw/cyber_alerts.csv` | 2800 rows; e.g. ALT-000001 | registered SOC + operational process_context | HIGH as file | process_context UNKNOWN 1735; not a SIEM | UNKNOWN | YES |
| `data/raw/enterprise_events.jsonl` | 6500 events | mixed enterprise observed/registered | HIGH as file | event_time vs received_time can invert (EVT-0000001) | UNKNOWN | YES |
| `data/telemetry/tag_telemetry.jsonl` | 31224 events; e.g. TEL-00000000 | observed telemetry | HIGH as file; quality often not GOOD | 4094 BAD/UNCERTAIN; 120 duplicate packets; 47 TEMP unit!=C; ingest!=event | UNKNOWN | YES |
| `data/ot_legacy.db` | 6 tables: assets 2016, vulns 1100, safety 450, WO 1250, remote 700, recovery 144 | registered replica | HIGH integrity_check=ok | Lineage vs CSV undocumented; subset of files | UNKNOWN | YES |
| `data/shadow/ot_asset_inventory_FINAL_v8.csv` | 220 rows | shadow | LOW as authority; HIGH as contradiction evidence | Handover says newer than CMDB; 220 IDs subset of assets.csv | UNKNOWN | YES |
| `data/shadow/risk_acceptance_tracker.csv` | 180 rows | shadow authority | LOW | 41 Unknown owners; thin rationales | UNKNOWN | YES |
| `data/shadow/shift_handover_email.txt` | 1 note, Unit 04 | shadow / operational interpretation | LOW as truth; HIGH as friction evidence | Vendor done vs ticket; bypass temporary; historian vs HMI | UNKNOWN | YES |
| `contracts/asset_api_v1.yaml` | 1 stub OpenAPI | code/contract | HIGH as text | Fields not implemented by FastAPI | UNKNOWN as plant API | YES |
| `contracts/asset_api_v2.yaml` | 1 stub OpenAPI | code/contract | HIGH as text | Field names disagree with v1 | UNKNOWN as plant API | YES |
| `contracts/telemetry_event_schema.json` | 1 JSON Schema | code/contract | HIGH as text | Missing ingest_time, source, asset_id which records contain | N/A (schema) | YES |
| `src/ot_command/__init__.py` | version string | code | HIGH | __version__=0.1.0 vs pyproject 2.0.0 | N/A | YES |
| `src/ot_command/api.py` | 2 routes | code | HIGH | Read-only; no asset API | N/A | YES |
| `src/ot_command/cli.py` | 1 command | code | HIGH | diagnostics only | N/A | YES |
| `src/ot_command/repository.py` | CSV/JSONL IO | code | HIGH | No permission layer | N/A | YES |
| `src/ot_command/diagnostics.py` | 14 counters | code | HIGH as heuristic | UNKNOWN lumped with NO; does not read vulns/process/shadow | N/A | YES |
| `src/ot_command/legacy/risk.py` | 4 functions | code | HIGH as defect evidence | CVSS rank; backup-flag recovery; safety-blind isolate | N/A | YES |
| `src/ot_command/core/policy.py` | ACTION_TIERS | code | HIGH as policy stub | Unused by isolation; incomplete vs docs/06 | N/A | YES |
| `tests/test_baseline.py` | 3 tests (pass) | eval/code | HIGH | Detects imperfections; does not test identity/temporal/safety join | N/A | YES |
| `tests/test_known_legacy_defects.py` | 3 tests (xfail strict) | eval/code | HIGH as known defect | Encodes desired future; legacy still fails | N/A | YES |
| `evals/README.md` | eval dimensions list | eval | MEDIUM | Aspirational; no harness | N/A | YES |
| `evals/golden_cases.jsonl` | 6 cases EVAL-001 to 006 | eval | MEDIUM | Stubs; must_include/must_not; not pytest | N/A | YES |
| `scenarios/cascade_001.json` | CASCADE-001, 10 timeline events | eval/scenario | MEDIUM | Narrative inject; 37 controllers / 6 unknown firmware unverified in this prompt | UNKNOWN as history | YES |
| `scenarios/inject_01.md` | Inventory mismatch | eval | LOW detail | Title only | N/A | YES |
| `scenarios/inject_02.md` | Historian quality | eval | LOW detail | Title only | N/A | YES |
| `scenarios/inject_03.md` | Unapproved vendor session | eval | LOW detail | Title only | N/A | YES |
| `scenarios/inject_04.md` | Safety bypass aging | eval | LOW detail | Title only | N/A | YES |
| `scenarios/inject_05.md` | Regional SCADA outage | eval | LOW detail | Title only | N/A | YES |
| `scenarios/inject_06.md` | Restore failure drill | eval | LOW detail | Title only | N/A | YES |

**Explicit non-permission:** CMDB, PASSIVE, CMMS, historian, SCADA, SIEM, operator notes, and the shadow spreadsheet are **not true by name**.

---

## 8. OM-1 capability evidence (96 FDE stack — this phase only)

These are **consulting-stack** capabilities. They are not the 96 forensic cells.

| ID | Capability | Evidence in this artifact | Status |
|---|---|---|---|
| C01 | Consulting judgement | §1: leadership ask vs FDE mandate; not another dashboard; not control automation | specced (charter) |
| C02 | Stakeholder discovery | §6 maps + affected groups including community/environment receptors | specced (charter) |
| C46 | Responsible AI | §2 advisory HITL; recommendation quality bar from `docs/06`; automation-bias named | specced (charter) |
| C48 | Governance | §5 RACI for evidence, isolate drafts, risk acceptance, eval gates, prompt/policy change | specced (charter) |
| C50 | Regulatory / standards applicability | §2 ISO/IEC 42001 scope-as-method; EU AI Act class = OPEN-002; no certificate | specced as method + OPEN |
| C80 | Operating-model design | Mandate + owners + ACTION_TIERS seed OM; sequential SDD after this | specced (seed) |
| C81 | Roles, RACI, decision-rights | §4–5 mapped to ACTION_TIERS 0–4; unnamed people OPEN-001 | specced + OPEN |

`specs/01_mandate.md` is **not** written in SDD-01; SDD-15 distills it. That is process, not a missing judgement.

---

## 9. Gate (SDD-01)

| Criterion | Result |
|---|---|
| No source with UNKNOWN operational-truth permission treated as permitted truth | **PASS** — §7 marks operational truth UNKNOWN; workshop forensics only |
| No target architecture (no KG/RAG/agent/twin as the answer) | **PASS** |
| Five states kept separate | **PASS** — §1 table |
| Forbidden control actions not recommended | **PASS** |
| Named human authority not invented | **PASS** — OPEN-001 |
| 96 forensic cells not substituted for OM-1 capabilities | **PASS** |

**Output to next:** approved **workshop mandate and operating context** (this file + `REPO_INVENTORY.md` + `OPEN_DECISIONS.md`). Discovery (SDD-02) may proceed. Implementation of product behavior may not.
