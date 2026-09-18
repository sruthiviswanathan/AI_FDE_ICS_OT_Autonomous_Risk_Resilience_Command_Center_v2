# Workflow 4 — Contextual risk: highest CVSS is not the plant’s problem

**Audience:** SOC, process engineering, plant leadership, executives  
**Live app:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)  
**Duration:** 6–8 minutes  
**Scenario rail:** **CASCADE-001** (pins the plant-relevant finding)  
**Screen:** **Contextual Risk** (`/risk`)  
**Decision the room must leave with:** CVSS is an **input**, not the sort key. A 9.8 that cannot reach the plant is not the first ticket. The LLM must not re-rank this list.

**One-line story:** Legacy sorted by scanner score. Operations sorts by “can it hit a critical unit, and can we recover?”

---

## How contextual risk works in this command center

This is not a chatbot picking a favourite CVE. It is a **deterministic rank** (ADR-03). Method name on the API: `contextual_operational_risk`. Note on the API: *legacy_rank remains CVSS-only for contrast; LLM must not re-rank*.

**Legacy (what we refuse to ship as default)**

`legacy_rank` in `src/ot_command/legacy/risk.py` sorts findings by `cvss` only. Highest number wins.

**Modern (what this screen shows)**

Each finding gets a **contextual score** from factors. CVSS still appears, labelled **input only — not the sort key**.

| Factor | What it asks | Demo numbers |
|---|---|---|
| **Process criticality** | How bad is it if this unit is hurt? | VUL-00098: HIGH **30 pts**. VUL-00706: LOW **10 pts** |
| **Reachability** | Can the network actually get there? | VUL-00098: YES **35 pts**. VUL-00706: NO **5 pts** |
| **CVSS input** | Scanner score, counted but not the sort key | 8.7 → **17.4 pts**. 9.8 → **19.6 pts** |
| **Compensating control** | Is something already reducing exposure? | ALLOWLIST **−3**. SEGMENTED **−2** |
| **Safety** | Barrier state join (may be 0 on this row) | **0** on both talking-pair rows |
| **Recovery** | Can we recover if we have to act? CURRENT backup is not ready | DEGRADED **8 pts** |

**Talking pair (EVAL-002)**

| | Scanner favourite | Plant problem |
|---|---|---|
| Finding | **VUL-00706** | **VUL-00098** |
| Asset | **OT-00654** | **OT-01016** |
| CVSS | **9.8** | **8.7** |
| Scanner severity | CRITICAL | HIGH |
| Reachable | **NO** | **YES** |
| Process criticality | **LOW** | **HIGH** (unit PLT-10-U06, safe-state MIN_LOAD) |
| Contextual score | **40.6** | **87.4** |
| Who would win on CVSS-only? | VUL-00706 | — |
| Who should be first for the plant? | — | VUL-00098 |

Same plant, even sharper: on **PLT-10** plant-wide, **VUL-00817** (CVSS **6.0**, reachable YES, CRITICAL) scores **95.0** and ranks **above** VUL-00098 (CVSS 8.7, score 87.4). A 6.0 can outrank an 8.7.

**What the UI will not do**

- Let the LLM reshuffle the table.
- Treat scanner severity as operational risk.
- Turn a high score into Isolate-execute.

---

## Room setup (30 seconds)

1. Open [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/). Wait if Render is slow.
2. Persona: **FDE** or **Full workshop view**.
3. Leave **execute=false** badges visible. This screen ranks. It does not act.

---

## Step 1 — Control Tower: CVSS is not even on this wall

**Click:** **Control Tower**.

Point at the diagnostic tiles (200 conflicts, 4094 bad tags, 61 barriers). Then say:

> “This wall is disagreement, not a CVE leaderboard. If I sorted the estate by highest CVSS, I would still not know which unit can be reached, which barrier is bypassed, or whether we can recover.”

![Live Control Tower](screenshots/risk/live-01-tower.png)

*Live capture: Control Tower. Estate diagnostics are not a CVSS rank.*

---

## Step 2 — Load CASCADE-001 so the plant finding is pinned

**Click the scenario rail:** **CASCADE-001**.

Pins you should see:

