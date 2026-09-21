# Live app demo — 8 end-to-end workflows

**App:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)  
**Mode:** synthetic, read-only command center (API 3.0.0)  
**Cold start:** Render may take 30–60 seconds on first open. Wait for Control Tower, then begin.

This is a **workbench**, not a chatbot and not a plant controller. There is no Execute Isolation and no PLC/SIS write. Demo it as: **load a scenario → walk the disagreement → stop at a governed recommendation**.

**One-line story:** cyber state ≠ operational state ≠ safety state ≠ resilience state.

---

## How to drive the UI

1. Open [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/).
2. Set persona to **FDE** or **Full** so every screen is visible.
3. Use the **scenario rail** (top/side) to load a named case. That pins plant / asset / alert and expected badges.
4. Click the left nav. Do not hide conflicts to beautify the room.

| Nav label | URL | Use it to show |
|---|---|---|
| Control Tower | `/` | Estate posture, unreadiness, “not another dashboard” |
| Estate Dashboard | `/estate` | 18-plant inventory signals (not risk rank) |
| Identity Reconciliation | `/identity` | Registered vs observed, alias collisions, no CMDB winner |
| Telemetry Quality | `/telemetry` | BAD tags, F≠C, event time vs ingest time |
| Contextual Risk | `/risk` | CVSS is an input, not the sort key |
| Safety vs Security | `/safety` | Bypass + SOC isolate vs process safe-state |
| Vendor Sessions | `/sessions` | Unapproved / no-MFA remote access |
| Process Graph | `/process` | Unit dependencies, blast radius unknown |
| Recovery Graph | `/recovery` | CURRENT backup ≠ recovery-ready |
| Incident Context | `/incident` | CASCADE timeline + pinned evidence |
| Recommendation Gate | `/recommend` | Draft / abstain, required humans, execute=false |
| Decision Trace | `/audit` | Inspectable tool/decision path |
| Inject / Simulation | `/simulation` | Load injects without claiming live OT |
| KPI Before/After | `/kpi` | What value looks like (disagreement, not isolate-speed) |
| Executive Brief | `/executive` | 90-second close for leadership |

Personas (if asked): **SOC / OT Analyst**, **Process Engineer**, **Safety Owner**, **Executive**, **FDE**, **Full**.

---

## Workflow 1 — Control Tower: do we trust the picture?

**Full stakeholder script + live screenshots:** [`WORKFLOW_01_CONTROL_TOWER.md`](WORKFLOW_01_CONTROL_TOWER.md)  
**Plain-English click path:** [`WORKFLOW_01_CONTROL_TOWER_DEMO_STEPS.md`](WORKFLOW_01_CONTROL_TOWER_DEMO_STEPS.md)

**Scenario rail:** Nominal  
**Click path:** Control Tower → Estate Dashboard (optional KPI Before/After)

**What to point at**

- Mode badge: `synthetic-read-only` · **SLO-OT: OK** (no execute — not plant health)
- Estate counts: **2016** assets, **31,224** telemetry events, **1,100** vulnerabilities, **450** barriers, **700** vendor sessions
- Derived signals: **200** identity conflicts, **4,094** bad/uncertain tags, **61** bypassed/degraded barriers, **137** unapproved vendor sessions, **25** stale/unknown backups
- Posture: **18/18 plants elevated** — five layers, worst wins; 860 HC is **inventory**, not rank

**Say:** Leadership asked for an autonomous command center. The estate already produces dashboards. What it does not produce is a trusted cyber-physical truth. This screen is inventory and disagreement — not a permission to act.

**Must not say:** “The plant is healthy because the app is green.”

---

## Workflow 2 — Identity: one name, two truths

**Full stakeholder script + live screenshots:** [`WORKFLOW_02_IDENTITY_RECONCILIATION.md`](WORKFLOW_02_IDENTITY_RECONCILIATION.md)

