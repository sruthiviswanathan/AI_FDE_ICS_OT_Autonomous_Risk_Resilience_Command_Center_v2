# Repository Analysis: ICS/OT Autonomous Risk & Resilience Command Center (v2)

**Project name:** AI FDE ICS/OT Autonomous Risk & Resilience Command Center  
**Package:** `ai-fde-ics-ot-command-center` version **2.0.0**  
**Repository type:** Synthetic, locally runnable brownfield simulation for AI Forward-Deployed Engineering  
**Analysis date:** 11 September 2026  
**Source:** Evidence from repository docs, source, tests, contracts, scenarios, and data manifests — not inferred from names alone.

---

## 1. What this project is

This repository is a **fictional multinational industrial control system (ICS) / operational technology (OT) estate**. It is built as a **brownfield discovery and modernization engagement**, not as a greenfield product rewrite.

Leadership in the fictional company wants an “autonomous risk and resilience command center.” The estate already produces many dashboards, but **no single system holds a trusted cyber-physical truth**. Plants, inventories, historians, safety systems, CMMS/EAM, SOC/SIEM, vendor access logs, and operator notes **disagree** about:

- what assets exist
- what state those assets are in
- how cyber findings map to physical process consequences
- which safety barriers are actually active
- whether recovery plans can be executed

The participant’s job is to do **forensics first**, then propose bounded AI. The repo is the messy inherited system-under-study.

**This is not a live plant.** All names, sites, vendors, and records are synthetic. The API is read-only. No code writes to PLCs, changes SIS, bypasses interlocks, or connects to real industrial equipment.

---

## 2. The core idea the project is discussing

The central forensic tension is:

> **Cyber state ≠ Operational state ≠ Safety state ≠ Resilience state**

A high CVSS score is not automatically the highest operational risk. An asset marked ACTIVE in a CMDB may be OFFLINE or UNSEEN in the field. A backup flagged CURRENT may have a stale restore test. A HIGH/CRITICAL cyber alert must not automatically trigger isolation if isolation would destabilize a process unit or conflict with safety.

The project trains engineers to separate five kinds of truth:

| Kind of state | Meaning |
|---|---|
| Observed state | What sensors, discovery, or field evidence show now |
| Registered state | What CMDB, CMMS, diagrams, or tickets claim |
| Operational interpretation | How operators and process engineers read the plant |
| Safety state | SIS, interlocks, alarms, trips, bypasses, proof tests |
| Decision authority | Who is allowed to act, and under what policy |

Every layer should be inspected for **imperfection, inconsistency, friction, complexity, volatility, uncertainty, hidden dependency, and unknown unknowns**.

---

## 3. Fictional industrial estate

The company operates **18 plants across five regions**: NA, EU, APAC, LATAM, and MEA. Plant types include chemicals, pharma, food, water, power, metals, oil & gas, and automotive. Maturity is mixed: **legacy, mixed, and modernizing**.

Seeded inventory (from `data/manifest.json`, seed `20260910`):

| Dataset | Count |
|---|---|
| Plants | 18 |
| Assets | 2,016 |
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

Observed asset types in `data/raw/assets.csv` include PLC, DCS controller, safety PLC, RTU, IED, HMI, historian, OPC server, gateway, engineering workstation, network switch, sensor, and VFD. Zones and protocols are mixed (for example DNP3, PROFINET, IEC 61850, IEC 104).

Parallel “shadow” sources exist on purpose:

- `data/shadow/ot_asset_inventory_FINAL_v8.csv` — a spreadsheet inventory that can be newer than the official CMDB
- `data/shadow/risk_acceptance_tracker.csv` — deferred/accepted risks with expiry and informal rationale
- `data/shadow/shift_handover_email.txt` — operator notes: vendor work without a ticket, a “temporary” safety bypass, historian/HMI disagreement, and a warning not to isolate a controller near minimum stable load

These shadow files exist to prove that **official systems are not authoritative by name alone**.

