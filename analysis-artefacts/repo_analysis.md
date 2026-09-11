# Repository Analysis — ICS/OT Autonomous Risk & Resilience Command Center v2

**Date:** 2026-09-11  
**Scope:** Full tree (code, contracts, data, evals, docs, packaging, runnability).  
**Method:** Evidence from files, record counts, code paths, and a live local run. No live OT connection. Highest CVSS is not treated as highest operational risk.

---

## 1. Executive summary

This repository is a **fictional, deterministic, locally runnable multinational ICS/OT brownfield simulation**. It is a training/problem estate for AI Forward-Deployed Engineering, not a production control system.

The software surface is a thin read-only Python package (~68 lines of application code). Around it sits a large contradictory evidence lake: 18 plants, 2,016 assets, 31,224 telemetry records, 2,800 cyber alerts, shadow spreadsheets, expired risk acceptances, and a safety-blind legacy risk engine.

**Is it runnable?** Partially. The diagnostics CLI and repo verifier run with the standard library. The HTTP API does **not** start on this workstation until `fastapi` / `uvicorn` are installed. There is no virtualenv and `python` is not on PATH (`py -3` is).

**Is it a working app?** It is a working **diagnostic probe** (`/health`, `/diagnostics`, CLI counters). It is **not** a working risk-and-resilience command center.

**Main problem:** there is no trusted cyber-physical truth. Cyber, operational, safety, and resilience state disagree and are never joined into a governed decision.

**Main painpoint:** leadership asked for autonomous decisions; the baseline can only count defects. Ranking uses CVSS alone, recovery trusts a backup flag, isolation ignores process-safe state.

---

## 2. What this repository is

| Attribute | Observed state |
|---|---|
| Purpose | Brownfield forensics before any AI/autonomy proposal |
| Domain | 18 sites, five regions, mixed-generation OT |
| Safety posture | Synthetic only. Read-only API. No PLC writes, SIS changes, or live isolation |
| Declared release | `2.0.0` (`pyproject.toml`, API, `data/manifest.json` `repo_version`) |
| Package dunder version | `src/ot_command/__init__.py` still says `0.1.0` |
| Manifest display name | still says Command Center **v1** |
| Seed | `20260910`, generated `2026-09-10` |
| Out of bounds | `restricted_answer_key/` is not in the tree and must not be used |

Suggested investigation path (from `AGENTS.md`): inventory → topology → asset identity → telemetry quality → process dependencies → cyber/safety context → recovery → authority → evals → bounded intervention.

---

## 3. Current state

### 3.1 What is implemented

```text
CSV / JSONL files  -->  repository.rows/jsonl  -->  diagnostics counters
SQLite ot_legacy.db -->  never queried by the app
FastAPI            -->  /health, /diagnostics   (needs fastapi; not installed here)
CLI                -->  diagnostics JSON        (stdlib; runs here)
legacy/risk.py     -->  unused by API; covered by expected-failure tests
core/policy.py     -->  unused by API; one unit test
```

| Module | Lines | Behavior |
|---|---|---|
| `src/ot_command/__init__.py` | 1 | `__version__ = "0.1.0"` |
| `src/ot_command/api.py` | 7 | FastAPI 2.0.0, two GET routes |
| `src/ot_command/cli.py` | 7 | Prints diagnostics JSON |
| `src/ot_command/repository.py` | 7 | CSV/JSONL loaders; no joins, no SQLite |
| `src/ot_command/diagnostics.py` | 25 | 14 independent counters |
| `src/ot_command/legacy/risk.py` | 13 | CVSS sort, backup-flag recovery, severity-only isolation |
| `src/ot_command/core/policy.py` | 8 | Action tiers; human approval if tier ≥ 3 |

`legacy_risk_score()` applies a criticality multiplier, but `legacy_rank()` ignores it and sorts on raw CVSS.

There is no UI, no asset API, no identity service, no process graph, no contextual risk model, no recovery graph, and no authority workflow in the running server.

### 3.2 Runnability (this workstation, 2026-09-11)

| Check | Result |
|---|---|
| `py -3` | Python 3.12.0 present |
| `python` | Not on PATH (Windows Store stub) |
| `.venv` | Not present |
| `fastapi` / `uvicorn` / `pytest` | Not installed |
| `py -3 scripts/verify_repo.py` | **VERIFY_OK** |
| `py -3 -m ot_command.cli diagnostics` | **Runs**; returns the 14 counters below |
| `from ot_command.api import app` | **Fails**: `ModuleNotFoundError: No module named 'fastapi'` |
| Makefile `run` / uvicorn | Not startable until `pip install -r requirements.txt` |

