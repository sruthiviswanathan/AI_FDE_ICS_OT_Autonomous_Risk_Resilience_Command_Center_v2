# Consolidated ICS/OT Repo Analysis — Single Source of Truth

**Estate:** AI FDE ICS/OT Autonomous Risk & Resilience Command Center v2  
**Package:** `ai-fde-ics-ot-command-center` **2.0.0**  
**Evidence date:** 11 September 2026 · data seed `20260910`  
**Status:** Team-usable consolidation of two independent analyses of the same repository  
**Safety bound:** Synthetic, locally runnable estate only. Highest CVSS is not highest operational risk. No recommendation here authorizes PLC writes, SIS changes, interlock bypasses, or unsafe isolation.

---

## How to read this document

Two members analyzed the **same** repository. Their facts do not compete. They cover different jobs:

| Tag | Source file | What that analysis is |
|---|---|---|
| <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span> | Agreed by both | Same claim, usually same number |
| <span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span> | `REPO_PROJECT_SUMMARY.md` | Repo / product briefing: what the package is, how to run it, layout, injects, evals, verification |
| <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span> | `08_legacy_forensic_analysis_HS.md` | Forensic pass: eight-lens review, joins on `data/raw`, pain counts, 90-day path, KPI numerators |
| <span style="background:#EDE9FE;color:#5B21B6;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A→B</span> | Shared fact, B more precise | Same diagnostic; B splits, qualifies, or joins it. **Not a contradiction.** |

Plain-text fallback if HTML colors do not render: **[BOTH]** · **[A]** · **[B]** · **[A→B]**.

**No seed-count conflict was found.** Where A says “779 undocumented paths” and B says “983 undocumented / 779 live in last 24h”, B is decomposing A’s diagnostic, not disagreeing with it.

---

## 0. Comparison at a glance

### What each file actually is

- **[A]** answers: *what is this repo, what does the software do, how is it laid out, how do we run and judge it?*
- **[B]** answers: *what is broken in the estate, with evidence counts, across eight forensic lenses, and how do we modernize without writing to controllers?*
- **[BOTH]** agree on the problem, the five kinds of truth, the L1–L12 model, the three legacy defects, the authority bounds, CASCADE-001, and the seeded inventory totals.

### Similar (overlap)

Both describe a **synthetic multinational ICS/OT brownfield**, not a live plant. Leadership wants an autonomous command center; what exists is **no trusted cyber-physical truth**. Both use the same core tension:

> **Cyber state ≠ Operational state ≠ Safety state ≠ Resilience state**

Both separate **observed / registered / operational interpretation / safety / decision authority**. Both refuse CVSS-as-risk, automatic isolation, and controller writes. Both cite the same seed inventory (18 plants, 2,016 assets, 31,224 telemetry records, and the rest of the manifest table) and the same `VERIFICATION.md` diagnostic block.

### Delta (what only one file gives you)

| If you only read A you miss | If you only read B you miss |
|---|---|
| Package identity, CLI/API runtime, repo tree, quick start, Python ≥ 3.11 | Eight-lens forensic model and L1–L12 × lens heatmap |
| Architecture ASCII (Purdue-like) | Plant maturity **7 legacy / 5 modernizing / 6 mixed**; criticality **13 HIGH / 5 MEDIUM** |
| Six inject table (01–06) and eval must-include / must-not table | CASCADE-001 **minute-by-minute** (08:01–08:55) |
| V2 verification: VERIFY_OK, 3 pass / 3 xfail | Forensic joins: CVSS vs reachability, restore-test age, zone violations, unknown fields |
| “What this project is not” | 90-day phased roadmap with exit gates |
| Dockerfile / Makefile / `ot_legacy.db` / restricted answer key | Moonshots vs unsafe closed-loop; version `0.1.0` vs `2.0.0` vs manifest v1 |
| Asset-type and protocol examples | KPI **numerators** already measurable on this seed |

### Bottom line for the team

Use **this file** as the working brief. Treat **A** as the onboarding / repo map and **B** as the evidence appendix that already did the joins. Modernization still starts with evidence, tests/evals, and human authority — then bounded recommenders. The first move is a **conflict-preserving identity and evidence layer**, not an agent. **[B]**

---

## 1. Provenance matrix — topic by topic

