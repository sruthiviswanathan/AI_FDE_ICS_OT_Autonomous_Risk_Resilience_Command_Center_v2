# ICS/OT Brownfield Forensic Review

**Estate:** AI FDE ICS/OT Autonomous Risk & Resilience Command Center v2  
**Lens set:** Imperfection, Inconsistency, Friction, Complexity, Volatility, Uncertainty, Hidden Dependency, Unknown Unknown  
**Evidence date:** 2026-09-11  
**Data generated:** 2026-09-10 (seed `20260910`)  
**Sources:** `data/raw`, `data/telemetry`, `data/shadow`, `data/reference`, `VERIFICATION.md`, `src/ot_command/legacy/risk.py`, `participant/CHALLENGE_BRIEF.md`, `docs/01`–`07`

This is a synthetic, locally runnable estate. Counts are observed in this repository, not inferred from live controllers. Highest CVSS is not treated as highest operational risk. No recommendation here authorizes PLC writes, SIS changes, interlock bypasses, or unsafe isolation.

---

## Core forensic tension

**Cyber state ≠ Operational state ≠ Safety state ≠ Resilience state**

The estate produces many dashboards. It does not produce a trusted cyber-physical truth.

---

## 1. Problem to be solved

Leadership wants an autonomous risk and resilience command center. What they have is 18 plants across five regions and eight industry types (chemicals, pharma, food, water, power, metals, oil and gas, automotive). Systems evolved independently: PLC/DCS, SCADA/HMI, historians, SIS, CMMS/EAM, SOC/SIEM, IAM/PAM, vendor remote access, and engineering workstations.

The operating failure is not “we need more AI.” It is that no actor — SOC, operations, safety, maintenance, or vendors — can answer, with evidence and uncertainty:

- what exists
- what state it is in
- what a cyber finding would do to the process
- which safety barrier is actually active
- whether a recovery plan is executable without making the unit unsafe

The goal is **not** to automate control. The goal is trustworthy cyber-physical situational awareness, contextual risk, resilience decisions, and governed action recommendations.

---

## 2. What we are being asked

Perform brownfield forensics **before** proposing AI.

- Preserve evidence. Do not silently clean intentional contradictions.
- Never treat CMDB, passive discovery, historian, SCADA, CMMS, SIEM, or operator notes as authoritative by name alone.
- Separate **observed state**, **registered state**, **operational interpretation**, **safety state**, and **decision authority**.
- Do not connect to real OT systems. Do not write to controllers.
- Any consequential target-state action must be bounded by policy, safety constraints, and human authority.
- Build tests/evals before introducing agentic automation.

### Required deliverables

| Deliverable | Why it exists in this estate |
|---|---|
| Current-state map | Architecture diagram is incomplete; vendor VPNs and service laptops sit outside it |
| Top engineering imperfections L1–L12 | Debt is layered; a cyber-only view hides safety and recovery failure |
| Asset identity reconciliation | CMDB, passive, CMMS, and a shadow spreadsheet disagree |
| Telemetry quality findings | Duplicates, unit mismatches, delay, BAD/UNCERTAIN quality |
| Process/asset dependency model | 33 critical process dependencies are undocumented |
| Contextual risk model | Legacy rank sorts by CVSS and ignores reachability and criticality |
| Safety/security conflict handling | SOC isolation can destabilize a unit near minimum stable load |
| Resilience/recovery graph | `backup CURRENT` is treated as recoverable; restore tests are years old |
| Target architecture | Capabilities only where evidence shows they solve a real gap |
| Bounded-autonomy model | Observe/correlate/recommend vs human-authorized vs forbidden |
| Evaluation/TEVV strategy | Golden cases already forbid CVSS-only rank and automatic isolation |
| KPI before/after model | Inventory disagreement, telemetry quality, restore freshness, approval latency |
| 90-day roadmap and executive defense | Autonomy is the last step, not the first |

---

## 3. Pain points

| Pain | Evidence in this repo |
|---|---|
| No trusted inventory | 200 ACTIVE assets observed OFFLINE/UNSEEN; 343 unknown owners; shadow spreadsheet covers 220 of 2,016 assets; 5 colliding aliases |
| Alerts without process meaning | 1,735 of 2,800 alerts have process context UNKNOWN, including 525 HIGH/CRITICAL |
| CVSS theater vs operational risk | Legacy rank sorts by CVSS; 53 findings with CVSS ≥ 9.0 are unreachable; 87 open reachable findings sit on CRITICAL assets |
| Safety-blind cyber response | HIGH/CRITICAL → `ISOLATE`; handover says do not isolate near minimum stable load |
| Ticket vs field | 244 CMMS CLOSED but not returned to service; 161 open/in-progress already returned; 94 temporary bypasses |
| Recovery theater | 108 of 119 CURRENT backups have restore tests older than 90 days; median restore-test age is 379 days |
| Shadow operations | Vendor VPNs, service laptops, `FINAL_v8` spreadsheet, expired risk acceptances (131 of 180) |