**Scenario rail:** inject_01 — Inventory mismatch  
**Click path:** Control Tower (200 / 5) → inject_01 → Identity Reconciliation → skip OT-00001 → Conflicts OT-00012 / OT-00033 → Search OT-00528 (PLT-05)  
**Pinned:** inject_01 badges name `OT-00528`; that asset’s plant is `PLT-05`

**What to point at**

- **OT-00528**: registered **RETIRED**, observed **ONLINE**
- Alias **PLT-01-DCS_CONTROLLER-105** maps to both **OT-00012** and **OT-00033**
- Also visible: **OT-00020** ACTIVE vs UNSEEN
- Badges: `cmdb_winner=false`, shadow `FINAL_v8` is evidence only, ≥200 state conflicts, 5 alias collisions estate-wide
- Persona note: do not promote the shadow spreadsheet to CMDB

**Say:** You cannot isolate what you cannot name. We keep registered, observed, operational, safety, and authority as five states. We do not silently merge.

**Must not say:** “CMDB is the winner” or “delete the colliding alias.”

---

## Workflow 3 — Telemetry: the historian is lying in Celsius

**Full stakeholder script + live screenshots:** [`WORKFLOW_03_TELEMETRY_QUALITY.md`](WORKFLOW_03_TELEMETRY_QUALITY.md)

**Scenario rail:** inject_02 — Historian quality degradation  
**Click path:** Control Tower (4094 / 120 / 47) → inject_02 → Telemetry Quality → tag `PLT-01-U03_TEMP` → first row **253.837 F GOOD UNIT MISMATCH**

**What to point at**

- Bad/uncertain **≥4094**, duplicates **≥120**, unit mismatch **F≠C (≥47)**
- Dual clock: **event_time** and **ingest_time**
- Timeline ordered by process time, not packet arrival
- Badge: GOOD quality is not “process healthy”

**Say:** A command center that plots BAD tags as healthy process data will make the wrong call. F is not C. Highest CVSS on a tag we cannot trust is still not operational risk.

**Must not say:** “Treat BAD as GOOD” or sort only by ingest time.

---

## Workflow 4 — Contextual risk: highest CVSS is not the plant’s problem

**Full stakeholder script + live screenshots:** [`WORKFLOW_04_CONTEXTUAL_RISK.md`](WORKFLOW_04_CONTEXTUAL_RISK.md)  
**Plain-English click path:** [`WORKFLOW_04_CONTEXTUAL_RISK_DEMO_STEPS.md`](WORKFLOW_04_CONTEXTUAL_RISK_DEMO_STEPS.md)

**Scenario rail:** CASCADE-001  
**Click path:** Control Tower → CASCADE-001 → Contextual Risk → **VUL-00098** (8.7, reachable YES, score 87.4) → Search **OT-00654** / **VUL-00706** (9.8, reachable NO, score 40.6) → CVSS-only (warn) then back

| Finding | Asset | CVSS | Reachable | Why it matters |
|---|---|---|---|---|
| VUL-00706 | OT-00654 | 9.8 | NO | High score, low operational consequence |
| VUL-00098 | OT-01016 | 8.7 | YES | Reachable, process unit PLT-10-U06, barrier bypassed |

**What to point at**

- Factor breakdown: process criticality, reachability, safety, compensating control, recovery
- Label on CVSS: **input only — not sort key**
- Recovery note: CURRENT backup alone is not RecoveryReady

**Say:** Legacy sorted by CVSS. Operations does not. The 9.8 that cannot reach the plant is not the first ticket.

**Must not say:** “We ranked by severity label / CVSS descending.”

---

## Workflow 5 — Safety vs security: isolate now can become the incident

**Full stakeholder script + live screenshots:** [`WORKFLOW_05_SAFETY_VS_SECURITY.md`](WORKFLOW_05_SAFETY_VS_SECURITY.md)  
**Plain-English click path:** [`WORKFLOW_05_SAFETY_VS_SECURITY_DEMO_STEPS.md`](WORKFLOW_05_SAFETY_VS_SECURITY_DEMO_STEPS.md)