| Topic | A | B | How to use it |
|---|:---:|:---:|---|
| Synthetic brownfield estate, not a live plant | Y | Y | **[BOTH]** |
| Core 4-state tension | Y | Y | **[BOTH]** |
| Five kinds of truth | Y | Y | **[BOTH]** |
| 18 plants, 5 regions, 8 industry types | Y | Y | **[BOTH]**; B adds maturity/criticality split |
| Seed inventory table (plants→events) | Y | Y | **[BOTH]** — identical counts |
| Shadow spreadsheet / risk tracker / handover email | Y | Y | **[BOTH]**; B adds coverage 220/2,016 and 131 expired acceptances |
| L1–L12 layer list | Y | Y | **[A]** names each layer; **[B]** scores each vs eight lenses |
| Current-state architecture diagram | Y | — | **[A]** |
| Undocumented vendor VPN / laptop / spreadsheet paths | Y | Y | **[BOTH]** |
| API v1 vs v2 field names | Y | Y | **[BOTH]** |
| Runtime CLI + FastAPI `/health` `/diagnostics` | Y | — | **[A]** |
| `legacy/risk.py` three defects + xfail tests | Y | Y | **[BOTH]** |
| `VERIFICATION.md` diagnostic counts | Y | Y | **[BOTH]**; **[A→B]** B splits several totals |
| Policy tiers 0–4 | Y | Y | **[A]** prose; **[B]** table from `policy.py` |
| Forbidden: PLC / SIS / interlock / trip suppress | Y | Y | **[BOTH]** |
| 14 participant deliverables | Y | Y | **[BOTH]**; B adds “why it exists in this estate” |
| Six tabletop injects | Y | — | **[A]** |
| CASCADE-001 story | Y | Y | **[A]** summary; **[B]** timed table |
| EVAL-001..006 gates | Y | Y | **[A]** full must/must-not table; B cites them |
| Repo layout, quick start, verification PASS | Y | — | **[A]** |
| “What this project is not” | Y | — | **[A]** |
| Eight forensic lenses + heatmap | — | Y | **[B]** |
| Pain-point table with extra joins | — | Y | **[B]** |
| 90-day roadmap with exit gates | — | Y | **[B]** |
| Moonshots / unsafe closed-loop | — | Y | **[B]** |
| KPI baseline **with numerators** | names only | Y | **[A→B]** |
| Version / schema / `generate_data.py` packaging debt | — | Y | **[B]** |
| First modernization move (identity layer) | implied | Y | **[B]** |

---

## 2. Count reconciliation

Shared diagnostics from `VERIFICATION.md` plus B’s forensic joins. **A and B never disagree on a shared number.**

### 2.1 Identical in both

| Finding | Count | Tag |
|---|---:|---|
| Plants | 18 | **[BOTH]** |
| Regions | 5 | **[BOTH]** |
| Assets | 2,016 | **[BOTH]** |
| Asset aliases | 6,048 | **[BOTH]** |
| Network edges | 3,780 | **[BOTH]** |
| Process units | 216 | **[BOTH]** |
| Process dependencies | 198 | **[BOTH]** |
| Tags | 864 | **[BOTH]** |
| Telemetry records | 31,224 | **[BOTH]** |
| Vulnerability findings | 1,100 | **[BOTH]** |
| Safety barriers | 450 | **[BOTH]** |
| Work orders | 1,250 | **[BOTH]** |
| Remote access sessions | 700 | **[BOTH]** |
| Cyber alerts | 2,800 | **[BOTH]** |
| Recovery records | 144 | **[BOTH]** |
| Enterprise events | 6,500 | **[BOTH]** |
| Asset state conflicts (ACTIVE registered, OFFLINE/UNSEEN observed) | 200 | **[BOTH]** |
| Alias collisions | 5 | **[BOTH]** |
| Duplicate telemetry packets | 120 | **[BOTH]** |
| Telemetry bad or uncertain | 4,094 | **[BOTH]** |
| Telemetry unit mismatches | 47 | **[BOTH]** |
| Safety bypassed or degraded | 61 | **[BOTH]** |
| Safety proof test due / not current | 73 | **[BOTH]** |
| Maintenance state conflicts (CMMS closed, field not returned) | 244 | **[BOTH]** |
| Unapproved remote sessions | 137 | **[BOTH]** |
| Remote sessions without confirmed MFA | 128 | **[BOTH]** |
| Recovery stale or unknown backup | 25 | **[BOTH]** |
| Recovery unverified dependencies | 29 | **[BOTH]** |
| Recovery stale or missing runbooks | 35 | **[BOTH]** |
| Undocumented network paths **observed last 24h** | 779 | **[BOTH]** / **[A→B]** |

### 2.2 A stated a total; B split or joined it