### Scale snapshot

| Object | Count |
|---|---:|
| Plants | 18 |
| Regions | 5 |
| Registered assets | 2,016 |
| Asset aliases | 6,048 |
| Network edges | 3,780 |
| Process units | 216 |
| Process dependencies | 198 |
| Tags | 864 |
| Telemetry records | 31,224 |
| Vulnerability findings | 1,100 |
| Safety barriers | 450 |
| Work orders | 1,250 |
| Remote access sessions | 700 |
| Cyber alerts | 2,800 |
| Recovery records | 144 |
| Enterprise events | 6,500 |

Plant maturity mix: 7 legacy / 5 modernizing / 6 mixed. Criticality: 13 HIGH / 5 MEDIUM.

---

## 4. End goal and target state

A governed command center that can produce a defensible cyber-physical picture:

1. Canonical identity, with source, freshness, and conflict flag.
2. Provenance-aware telemetry (quality, unit, event time vs ingest time).
3. Process and recovery dependency graphs.
4. Contextual risk that can outrank CVSS.
5. Safety-aware response policy.
6. Bounded recommendations.
7. Human authority on consequential acts.
8. Evals that fail closed.

| Capability | Current (observed) | Target (bounded) |
|---|---|---|
| Identity | 3 aliases per asset, 5 collisions, shadow 11% coverage | Canonical ID with source, freshness, and conflict flag |
| Telemetry | 13% bad/uncertain, 120 duplicate packets, 47 unit errors, 120 s mean delay | Quality, unit, and ingest-vs-event time on every use |
| Risk | Sort by CVSS | Reachability × criticality × safety × recovery × compensating controls |
| Containment | HIGH/CRITICAL → `ISOLATE` | Recommend only; refuse isolation that violates safe-state |
| Recovery | Backup CURRENT ⇒ ready | Ready iff restore test, runbook, and dependencies are verified |
| Autonomy | No real action surface; policy tiers exist on paper | Tiers 0–1 autonomous; 2 policy-controlled; ≥3 human; 4 forbidden in this repo |

Knowledge graphs, RAG, and digital twins are optional, not assumed. Use them only when evidence shows they solve a real gap.

---

## 5. Moonshots

### Safe to explore after evals

- Read-only digital twin / replay of CASCADE-001 with uncertainty bands.
- Predictive degradation only on tags that already have GOOD-quality history.
- Evidence graph only where `correlation_id` is non-empty and provenance is known.
- Decision agents limited to observe, correlate, summarize, rank, and recommend.

### Out of scope / unsafe

- Closed-loop isolation from SIEM severity.
- PLC writes, setpoint changes, SIS edits, interlock bypass, trip suppression.
- Auto-restart after restore without process authority.
- Treating a global command center as a live controller.

Allowed autonomous behavior in this repository: collect, correlate, enrich, summarize, rank evidence, and run read-only simulation.

Human-authorized consequential behavior: network isolation, remote-access changes, firewall policy changes, maintenance-mode transitions.

Forbidden here: PLC logic writes, setpoint changes, SIS modifications, interlock bypass, trip suppression, unsafe restart.

Every recommendation must expose evidence, freshness, uncertainty, process impact, safety impact, rollback considerations, and required authority.

---

## 6. How to get there

Suggested path from `AGENTS.md`, bound to this estate’s evidence. Tests before agents.

