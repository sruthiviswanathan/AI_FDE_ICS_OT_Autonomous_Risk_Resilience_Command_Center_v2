# Workflow 3 — Telemetry: the historian is lying in Celsius

**Audience:** process engineers, SOC, historian / data owners, safety, executives  
**Live app:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)  
**Duration:** 6–8 minutes  
**Scenario rail:** **inject_02 — Historian quality degradation** (EVAL-009 / EVAL-004 / EVAL-022)  
**Screen:** **Telemetry Quality** (`/telemetry`)  
**Decision the room must leave with:** a historian number is not process truth until **quality**, **unit**, and **which clock** are checked. The app does **not** convert F to C, and it does **not** treat GOOD as “the unit is healthy.”

**One-line story:** The historian can be on time, marked GOOD, and still be lying in Fahrenheit.

---

## How telemetry works in this command center

This is not a live plant feed. It is a **read-only historian slice** from `data/telemetry/tag_telemetry.jsonl`.

Each packet is a bundle. The UI shows the bundle. It does not “fix” it.

| Piece | What it means | Demo example |
|---|---|---|
| **Tag** | Historian point name | `PLT-01-U03_TEMP` |
| **Asset** | Which box the tag is joined to | **OT-00063** |
| **Value** | The number in the packet | **253.837** |
| **Unit** | Unit **on the packet** | **F** |
| **Engineering unit** | Unit the tag is supposed to use | **C** |
| **Quality** | Historian quality flag | **GOOD**, **BAD**, or **UNCERTAIN** |
| **Event time** | When the process event is claimed to have happened | `2026-09-01T00:00:00` |
| **Ingest time** | When the command center received the packet | `2026-09-01T00:02:09` |
| **Lag** | Ingest minus event (seconds) | **129** on the F row |
| **Source** | Where the packet came from | **HISTORIAN** |

**Dual clock (ADR-02):** the timeline is ordered by **event time**, not by when the packet arrived. Ingest time is freshness, not sequence. Telemetry lag on this estate: p50 about **119s**, max **240s**, **0** negative (packets do not arrive before the event in this historian file).

**What the engines do**

- Count BAD / UNCERTAIN packets (estate **4094**).
- Count duplicate packets (estate **120**).
- Count `*_TEMP` tags whose packet unit is not **C** (estate **47**).
- Flag **UNIT MISMATCH** when packet unit ≠ engineering unit.
- Keep GOOD, BAD, and UNCERTAIN visible. They do **not** impute BAD → GOOD.

**What they refuse**

- Plot F as if it were C.
- Silently convert 253.837 F into Celsius and drop the flag.
- Sort the process story by ingest time only.
- Treat quality GOOD as “process healthy” (OPEN-026).
- Use a mismatched or BAD tag as a control input.

**Two scopes you will see on the same page — do not mix them up**

| Scope | Bad / uncertain | Duplicates | Unit mismatches | Where |
|---|---|---|---|---|
| **Whole estate** | **4094** | **120** | **47** | Control Tower tiles + inject_02 badges |
| **This tag / PLT-01 slice** | **203** | **6** | **2** | Telemetry Quality header after inject_02 |

The 4094 is the estate problem. The first timeline row is the one packet you can point at.

---

## Room setup (30 seconds)

1. Open [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/). Wait if Render is waking up.
2. Persona: **FDE** or **Full workshop view**.
3. Mode stays `synthetic-read-only`. No PLC write, no “correct the historian” button.

---

## Step 1 — Control Tower: prove the historian is already dirty

**Click:** **Control Tower**.

**Point at three tiles**

| Tile | Number | Stakeholder translation |
|---|---|---|
| Bad / uncertain telemetry | **4094** | Packets the historian itself does not trust |
| Duplicate telemetry | **120** | Same tag / time / value seen more than once |
| Telemetry unit mismatches | **47** | Temperature tags not in Celsius |

**Say:** “Thirty-one thousand historian events sit behind this screen. Four thousand of them are already bad or uncertain. Forty-seven temperature tags are not in C. If we chart this as a healthy trend, we will make the wrong call.”

![Live Control Tower — telemetry tiles](screenshots/telemetry/live-01-tower-telemetry-tiles.png)

*Live capture: Control Tower. Circle **4094**, **120**, and **47**. These are estate diagnostics, not a risk rank.*

---

## Step 2 — Load inject_02 so the story is pinned

**Click the scenario rail:** **inject_02**.

Badges should appear:

- **BAD/UNCERTAIN ≥4094**
- **DUPLICATES ≥120**
- **UNIT MISMATCH F≠C (≥47)**
- **EVENT_TIME + INGEST_TIME**
- Scenario: *Historian quality degradation*
- Eval: **EVAL-009**