---

## 4. The L1–L12 imperfection model

The estate is organized as twelve brownfield layers. Participants are expected to find imperfections in each, not just “fix the cyber dashboard.”

1. **L1 — Software / Engineering Logic** — duplicated rules, hard-coded risk thresholds, weak tests, stale scripts.
2. **L2 — OT Systems / Protocols** — mixed PLC/DCS/SCADA/HMI/historian/gateway generations and protocol drift.
3. **L3 — Data / Telemetry** — missing/duplicate/stale tags, unit mismatches, quality flags, clock drift, weak provenance.
4. **L4 — Asset / Configuration** — competing inventories, aliases, firmware mismatches, undocumented devices.
5. **L5 — Physical Process / Control** — unit dependencies, abnormal states, safe-state constraints, cyber-physical causality.
6. **L6 — Cyber Risk / Exposure** — CVSS disconnected from reachability, process criticality, safety, and recovery.
7. **L7 — Safety / Protection** — SIS, alarms, trips, bypasses, proof-test overdue; security response can fight process safety.
8. **L8 — Operations / Maintenance** — work orders vs field reality, overrides, contractors, temporary changes.
9. **L9 — Enterprise / IT-OT Ecosystem** — SOC/SIEM, CMMS/EAM, ERP/MES, IAM/PAM, vendors each hold partial truth.
10. **L10 — Resilience / Recovery** — stale backups, untested restore paths, missing runbooks, unverified dependencies.
11. **L11 — Decision Intelligence Gaps** — alert overload, weak contextual ranking, poor causality, uncertainty ignored.
12. **L12 — Autonomy / Safety / Assurance** — authority boundaries, HITL, TEVV, explainability, audit, governance.

---

## 5. Current-state architecture

Documented current-state flow (`docs/03_current_state_architecture.md`):

```text
Enterprise IT / SOC / IAM / ERP
             |
            DMZ
      /       |        \
 Historian  Jump Host  MES Bridge
     |         |          |
    SCADA ---- Engineering -- CMMS/EAM
     |            |
  PLC/DCS ------ Gateways
     |            |
  Sensors      Field Devices
     |
 Physical Process
```

Alongside that Purdue-like stack sit **undocumented paths**: vendor VPNs, service laptops, spreadsheets, shift notes, and stale diagrams. There is **no single system of cyber-physical truth** and **no verified end-to-end recovery graph**.

API contracts themselves are inconsistent: `contracts/asset_api_v1.yaml` uses `assetId` / `fwVersion` / `operationalState`, while `contracts/asset_api_v2.yaml` uses `asset_id` / `firmware` / `observed_state`. That is intentional integration debt.

---

## 6. What the software actually does today

The packaged application is small and deliberately limited.

### Runtime surfaces

- **CLI:** `python -m ot_command.cli diagnostics` prints JSON counts of seeded imperfections.
- **Read-only API:** FastAPI app `ot_command.api:app` with `/health` and `/diagnostics` only. Health reports `mode: synthetic-read-only`.
- **Repository layer:** CSV/JSONL readers over local files. No live OT connectors.
- **Policy:** `src/ot_command/core/policy.py` defines action tiers 0–4. Observe/correlate/summarize are autonomous. Isolation, remote-access changes, and firewall changes require a human. PLC writes, setpoint changes, SIS modifications, and interlock bypasses are out of scope.

### Intentionally broken legacy logic

`src/ot_command/legacy/risk.py` is labeled “intentionally simplistic”:

- **Risk ranking** sorts by CVSS alone and ignores process/safety/recovery context.
- **Recovery ready** is true whenever `backup_status == "CURRENT"`, ignoring restore-test freshness, runbooks, and dependencies.
- **Isolation** recommends `ISOLATE` for HIGH/CRITICAL alerts with no safety check.