| Phase | Window | Work | Exit gate |
|---|---|---|---|
| 0 Preserve | Days 1–7 | Freeze evidence. Run diagnostics. Do not clean intentional contradictions. | Baseline KPI snapshot published; expected-fail tests still xfail |
| 1 Inventory + identity | Days 8–21 | Reconcile CMDB / passive / CMMS / shadow. Map alias collisions. Flag UNKNOWN owners. | Every asset has a conflict record or a canonical ID with confidence |
| 2 Topology + telemetry | Days 15–35 | Treat undocumented observed edges as first-class. Unit / quality / delay model. | No ranking uses a BAD sample as a fact; °F vs °C is explicit |
| 3 Process + safety | Days 28–50 | Join units, dependencies, barriers, safe-states. Mark isolation-unsafe units. | Isolation recommendations carry process consequence or are refused |
| 4 Contextual risk + recovery | Days 40–65 | Replace CVSS sort. Recovery ready requires restore, runbook, and deps. | `legacy_rank` / `legacy_recovery_ready` / isolation xfail tests flip to pass |
| 5 Authority + evals | Days 55–80 | Expand `golden_cases.jsonl`. Enforce policy tiers. HITL on ≥3. | EVAL-001..006 plus outage / adversarial cases green |
| 6 Bounded recommenders | Days 70–90 | Observe / correlate / summarize / recommend only. KPI before/after. Executive defense. | Time-to-cyber-physical confidence down; no control writes added |

---

## 7. Eight-lens analysis (detail)

### 7.1 Imperfection — defective logic that still runs

Imperfection here is engineering logic and incomplete artifacts that still run in production.

The production ranking code is simplistic on purpose and is still the decision machinery:

- `legacy_rank` sorts findings by CVSS.
- `legacy_recovery_ready` returns true if `backup_status == CURRENT`.
- `legacy_isolation_recommendation` returns `ISOLATE` for HIGH/CRITICAL with no safe-state check.

Those three behaviors are locked in as expected-fail tests in `tests/test_known_legacy_defects.py`.

Packaging is also imperfect:

- `ot_command.__version__` is `0.1.0`
- `pyproject.toml` and API claim `2.0.0`
- `data/manifest.json` still titles the dataset v1

The telemetry JSON Schema requires `event_id`, `tag_id`, `event_time`, `value`, `unit`, `quality` but omits `ingest_time`, `asset_id`, and `source` that the JSONL actually carries. `generate_data.py` does not generate data; it only checks that files exist.

Asset backup age: 1,133 assets have `backup_age_days` > 180; 258 exceed 365. 51 tags are historian-disabled, so those loops are blind in the only telemetry store.

**Effect:** wrong actions look automated and confident.

### 7.2 Inconsistency — locally true, globally false

Registered state uses `ACTIVE` / `UNKNOWN` / `RETIRED`. Observed state uses `ONLINE` / `OFFLINE` / `UNSEEN` / `INTERMITTENT`. They are different languages. Naive string equality fails on all 2,016 assets. The honest operational conflict set is **200** ACTIVE assets that are OFFLINE or UNSEEN.

Further inconsistencies:

| Split | Count / note |
|---|---|
| Alias collisions (same alias, more than one asset) | 5 |
| Aliases per asset | 3 (CMDB, PASSIVE, CMMS) |
| Asset API v1 vs v2 | `assetId`/`fwVersion`/`operationalState` vs `asset_id`/`firmware`/`observed_state` |
| CMMS CLOSED, field not RETURNED_TO_SERVICE | 244 |
| CMMS OPEN/IN_PROGRESS, field already returned | 161 |
| Severity HIGH with CVSS < 7 | 144 |
| Severity LOW with CVSS ≥ 7 | 143 |
| Temperature samples in °F against engineering unit °C | 47 |
| Enterprise events received before event_time | 407 |
| SAFETY_PLC outside L0/L1 | 89 |
| SENSOR in DMZ | 30 |
| PLC in DMZ | 29 |
| HMI in L0_FIELD | 35 |

Shadow inventory (`ot_asset_inventory_FINAL_v8.csv`) covers 220 of 2,016 assets (11%). Overlapping records match firmware/state/owner; coverage, not field drift, is the inconsistency. Night-shift email says the spreadsheet is newer than CMDB for a new gateway.

**Effect:** every system can be “right” in its own schema and still be unusable for a decision.

### 7.3 Friction — cost of assembling one decision

Nine enterprise sources emit 6,500 events: SIEM, MES, HISTORIAN, IAM, CMMS, SCADA, EAM, VENDOR_PORTAL, PASSIVE_DISCOVERY. **3,251 have an empty correlation ID.**

| Friction signal | Count |
|---|---:|
| Alerts with process_context UNKNOWN | 1,735 / 2,800 (62%) |
| HIGH/CRITICAL alerts with unknown process | 525 |
| Alerts SUPPRESSED | 683 |
| Alerts OPEN | 693 |
| Mean historian ingest delay | 120.3 s |
| Telemetry delayed > 60 s | 23,414 / 31,224 |
| Remote methods | jump_host 182, RDP 179, service laptop 170, vendor VPN 169 |
| Unknown remote identity | 140 |
| Work orders noting operator workaround active | 252 |
| Risk acceptances expired by 2026-09-11 | 131 / 180 |