**Scenario rail:** CASCADE-001  
**Click path:** Control Tower → CASCADE-001 → Safety vs Security (**PLT-10-SAFE-07 BYPASSED / NO**) → Recommendation Gate → **Request draft packet** → **DO_NOT_ISOLATE**, execute No

**inject_04 pins:** plant `PLT-03`, asset `OT-00211`, barrier `PLT-03-SAFE-14`, unit `PLT-03-U05` MIN_LOAD

**CASCADE pins:** plant `PLT-10`, asset `OT-01016`, alert `ALT-002783`, barrier `PLT-10-SAFE-07`, safe-state **MIN_LOAD**

**What to point at**

- Barrier **BYPASSED**, `bypass_authorized=NO`
- UNKNOWN is not authorized
- SOC would isolate; process safe-state is MIN_LOAD
- No execute control on this page

**Say:** Isolation is a draft. Required humans: Process Engineering + Safety + VP Ops. A HIGH alert is not a write to the PLC.

**Must not say:** “Click isolate” or treat UNKNOWN permission as permission.

---

## Workflow 6 — Vendor access: someone is already on the network

**Full stakeholder script + live screenshots:** [`WORKFLOW_06_VENDOR_ACCESS.md`](WORKFLOW_06_VENDOR_ACCESS.md)  
**Plain-English click path:** [`WORKFLOW_06_VENDOR_ACCESS_DEMO_STEPS.md`](WORKFLOW_06_VENDOR_ACCESS_DEMO_STEPS.md)

**Scenario rail:** inject_03  
**Click path:** Control Tower (137 / 128 / 337) → inject_03 (**OT-01645 SAFETY_PLC**) → Vendor Sessions (RA-00038 UNKNOWN, RA-00210 window NO) → Recommendation Gate → **ABSTAIN**

**What to point at**

- Unapproved sessions **≥137**, MFA gaps **≥128**
- Rows where approved window is NO or MFA is not YES
- Badge: `change_remote_access` is **tier 3** (human authorize)
- UNKNOWN identity ≠ approval

**Say:** Before we talk containment, check who is already inside. The system can recommend “confirm the vendor window.” It must not auto-kill VPN.

**Must not say:** “Disable vendor_vpn from this screen.”

---

## Workflow 7 — Recovery: backup CURRENT is not recovery-ready

**Full stakeholder script + live screenshots:** [`WORKFLOW_07_RECOVERY.md`](WORKFLOW_07_RECOVERY.md)  
**Plain-English click path:** [`WORKFLOW_07_RECOVERY_DEMO_STEPS.md`](WORKFLOW_07_RECOVERY_DEMO_STEPS.md)

**Scenario rail:** inject_06 — Restore failure during recovery drill  
**Click path:** Control Tower (25 / 29 / 35) → inject_06 → Recovery Graph (**PLT-01 0/8**, **IDENTITY** CURRENT / 360 / STALE / NO) → Recommendation Gate → **ABSTAIN**  
**Pinned:** plant `PLT-01`, component **IDENTITY** (skip leftover `OT-00001`)

**What to point at**

- Backup **CURRENT**
- Restore test **360 days** (badge: >180d)
- Runbook **STALE**
- RecoveryReady **false** — plant scoreboard **0 / 8**
- Badge: `CURRENT ≠ RecoveryReady`, no live restore UI

Optional branch: **inject_05** Regional SCADA outage → Process Graph + Recovery Graph. Show 779 undocumented paths and “no regional isolate.” Same PLT-01 table already shows **SCADA** backup **STALE**, fallback **NO**.

**Say:** If we isolate, can we recover? Not because a backup flag is green. Ready means fresh restore test **and** current runbook **and** verified dependencies.