After installing requirements, the HTTP surface would still be only `/health` and `/diagnostics`.

### 3.3 Data estate

Counts match `data/manifest.json` unless noted.

| Dataset | Records | Role |
|---|---|---|
| Plants | 18 | NA/EU/APAC/LATAM/MEA; 8 industry types |
| Assets | 2,016 | 13 types; zones L0–L3 + DMZ |
| Asset aliases | 6,048 | CMDB + passive + CMMS per asset |
| Network edges | 3,780 | Documented vs observed vs approved |
| Process units | 216 | Safe states: STOPPED, RECIRCULATE, MIN_LOAD, ISOLATED |
| Process dependencies | 198 | Material-flow and control links |
| Tags | 864 | TEMP / PRESSURE / FLOW / VIBRATION |
| Telemetry | 31,224 | Historian JSONL (~7.1 MB) |
| Vulnerabilities | 1,100 | CVSS, reachability, compensating control |
| Safety barriers | 450 | SIS trip, alarm, permissive, relief, interlock |
| Work orders | 1,250 | CMMS status vs field status |
| Remote access sessions | 700 | Jump host, vendor VPN, RDP, service laptop |
| Cyber alerts | 2,800 | SOC status + optional process context |
| Recovery records | 144 | 8 components × 18 plants |
| Enterprise events | 6,500 | SIEM, MES, IAM, CMMS, SCADA, EAM, vendor portal, passive discovery |
| Shadow inventory | 220 | Spreadsheet **not** in manifest `files` |
| Shadow risk acceptances | 180 | Spreadsheet tracker |
| Shift handover | 1 email | Unstructured operational override |

SQLite `data/ot_legacy.db` (~600 KB) copies six CSV tables. Integrity check passes. Application code never opens it.

### 3.4 Packaging vs product

V2 release engineering is healthier than the product:

- Verifier covers compile, JSON, CSV shape, SQLite integrity, required files, banned-term scan
- `VERIFICATION.md` records VERIFY_OK, 3 passed / 3 xfailed tests, diagnostic counts
- `checksums.sha256` is integrity evidence, not a regulatory signature
- Dockerfile / Makefile / `.env.example` exist; `.env` values are not read by the app
- `scripts/generate_data.py` only checks that manifest files exist; it does not generate data
- `evals/golden_cases.jsonl` (6 cases) are prompt contracts, not pytest
- OpenAPI `asset_api_v1.yaml` / `v2.yaml` are not served
- Scenario injects `inject_01.md`–`inject_06.md` are one-paragraph stubs

### 3.5 Diagnostic baseline (reproduced)

| Signal | Count |
|---|---|
| asset_state_conflicts | 200 |
| alias_collisions | 5 |
| undocumented_network_paths | 779 |
| duplicate_telemetry_packets | 120 |
| telemetry_bad_or_uncertain | 4,094 |
| telemetry_unit_mismatches | 47 |
| safety_bypassed_or_degraded | 61 |
| safety_proof_test_due | 73 |
| maintenance_state_conflicts | 244 |
| unapproved_remote_sessions | 137 |
| remote_sessions_without_confirmed_mfa | 128 |
| recovery_stale_or_unknown_backup | 25 |
| recovery_unverified_dependencies | 29 |
| recovery_stale_or_missing_runbooks | 35 |

Tests (from `VERIFICATION.md`, not re-run here because pytest is not installed): **3 passed, 3 xfailed** (CVSS ranking, backup-as-ready, safety-blind isolate).

---

## 4. Main problem

**Cyber state ≠ operational state ≠ safety state ≠ resilience state**, and nothing in the runtime reconciles them before a recommendation is made.

A trustworthy command-center record would bind, for one asset or unit:

1. **Registered state** (CMDB / CMMS / ACTIVE)
2. **Observed state** (passive / historian / OFFLINE, UNSEEN)
3. **Operational interpretation** (field work-order status, shift notes, process context)
4. **Safety state** (barrier mode, proof-test, bypass authority, unit safe-state)
5. **Resilience state** (backup freshness, restore-test age, runbook, verified dependencies)
6. **Decision authority** (who may isolate, who must approve, what is forbidden)

Today those live in separate files. Diagnostics count disagreements. Legacy logic then collapses the world to one number (CVSS), one flag (backup CURRENT), or one alert severity (ISOLATE).

CASCADE-001 is the same problem as a timeline: firmware advisory → unknown firmware → unexpected write → vendor session → historian deviation → alarm → bypassed SIS → SOC says isolate → process engineer says isolation may destabilize the unit. No function in this repo can produce a governed answer to that scene.