Night-shift truth lives in `data/shadow/shift_handover_email.txt`. CASCADE-001 is friction in one timeline: firmware advisory → unknown firmware → unexpected write → vendor session → historian deviation → operator alarm → safety bypassed → SOC says isolate → process says that may destabilize the unit.

**Effect:** time-to-cyber-physical confidence is long; SOC and operations argue from different clocks and different worlds.

### 7.4 Complexity — no single playbook survives a site

- 18 plants, 5 regions, 8 industry types, 6 business units
- Maturity mix: 7 legacy / 5 modernizing / 6 mixed
- 13 asset types, 10 protocols, 5 zone labels, 10 vendors, 815 firmware strings
- 216 process units; safe states STOPPED / RECIRCULATE / MIN_LOAD / ISOLATED
- 19 units with no manual mode; 44 LIMITED
- Recovery: 8 components × 18 plants
- Policy: five action-authority tiers (observe → SIS/setpoint writes)
- Analysis must span L1–L12
- Timezones span UTC−5 to UTC+8, so “last 24h” on a network edge is not a global instant

**Effect:** a global rule (especially “isolate on HIGH”) is operationally unsafe at some units by construction.

### 7.5 Volatility — baselines rot inside a shift

| Volatile signal | Count |
|---|---:|
| Assets observed INTERMITTENT | 129 |
| UNEXPECTED_WRITE alerts | 404 |
| CONFIG_DRIFT alerts | 388 |
| NEW_DEVICE alerts | 399 |
| Work orders with temporary bypass | 94 |
| Safety BYPASSED | 26 |
| Safety DEGRADED | 35 |

CASCADE-001 starts with a firmware advisory and unknown firmware on six controllers. Vendor sessions and night-shift firmware work land before tickets update. Work-order notes include “awaiting vendor” and “parts substituted.”

**Effect:** an inventory snapshot taken this morning is not the incident picture at 08:55.

### 7.6 Uncertainty — unknown is a first-class state

Unknown is not missing data to be filled. It is a recorded state that decisions must carry.

| Unknown / uncertain field | Count |
|---|---:|
| Asset owner Unknown | 343 |
| Registered state UNKNOWN | 122 |
| Vuln reachability UNKNOWN | 344 |
| Compensating control UNKNOWN | 235 |
| Compensating control NONE | 222 |
| Safety bypass_authorized UNKNOWN | 157 |
| Remote approved UNKNOWN | 76 |
| Remote MFA UNKNOWN | 72 |
| Recovery backup UNKNOWN | 9 |
| Recovery dependency_verified UNKNOWN | 13 |
| Alert process_context UNKNOWN | 1,735 |
| Enterprise payload_state UNKNOWN | 1,081 |
| Telemetry UNCERTAIN | 2,743 |
| Telemetry BAD | 1,351 |
| Telemetry bad or uncertain rate | 13.1% |
| Risk-acceptance owner Unknown | 41 |
| Tags with historian disabled | 51 |

Eval cases explicitly forbid assuming CMDB is always correct and require uncertainty in temporal reconstruction (`event_time` vs received/ingest time).

**Effect:** a score without confidence is unsafe. Every recommendation must carry freshness and uncertainty.

### 7.7 Hidden dependency — blast radius that diagrams omit

| Hidden / undocumented dependency | Count |
|---|---:|
| Network edges undocumented | 983 / 3,780 |
| Undocumented **and** observed last 24h | 779 |
| Observed but approved_path = NO | 168 |
| Approved_path UNKNOWN | 240 |
| Documented but not observed last 24h | 527 |
| Process dependencies undocumented | 51 / 198 |
| Critical undocumented process dependencies | 33 |
| Recovery dependencies unverified | 29 |
| Units with no manual mode | 19 |
| Units with LIMITED manual mode | 44 |

The architecture note names the parallel estate: vendor VPNs, service laptops, spreadsheets, shift notes, stale diagrams. Shadow risk-acceptance and `ot_asset_inventory_FINAL_v8.csv` are not in `manifest.json`’s file list, so a naive pipeline never sees them.

Handover instruction: do not isolate the controller without process engineering review; the unit is running near minimum stable load.

**Effect:** isolation and restore have unmodeled consequences. “Compensating controls assumed” on 44 risk acceptances is not a control.