**Say:** “inject_02 does not invent a broken historian. It pins the quality problem we already have, and it reminds us there are two clocks.”

![Live Control Tower after inject_02](screenshots/telemetry/live-02-inject02-tower.png)

*Live capture after inject_02. Top bar and scenario rail show the four telemetry badges. Footer still says this API does not execute.*

---

## Step 3 — Open Telemetry Quality (this is the workbench)

**Click left nav:** **Telemetry Quality**.

inject_02 should already scope the page to tag **PLT-01-U03_TEMP**. If the tag box is empty, type `PLT-01-U03_TEMP` and click **Search timeline**.

You should see four zones:

1. **Quality counters** for the current scope (plant/tag), plus the note that historian tags cover only a subset of assets (~182 estate-wide).
2. **Ingest lag** — p50 **119**, max **240**, negative count **0**.
3. **Tag search** — `PLT-01-U03_TEMP` / Search timeline / Clear tag.
4. **Timeline table** with both clocks: Event time, Ingest time, Lag (s), Tag, Value, Unit, Quality, Flags.

![Live Telemetry Quality after inject_02](screenshots/telemetry/live-03-telemetry-after-inject02.png)

**Presenter trap:** the header may show **203** bad/uncertain and **2** unit mismatches. That is the **tag / plant slice**, not the estate. The estate numbers stay on the badges: **4094** and **47**. Say both. Do not let the room think the problem shrank.

Same page, full table:

![Live Telemetry timeline table](screenshots/telemetry/live-04-telemetry-scrolled.png)

---

## Step 4 — Story A: the lying Celsius row (EVAL-022)

**Point at the first timeline row. Read it slowly.**

| Field | What the screen shows | What you say |
|---|---|---|
| Event time | 2026-09-01 00:00:00 | When the process event is claimed |
| Ingest time | 2026-09-01 00:02:09 | When we received it — **129 seconds later** |
| Tag | **PLT-01-U03_TEMP** | A temperature tag. Engineering unit is **C** |
| Value | **253.837** | Do not call this “253 degrees C” |
| Unit | **F** | The packet is Fahrenheit |
| Quality | **GOOD** | The historian still marked it good |
| Flags | **UNIT MISMATCH** | This is the punch |

