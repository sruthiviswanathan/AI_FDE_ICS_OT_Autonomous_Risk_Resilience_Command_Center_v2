# Workflow 1 — Control Tower: do we trust the picture?

**Audience:** executives, SOC, plant operations, safety, continuity  
**Live app:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)  
**Duration:** 6–8 minutes  
**Scenario rail:** **Nominal** — *Estate nominal posture*  
**Screens:** **Control Tower** (`/`) → **Estate Dashboard** (`/estate`). Optional: **KPI Before/After**.  
**Decision the room must leave with:** this is inventory and disagreement, not a trusted plant picture and not a permission to act. **SLO-OT: OK** means zero execute in software — it does **not** mean the estate is healthy.

**One-line story:** Leadership asked for an autonomous command center. The estate already produces dashboards. What it does not produce is a trusted cyber-physical truth.

---

## How the Control Tower works in this command center

This screen is a **read-only join** of workshop files. It does not poll live PLCs. Freshness is **WORKSHOP-STATIC**. Mode is **synthetic-read-only**. Engines are **deterministic**.

The caption on the tiles says it plainly:

> Workshop inventory joins — estate-wide counts from deterministic engines, **not contextual risk rank**.

Two different number families sit on this page. Do not mix them.

**Inventory (how much stuff we registered)**

| Count | Number |
|---|---|
| Plants | **18** |
| Assets | **2016** |
| Telemetry events | **31,224** |
| Cyber alerts | **2800** (**860** HIGH/CRITICAL as inventory, not rank) |
| Vulnerabilities | **1100** |
| Safety barriers | **450** |
| Vendor sessions | **700** |
| Recovery rows | **144** |

**Disagreement (why we do not trust the picture)**

These tiles are the 14 diagnostic joins. They are **not** a risk leaderboard.

| Tile | Number | Question it asks |
|---|---|---|
| State conflicts | **200** | Registered ACTIVE vs observed OFFLINE/UNSEEN |
| Alias collisions | **5** | One name, two asset IDs |
| Bad / uncertain telemetry | **4094** | Quality is not GOOD |
| Duplicate telemetry | **120** | Same packet twice |
| Telemetry unit mismatches | **47** | TEMP tags not in C |
| Barriers degraded | **61** | Safety state not ACTIVE |
| Safety proof test due | **73** | Proof test not CURRENT |
| Unapproved remote sessions | **137** | Approved window not YES |
| Sessions without MFA | **128** | MFA not YES |
| Vendor session anomalies | **337** | Window / MFA / identity gaps |
| Stale / unknown backup | **25** | Backup flag not CURRENT (this **understates** unreadiness) |
| Unverified recovery deps | **29** | Deps not YES |
| Stale / missing runbooks | **35** | Runbook not CURRENT |
| Live undocumented paths | **779** | Observed but not documented |
| Maintenance conflicts | **244** | CMMS CLOSED vs field not returned |

**Five kinds of truth** (keep them separate; the tower does not pick a winner)

| State | What the tiles are hinting |
|---|---|
| Registered | CMDB / inventory flags |
| Observed | Passive / last-seen |
| Operational | Process context on alerts (many **UNKNOWN**) |
| Safety | Barrier and proof-test joins |
| Authority | No execute here — tier ≥3 is human |