- Plant **PLT-10**, asset **OT-01016** (DCS controller), alert **ALT-002783 HIGH**
- Badges: barrier bypassed unauthorized, safe-state **MIN_LOAD**, vendor session, SOC vs PE dissent, shift notes untrusted, **execute=false**
- Eval: **EVAL-007**

**Say:** “We are about to rank the finding on the controller in the cascade. Not ‘the scariest CVE in the catalogue.’”

![Live Control Tower after CASCADE-001](screenshots/risk/live-02-cascade-tower.png)

---

## Step 3 — Open Contextual Risk (read the workbench, not just the number)

**Click left nav:** **Contextual Risk**.

You should see:

1. Plant / Asset dropdowns and **Search**.
2. Two modes: **Contextual rank (default)** and **CVSS-only (warn)**.
3. A note: workshop corpus has **one finding per asset**. Filtering OT-01016 shows **at most one row**. For a list, choose **All assets (plant-wide)** in the Asset dropdown.
4. A table: Finding, Asset, **CVSS (input)**, Reach, Criticality, Severity, **Score**.
5. Factor breakdown cards under the row.

**Presenter trap:** CASCADE pins **OT-01016**, so you may see **only VUL-00098**. That is the plant finding. The 9.8 comparison is a second search (Step 5). Do not panic that the 9.8 is missing from this first view.

![Live Contextual Risk — VUL-00098](screenshots/risk/live-03-risk-cascade.png)

Same breakdown, full page:

![Live Contextual Risk — factor cards](screenshots/risk/live-04-risk-scrolled.png)

---

## Step 4 — Read VUL-00098 out loud (this is the plant problem)

Point at the row:

| Field | Value |
|---|---|
| Finding | **VUL-00098** |
| Asset | **OT-01016** |
| CVSS (input) | **8.7** |
| Reach | **YES** |
| Criticality | **HIGH** |
| Severity (scanner label) | **HIGH** |
| Contextual score | **87.4** |

Then the factor cards:

- Process criticality **30 pts** (HIGH)
- Reachability **35 pts** (YES) — this is the biggest operational weight
- CVSS input **17.4 pts** (8.7) — **input only — not the sort key**
- Compensating control **−3 pts** (ALLOWLIST)
- Safety **0 pts** on this card (the bypass still sits on the CASCADE badges and Safety screen)
- Recovery **8 pts**, status **DEGRADED** — *CURRENT backup alone is not RecoveryReady*

**Say:** “Reachability and process criticality outweigh the scanner score. 8.7 is not small. It is just not why this row is first for the plant.”