| A (or shared diagnostic) | B refinement | Tag |
|---|---|---|
| Undocumented live paths **779** | 983 undocumented of 3,780; **779** of those observed last 24h; 168 observed with `approved_path=NO`; 240 `approved_path UNKNOWN`; 527 documented but not observed last 24h | **[A→B]** |
| Telemetry bad or uncertain **4,094** | UNCERTAIN 2,743 + BAD 1,351 = **13.1%** of 31,224 | **[A→B]** |
| Safety bypassed or degraded **61** | BYPASSED 26 + DEGRADED 35; 21 unauthorized among bypassed/degraded; 57 ACTIVE barriers with overdue proof test | **[A→B]** |
| Unit mismatches **47** | Temperature samples in °F against engineering unit °C | **[A→B]** |
| Maintenance conflicts **244** | Reverse split also exists: 161 CMMS OPEN/IN_PROGRESS already returned to service | **[A→B]** |
| Process dependencies **198** | 51 undocumented; **33 critical** undocumented | **[B]** |
| Maturity “legacy / mixed / modernizing” | **7 / 5 / 6** plus criticality **13 HIGH / 5 MEDIUM** | **[A→B]** |
| Recovery “CURRENT ⇒ ready is wrong” | 108 of 119 CURRENT backups have restore tests older than 90 days; median restore-test age **379** days (min 13 / max 688); 74 tests older than 365 days; 42/144 no manual fallback | **[A→B]** |
| Shadow inventory exists | Covers **220 / 2,016 (11%)**; overlapping records match firmware/state/owner — coverage gap, not field drift | **[A→B]** |
| Handover: do not isolate near min stable load | Same instruction, used as the safety-vs-cyber proof for CASCADE-001 | **[BOTH]** |

### 2.3 Counts that exist only in B

| Finding | Count | Tag |
|---|---:|---|
| Unknown owners | 343 | **[B]** |
| Alerts with process_context UNKNOWN | 1,735 / 2,800 (62%) | **[B]** |
| HIGH/CRITICAL alerts with unknown process | 525 | **[B]** |
| Alerts SUPPRESSED / OPEN | 683 / 693 | **[B]** |
| Open vulnerabilities | 799 | **[B]** |
| CVSS ≥ 9.0 and not network-reachable | 53 | **[B]** |
| CVSS < 7, reachable, OPEN | 136 | **[B]** |
| OPEN + reachable on CRITICAL assets | 87 | **[B]** |
| HIGH/CRITICAL OPEN + reachable | 147 | **[B]** |
| Severity HIGH with CVSS < 7 / LOW with CVSS ≥ 7 | 144 / 143 | **[B]** |
| Expired risk acceptances (as of 2026-09-11) | 131 / 180 | **[B]** |
| Temporary bypass work orders | 94 | **[B]** |
| Operator workaround active on work orders | 252 | **[B]** |
| Assets with `backup_age_days` > 180 / > 365 | 1,133 / 258 | **[B]** |
| Tags with historian disabled | 51 | **[B]** |
| Enterprise events received before `event_time` | 407 | **[B]** |
| Empty correlation ID on enterprise events | 3,251 | **[B]** |
| Mean historian ingest delay | 120.3 s | **[B]** |
| Telemetry delayed > 60 s | 23,414 / 31,224 | **[B]** |
| Registered state UNKNOWN | 122 | **[B]** |
| Assets observed INTERMITTENT | 129 | **[B]** |
| UNEXPECTED_WRITE / CONFIG_DRIFT / NEW_DEVICE alerts | 404 / 388 / 399 | **[B]** |
| Vuln reachability UNKNOWN / compensating control UNKNOWN / NONE | 344 / 235 / 222 | **[B]** |
| Safety bypass_authorized UNKNOWN | 157 | **[B]** |
| Remote approved UNKNOWN / MFA UNKNOWN | 76 / 72 | **[B]** |
| Unapproved remote **and** no MFA | 23 | **[B]** |
| Unknown remote identity | 140 | **[B]** |
| Remote methods: jump_host / RDP / service laptop / vendor VPN | 182 / 179 / 170 / 169 | **[B]** |
| SAFETY_PLC outside L0/L1 | 89 | **[B]** |
| SENSOR in DMZ / PLC in DMZ / HMI in L0_FIELD | 30 / 29 / 35 | **[B]** |
| Aliases per asset | 3 (CMDB, PASSIVE, CMMS) | **[B]** |
| Units with no manual mode / LIMITED | 19 / 44 | **[B]** |
| Firmware strings / vendors / protocols / asset types / zone labels / business units | 815 / 10 / 10 / 13 / 5 / 6 | **[B]** |

---

## 3. Consolidated analysis (team source of truth)

The rest of this file is the merged brief. Every subsection is tagged so you can see who contributed what.

### 3.1 What this project is  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span>

This repository is a **fictional multinational ICS/OT estate**, built as a **brownfield discovery and modernization engagement**, not a greenfield rewrite.

Leadership wants an “autonomous risk and resilience command center.” The estate already produces many dashboards, but **no single system holds a trusted cyber-physical truth**. Plants, inventories, historians, safety systems, CMMS/EAM, SOC/SIEM, vendor access logs, and operator notes disagree about:

- what assets exist
- what state those assets are in
- how cyber findings map to physical process consequences
- which safety barriers are actually active
- whether recovery plans can be executed without making the unit unsafe