### 7.8 Unknown unknown — what sensing cannot confirm or deny

These are things the current sensing system is structurally unable to confirm or deny.

- Shadow inventory covers 11% of registered assets; the handover claims it is newer for at least one gateway. The unknown is which assets exist only there, only in CMDB, or in neither.
- CASCADE-001 has six controllers with unknown firmware after a family advisory.
- Historian pressure trend looked flat for ~20 minutes while HMI moved — two sensors of the same process, no adjudicator.
- Colliding aliases mean identity is not injective.
- 399 NEW_DEVICE alerts imply discovery that inventories did not predict.
- Risk acceptances cite “compensating controls assumed.”
- What is not in any file — rogue serial links, contractor jump boxes, oral standing orders — is definitionally out of the dataset.

**Effect:** absence of a record is not absence of a device or a path. Keep an unknown-unknown register. Do not impute completeness.

---

## 8. Eight-lens summary

| Lens | Severity | Dominant evidence | Operational effect |
|---|---|---|---|
| Imperfection | High | CVSS-only rank; backup-flag recovery; safety-blind ISOLATE; version 0.1.0 vs 2.0.0 vs manifest v1 | Wrong action looks automated and confident |
| Inconsistency | High | Registered vs observed vocabularies never match; 244 CMMS/field splits; 47 °F vs °C; API v1 vs v2 fields | Every source can be locally true and globally false |
| Friction | High | 62% alerts lack process context; 9 event sources; 170 service laptops; shift handover is email | Time-to-confidence is long; SOC and process argue |
| Complexity | High | 18 plants, 8 types, 13 asset classes, 10 protocols, 815 firmwares, 12 layers, 5 action tiers | No single playbook survives contact with a site |
| Volatility | Medium-high | 129 intermittent assets; 404 unexpected writes; 94 temp bypasses; 399 new-device alerts | Baselines rot inside a shift |
| Uncertainty | High | Unknown owners 343; vuln reachability UNKNOWN 344; bypass auth UNKNOWN 157; quality UNCERTAIN 2,743 | Decisions must carry confidence, not just a score |
| Hidden dependency | High | 779 undocumented live paths; 33 critical undocumented process deps; 29 unverified recovery deps | Isolation and restore have unmodeled blast radius |
| Unknown unknown | High (acknowledged) | Shadow inventory 11% coverage; 6 unknown firmware in CASCADE-001; historian flat vs HMI moving | Absence of a record is not absence of a device or a path |

---

## 9. L1–L12 × eight lenses

H = evidence-backed and material to decisions. M = present but secondary. L = not the main failure mode in this dataset.

| Layer | Imperf. | Incons. | Friction | Complex. | Volat. | Uncert. | Hidden dep. | Unk. unk. |
|---|---|---|---|---|---|---|---|---|
| L1 Software / logic | H | M | M | M | L | M | M | M |
| L2 OT / protocols | H | H | H | H | M | H | H | H |
| L3 Data / telemetry | H | H | H | M | M | H | M | M |
| L4 Asset / config | H | H | H | H | M | H | H | H |
| L5 Process / control | M | M | H | H | M | H | H | H |
| L6 Cyber / exposure | H | H | H | H | H | H | H | M |
| L7 Safety / protection | H | H | H | H | H | H | H | H |
| L8 Ops / maintenance | H | H | H | M | H | H | H | M |
| L9 IT-OT ecosystem | M | H | H | H | M | H | H | H |
| L10 Resilience | H | H | H | M | L | H | H | H |
| L11 Decision intelligence | H | H | H | H | H | H | M | H |
| L12 Autonomy / TEVV | H | M | H | H | L | H | M | H |

**How to read this:** L7, L4, L6, L10, and L11 are the densest failure cluster: identity, cyber ranking, safety barriers, untested restore, and decision machinery all disagree at once. That is exactly CASCADE-001.

---

## 10. Diagnostic concentrations

From `VERIFICATION.md` plus forensic joins on `data/raw`.

| Diagnostic | Count |
|---|---:|
| Undocumented live network paths | 779 |
| Telemetry bad or uncertain | 4,094 |
| Alerts with unknown process context | 1,735 |
| Open vulnerabilities | 799 |
| CMMS vs field conflicts (closed, not RTS) | 244 |
| Asset state conflicts (ACTIVE + OFFLINE/UNSEEN) | 200 |
| Unapproved remote sessions | 137 |
| Remote sessions without confirmed MFA | 128 |
| Expired risk acceptances (as of 2026-09-11) | 131 |
| Safety bypassed or degraded | 61 |
| Safety proof tests not current | 73 |
| Duplicate telemetry packets | 120 |
| Telemetry unit mismatches (°F vs °C) | 47 |
| Alias collisions | 5 |
| Recovery stale or unknown backup | 25 |
| Recovery unverified dependencies | 29 |
| Recovery stale or missing runbooks | 35 |
| Maintenance state conflicts | 244 |