Live: [risk for OT-01016](https://ics-ot-command-center.onrender.com/risk/contextual?asset_id=OT-01016&limit=8)

---

## Step 5 — Show the 9.8 that should not win (EVAL-002)

Keep **Contextual rank (default)** on.

1. Change **Asset** to **OT-00654** (or Search that ID). Plant may leave PLT-10; that is fine.
2. You should get **VUL-00706**.

| Field | VUL-00706 (scanner favourite) | VUL-00098 (plant problem) |
|---|---|---|
| CVSS | **9.8** | **8.7** |
| Scanner severity | CRITICAL | HIGH |
| Reachable | **NO** | **YES** |
| Process criticality | **LOW** (10 pts) | **HIGH** (30 pts) |
| Reach points | **5** | **35** |
| Contextual score | **40.6** | **87.4** |

**Say:** “Legacy `legacy_rank` would put 9.8 first. This engine gives it 40.6 because it cannot reach the plant and the process is LOW. The 8.7 that can reach a HIGH unit scores 87.4. Highest CVSS is not the plant’s problem.”

Live: [risk for OT-00654](https://ics-ot-command-center.onrender.com/risk/contextual?asset_id=OT-00654&limit=8)

**Optional 20 seconds — same plant, even clearer:** set Plant **PLT-10**, Asset **All assets (plant-wide)**, Search. **VUL-00817** CVSS **6.0** scores **95.0** and sits above VUL-00098 (8.7 / 87.4). A six can outrank an eight-point-seven.

Live: [PLT-10 plant-wide](https://ics-ot-command-center.onrender.com/risk/contextual?plant_id=PLT-10&limit=12)

---

## Step 6 — Flip CVSS-only (warn) so people see the anti-pattern

Go back to the CASCADE pin (OT-01016) if you left it.

1. Click **CVSS-only (warn)**.
2. Point at the amber banner: **CVSS-only sort is anti-pattern (APP-AT-002)**.
3. Say: “This toggle exists to show the old habit. It is labelled a warning on purpose. We do not present this as the product default.”
4. Click **Contextual rank (default)** again before you leave the screen.

![Live CVSS-only warning](screenshots/risk/live-05-cvss-only.png)

*Live capture: CVSS-only (warn) selected. Banner states the anti-pattern. With one asset filtered you still see one row — the warning is the point, not a new table.*

---

## Step 7 — Close: ranking is not permission to isolate

Stay on Contextual Risk. Point at CASCADE badges: **SOC vs PE dissent**, **execute=false**.

**Say:** “Even the right rank is not an isolate button. SOC may still want speed. Process still has MIN_LOAD. This screen tells us which finding to talk about. Safety and Recommendation Gate decide whether a draft is even allowed. No PLC write.”

| The screen **did** | The screen **must not** |
|---|---|
| Show CVSS as an input | Sort by CVSS as the product default |
| Weight reachability and process criticality | Let the LLM re-rank |
| Contrast 9.8 / unreachable vs 8.7 / reachable | Call scanner CRITICAL “the plant emergency” |
| Warn on CVSS-only | Hide the warning and demo CVSS as “smarter AI” |
| Keep execute=false | Isolate because the score is 87.4 |

**Closing sentence:** “Contextual risk means: can it reach a unit that matters, and can we recover? The 9.8 that cannot get there is not ticket one.”

---

## Plain-English click path (print this)

1. Open the app. Persona **FDE** / **Full**.
2. **Control Tower** — “This wall is not a CVE leaderboard.”
3. Scenario rail → **CASCADE-001**. Pins **OT-01016** / **ALT-002783**.
4. Left nav → **Contextual Risk**. Mode **Contextual rank (default)**.
5. Read **VUL-00098**: CVSS **8.7**, Reach **YES**, score **87.4**. Point at “CVSS is input only — not the sort key.”
6. Search asset **OT-00654**. Read **VUL-00706**: CVSS **9.8**, Reach **NO**, score **40.6**.
7. Say: “9.8 loses. 8.7 wins for the plant because it is reachable.”
8. Optional: Plant **PLT-10**, Asset **All assets (plant-wide)** — a **6.0** can sit above an **8.7**.
9. Click **CVSS-only (warn)** — read the anti-pattern banner — switch back to Contextual rank.
10. “We ranked. We did not isolate.”

---

## 90-second version

1. CASCADE-001 → **Contextual Risk**.  
2. **VUL-00098** / OT-01016: 8.7, reachable YES, score **87.4**.  
3. Search **OT-00654** / **VUL-00706**: 9.8, reachable NO, score **40.6**.  
4. “Highest CVSS is not the plant’s problem. CVSS is an input, not the sort key. No isolate.”

---

## If someone asks “so what do we do?”

Answer only this:

- **SOC:** do not open the 9.8 first just because the scanner shouted CRITICAL.
- **Process:** OT-01016 is reachable and HIGH — that is the conversation, still not an isolate execute.
- **Leadership:** ticket order follows plant consequence, not CVSS descending.
- **Nobody:** the LLM does not get to reshuffle this list.

---

## Forbidden lines in this workflow

- “We ranked by CVSS / severity label.”
- “CRITICAL means isolate.”
- “The AI decided the order.”
- “9.8 is always first.”
- Any Execute Isolation / PLC language.

---

## Screenshot index

| File | What it shows |
|---|---|
| `screenshots/risk/live-01-tower.png` | Control Tower (not a CVE board) |
| `screenshots/risk/live-02-cascade-tower.png` | CASCADE-001 pins OT-01016 |
| `screenshots/risk/live-03-risk-cascade.png` | Contextual Risk workbench, VUL-00098 |
| `screenshots/risk/live-04-risk-scrolled.png` | Factor breakdown cards |
| `screenshots/risk/live-05-cvss-only.png` | CVSS-only (warn) anti-pattern banner |