The participant’s job is **forensics first**, then bounded AI. The repo is the messy inherited system-under-study.

<span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span> Package name `ai-fde-ics-ot-command-center` version **2.0.0**. This is a teaching and assessment environment for AI Forward-Deployed Engineers.

**This is not a live plant.** All names, sites, vendors, and records are synthetic. The API is read-only. No code writes to PLCs, changes SIS, bypasses interlocks, or connects to real industrial equipment.

### 3.2 Core forensic tension  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span>

**Cyber state ≠ Operational state ≠ Safety state ≠ Resilience state**

A high CVSS score is not automatically the highest operational risk. An asset marked ACTIVE in a CMDB may be OFFLINE or UNSEEN in the field. A backup flagged CURRENT may have a stale restore test. A HIGH/CRITICAL cyber alert must not automatically trigger isolation if isolation would destabilize a process unit or conflict with safety.

Five kinds of truth must stay separate:

| Kind of state | Meaning |
|---|---|
| Observed state | What sensors, discovery, or field evidence show now |
| Registered state | What CMDB, CMMS, diagrams, or tickets claim |
| Operational interpretation | How operators and process engineers read the plant |
| Safety state | SIS, interlocks, alarms, trips, bypasses, proof tests |
| Decision authority | Who is allowed to act, and under what policy |

<span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span> Registered vocabulary is `ACTIVE` / `UNKNOWN` / `RETIRED`. Observed vocabulary is `ONLINE` / `OFFLINE` / `UNSEEN` / `INTERMITTENT`. They are different languages. Naive string equality fails on all 2,016 assets. The honest operational conflict set is the **200** ACTIVE assets that are OFFLINE or UNSEEN.

Every layer should be inspected for **imperfection, inconsistency, friction, complexity, volatility, uncertainty, hidden dependency, and unknown unknowns**. **[BOTH]** name the lenses; **[B]** uses them as the analysis frame.

### 3.3 Problem to be solved  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span>

The operating failure is not “we need more AI.” No actor — SOC, operations, safety, maintenance, or vendors — can answer, with evidence and uncertainty, the five questions in §3.1.

The goal is **not** to automate control. The goal is trustworthy cyber-physical situational awareness, contextual risk, resilience decisions, and governed action recommendations.

### 3.4 Fictional industrial estate  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span>

18 plants across five regions: NA, EU, APAC, LATAM, MEA. Plant types: chemicals, pharma, food, water, power, metals, oil & gas, automotive.

<span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span> Maturity mix: **7 legacy / 5 modernizing / 6 mixed**. Criticality: **13 HIGH / 5 MEDIUM**. Also: 6 business units, 13 asset types, 10 protocols, 5 zone labels, 10 vendors, 815 firmware strings. Timezones span UTC−5 to UTC+8, so “last 24h” on a network edge is not a global instant.

<span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span> Observed asset types in `data/raw/assets.csv` include PLC, DCS controller, safety PLC, RTU, IED, HMI, historian, OPC server, gateway, engineering workstation, network switch, sensor, and VFD. Example protocols: DNP3, PROFINET, IEC 61850, IEC 104.

Seeded inventory (`data/manifest.json`, seed `20260910`) is the table in §2.1.

Parallel **shadow** sources exist on purpose:

- `data/shadow/ot_asset_inventory_FINAL_v8.csv` — spreadsheet inventory that can be newer than the official CMDB · **[BOTH]** · coverage **220 / 2,016 (11%)** **[B]**
- `data/shadow/risk_acceptance_tracker.csv` — deferred/accepted risks · **[BOTH]** · **131 of 180 expired** by 2026-09-11; 41 owners Unknown; “compensating controls assumed” on 44 **[B]**
- `data/shadow/shift_handover_email.txt` — vendor work without a ticket, a “temporary” safety bypass, historian/HMI disagreement, and a warning **not to isolate a controller near minimum stable load** **[BOTH]**

<span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span> Shadow files are **not** in `manifest.json`’s file list, so a naive pipeline never sees them. Overlapping shadow/CMDB records match firmware/state/owner; the inconsistency is **coverage**, not field drift. Night-shift email says the spreadsheet is newer than CMDB for a new gateway.

These shadow files exist to prove that **official systems are not authoritative by name alone.**

### 3.5 The L1–L12 imperfection model  <span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span> names · <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span> scores

Participants are expected to find imperfections in each layer, not just “fix the cyber dashboard.”

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

#### L1–L12 × eight lenses  <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span>

H = evidence-backed and material. M = present but secondary. L = not the main failure mode in this dataset.

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

### 3.6 Current-state architecture  <span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span> diagram · <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span> undocumented paths

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