These are **not accidental bugs**. Tests in `tests/test_known_legacy_defects.py` are marked `xfail` with stated rationale. V2 treats accidental packaging/import defects as release blockers, but **preserves authentic brownfield contradictions**.

### Baseline diagnostics already visible in the data

From `VERIFICATION.md` (seeded findings detected by `run_diagnostics()`):

| Finding | Count |
|---|---|
| Asset state conflicts (ACTIVE registered, OFFLINE/UNSEEN observed) | 200 |
| Alias collisions | 5 |
| Undocumented network paths (not documented, seen in last 24h) | 779 |
| Duplicate telemetry packets | 120 |
| Telemetry bad or uncertain | 4,094 |
| Telemetry unit mismatches | 47 |
| Safety bypassed or degraded | 61 |
| Safety proof test due | 73 |
| Maintenance state conflicts (CMMS closed, field not returned) | 244 |
| Unapproved remote sessions | 137 |
| Remote sessions without confirmed MFA | 128 |
| Recovery stale or unknown backup | 25 |
| Recovery unverified dependencies | 29 |
| Recovery stale or missing runbooks | 35 |

---

## 7. Safety, authority, and what must never be automated

Allowed autonomous behavior: **collect, correlate, enrich, summarize, rank evidence, run read-only simulation**.

Possibly policy-controlled and reversible in a real implementation: request fresh telemetry, open a ticket, increase logging, capture evidence.

Human-authorized only: network isolation, remote-access changes, firewall policy, maintenance-mode transitions.

**Out of scope for this repository and generally highly restricted:**

- PLC logic writes
- setpoint changes
- SIS modifications
- interlock bypass
- trip suppression
- unsafe restart / live controller writes

Every recommendation is expected to expose **evidence, freshness, uncertainty, process impact, safety impact, rollback, and required authority**.

---

## 8. What participants are supposed to produce

From `participant/CHALLENGE_BRIEF.md` and `AGENTS.md`, this is a production brownfield engagement. Suggested investigation path:

**inventory → topology → asset identity → telemetry quality → process dependencies → cyber/safety context → recovery dependencies → decision/authority model → evals → intervention**

Expected deliverables:

1. Current-state map
2. Top engineering imperfections across L1–L12
3. Asset identity reconciliation
4. Telemetry quality findings
5. Process/asset dependency model
6. Contextual risk model (not CVSS-only)
7. Safety/security conflict handling
8. Resilience/recovery graph
9. Target architecture
10. Bounded-autonomy model
11. Evaluation / TEVV strategy
12. KPI before/after model
13. 90-day roadmap
14. Executive defense

`restricted_answer_key/` is out of bounds. V2 removed restricted answer-key material from the distributable tree.

Target capabilities (`docs/04_target_capabilities.md`) may include canonical identity, provenance-aware telemetry, process dependency, contextual risk, safety-aware response, recovery graphs, evidence/knowledge models, predictive degradation, read-only digital twin, and bounded decision agents. **KG, digital twin, RAG, and agents are not automatically correct** — use them only when evidence shows they solve a real problem.

---

## 9. Scenarios, evals, and how “good” is judged

### Exercise injects

Six tabletop injects force multi-consequence reasoning after initial discovery:

| Inject | Theme |
|---|---|
| 01 | Inventory mismatch |
| 02 | Historian quality degradation |
| 03 | Unapproved vendor session |
| 04 | Safety bypass aging |
| 05 | Regional SCADA outage |
| 06 | Restore failure during a recovery drill |

Each inject requires assessment of **cyber, process, safety, operational, and resilience** consequences, evidence gaps, and an authority-bounded response.

### Cascade scenario

`scenarios/cascade_001.json` is a timed cyber-physical ambiguity case: firmware advisory → unknown firmware → unexpected write alert → active vendor session → historian deviation → operator alarm → bypassed safety barrier → SOC wants isolation → process engineer warns isolation may destabilize the unit. The command center must reconcile evidence, not blindly isolate.

### Evals / TEVV