---

## 5. Painpoints

### 5.1 Operational / domain

| Pain | Evidence |
|---|---|
| No single identity | 2,016 official IDs + 6,048 aliases; 5 passive collisions map two assets to one name |
| Inventories disagree in coverage | Official 2,016 assets; shadow spreadsheet 220 (11%); handover says the spreadsheet is newer than CMDB for a new gateway |
| Telemetry is not process truth | 4,094 / 31,224 records not GOOD (13.1%); 120 duplicates; 47 °C/°F mismatches |
| Most assets are uninstrumented | Tags cover **182 / 2,016 assets (9%)**. 1,834 assets have no process join |
| Alerts lack process meaning | 1,735 / 2,800 alerts (62%) have `process_context=UNKNOWN`, including 525 HIGH/CRITICAL |
| Vulnerability semantics are broken | 540 / 1,100 findings have severity labels that contradict CVSS bands; 53 CVSS ≥ 9.0 are `network_reachable=NO` |
| Safety vs security conflict | 61 barriers bypassed/degraded; 73 proof-test due/overdue; 18 bypasses not authorized; isolation ignores this |
| Maintenance truth is split | 244 work orders CLOSED in CMMS but not RETURNED_TO_SERVICE in the field; 94 temporary bypasses |
| Remote access is not a control | 137 sessions outside approved window; 128 without confirmed MFA; 140 identity=`unknown` |
| Recovery is a label | 119 backups marked CURRENT; **108 of those** have restore tests older than 90 days |
| Shadow authority | 180 risk acceptances; **131 expired** as of 2026-09-11; **170 / 180** `plant_id` values do not match the asset’s plant |
| Autonomy requested, authority unused | Policy tiers exist; no API path consults them |

### 5.2 Engineering / workflow

- Named “command center,” ships two read-only endpoints.
- `generate_data.py` is a presence check, not a generator.
- Diagnostics load full telemetry JSONL into memory; enterprise events, vulns, alerts, process graph are unused by that path.
- `pyproject.toml` has no `[build-system]` and no dependencies; runtime deps live only in `requirements.txt`.
- `hashlib` imported in `verify_repo.py` and unused.
- Evals and the KPI catalogue are not wired to CI, so modernization cannot prove improvement yet.
- README/Makefile assume `python`; this environment needs `py -3`.

---

## 6. Inconsistencies

Keep two classes separate (`docs/07_v2_audit_and_changelog.md`): **intentional brownfield evidence** vs **accidental release defects**. Do not silently clean the first class.

### 6.1 Intentional domain inconsistencies

**Identity / configuration (L4)**

- 200 assets registered ACTIVE while observed OFFLINE (90) or UNSEEN (110); plus 120 ACTIVE + INTERMITTENT
- 99 registered RETIRED but observed ONLINE
- 122 registered UNKNOWN; 343 owners Unknown
- Five colliding passive aliases, e.g. `PLT-01-DCS_CONTROLLER-105` → `OT-00012` and `OT-00033`
- `COLLIDE-00`-style CMDB names look like collisions but are unique; the real collisions are the five duplicated passive names

**Network / protocol (L2)**

- 983 undocumented edges; **779 observed in last 24h**
- 204 unapproved paths; 168 of those still observed
- 240 `approved_path=UNKNOWN`
- 648 approved paths not observed in 24h
- Ten protocols in parallel (DNP3, ModbusTCP, EtherNetIP, PROFINET, PROFIBUS, OPC DA/UA, IEC 104/61850, VendorSerial)

**Purdue placement is scrambled**

| Asset type | Typical expectation | Observed |
|---|---|---|
| SAFETY_PLC | L0/L1 | 89 / 162 outside L0/L1, including 30 in DMZ |
| SENSOR | L0 | spread across L0–L3 + DMZ |
| HISTORIAN | L2/L3 | 36 in L0_FIELD |
| ENG_WORKSTATION | L2/L3 | 40 in L0_FIELD, 22 in DMZ |

**Telemetry (L3)**

- Quality: GOOD 27,130 / UNCERTAIN 2,743 / BAD 1,351
- 47 TEMP tags in `F` while the tag catalogue unit is `C`
- Contract omits `ingest_time`, `source`, `asset_id` that the data and EVAL-004 already use
- Enterprise events: **407 / 6,500** have `received_time` before `event_time` (clock skew)

**Process (L5)**

- 51 / 198 dependencies undocumented; **33 of those are marked critical**
- Process units have no `asset_id`; the only join to assets is via tags (182 assets)

**Cyber (L6)**