**Must not say:** “Backup exists, therefore recoverable.”

---

## Workflow 8 — CASCADE-001 at 08:55: the closer

**Full stakeholder script + live screenshots:** [`WORKFLOW_08_CASCADE.md`](WORKFLOW_08_CASCADE.md)  
**Plain-English click path:** [`WORKFLOW_08_CASCADE_DEMO_STEPS.md`](WORKFLOW_08_CASCADE_DEMO_STEPS.md)

**Scenario rail:** CASCADE-001  
**Click path:** Incident Context → Safety vs Security → Vendor Sessions → Process Graph → Recovery Graph → Recommendation Gate → Decision Trace

**Pinned:** `PLT-10` / `OT-01016` / `ALT-002783` / `PLT-10-U06` / `PLT-10-SAFE-07`

Walk the timeline out loud:

| Time | What the room sees | Screen |
|---|---|---|
| 08:01–08:07 | Firmware advisory; inventory incomplete | Identity |
| 08:19 | Unexpected write alert | Incident / Risk |
| 08:24 | Vendor session on engineering workstation | Vendor Sessions |
| 08:31–08:34 | Historian / operator alarm | Telemetry |
| 08:38 | Safety barrier recorded bypassed | Safety vs Security |
| 08:47 | SOC says isolate immediately | Recommendation Gate |
| 08:50 | Process engineer: isolation may destabilize the unit | Process Graph |
| **08:55** | Governed draft or abstain | Recommendation Gate + Decision Trace |

**Badges that must stay visible:** Barrier BYPASSED unauthorized · safe_state MIN_LOAD · 08:24 vendor session · SOC vs PE dissent · shift notes UNTRUSTED · **execute=false**

**Say the decision:** Draft packet or abstain. Surface bypass + min-load + vendor session + recovery not ready. Name the humans. Do not execute isolate. Shift notes are untrusted text, not policy.

**Optional 30-second encore:** load **AI outage**. Identity, telemetry, recovery, and recommendation tables stay up. Deterministic engines still run. No blank screen. Tier-4 actions still refused.

---

## 10-minute click path (use this in the room)

Open [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/) · persona **FDE** / **Full**

1. **Nominal** → Control Tower → Estate Dashboard  
2. **inject_01** → Identity Reconciliation (`OT-00528`)  
3. **inject_02** → Telemetry Quality (`PLT-01-U03_TEMP`)  
4. Contextual Risk (CVSS is not the sort key)  
5. **inject_04** or stay for CASCADE → Safety vs Security  
6. **inject_03** → Vendor Sessions  
7. **inject_06** → Recovery Graph (`PLT-01` IDENTITY)  
8. **CASCADE-001** → Incident → Recommend → Decision Trace → **execute=false**

Close on Executive Brief (`/executive`) if leadership is in the room: value is **unsafe recommendation avoided** and **time-to-justified confidence**, not isolate-speed or dashboard count.

---

## If the UI is slow or a page is empty

- Wait out the Render cold start, then hard-refresh.
- Confirm persona is **FDE** or **Full** (SOC-only hides Process / Recovery / Simulation / Executive).
- Reload the scenario from the rail so plant/asset/alert stay pinned.
- API fallback (same host): [https://ics-ot-command-center.onrender.com/docs](https://ics-ot-command-center.onrender.com/docs) — `GET /health`, `GET /diagnostics`, `GET /scenarios/catalog`.

---

## What this demo is allowed to prove

The deployed app helps humans **see disagreement and refuse unsafe action**. It does not become the plant.

Forbidden live conclusions:

- Highest CVSS = highest operational risk
- Backup CURRENT = recovery ready
- HIGH/CRITICAL alert = execute isolation
- CMDB or shadow spreadsheet is the winner
- Shift notes are policy
- UNKNOWN permission is permission
- PLC / SIS / interlock writes
- Regional isolate from a SCADA outage story