Live APIs: [GET /health](https://ics-ot-command-center.onrender.com/health) · [GET /diagnostics](https://ics-ot-command-center.onrender.com/diagnostics) · [GET /data/views/estate](https://ics-ot-command-center.onrender.com/data/views/estate)

**Policy on this page**

| Line on screen | Meaning |
|---|---|
| Mode: **synthetic-read-only** | Not connected to real OT |
| **SLO-OT: OK** | Zero OT execute actions in software |
| Tier ≥3 is not license to execute (OPEN-001) | Isolate / access change stay human |
| Tier-4 refuse: 4 | No PLC / SIS / setpoint / interlock write |
| Conflicts visible — not hidden for demo | Do not “clean” the room |

**Demo traps**

- Nominal pins leftover **OT-00001 PLC** and **ALT-001744 LOW**. Skip that as “the healthy asset.”
- **SLO-OT: OK** is a **software** SLO. It is not a plant health badge.
- **18/18 plants elevated** is composite disagreement. It is not “18 plants about to explode.”
- The **25** stale-backup tile only counts flags that are not CURRENT. Most CURRENT backups still fail restore tests (Workflow 7).
- Quick incidents tagged **CTX UNKNOWN** are not isolate tickets.

---

## Room setup (30 seconds)

1. Open [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/). Wait if Render is slow.
2. Persona: **FDE** or **Full** (the label in the top right is **Full workshop view**).
3. Scenario rail: **Nominal**. Badges: **SYNTHETIC-READ-ONLY**, **DETERMINISTIC ENGINES**.
4. You will walk: mode + SLO → diagnostic tiles → 18/18 posture → Estate map (five layers) → “this is not permission to act.”

---

## Step 1 — Prove what this app is (and is not)

**Click:** **Control Tower** (or just land on `/`). Confirm **Nominal**.

Point at the top right and the header chips:

- Mode: **synthetic-read-only** · API **3.0.0**
- **NOMINAL** · **SYNTHETIC-READ-ONLY** · **DETERMINISTIC ENGINES**
- **SLO-OT: OK** · **WORKSHOP-STATIC**
- Footer: *Tier ≥3 is not license to execute in this API (OPEN-001)*

**Say:** “Leadership asked for an autonomous command center. First we prove the picture is not trusted. This UI is a workbench on synthetic files. It is not a plant controller. SLO-OT OK means we have not executed against OT. It does not mean the plants are fine.”

![Live Control Tower — Nominal](screenshots/tower/live-02-tower-viewport.png)

---

## Step 2 — Read the disagreement tiles (not the 2016-asset count)

Stay on Control Tower. Ignore **2016 assets** for a minute. Point at five tiles, one breath each:

| Point at | Say |
|---|---|
| **200** state conflicts | “We cannot name the box. Registered and observed disagree two hundred times.” |
| **4094** bad / uncertain telemetry | “We cannot trust the historian as process truth.” |
| **61** barriers degraded | “Protection is already degraded. Security is not the only clock.” |
| **137** unapproved remote sessions | “Someone may already be inside.” |
| **25** stale / unknown backup | “And this number is the *wrong* comfort — it understates recovery unreadiness.” |

Optional extras if the room is technical: **5** alias collisions, **779** undocumented paths, **244** maintenance conflicts, **47** unit mismatches (F≠C).

**Say:** “These counts come from deterministic joins. They are not a CVSS sort. They are why the next seven workflows exist.”

Same page, full scroll (posture cards + policy):

![Live Control Tower — full page](screenshots/tower/live-01-tower.png)

---

## Step 3 — Estate posture: 18/18 elevated is not “all plants on fire”

Scroll to **Estate posture**.

> **18/18 plants elevated · 2016 assets · 2800 alerts · 860 HC (inventory)**

Each plant card shows five red pills: **CYBER · PROCESS · SAFETY · RECOVERY · EVIDENCE**.

Caption on the page:

> cyber ≠ operational ≠ safety ≠ recovery — composite OK only when all layers are OK.

**Say:** “Every plant is elevated because at least one layer is not OK. Composite is worst-layer-wins. This is not a heat map of CVSS. It is a heat map of disagreement. 860 HIGH/CRITICAL is an inventory count, not the ticket order — that is Contextual Risk, later.”

Point at **Quick incidents**. Several HIGH/CRITICAL rows carry **CTX UNKNOWN**.

**Say:** “UNKNOWN process context is not NORMAL. A HIGH label with a blank process context is not a license to isolate. That is Workflow 5 and Workflow 8. Today we only prove we do not trust the picture yet.”

Skip leftover **OT-00001** / **ALT-001744 LOW** in the header.

---

## Step 4 — Estate Dashboard: five layers, still not a rank

**Click left nav:** **Estate Dashboard** (or **Open Estate Dashboard** on the tower).

Banner: *Control Tower · Interactive plant / asset / alert view — inventory signals, **not contextual risk rank**.*

Read the five layer definitions on the map legend:

| Layer | What “red” means here |
|---|---|
| **CYBER** | HIGH/CRITICAL alerts still OPEN or TRIAGED in the SOC queue |
| **PROCESS** | HC alerts where SOC severity and process context disagree (DEGRADED or UNKNOWN) |
| **SAFETY** | Barriers degraded, or bypass authorized unknown/no |
| **RECOVERY** | Backup or runbook stale, or recovery dependencies not verified |
| **EVIDENCE** | Registered vs observed asset state conflicts |

Pill colours: **OK** layer clear · **CAUTION** watch / unresolved · **AT RISK** blocks composite OK.

**Say:** “This map is how we refuse a single green dashboard. Cyber can look loud while safety is already bypassed. Recovery can look CURRENT while restore tests are stale. We keep the layers.”

![Live Estate Dashboard — five-layer legend](screenshots/tower/live-04-estate-viewport.png)

Scroll to **Inventory summary** and **Alerts by plant**:

- **2016** assets · **2800** alerts recorded · **200** state conflicts
- Every visible plant: composite **NOT OK**
- Useful exception to point at: **PLT-11** recovery pill can be green while cyber / process / safety / evidence stay red — composite is still **NOT OK**. Worst layer wins.

![Live Estate — 18 plants, composite NOT OK](screenshots/tower/live-05-estate-plants.png)

If you click a plant, **Drill-down · PLT-01 NOT OK** opens. Do **not** linger on **OT-00001** / **ALT-001744 LOW** as if that LOW alert were the estate story.

![Drill-down trap — leftover OT-00001 is not the estate](screenshots/tower/live-06-estate-alerts.png)

---

## Step 5 — Optional 30 seconds: KPI Before/After

**Click:** **KPI Before/After**.

The same diagnostic numbers refresh from the API. Point at two lines only:

| Signal | Observed | Note |
|---|---|---|
| SLO-OT execute violations | **OK** | must remain OK |
| SLO-LAT p95 | **BASELINE_PENDING** | OPEN-006 — do not invent a latency win |

**Say:** “Value in this workshop is disagreement made visible and unsafe action refused. We do not score ourselves on isolate-speed. Latency is still BASELINE_PENDING. That is honest.”

![Live KPI Before/After](screenshots/tower/live-07-kpi.png)

---

## Step 6 — Close in one sentence

Point at **18/18 elevated** and **SLO-OT: OK**.

> We do not trust the picture yet. Eighteen plants disagree with themselves. The app is allowed to show that. It is not allowed to write the plant.

| The screen **did** | The screen **must not** |
|---|---|
| Show 200 / 4094 / 61 / 137 / 25 as joins | Call 2016 assets “coverage, so we are fine” |
| Keep **SLO-OT: OK** as a no-execute SLO | Treat SLO-OT OK as plant health |
| Elevate **18/18** on worst-layer composite | Rank plants by CVSS or alert volume |
| Label 860 HC as **inventory** | Use 860 as the ticket order |
| Keep CTX UNKNOWN visible | Coerce UNKNOWN to NORMAL |
| Stay synthetic, read-only, deterministic | Connect to live OT or hide conflicts to beautify the room |

This screen **sets up** Workflows 2–8. You do not have to open those pages today. Just name them: identity, telemetry, risk, safety, vendor, recovery, CASCADE closer.

---

## Plain-English click path (print this)

1. Open the app. Persona **FDE** / **Full**. Scenario **Nominal**.
2. Point at **synthetic-read-only** and **SLO-OT: OK**. “Not a plant controller.”
3. **Control Tower** tiles: **200**, **4094**, **61**, **137**, **25**.
4. **Estate posture:** **18/18 elevated**. “Worst layer wins. Cyber ≠ ops ≠ safety ≠ recovery.”
5. Skip leftover **OT-00001**.
6. **Estate Dashboard** → five-layer legend → table all **NOT OK**.
7. Optional **KPI Before/After**: SLO-OT must remain OK; latency is BASELINE_PENDING.
8. “We do not trust the picture. We have not been given permission to act.”

---

## 90-second version

1. Nominal. Mode synthetic-read-only. SLO-OT OK ≠ healthy plant.  
2. Tiles: **200** identity, **4094** dirty tags, **61** barriers, **137** vendor, **25** backups.  
3. **18/18** plants elevated — five layers, worst wins.  
4. “This is inventory of disagreement. Not another dashboard. Not isolate.”

---

## If someone asks “so what do we do?”

- **Executives:** do not fund “more dashboards.” Fund trusted joins and a gate that can **refuse**.
- **SOC:** HIGH on this page is inventory. Rank comes later on Contextual Risk. UNKNOWN context is not isolate.
- **Operations / safety:** your layer can make composite NOT OK even when cyber is quiet — that is the point.
- **Continuity:** the **25** backup tile is not a DR attestation (Workflow 7).
- **Everyone:** next click is a named disagreement (Workflow 2 identity), not “execute.”

---

## Forbidden lines in this workflow

- “The plant is healthy because the app is green / SLO-OT is OK.”
- “2016 assets, so inventory is complete.”
- “18/18 red means isolate everything.”
- “Highest alert count is the first ticket.”
- “Hide the conflicts so the demo looks clean.”
- Any PLC / SIS / execute-isolation language from this screen.

---

## Screenshot index

| File | What it shows |
|---|---|
| `screenshots/tower/live-02-tower-viewport.png` | Nominal tiles 200 / 61 / 779 / 25 / 4094 |
| `screenshots/tower/live-01-tower.png` | Full Control Tower, 18/18 posture, policy footer |
| `screenshots/tower/live-04-estate-viewport.png` | Five-layer map legend |
| `screenshots/tower/live-05-estate-plants.png` | 2016 / 2800 / 200 · all plants NOT OK |
| `screenshots/tower/live-06-estate-alerts.png` | PLT-01 drill-down; skip OT-00001 |
| `screenshots/tower/live-07-kpi.png` | Same diagnostics; SLO-OT must remain OK |