- Example: `VUL-00001` HIGH / CVSS 5.2 / not reachable / MITIGATED. `VUL-00003` MEDIUM / CVSS 9.2 / reachable / OPEN
- 799 OPEN findings; 409 OPEN and HIGH/CRITICAL
- Compensating control NONE or UNKNOWN on 457 findings

**Safety (L7)**

- ACTIVE 389 / DEGRADED 35 / BYPASSED 26
- Proof test CURRENT 377 / DUE 29 / OVERDUE 44
- `bypass_authorized` YES 136 / NO 157 / UNKNOWN 157
- 10 SIS_TRIP barriers not ACTIVE
- Shift email: Unit 04 bypass still visible; do not isolate near minimum stable load

**Operations (L8)**

- 244 CMMS-closed orders not returned to service
- 938 / 1,250 work orders have `opened_at` after 2026-09-11 (future relative to analysis date)

**Enterprise (L9)**

Plant region vs timezone is frequently implausible (e.g. `PLT-01` NA with `UTC+5:30`, `PLT-07` EU with `UTC-5`). Nine enterprise sources emit overlapping event types with payload states that may not match asset observed_state.

**Resilience (L10)**

- `legacy_recovery_ready("CURRENT")` is true even when restore test is hundreds of days old (`PLT-01` HISTORIAN last test 657 days, backup CURRENT)
- Manual fallback NO on 42 component records
- Asset `backup_age_days` max 420; 1,581 assets > 90 days; unused by recovery logic

**Authority (L12)**

- Risk tracker plant_id is wrong for 170 / 180 rows
- 41 acceptances owned by Unknown
- Unknown policy actions default to tier 4 (restrictive), but nothing calls the policy on a live path

### 6.2 Accidental engineering inconsistencies (safe to fix)

| Item | Detail |
|---|---|
| Package version | `0.1.0` vs release `2.0.0` |
| Manifest name | still labeled v1 |
| Dual store | unused SQLite copy of CSVs |
| Manifest completeness | shadow files exist on disk but are omitted from `files[]` |
| OpenAPI vs app | v1 vs v2 field names; neither endpoint exists |
| Telemetry schema | behind the data and behind EVAL-004 |
| Generator name | does not generate |
| Policy unused | cannot fail closed in the API |
| `legacy_risk_score` unused | ranking does not use the only criticality-aware function |
| Python entry | README `python` vs this host `py -3` |
| Deps not installed | HTTP app not runnable until pip install |

---

## 7. Complexity

Complexity is integrative, not algorithmic. Volume is modest (telemetry ~7 MB). Cognitive load is high because **joins are missing and keys are unstable**.

| Layer | Primary sources | Used by running code? |
|---|---|---|
| L1 Software | `legacy/risk.py`, hard-coded rules | Yes (the defect) |
| L2 OT/protocols | assets.protocol, network_edges | Undocumented-path counter only |
| L3 Telemetry | tags, tag_telemetry.jsonl, enterprise_events | Duplicates/quality/units only; events unused |
| L4 Asset/config | assets, aliases, shadow inventory | State conflicts + alias collisions; shadow unused |
| L5 Process | process_units, process_dependencies, tags | **Unused** |
| L6 Cyber | vulnerabilities, cyber_alerts | **Unused** (legacy rank in tests only) |
| L7 Safety | safety_barriers, unit.safe_state | Bypass/proof-test counts |
| L8 Operations | work_orders, shift email | CMMS vs field; email unused |
| L9 Enterprise | enterprise_events, vendors | **Unused** |
| L10 Recovery | recovery_readiness, backup_age_days | Backup/runbook/deps counters |
| L11 Decision intel | alerts, evals, CASCADE-001 | **Unused** |
| L12 Autonomy | policy.py, docs/06 | Test only |

Hidden complexity:

- Asset ↔ unit is available only where tags exist (9% of assets)
- Plant, unit, and asset each have independent `criticality`; nothing reconciles them
- Enterprise `correlation_id` exists but is not used to stitch an incident
- Diagnostics unit check only covers `*_TEMP` vs `C`

Code cyclomatic complexity is low. Operational risk if trusted is high.

---

## 8. Dependencies

### 8.1 Runtime / packaging

| Dependency | Version | Role |
|---|---|---|
| Python | ≥ 3.11 declared; 3.12.0 observed | Runtime |
| fastapi | 0.115.0 | HTTP (not installed here) |
| uvicorn | 0.30.6 | ASGI (not installed here) |
| pydantic | 2.9.2 | Transitive; unused in app code |
| pytest | 8.3.3 | Tests (not installed here) |