API contracts are inconsistent on purpose: `contracts/asset_api_v1.yaml` uses `assetId` / `fwVersion` / `operationalState`; `contracts/asset_api_v2.yaml` uses `asset_id` / `firmware` / `observed_state`.

### 3.7 What the software actually does today  <span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span>

The packaged application is small and deliberately limited.

**Runtime surfaces**

- **CLI:** `python -m ot_command.cli diagnostics` prints JSON counts of seeded imperfections.
- **Read-only API:** FastAPI app `ot_command.api:app` with `/health` and `/diagnostics` only. Health reports `mode: synthetic-read-only`.
- **Repository layer:** CSV/JSONL readers over local files. No live OT connectors.
- **Policy:** `src/ot_command/core/policy.py` defines action tiers 0–4.

Python requirement is **≥ 3.11**. Dependencies: FastAPI, Uvicorn, Pydantic, pytest only.

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

#### Packaging debt that A does not surface  <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span>

- `ot_command.__version__` is `0.1.0` while `pyproject.toml` and the API claim `2.0.0`
- `data/manifest.json` still titles the dataset v1
- Telemetry JSON Schema requires `event_id`, `tag_id`, `event_time`, `value`, `unit`, `quality` but omits `ingest_time`, `asset_id`, and `source` that the JSONL actually carries
- `generate_data.py` does not generate data; it only checks that files exist

V2 treats accidental packaging/import defects as release blockers, but **preserves authentic brownfield contradictions**. **[A]**

### 3.8 Intentionally broken legacy logic  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span>

`src/ot_command/legacy/risk.py` is labeled “intentionally simplistic”:

- **`legacy_rank`** sorts by CVSS alone and ignores process/safety/recovery context.
- **`legacy_recovery_ready`** is true whenever `backup_status == "CURRENT"`, ignoring restore-test freshness, runbooks, and dependencies.
- **`legacy_isolation_recommendation`** returns `ISOLATE` for HIGH/CRITICAL alerts with no safety check.

These are **not accidental bugs**. Tests in `tests/test_known_legacy_defects.py` are marked `xfail` with stated rationale.

**Effect [B]:** wrong actions look automated and confident.

### 3.9 Pain points (evidence-backed)  <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span> table · diagnostics **[BOTH]**

| Pain | Evidence in this repo |
|---|---|
| No trusted inventory | 200 ACTIVE assets observed OFFLINE/UNSEEN; 343 unknown owners; shadow spreadsheet covers 220 of 2,016 assets; 5 colliding aliases |
| Alerts without process meaning | 1,735 of 2,800 alerts have process context UNKNOWN, including 525 HIGH/CRITICAL |
| CVSS theater vs operational risk | Legacy rank sorts by CVSS; 53 findings with CVSS ≥ 9.0 are unreachable; 87 open reachable findings sit on CRITICAL assets |
| Safety-blind cyber response | HIGH/CRITICAL → `ISOLATE`; handover says do not isolate near minimum stable load |
| Ticket vs field | 244 CMMS CLOSED but not returned to service; 161 open/in-progress already returned; 94 temporary bypasses |
| Recovery theater | 108 of 119 CURRENT backups have restore tests older than 90 days; median restore-test age is 379 days |
| Shadow operations | Vendor VPNs, service laptops, `FINAL_v8` spreadsheet, expired risk acceptances (131 of 180) |

Full diagnostic tables: §2.

### 3.10 Eight-lens forensic detail  <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span>

This is the unique analytic spine of the HS forensic review. Keep it; A does not replace it.

#### Imperfection — defective logic that still runs

The three `legacy_*` functions above are still the decision machinery. Packaging versions disagree (`0.1.0` vs `2.0.0` vs manifest v1). 1,133 assets have `backup_age_days` > 180; 258 exceed 365. 51 tags are historian-disabled, so those loops are blind in the only telemetry store.

**Effect:** wrong actions look automated and confident.

#### Inconsistency — locally true, globally false

Besides the 200 state conflicts and v1/v2 API split: 244 + 161 CMMS/field splits; 144 HIGH with CVSS < 7 and 143 LOW with CVSS ≥ 7; 47 °F vs °C; 407 enterprise events received before `event_time`; zone violations (89 SAFETY_PLC outside L0/L1, 30 SENSOR in DMZ, 29 PLC in DMZ, 35 HMI in L0_FIELD).

**Effect:** every system can be “right” in its own schema and still be unusable for a decision.

#### Friction — cost of assembling one decision

Nine enterprise sources emit 6,500 events: SIEM, MES, HISTORIAN, IAM, CMMS, SCADA, EAM, VENDOR_PORTAL, PASSIVE_DISCOVERY. **3,251 have an empty correlation ID.** 62% of alerts lack process context. Mean historian ingest delay 120.3 s; 23,414 / 31,224 samples delayed > 60 s. Remote methods include 170 service laptops and 169 vendor VPNs. Night-shift truth lives in email. CASCADE-001 is this friction compressed into one hour.

