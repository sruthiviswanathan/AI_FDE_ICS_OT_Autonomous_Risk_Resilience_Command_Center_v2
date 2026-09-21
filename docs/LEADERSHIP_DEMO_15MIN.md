# Leadership demo — 15 minutes

**Application:** [https://ics-ot-command-center.onrender.com](https://ics-ot-command-center.onrender.com)  
**Audience:** VP Operations, security, process, safety, and platform leadership  
**Duration:** 15 minutes (plus optional Q&A)  
**Persona for this walkthrough:** **Full workshop view** (top-right **Persona** selector)

This script describes only what the deployed command center actually implements. It is a **synthetic, read-only advisory workbench**. It does not connect to live plants and it cannot write to controllers.

---

## What this product is (say this once, then demo)

The ICS/OT Command Center is a **governed advisory workbench** over a fictional 18-plant brownfield estate. Deterministic engines join inventory, telemetry, risk, safety, recovery, and authority evidence. Operators get a **draft recommendation packet**. Software never isolates, never writes a PLC, and never changes a SIS.

**One sentence to keep repeating:**

> Cyber state, operational state, safety state, recovery state, and decision authority are five different truths. This product keeps them separate and refuses unsafe action.

Mode shown in the header: **synthetic-read-only** · API **3.0.0**.

---

## Before the meeting (not part of the 15 minutes)

1. Open the URL. Render may take **30–60 seconds** on a cold start. Wait until **Risk & Resilience Control Tower** loads.
2. Set **Persona** to **Full workshop view**. (Persona is a **navigation filter only** — not login, not authorization.)
3. Confirm the left **Scenario rail** is visible.
4. If a banner says the API is unreachable, hard-refresh once. Fallback: [OpenAPI docs on the same host](https://ics-ot-command-center.onrender.com/docs).

Do **not** click **Authorize**. That control is implemented as **disabled** (OPEN-001: no named authorizer in software).

---

## Minute-by-minute room script

| Clock | Screen | Purpose |
|------:|--------|---------|
| 0:00–1:30 | Framing on Control Tower | What it is / is not |
| 1:30–3:30 | Control Tower + Estate Dashboard | Estate disagreement, five posture layers |
| 3:30–5:00 | Identity Reconciliation (`inject_01`) | Inventories do not agree |
| 5:00–6:30 | Contextual Risk (stay on CASCADE pins) | Highest CVSS is not the ticket |
| 6:30–13:00 | CASCADE-001 | The decision story |
| 13:00–15:00 | Recommendation Gate → Decision Trace → Executive Brief | Close: draft only, inspectable, no execute |

If time slips, skip Identity and Contextual Risk. The CASCADE block is the closer.

---

### 0:00–1:30 — Frame the product

**Stay on:** Control Tower (`/`)

**Click:** Scenario rail → **Nominal**.

**Point at:**

- Header **Mode: synthetic-read-only**
- Badge **Deterministic engines**
- **SLO-OT** status on the CTQ strip (this is “no OT execute in software,” not plant health)
- Footer note that freshness is **workshop-static**

**Say:**

> This is not a chat bot and not a plant controller. Leadership asked for a command center that can advise on cyber-physical risk without becoming the incident. Everything you will see is a synthetic 18-plant estate. The API is read-only. There is no isolate button that does anything.

**Do not say:** “The plant is healthy because SLO-OT is OK.” SLO-OT OK means the product did not execute on OT.

---

### 1:30–3:30 — The estate already disagrees with itself

**Stay on:** Control Tower, then **Estate Dashboard**.

**Point at the estate diagnostics strip** (live counts from the workshop dataset; expect this order of magnitude):

| Signal | What it means in this product |
|--------|-------------------------------|
| ~200 state conflicts | Registered inventory vs observed state |
| ~5 alias collisions | The same name maps to more than one asset |
| ~4,094 bad / uncertain telemetry | Historian quality is not “process healthy” |
| ~61 barriers degraded / bypassed | Safety protection is already messy |
| ~137 unapproved remote sessions | Someone may already be inside |
| ~25 stale / unknown backups | Backup CURRENT is not recovery-ready |
| 779 undocumented observed paths | Blast radius is not fully documented |

**Scroll to Estate posture.** Expect **18/18 plants elevated**. HIGH/CRITICAL alert counts on this screen are **inventory**, not a risk ranking.

**Click:** **Open Estate Dashboard →** (or left nav **Estate Dashboard**).

**On Estate Dashboard, point at:**

- Banner: inventory signals, **not contextual risk rank**
- Default **Graph** view of 18 plants by region (NA / EU / APAC / LATAM / MEA); **Grid** toggle exists
- Five posture pills on a plant: **Cyber · Process · Safety · Recovery · Evidence**. Composite is OK only when every layer is OK (worst layer wins)
- Optional click on one plant → drill-down of assets, alerts, and a hop-capped neighborhood graph

**Say:**

> Dashboards already exist in this estate. What they do not produce is a trusted cyber-physical truth. We keep five layers. We do not paint one green score over them.

**Do not say:** “Isolate the company because 18 plants are red.” Elevation is disagreement, not an execute signal.

---

### 3:30–5:00 — You cannot isolate what you cannot name

**Click:** Scenario rail → **inject_01** (Inventory mismatch).  
Context bar should pin **PLT-01** / **OT-00528**.

**Click:** left nav **Identity Reconciliation**.

**Point at:**

- **Registered state** vs **Observed state** as separate fields (example in this dataset: **OT-00528** registered **RETIRED**, observed **ONLINE**)
- Trust flags: **CMDB winner = false**, **Merged = false**
- Alias collision table (estate-wide **5** collisions; colliding aliases are listed, not merged)
- Plant conflict counts for **REGISTERED_VS_OBSERVED** vs **ALIAS_COLLISION**
- Provenance link that pins `source_path` in the right-hand **Provenance & Retrieval** drawer

**Say:**

> The product shows the conflict. It does not pick a CMDB winner and it does not promote the shadow spreadsheet into the master inventory.

**Do not say:** “Merge the aliases” or “CMDB is the source of truth.” Those controls are not implemented — and are forbidden.

**Skip if behind:** go straight to CASCADE-001.

---

### 5:00–6:30 — Highest CVSS is not the plant’s problem

**Click:** Scenario rail → **CASCADE-001**.  
Pins: plant **PLT-10**, asset **OT-01016**, alert **ALT-002783**.

**Click:** left nav **Contextual Risk**.

**Point at:**

- Default button **Contextual rank (default)** — this is the implemented sort
- Columns: Finding, Asset, **CVSS (input)**, Reach, Criticality, Severity, Score
- Row **VUL-00098** on **OT-01016** (reachable, process-relevant) vs a higher-CVSS finding that is **not** reachable
- **Details** expands **factor breakdown** (reachability, process criticality, safety, compensating control, recovery) plus evidence JSON

**Optional 10 seconds:** click **CVSS-only (warn)** so the amber banner appears: *CVSS-only sort is anti-pattern*. Switch back to contextual rank.

**Say:**

> CVSS is an input. It is not the ticket order. A 9.8 that cannot reach the unit is not the first problem on this plant.

**Do not say:** “We ranked by CVSS descending.” That is the warning mode, not the product default.

---

### 6:30–13:00 — CASCADE-001: one morning, one draft, no execute

This is the leadership story. Stay on **CASCADE-001**. Do not bounce through inject_02–06 unless someone asks.

Badges that must stay on screen:

- Barrier BYPASSED unauthorized
- safe_state MIN_LOAD
- 08:24 vendor session
- SOC vs PE dissent
- shift notes UNTRUSTED
- **execute=false**

#### 6:30–8:00 — Incident Context

**Click:** **Incident Context** (or the incident banner **Open Incident Graph**).  
If the timeline is empty, click **Load CASCADE-001**.

**Read these times out loud** (paraphrase the rest):

| Time | What the room sees |
|------|--------------------|
| 08:24 | Vendor session on the engineering workstation |
| 08:38 | Related safety barrier recorded as bypassed |
| 08:47 | SOC recommends immediate isolation |
| 08:50 | Process engineer warns abrupt isolation may destabilize the unit |
| 08:55 | Command center must recommend a **safe governed** response |

**Point at:**

- Red **Shift handover UNTRUSTED** panel (OPEN-018). The workshop corpus has one unbound Unit 04 night-shift email. It is **not** PLT-10’s shift record and it is **not policy**.
- **Task-scoped graph (Q5)** — visual cascade by default; **Citations** toggle exists; pan/zoom on denser graphs; hop cap 8

**Say:**

> 08:47 is a demand. 08:50 is dissent. 08:55 is a draft. The email is untrusted text.

#### 8:00–9:00 — Safety vs Security (proof, one screen)

**Click:** **Safety vs Security**.

**Point at:**

- Degraded-barrier and bypassed-unauthorized counts
- Barrier **PLT-10-SAFE-07** on unit **PLT-10-U06**: state **BYPASSED**, bypass authorized **NO**
- UNKNOWN bypass is shown as UNKNOWN (not treated as YES)
- Q3 safety-context graph under the table (visual default)

**Say:**

> Protection is already degraded. Isolate is not automatically safer. This screen has no bypass or SIS-modify action.

#### 9:00–10:00 — Vendor already inside (proof, one screen)

**Click:** **Vendor Sessions**.

**Point at:**

- Estate tiles: unapproved sessions and MFA-not-confirmed (workshop dataset: **≥137** / **≥128**)
- Table filtered to **PLT-10**
- A session with approved window **NO** (e.g. **RA-00025** in this dataset)
- **Pin** on a row → provenance drawer

**Say:**

> Someone may already be on the network. This product can show that. It cannot disable VPN or change remote access. Those are tier-3 human actions with no execute API.

#### 10:00–11:00 — Process and recovery (proof, two short screens)

**Click:** **Process Graph**.

**Point at:** hop-capped Q2 dependency graph; undocumented observed paths drawn distinctly; footer **Hop cap 8 · Forbidden: regional isolate action**.

**Click:** **Recovery Graph**.

**Point at:**

- Plant scoreboard **Recovery ready X / Y** (PLT-10 in this dataset is **0 / 8**)
- Component table: backup, restore-test days, runbook, deps verified, manual fallback, **RecoveryReady**, blockers
- Rows where backup is **CURRENT** and RecoveryReady is **NO** (highlighted)
- Q4 recovery-dependency graph

**Say:**

> If we isolate, can we recover? Not because a backup flag is green. Ready means tested restore, current runbook, and verified dependencies. There is no live restore button.

#### 11:00–13:00 — The packet (the closer)

**Click:** **Recommendation Gate**.

Confirm context bar: **PLT-10** · **OT-01016** · **ALT-002783**.

**Click:** **Request draft packet**.

Wait for **Workflow progress** (eight deterministic engine states: request validation → identity → risk → safety → recovery → authority → recommendation → human review).

**Read the packet fields that are actually rendered:**

| Field | What to expect on CASCADE-001 |
|-------|-------------------------------|
| Recommendation | **DO_NOT_ISOLATE** (or **ABSTAIN** if joins are missing — both are implemented outcomes) |
| Execute | **false** / No |
| Safe state | **MIN_LOAD** |
| Process impact / safety impact | Shown on the packet |
| Authorizable | **false** while CTQ-ISO is incomplete (`ctq_iso_complete=false` on this scenario) |
| Required authority | Role names only: Process Engineer, Safety/SIS Owner, VP Operations — **no named person** (OPEN-001) |
| Authorize button | **Disabled** — label *Authorize (disabled — OPEN-001)* |
| Footer | *Advisory only — no Execute Isolation · Write PLC · Modify SIS* |

**Say:**

> SOC wanted isolate at 08:47. Process warned at 08:50. At 08:55 the implemented product drafts DO_NOT_ISOLATE with execute false. Required humans are listed as roles. Nobody is bound by name. There is no execute path in this UI or in the API.

---

### 13:00–15:00 — Governance close

**Click:** **Decision Trace**.

**Point at:**

- SLO cards from `GET /ops/slo` (including **SLO-OT**)
- Cost-model card (workshop note: AI disabled default ⇒ 0 tokens)
- Trace table after the packet: actor, purpose (**CASCADE-001 triage**), recommendation, **Execute = false**, latency

**Click:** **Executive Brief**.

**Point at (this page is implemented as a short read-only brief, not a second command center):**

- Posture summary: state conflicts, safety degraded, recovery gaps, unapproved vendor sessions
- CTQ checklist: SLO-OT, SLO-EVAL, **AI default: OFF (ADR-12)**, **Execute routes: 0**
- Drill links: Simulation, Audit, Control Tower
- Footer: *No execute controls on this surface*

**Optional 20 seconds if asked “does AI have to be up?”:** Scenario rail → **AI outage**. Tables on Control Tower, Identity, Telemetry, Recovery, and Recommendation stay visible. Deterministic engines still run. There is **no AI on/off toggle in the header**; the workshop path is AI-off by design.

**Close with:**

> What is implemented today: evidence-cited disagreement, contextual rank that is not CVSS-only, safety and recovery joins, a draft packet, and an audit row. What is not implemented: live plant control, named software authorization, or autonomous isolation. The win we can show is **unsafe isolate avoided**, not faster cutover.

---

## Implemented surface (inventory for the room)

Use this if someone asks “what screens exist?” All of these are in the React app and on the deployed site.

| Nav label | Route | What it does |
|-----------|-------|----------------|
| Control Tower | `/` | Estate diagnostics, SLO-OT, elevated alerts, posture chips |
| Estate Dashboard | `/estate` | 18-plant graph/grid, five-layer posture, plant/asset/alert drill-down |
| Identity Reconciliation | `/identity` | Registered vs observed, alias collisions, `cmdb_winner=false` |
| Telemetry Quality | `/telemetry` | Bad/uncertain, duplicates, unit mismatch, dual-clock timeline |
| Contextual Risk | `/risk` | Contextual rank (default) + CVSS-only warning mode |
| Safety vs Security | `/safety` | Degraded/bypassed barriers; UNKNOWN ≠ authorized |
| Vendor Sessions | `/sessions` | Unapproved / MFA gaps; plant-scoped table; no VPN kill |
| Process Graph | `/process` | Hop-capped Q2 dependencies; undocumented paths |
| Recovery Graph | `/recovery` | RecoveryReady predicate + blockers; no restore orchestration |
| Incident Context | `/incident` | CASCADE timeline, UNTRUSTED shift note, Q5 graph |
| Recommendation Gate | `/recommend` | `POST /recommend` draft packet; Authorize disabled |
| Decision Trace | `/audit` | Append-only traces, SLO, cost model |
| Inject / Simulation | `/simulation` | Load scenarios; **Run full harness (EVAL-001…031)** |
| KPI Before/After | `/kpi` | Live diagnostic/SLO table (not a scored improvement program) |
| Executive Brief | `/executive` | Read-only posture + CTQ checklist |

**Global chrome that is implemented:**

- Persona selector: SOC / OT Analyst, Process Engineer, Safety / SIS Owner, Executive / VP Ops, FDE / Platform, Full workshop view
- Context bar: cascading plant / asset / alert pickers (fields hide per persona)
- Scenario rail: Nominal, CASCADE-001, inject_01…06, AI outage
- Provenance drawer: STRUCTURED · GRAPH · VECTOR (**disabled**) · POLICY · MEMORY

**Backend that the UI actually calls:** gold read-only GETs plus local **`POST /recommend`** and **`POST /eval/run`**. No OT execute routes.

---

## Personas (implemented as view filters)

| Persona | Lands on | What they see |
|---------|----------|----------------|
| SOC / OT Analyst | Control Tower | Triage screens; scenario rail on |
| Process Engineer | Process Graph | Process, recovery, telemetry, incident, recommend |
| Safety / SIS Owner | Safety vs Security | Safety, process, incident, recommend |
| Executive / VP Ops | Executive Brief | Brief, KPI, recovery, recommend, tower, estate; drawer collapsed; **scenario rail hidden** |
| FDE / Full | Control Tower | Every screen |

Switching persona **never** enables Authorize or Execute. UNKNOWN permission is not permission.

If you switch to **Executive / VP Ops** during the demo, the scenario rail disappears — switch back to **Full** before CASCADE.

---

## Scenario rail (what each load actually does)

Selecting a scenario sets plant / asset / alert, expected badges, and primary route chips. Conflicts are **not** hidden.

| Rail label | Pins | Implemented point |
|------------|------|-------------------|
| Nominal | PLT-01 / OT-00001 / ALT-001744 | Estate baseline |
| CASCADE-001 | PLT-10 / OT-01016 / ALT-002783 | Cyber-physical ambiguity; Authorize stays disabled |
| inject_01 | PLT-01 / OT-00528 | Inventory mismatch |
| inject_02 | PLT-01 + tag PLT-01-U03_TEMP | Historian quality (use **Telemetry Quality**) |
| inject_03 | PLT-15 / OT-01645 | Unapproved vendor session |
| inject_04 | PLT-03 / OT-00211 | Safety bypass aging |
| inject_05 | PLT-01 | Undocumented paths; no regional isolate |
| inject_06 | PLT-01 IDENTITY | CURRENT backup ≠ RecoveryReady |
| AI outage | PLT-01 / OT-01016 | Deterministic tables remain; no blank screen |

Do **not** walk all nine in 15 minutes. The script above uses Nominal → inject_01 → CASCADE-001.

---

## What is not implemented (say this if asked)

Do not demo or promise any of the following. They are out of the product as built.

- Live plant, historian, SIEM, or CMMS connectivity
- PLC write, setpoint change, SIS modify, interlock bypass, trip suppression
- Execute isolation, firewall push, VPN disable, or any OT write API
- One-click Authorize or a named Authorizer bound in software (OPEN-001)
- Production API authentication / SSO (OPEN-029)
- Persona as IAM — it only filters navigation
- LLM / AI explainer as a primary surface (ADR-12: AI default OFF; **no header AI toggle** is implemented)
- VECTOR retrieval driving rank, isolation, or ACTION_TIERS (tab is disabled)
- Merging aliases or promoting shadow inventory to CMDB
- Imputing BAD telemetry to GOOD, or treating GOOD quality as “process healthy”
- Treating UNKNOWN process context or UNKNOWN bypass as NORMAL / YES
- Live restore / DR orchestration UI
- Regional isolate from a SCADA-outage story
- Numeric KPI pass thresholds as a scored “before vs after” program (OPEN-006 — KPI page shows live diagnostics)
- Dual-column SOC vs PE editor on the Recommendation Gate (dissent is on the CASCADE timeline and packet, not a two-pane markup tool)
- EU AI Act certification, external pentest sign-off, or legal class

**Kill criterion already encoded in the product:** if the UI or API added an OT write or isolate-execute surface, this increment would be out of mandate.

---

## If the room asks a hard question

| Question | Honest answer from what is built |
|----------|----------------------------------|
| Can it isolate the endpoint? | No. Recommendation is draft/abstain. `execute` is false. No execute control exists. |
| Who authorizes? | Roles are listed on the packet. Named person binding is not implemented. |
| Does highest CVSS win? | No. Default rank is contextual. CVSS-only is a warning mode. |
| Is CMDB the winner? | No. Identity shows `cmdb_winner=false`. |
| Backup is CURRENT — are we ready? | Only if RecoveryReady is true (restore test, runbook, verified deps). CURRENT alone is not ready. |
| Can we turn AI on? | Workshop engines are deterministic. AI default is OFF. No implemented header toggle. Optional explainer must not change rank/isolation/recovery predicates. |
| How do we know it refuses unsafe actions? | Decision Trace after `POST /recommend`; eval harness on **Inject / Simulation** (`EVAL-001…031`). Do not run the full harness in the 15-minute slot unless asked. |
| Is this production OT? | No. Synthetic workshop-static data. Mode `synthetic-read-only`. |

---

## Timing recovery

| If you have only… | Do this |
|-------------------|---------|
| **8 minutes** | Nominal Control Tower (1 min) → Estate Dashboard (1 min) → CASCADE-001 Incident (2 min) → Safety (1 min) → Recommendation Gate (2 min) → Executive Brief (1 min) |
| **5 minutes** | CASCADE-001 badges → Incident 08:47 vs 08:50 → Request draft packet → DO_NOT_ISOLATE / execute=false |
| **Someone wants injects** | After the close, load **inject_02** (telemetry F≠C), **inject_03** (vendor), **inject_06** (CURRENT ≠ ready) — one screen each |

---

## Presenter rules (demo integrity)

- Do not hide conflict badges to make the estate look clean.
- Do not click disabled **Authorize** as if it will enable.
- Do not describe SLO-OT OK as operational health.
- Do not invent a named executive, KPI target, or ACTION_TIERS verb that is not on screen.
- If a graph errors, the **tables are the product**. Keep going.
- If persona is Executive and the rail is missing, switch back to **Full workshop view**.