Data access is stdlib only (`csv`, `json`, `pathlib`). SQLite is used by the verifier, not by the app. Named OT/IT systems (SCADA, CMMS, SIEM, IAM/PAM, MES, ERP) are **files**, not integrations. No production credentials belong in `.env.example`.

### 8.2 Join path required for one HIGH alert

```text
cyber_alerts.asset_id
    → assets (observed vs registered, zone, firmware, owner, criticality)
    → asset_aliases (collision check)
    → network_edges (reachability / undocumented path)
    → vulnerabilities (open findings)
    → tags (if any) → process_units.safe_state
    → process_dependencies (downstream units)
    → safety_barriers on that unit
    → work_orders (bypass / field status)
    → remote_access_sessions (active vendor)
    → recovery_readiness (plant + component)
    → shadow risk tracker (often wrong plant)
    → shift_handover_email (unstructured override)
    → enterprise_events (clock-skewed corroboration)
```

Missing edges: no asset→unit foreign key; no alert→barrier link; recovery is plant+component, not asset-level.

### 8.3 Hidden operational dependencies

- 33 undocumented **critical** unit dependencies
- Recovery `dependency_verified` NO/UNKNOWN on 29 plant-components
- Vendor access methods in `vendors.csv` do not constrain `remote_access_sessions.method`
- Manual fallback NO on 42 records: isolation may have no documented degraded-operation path

### 8.4 Authority model (documented, not enforced in the API)

| Tier | Examples | Autonomy |
|---|---|---|
| 0 | observe, correlate, summarize | Allowed |
| 1 | recommend | Allowed with evidence |
| 2 | fresh telemetry, ticket, extra logging | Policy-controlled, reversible |
| 3 | isolate, remote-access change, firewall | Human-authorized |
| 4 | PLC write, setpoint, SIS, interlock bypass | Out of scope / forbidden |

CASCADE-001 is a tier-3 decision with tier-4 temptation. Code cannot execute tiers 2–4; `legacy_isolation_recommendation` still verbalizes ISOLATE without checking L5/L7/L10/L12.

### 8.5 Test / eval gap

Golden cases require evidence, reachability, safety, restore tests, and bounded autonomy. Pytest does not load `evals/golden_cases.jsonl`. Baseline tests only assert counts `> 0`. A ranking “fix” could still fail EVAL-002–005 without CI noticing.

---

## 9. What “good” would have to change

Preserve evidence. Do not treat CMDB, passive discovery, historian, SCADA, CMMS, SIEM, or operator notes as canonical by name. Build evals before agents. No controller writes.

1. **Identity reconciliation** — canonical key plus competing aliases, collision graph, confidence, source freshness.
2. **Join model** — asset ↔ unit ↔ tag ↔ barrier ↔ recovery component, with explicit unknown where tags are missing (91% of assets).
3. **Contextual risk** — reachability, unit criticality, compensating control, barrier state, recovery executability. Highest CVSS must not win by default.
4. **Safety-aware recommendations** — isolation is a proposal; require safe-state, bypass aging, and human tier ≥ 3.
5. **Recovery graph** — backup flag ∧ restore-test freshness ∧ runbook ∧ verified deps ∧ manual fallback.
6. **Executable evals** — promote `golden_cases.jsonl` into tests before changing `legacy/*`.
7. **KPI before/after** — `docs/05_kpis_baseline.md` lists measures; none are computed in code.
8. **Accidental fixes only** — version alignment, schema completeness, SQLite/API honesty, installable venv. Do not “clean” seeded contradictions.

To run the HTTP probe after that:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH='src'
py -3 -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

---

## 10. Bottom line

| Question | Answer |
|---|---|
| Current state | Verified v2 **simulation package**: rich, deliberately messy OT evidence lake + a thin diagnostic probe |
| Runnable here? | CLI diagnostics and verifier: yes. HTTP app and pytest: not until dependencies are installed |
| Working command center? | No. Two read-only routes / one CLI command |
| Main problem | No reconciled cyber-physical decision object |
| Main painpoint | Autonomy is desired; ranking, recovery, and containment are one-dimensional and unsafe to trust |
| Inconsistencies | Domain mess is the curriculum; version/SQLite/schema/eval/install wiring is leftover engineering debt |
| Complexity | Low code complexity, high join/authority/safety complexity |
| Dependencies | File-backed sources that barely reference each other; process and recovery graphs are partial; policy is inert |
| Safe next move | Evidence-preserving identity + context model + evals; still no live writes, SIS changes, or unattended isolation |

This repository is working as a brownfield **problem statement**. It is not yet a command center.