**Effect:** time-to-cyber-physical confidence is long; SOC and operations argue from different clocks.

#### Complexity — no single playbook survives a site

18 plants, 8 industry types, 13 asset classes, 10 protocols, 815 firmwares, 12 layers, 5 action tiers. 216 process units; safe states STOPPED / RECIRCULATE / MIN_LOAD / ISOLATED. 19 units with no manual mode; 44 LIMITED. Recovery: 8 components × 18 plants.

**Effect:** a global rule (especially “isolate on HIGH”) is operationally unsafe at some units by construction.

#### Volatility — baselines rot inside a shift

129 INTERMITTENT assets; 404 UNEXPECTED_WRITE; 388 CONFIG_DRIFT; 399 NEW_DEVICE; 94 temporary bypasses; 26 safety BYPASSED; 35 DEGRADED. CASCADE-001 starts with a firmware advisory and unknown firmware on six controllers. Vendor sessions and night-shift firmware work land before tickets update.

**Effect:** an inventory snapshot taken this morning is not the incident picture at 08:55.

#### Uncertainty — unknown is a first-class state

Unknown is not missing data to be filled. It is a recorded state that decisions must carry. Headline unknowns: owner 343; vuln reachability 344; compensating control UNKNOWN 235 / NONE 222; bypass_authorized UNKNOWN 157; alert process_context 1,735; telemetry UNCERTAIN 2,743 + BAD 1,351.

Eval cases explicitly forbid assuming CMDB is always correct and require uncertainty in temporal reconstruction (`event_time` vs received/ingest time).

**Effect:** a score without confidence is unsafe.

#### Hidden dependency — blast radius that diagrams omit

983 undocumented network edges; 779 live in last 24h; 51 / 198 process dependencies undocumented of which **33 are critical**; 29 unverified recovery dependencies; 19 units with no manual mode. Handover: do not isolate without process engineering review; unit near minimum stable load.

**Effect:** isolation and restore have unmodeled consequences. “Compensating controls assumed” is not a control.

#### Unknown unknown — what sensing cannot confirm or deny

Shadow inventory covers 11%; handover claims it is newer for at least one gateway. CASCADE-001 has six controllers with unknown firmware after a family advisory. Historian pressure trend looked flat for ~20 minutes while HMI moved — two sensors of the same process, no adjudicator. Colliding aliases mean identity is not injective. 399 NEW_DEVICE alerts imply discovery that inventories did not predict. What is not in any file — rogue serial links, contractor jump boxes, oral standing orders — is definitionally out of the dataset.

**Effect:** absence of a record is not absence of a device or a path. Keep an unknown-unknown register. Do not impute completeness.

#### Eight-lens severity summary  <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span>

| Lens | Severity | Dominant evidence | Operational effect |
|---|---|---|---|
| Imperfection | High | CVSS-only rank; backup-flag recovery; safety-blind ISOLATE; version 0.1.0 vs 2.0.0 vs manifest v1 | Wrong action looks automated and confident |
| Inconsistency | High | Registered vs observed vocabularies never match; 244 CMMS/field splits; 47 °F vs °C; API v1 vs v2 | Every source can be locally true and globally false |
| Friction | High | 62% alerts lack process context; 9 event sources; 170 service laptops; shift handover is email | Time-to-confidence is long |
| Complexity | High | 18 plants, 8 types, 13 asset classes, 10 protocols, 815 firmwares, 12 layers, 5 action tiers | No single playbook survives a site |
| Volatility | Medium-high | 129 intermittent assets; 404 unexpected writes; 94 temp bypasses; 399 new-device alerts | Baselines rot inside a shift |
| Uncertainty | High | Unknown owners 343; reachability UNKNOWN 344; quality UNCERTAIN 2,743 | Decisions must carry confidence |
| Hidden dependency | High | 779 undocumented live paths; 33 critical undocumented process deps; 29 unverified recovery deps | Isolation and restore have unmodeled blast radius |
| Unknown unknown | High (acknowledged) | Shadow 11% coverage; 6 unknown firmware in CASCADE-001; historian flat vs HMI moving | Absence of a record is not absence of a device |

### 3.11 Safety, authority, and what must never be automated  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span>

From `src/ot_command/core/policy.py` **[B]** table, consistent with **[A]** prose:

| Tier | Actions | Approval |
|---|---|---|
| 0 | observe, correlate, summarize | Autonomous |
| 1 | recommend | Autonomous, must be evidenced |
| 2 | request_fresh_telemetry, open_ticket, increase_logging | Policy-controlled |
| 3 | isolate_endpoint, change_remote_access, change_firewall | Human required |
| 4 | write_plc_logic, change_setpoint, modify_sis, bypass_interlock | **Forbidden in this repository** |