Live record: [timeline for PLT-01-U03_TEMP](https://ics-ot-command-center.onrender.com/telemetry/timeline?tag_id=PLT-01-U03_TEMP&limit=8)  
Event id: **TEL-00000288** · asset **OT-00063** · source HISTORIAN · `engineering_unit: C` · `unit_mismatch: true`

**Say:** “Quality is GOOD. The number is 253. If we plot this on a Celsius chart, it looks like a runaway temperature. It is Fahrenheit. The historian is lying in Celsius. We flag the mismatch. We do not convert it in silence. We do not use it for control.”

Then point at the next row: same tag, unit **C**, value ~129, quality GOOD, **no** mismatch flag.

**Say:** “Same tag, minutes later, now in C. If you mixed these two points on one trend, you invented a process event that never happened.”

Also point at a later row with quality **UNCERTAIN** (for example 02:20:00, value ~132, unit C).

**Say:** “UNCERTAIN is not secretly GOOD. BAD is not secretly GOOD. GOOD is not ‘the unit is healthy.’”

---

## Step 5 — Story B: two clocks (EVAL-004)

Keep the same table. Do not re-sort it.

1. Run a finger down **Event time** — that is process order.
2. Point at **Ingest time** and **Lag (s)** — packets arrive about 1–4 minutes late.
3. Point at ingest lag header: negative count **0** on this historian (packets are late, not from the future). Enterprise logs elsewhere can invert; this tag file does not.

**Say:** “If I sorted by when the packet arrived, I would tell the wrong story of the unit. Event time is the process clock. Ingest time is the mail delay. Both stay on screen.”

**Must not do in the demo:** click anything that would order the table by ingest time only. The product timeline `order` is `event_time`. Asking the API to order by ingest_time is rejected.

---

## Step 6 — Show why this is not “just a data-quality slide”

Stay on tag **PLT-01-U03_TEMP**. Do **not** isolate.

Walk the consequence split in words (you can stay on this page):

| Lens | What dirty telemetry does |
|---|---|
| **Cyber** | A SOC trend built on F-as-C looks like an attack or a runaway. It may be a unit flag. |
| **Process** | Operators cannot tell if 253 is a real temperature or a unit lie. |
| **Safety** | You must not trip, bypass, or isolate from a mismatched GOOD packet. |
| **Resilience** | Recovery and “is the unit stable?” need quality-aware evidence, not a pretty chart. |
| **Authority** | The app may **observe / correlate / summarize**. It must not write a setpoint to “correct” the tag. |

If you have 20 extra seconds, open **Recommendation Gate** and show there is still **no execute**. Telemetry quality is an input to a draft, not a control action.

---

## Step 7 — Close: what telemetry reconciliation did / did not do

| The screen **did** | The screen **must not** |
|---|---|
| Show event time and ingest time together | Sort the process story by ingest time only |
| Flag **UNIT MISMATCH** on TEL-00000288 | Plot 253.837 as Celsius |
| Keep quality GOOD / UNCERTAIN / BAD visible | Impute BAD → GOOD |
| Scope estate 4094 vs tag-slice 203 | Hide BAD rows to beautify the demo |
| Cite `data/telemetry/tag_telemetry.jsonl` | Treat GOOD as process healthy |
| Stay read-only | Write a PLC / historian correction |

**Closing sentence:** “Telemetry reconciliation means: keep the packet honest. Two clocks, a quality flag, and a unit flag. Humans still decide. This app will not convert F to C and it will not drive the plant from a dirty tag.”

---

## Who speaks when

| Stakeholder | What you ask them to look at | What you ask them to decide later (not in the UI) |
|---|---|---|
| Process engineer | First row: 253.837 F vs later ~129 C | Is the tag in the wrong unit, or is the process really hot? |
| Historian / data owner | Dual clock + UNIT MISMATCH flag | Who owns engineering unit C vs packet unit F |
| SOC | Do not raise a cyber incident from a unit lie | Quality join before “anomalous temperature” |
| Safety | GOOD + mismatch is not a trip condition | No SIS / interlock change from this screen |
| Executive | 4094 dirty packets, 47 F-on-TEMP | Value is unsafe-chart avoided, not a prettier trend |

---

## Plain-English click path (print this)

1. Open the app. Persona **FDE** / **Full**.
2. **Control Tower** → point at **4094**, **120**, **47**.
3. Scenario rail → **inject_02**. Read the four badges.
4. Left nav → **Telemetry Quality**.
5. Confirm tag box is **PLT-01-U03_TEMP** (Search timeline if needed).
6. Explain header **203 / 6 / 2** is this slice; badges **4094 / 47** are the estate.
7. First row: value **253.837**, unit **F**, quality **GOOD**, flag **UNIT MISMATCH**.
8. Next rows: same tag in **C**. Point at **UNCERTAIN** rows too.
9. Point at **Event time** vs **Ingest time** vs **Lag**.
10. Say: “We do not convert. We do not chart this as healthy C. We do not isolate from it.”

---

## 90-second version

1. Control Tower → **4094** bad/uncertain, **47** unit mismatches.  
2. Click **inject_02**.  
3. **Telemetry Quality** → tag `PLT-01-U03_TEMP`.  
4. First row: **253.837 F**, quality **GOOD**, **UNIT MISMATCH**.  
5. “The historian is lying in Celsius. Two clocks. No silent conversion. No control use.”

---

## If someone asks “so what do we do?”

Answer only this:

- **Process:** do not change setpoints from this tag until unit and quality are confirmed.
- **Historian owner:** packet unit F vs engineering unit C on `PLT-01-U03_TEMP` / TEL-00000288.
- **SOC:** an “anomalous 253 C” may be a unit flag, not an attack.
- **Safety:** GOOD is not permission to act.

---

## Forbidden lines in this workflow

- “We’ll just convert F to C.”
- “Quality is GOOD, so the process is healthy.”
- “Sort by when we received it — that’s close enough.”
- “Hide the BAD rows so the demo looks clean.”
- “Isolate / trip / write the PLC because temperature spiked.”

---

## Screenshot index

Live captures (this deployment):

| File | What it shows |
|---|---|
| `screenshots/telemetry/live-01-tower-telemetry-tiles.png` | Control Tower: 4094 / 120 / 47 |
| `screenshots/telemetry/live-02-inject02-tower.png` | inject_02 badges on Control Tower |
| `screenshots/telemetry/live-03-telemetry-after-inject02.png` | Telemetry Quality + first UNIT MISMATCH row |
| `screenshots/telemetry/live-04-telemetry-scrolled.png` | Full dual-clock timeline |

API fallback (same host):

- [GET /telemetry/quality?plant_id=PLT-01](https://ics-ot-command-center.onrender.com/telemetry/quality?plant_id=PLT-01)
- [GET /telemetry/timeline?tag_id=PLT-01-U03_TEMP](https://ics-ot-command-center.onrender.com/telemetry/timeline?tag_id=PLT-01-U03_TEMP&limit=8)