### Additional forensic joins

| Finding | Count |
|---|---:|
| CVSS ≥ 9.0 and not network-reachable | 53 |
| CVSS < 7, reachable, OPEN | 136 |
| OPEN + reachable on CRITICAL assets | 87 |
| HIGH/CRITICAL OPEN + reachable | 147 |
| CURRENT backup with restore test > 90 days | 108 |
| Restore tests older than 365 days | 74 |
| Restore-test age min / median / max (days) | 13 / 379 / 688 |
| No manual fallback | 42 / 144 |
| Unauthorized bypassed or degraded barriers | 21 |
| ACTIVE barriers with overdue proof test | 57 |
| Unapproved remote and no MFA | 23 |

---

## 11. CASCADE-001 — proof scenario

`scenarios/cascade_001.json` compresses the eight lenses into one hour.

| Time | Event | Lens / layer |
|---|---|---|
| 08:01 | Firmware advisory on a controller family | Volatility / L2 / L4 |
| 08:07 | 37 potentially affected; 6 unknown firmware | Uncertainty / unknown unknown |
| 08:19 | Unexpected write alert | Cyber / L6 |
| 08:24 | Vendor session on engineering workstation | Hidden dependency / L8 / L9 |
| 08:31 | Historian flow trend begins deviating | Telemetry / L3 / L5 |
| 08:34 | Operator acknowledges unexpected alarm | Ops / L8 |
| 08:38 | Related safety barrier recorded as bypassed | Safety / L7 |
| 08:47 | SOC recommends immediate isolation | Imperfection / friction / L11 |
| 08:50 | Process engineer warns isolation may destabilize the unit | Safety vs cyber / L5 / L12 |
| 08:55 | Command center must reconcile evidence and recommend a safe governed response | Target state |

Correct response class: evidence-ranked recommendation with uncertainty, process consequence, and human authority. Incorrect response class: automatic PLC isolation.

---

## 12. Authority model (already in code)

From `src/ot_command/core/policy.py`:

| Tier | Actions | Approval |
|---|---|---|
| 0 | observe, correlate, summarize | Autonomous |
| 1 | recommend | Autonomous, must be evidenced |
| 2 | request_fresh_telemetry, open_ticket, increase_logging | Policy-controlled |
| 3 | isolate_endpoint, change_remote_access, change_firewall | Human required |
| 4 | write_plc_logic, change_setpoint, modify_sis, bypass_interlock | Forbidden in this repository |

---

## 13. KPI baseline to measure before/after

From `docs/05_kpis_baseline.md`, the ones this forensic pass already has a numerator for:

- Asset inventory disagreement rate (200 state conflicts; 5 alias collisions; shadow 11% coverage)
- Unknown/unowned asset rate (343 / 2,016 unknown owner)
- Telemetry bad/uncertain quality rate (4,094 / 31,224 = 13.1%)
- Stale configuration / backup age (1,133 > 180 days)
- Alerts per actionable incident (2,800 alerts; 62% lack process context)
- Safety-bypass aging (61 bypassed/degraded; 73 proof not current)
- Vulnerability-to-process-impact coverage (legacy: none; 87 open reachable on CRITICAL assets)
- Remote-session approval compliance (137 unapproved; 128 MFA unconfirmed)
- Restore-test freshness (median 379 days; 108 CURRENT backups stale)
- Recovery runbook completeness (35 stale or missing)
- Decision evidence completeness (3,251 events with empty correlation ID)

Do not claim improvement until these are re-measured on the same seed and the three expected-fail tests pass.

---

## 14. Non-negotiable

- Preserve evidence before changing behavior.
- Highest CVSS is never treated as highest operational risk.
- Distinguish cyber, process, safety, and resilience consequences.
- Test before modernization.
- Every recommendation must expose evidence, freshness, uncertainty, process impact, safety impact, rollback, and required authority.

The first modernization move is not an agent. It is a **conflict-preserving identity and evidence layer**, then contextual risk that can lose to process safety, then evals that fail closed, then recommenders that cannot write to a controller.