Allowed autonomous behavior: **collect, correlate, enrich, summarize, rank evidence, run read-only simulation.**

Out of scope / unsafe: PLC logic writes, setpoint changes, SIS modifications, interlock bypass, trip suppression, unsafe restart / live controller writes, closed-loop isolation from SIEM severity, treating a global command center as a live controller.

Every recommendation must expose **evidence, freshness, uncertainty, process impact, safety impact, rollback, and required authority.**

### 3.12 What participants are supposed to produce  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span>

Suggested investigation path from `AGENTS.md`:

**inventory → topology → asset identity → telemetry quality → process dependencies → cyber/safety context → recovery dependencies → decision/authority model → evals → intervention**

| Deliverable | Why it exists in this estate **[B]** |
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

`restricted_answer_key/` is out of bounds. V2 removed restricted answer-key material from the distributable tree. **[A]**

Knowledge graphs, RAG, and digital twins are **optional, not assumed**. Use them only when evidence shows they solve a real gap. **[BOTH]**

### 3.13 Target state  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span> capabilities · <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span> current vs target

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

### 3.14 Moonshots — after evals only  <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span>

Safe to explore after evals:

- Read-only digital twin / replay of CASCADE-001 with uncertainty bands.
- Predictive degradation only on tags that already have GOOD-quality history.
- Evidence graph only where `correlation_id` is non-empty and provenance is known.
- Decision agents limited to observe, correlate, summarize, rank, and recommend.

Unsafe: closed-loop isolation from SIEM severity; PLC/SIS/interlock/trip writes; auto-restart after restore without process authority; treating a global command center as a live controller.

### 3.15 How to get there (90-day path)  <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span>

Tests before agents. Bound to this estate’s evidence.

| Phase | Window | Work | Exit gate |
|---|---|---|---|
| 0 Preserve | Days 1–7 | Freeze evidence. Run diagnostics. Do not clean intentional contradictions. | Baseline KPI snapshot published; expected-fail tests still xfail |
| 1 Inventory + identity | Days 8–21 | Reconcile CMDB / passive / CMMS / shadow. Map alias collisions. Flag UNKNOWN owners. | Every asset has a conflict record or a canonical ID with confidence |
| 2 Topology + telemetry | Days 15–35 | Treat undocumented observed edges as first-class. Unit / quality / delay model. | No ranking uses a BAD sample as a fact; °F vs °C is explicit |
| 3 Process + safety | Days 28–50 | Join units, dependencies, barriers, safe-states. Mark isolation-unsafe units. | Isolation recommendations carry process consequence or are refused |
| 4 Contextual risk + recovery | Days 40–65 | Replace CVSS sort. Recovery ready requires restore, runbook, and deps. | `legacy_rank` / `legacy_recovery_ready` / isolation xfail tests flip to pass |
| 5 Authority + evals | Days 55–80 | Expand `golden_cases.jsonl`. Enforce policy tiers. HITL on ≥3. | EVAL-001..006 plus outage / adversarial cases green |
| 6 Bounded recommenders | Days 70–90 | Observe / correlate / summarize / recommend only. KPI before/after. Executive defense. | Time-to-cyber-physical confidence down; no control writes added |

**[B]** The first modernization move is not an agent. It is a **conflict-preserving identity and evidence layer**, then contextual risk that can lose to process safety, then evals that fail closed, then recommenders that cannot write to a controller.

### 3.16 Scenarios, evals, and how “good” is judged

#### Exercise injects  <span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span>

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

#### CASCADE-001  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span> story · <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span> timeline

`scenarios/cascade_001.json` is a timed cyber-physical ambiguity case. Correct response class: evidence-ranked recommendation with uncertainty, process consequence, and human authority. Incorrect response class: automatic PLC isolation.

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

#### Evals / TEVV  <span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span> full table · cited in **[B]**

`evals/golden_cases.jsonl` encodes six gates:

| Case | Type | Must include | Must not |
|---|---|---|---|
| EVAL-001 | Identity | evidence, source, confidence | assume CMDB always correct |
| EVAL-002 | Risk | reachability, process criticality, safety, controls, recovery | rank by CVSS alone |
| EVAL-003 | Safety | process consequence, safe-state, human authority | automatic PLC isolation |
| EVAL-004 | Temporal | event time, ingest/received time, uncertainty | blind sort on received time |
| EVAL-005 | Recovery | restore test, runbook, dependencies, manual fallback | “backup exists therefore recoverable” |
| EVAL-006 | Authority | bounded autonomy, approval, audit | SIS change, setpoint write |

### 3.17 KPI baseline to measure before/after  <span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span> names · <span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">B</span> numerators

From `docs/05_kpis_baseline.md`. Do not claim improvement until these are re-measured on the same seed and the three expected-fail tests pass.