`evals/golden_cases.jsonl` encodes six gates:

| Case | Type | Must include | Must not |
|---|---|---|---|
| EVAL-001 | Identity | evidence, source, confidence | assume CMDB always correct |
| EVAL-002 | Risk | reachability, process criticality, safety, controls, recovery | rank by CVSS alone |
| EVAL-003 | Safety | process consequence, safe-state, human authority | automatic PLC isolation |
| EVAL-004 | Temporal | event time, ingest/received time, uncertainty | blind sort on received time |
| EVAL-005 | Recovery | restore test, runbook, dependencies, manual fallback | “backup exists therefore recoverable” |
| EVAL-006 | Authority | bounded autonomy, approval, audit | SIS change, setpoint write |

Baseline KPIs (`docs/05_kpis_baseline.md`) include inventory disagreement, unknown/unowned assets, telemetry quality, time to contextualize an OT alert, safety-bypass aging, restore-test freshness, false-positive escalation, decision evidence completeness, human approval latency, and AI cost per analyzed incident.

---

## 10. Repository layout

| Path | Role |
|---|---|
| `README.md`, `AGENTS.md`, `VERIFICATION.md` | Engagement rules, safety, release evidence |
| `docs/` | Domain, L1–L12, architecture, target capabilities, KPIs, assurance, v2 changelog |
| `participant/` | Challenge brief and discovery checklist |
| `data/raw/`, `data/telemetry/`, `data/reference/` | Official-looking synthetic sources |
| `data/shadow/` | Informal/competing truth (spreadsheet, risk tracker, handover email) |
| `data/ot_legacy.db` | SQLite copy of the estate |
| `src/ot_command/` | CLI, API, diagnostics, repository, policy, legacy risk |
| `contracts/` | Conflicting v1/v2 asset APIs and telemetry schema |
| `scenarios/` | Injects and cascade timeline |
| `evals/` | Golden cases / TEVV starter set |
| `tests/` | Baseline assertions plus expected-failure legacy tests |
| `scripts/` | Manifest check (`generate_data.py --check-only`) and `verify_repo.py` |
| `tools/inspect_repo.py` | Convenience diagnostics dump |
| `Dockerfile`, `Makefile`, `.env.example` | Local/container run |

Python requirement is **>= 3.11**. Dependencies are FastAPI, Uvicorn, Pydantic, and pytest only.

Quick start:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_data.py --check-only
python -m ot_command.cli diagnostics
pytest -q
# optional: uvicorn ot_command.api:app --reload
```

V2 verification recorded: structural verifier **VERIFY_OK**, compile/import **PASS**, SQLite integrity **PASS**, JSON/CSV checks **PASS**, 3 tests passed / 3 expected failures, no real control endpoints configured.

---

## 11. What this project is *not*

- Not a production OT command center connected to real plants.
- Not a mandate to deploy agents, a knowledge graph, RAG, or a digital twin by default.
- Not a CVE-scoring contest. Highest CVSS is not highest operational risk.
- Not permission to write to controllers, change SIS, or isolate networks autonomously.
- Not a clean dataset. Inconsistencies are **evidence**, not dirt to silently clean.

---

## 12. Bottom line

This repo is a **teaching and assessment environment** for AI Forward-Deployed Engineers working a messy ICS/OT brownfield.

It discusses one problem from many angles: **how to build trustworthy cyber-physical situational awareness and governed recommendations** when inventories conflict, telemetry is dirty, safety and security disagree, recovery is unverified, and autonomy must stay bounded.

The inherited baseline “works well enough to operate,” but it is full of conflicting inventories, stale configurations, weak contextual risk, undocumented bypasses, recovery gaps, shadow processes, and fragmented authority. Modernization starts with **evidence**, **tests/evals**, and **human authority** — then, and only then, bounded AI.

---

*All findings above are drawn from repository files. This analysis does not recommend live controller writes, SIS changes, interlock bypasses, or unsafe isolation.*