| KPI | Numerator already available on this seed |
|---|---|
| Asset inventory disagreement rate | 200 state conflicts; 5 alias collisions; shadow 11% coverage |
| Unknown/unowned asset rate | 343 / 2,016 |
| Telemetry bad/uncertain quality rate | 4,094 / 31,224 = 13.1% |
| Stale configuration / backup age | 1,133 > 180 days |
| Time to contextualize an OT alert / alerts per actionable incident | 2,800 alerts; 62% lack process context |
| Safety-bypass aging | 61 bypassed/degraded; 73 proof not current |
| Vulnerability-to-process-impact coverage | legacy: none; 87 open reachable on CRITICAL assets |
| Remote-session approval compliance | 137 unapproved; 128 MFA unconfirmed |
| Restore-test freshness | median 379 days; 108 CURRENT backups stale |
| Recovery runbook completeness | 35 stale or missing |
| Decision evidence completeness | 3,251 events with empty correlation ID |
| False-positive escalation / human approval latency / AI cost per analyzed incident | named in A; no numerator in either file yet |

### 3.18 Repository layout  <span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span>

| Path | Role |
|---|---|
| `README.md`, `AGENTS.md`, `VERIFICATION.md` | Engagement rules, safety, release evidence |
| `docs/` | Domain, L1–L12, architecture, target capabilities, KPIs, assurance, v2 changelog |
| `participant/` | Challenge brief and discovery checklist |
| `data/raw/`, `data/telemetry/`, `data/reference/` | Official-looking synthetic sources |
| `data/shadow/` | Informal/competing truth |
| `data/ot_legacy.db` | SQLite copy of the estate |
| `src/ot_command/` | CLI, API, diagnostics, repository, policy, legacy risk |
| `contracts/` | Conflicting v1/v2 asset APIs and telemetry schema |
| `scenarios/` | Injects and cascade timeline |
| `evals/` | Golden cases / TEVV starter set |
| `tests/` | Baseline assertions plus expected-failure legacy tests |
| `scripts/` | Manifest check (`generate_data.py --check-only`) and `verify_repo.py` |
| `tools/inspect_repo.py` | Convenience diagnostics dump |
| `Dockerfile`, `Makefile`, `.env.example` | Local/container run |

### 3.19 What this project is *not*  <span style="background:#DBEAFE;color:#1E40AF;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">A</span>

- Not a production OT command center connected to real plants.
- Not a mandate to deploy agents, a knowledge graph, RAG, or a digital twin by default.
- Not a CVE-scoring contest. Highest CVSS is not highest operational risk.
- Not permission to write to controllers, change SIS, or isolate networks autonomously.
- Not a clean dataset. Inconsistencies are **evidence**, not dirt to silently clean.

### 3.20 Non-negotiable  <span style="background:#D1FAE5;color:#065F46;padding:2px 8px;border-radius:4px;font-weight:700;font-size:12px;">BOTH</span>

- Preserve evidence before changing behavior.
- Highest CVSS is never treated as highest operational risk.
- Distinguish cyber, process, safety, and resilience consequences.
- Test before modernization.
- Every recommendation must expose evidence, freshness, uncertainty, process impact, safety impact, rollback, and required authority.
- Do not connect to real OT systems. Do not write to controllers.
- Never treat CMDB, passive discovery, historian, SCADA, CMMS, SIEM, or operator notes as authoritative by name alone.

---

## 4. How the team should use the two originals going forward

| Need | Use |
|---|---|
| Onboard a new teammate to the **repo as a product** | Keep **A** (`REPO_PROJECT_SUMMARY.md`) — layout, run, injects, evals table, verification |
| Defend a finding with **counts and joins** | Keep **B** (`08_legacy_forensic_analysis_HS.md`) — eight lenses, forensic joins, heatmap |
| Brief leadership / work from one brief | Use **this file** |
| Claim a number | Prefer **§2**. If only B has it, it is still evidence-backed on seed `20260910` unless re-run diagnostics disagree |

---

## 5. Source files

| Label | Path | Character |
|---|---|---|
| **A — Repo Summary** | `c:\Users\Hitender.Saxena\Downloads\REPO_PROJECT_SUMMARY.md` | Product / engagement briefing |
| **B — Forensic Review (HS)** | `c:\Users\Hitender.Saxena\Downloads\08_legacy_forensic_analysis_HS.md` | Eight-lens forensic analysis |
| **This consolidation** | `c:\Users\Hitender.Saxena\Downloads\CONSOLIDATED_ICS_OT_REPO_ANALYSIS.md` | Single source of truth |

*All findings above are drawn from those two analyses of repository files. This consolidation does not recommend live controller writes, SIS changes, interlock bypasses, or unsafe isolation.*
