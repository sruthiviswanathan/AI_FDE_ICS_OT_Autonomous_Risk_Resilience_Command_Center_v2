# Workflow 5 — Safety vs security: isolate now can become the incident

**Audience:** SOC, process engineering, safety / SIS owners, executives  
**Live app:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)  
**Duration:** 6–8 minutes  
**Scenario rail:** **CASCADE-001** (preferred). Optional short add-on: **inject_04**.  
**Screens:** **Safety vs Security** → **Recommendation Gate**  
**Decision the room must leave with:** a HIGH SOC alert is not a license to isolate. Isolation is never execute in this app. Observing a bypass is not permission to bypass an interlock.

**One-line story:** At 08:47 SOC says isolate. At 08:50 process says that may destabilize the unit. The command center must not become the incident.

---

## How safety vs security works in this command center

Two different truths can be true at the same time:

| Lens | What it sees in CASCADE-001 |
|---|---|
| **Security (SOC)** | Alert **ALT-002783** HIGH on **OT-01016**. Type CONFIG_DRIFT. SOC status **SUPPRESSED**. Process context **UNKNOWN**. Legacy habit: HIGH → **ISOLATE**. |
| **Safety / process** | Barrier **PLT-10-SAFE-07** on unit **PLT-10-U06** is **BYPASSED**, authorized **NO**. Safe-state is **MIN_LOAD**. Process engineer at 08:50: abrupt isolation may destabilize the unit. |

**Policy (ADR-04 / ACTION_TIERS)**

| Action | Tier | What the demo does |
|---|---|---|
| observe / correlate / summarize | 0 | Allowed |
| recommend | 1 | Draft only |
| isolate_endpoint | 3 | Human authorize — **not executed here** |
| write_plc_logic / change_setpoint / modify_sis / bypass_interlock | 4 | **Refuse** |

API note on `/safety/conflicts`: *IsolationRecommendation never equals execute; tier 3 isolate_endpoint is human-only.*

**What “reconciliation” means here**

- Show the bypass and the SOC demand **together**.
- Keep **UNKNOWN** process context as UNKNOWN (not NORMAL).
- Keep **bypass_authorized=NO** (UNKNOWN is not permission either).
- Produce **DO_NOT_ISOLATE**, **EXECUTE = No**, safe-state **MIN_LOAD**.
- Name required humans. Disable Authorize (OPEN-001).
- There is **no Execute Isolation** button.

---

## Room setup (30 seconds)

1. Open [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/). Wait if Render is slow.
2. Persona: **FDE** or **Full**.
3. You will walk **08:38 bypass → 08:47 SOC isolate → 08:50 PE warning → 08:55 governed draft**.

---

## Step 1 — Control Tower: safety is already degraded estate-wide

**Click:** **Control Tower**.

Point at:

- **61** barriers degraded
- **73** safety proof tests due

**Say:** “Security is not the only clock in this building. Protection is already degraded on dozens of barriers. If we isolate from a HIGH label, we may hit a unit that is already running with a bypass.”

![Live Control Tower](screenshots/safety/live-01-tower.png)

---

## Step 2 — Load CASCADE-001 (the 08:47 vs 08:50 story)

**Click scenario rail:** **CASCADE-001**.

Pins:

- Plant **PLT-10**, asset **OT-01016**, alert **ALT-002783 HIGH**
- Badges: **BARRIER BYPASSED UNAUTHORIZED**, **SAFE_STATE MIN_LOAD**, **08:24 VENDOR SESSION**, **SOC VS PE DISSENT**, **SHIFT NOTES UNTRUSTED**, **EXECUTE=FALSE**
- Eval **EVAL-007**
- Footer: *Tier 3 is not license to execute in this API*

Walk the times out loud:

| Time | What happened |
|---|---|
| 08:38 | Safety barrier recorded bypassed |
| 08:47 | SOC recommends immediate isolation |
| 08:50 | Process engineer: isolation may destabilize the unit |
| **08:55** | Command center must recommend a safe governed response — not execute |

**Say:** “SOC speed and process stability are in conflict. That conflict is the product.”

![Live Control Tower after CASCADE-001](screenshots/safety/live-02-cascade-tower.png)

---

## Step 3 — Open Safety vs Security (the conflict board)

**Click left nav:** **Safety vs Security**.

For **PLT-10** you should see:

| Tile | Number |
|---|---|
| Degraded barriers | **8** |
| Bypassed unauthorized | **1** |
| High/Critical unknown context | **29** |

Table row (the punch):

| Barrier | Unit | State | Bypass authorized | Flag |
|---|---|---|---|---|
| **PLT-10-SAFE-07** | **PLT-10-U06** | **BYPASSED** | **NO** | **SAFETY DEGRADED** |

Right-hand **Provenance** graph: alert → asset → unit → barriers (one red/bypassed). Caption: *Timeline cascade — read left to right (vendor → barrier → isolate → destabilize).*

**Say:** “The barrier that should protect this unit is already bypassed, and that bypass is not authorized. Isolating the controller now is not ‘making it safer.’ It may be the next incident.”

![Live Safety vs Security conflict board](screenshots/safety/live-03-safety-cascade.png)

**Presenter trap — red “Safety context (Q3)” error.** The panel may show `Q3 requires asset_id or alert_id` even though OT-01016 and ALT-002783 are in the top bar. **Do not freeze.** The conflict **table** is the evidence. Click the top **Search** if you want; the table and badges still tell the story if Q3 stays empty. Do not apologize as if the demo failed.

![Same board after Search — table still holds](screenshots/safety/live-06-safety-after-search.png)

Live API: [PLT-10 safety conflicts](https://ics-ot-command-center.onrender.com/safety/conflicts?plant_id=PLT-10)

Also say: **winner = null**. Safety does not pick a silent winner over SOC, or the other way around.

---

## Step 4 — Name the two truths on the same alert

Keep CASCADE pinned. Point at alert **ALT-002783**:

| Field | Value | Why it matters |
|---|---|---|
| Severity | **HIGH** | Legacy `legacy_isolation_recommendation` would say **ISOLATE** |
| SOC status | **SUPPRESSED** | SOC ticket state is **not** an SIS trip suppression |
| Process context | **UNKNOWN** | UNKNOWN is not NORMAL. Do not isolate from a blank |
| Safe-state | **MIN_LOAD** | Process mode if things go wrong — not “isolate the box” |

**Say:** “HIGH plus SUPPRESSED plus UNKNOWN is not a green light. Legacy would isolate. Safety says the unit is already degraded. UNKNOWN process context means abstain from execute.”

---

## Step 5 — Recommendation Gate: prove there is no isolate button

**Click:** **Recommendation Gate**.

1. Confirm plant **PLT-10**, asset **OT-01016**, alert **ALT-002783**.
2. Click **Request draft packet**.
3. Wait for the workflow chips (Identity, Risk, Safety, Recovery, Authority, Human Review).

Read the packet slowly:

| Field | What the screen shows |
|---|---|
| Recommendation | **DO_NOT_ISOLATE** |
| Execute | **No** |
| Safe state | **MIN_LOAD** |
| Process impact | Unit **PLT-10-U06**, process context **UNKNOWN**, production criticality **HIGH** |
| Safety impact | Observed bypass is **not** permission to `bypass_interlock` (**tier 4 refuse**) |
| Required authority | Process Engineer · Safety/SIS Owner · VP Operations |
| Authorize | **Disabled — OPEN-001** |
| Banner | Advisory only — **no Execute Isolation / Write PLC / Modify SIS** |

**Say:** “This is the whole safety-vs-security product. SOC wanted isolate at 08:47. The packet is DO_NOT_ISOLATE. Execute is No. Authorize is disabled. Observing a bypass is not a bypass tool.”

![Live Recommendation Gate — DO_NOT_ISOLATE](screenshots/safety/live-07-draft-packet.png)

If the packet has not loaded yet, you only see **Request draft packet**. Click it. There is still no Execute control.

![Gate before the packet](screenshots/safety/live-05-recommend.png)

---

## Step 6 — Optional 30 seconds: inject_04 (bypass aging, different plant)

If you have time:

1. Scenario rail **inject_04**.
2. Stay on **Safety vs Security**, plant **PLT-03**.
3. Point at **PLT-03-SAFE-14** on **PLT-03-U05**: BYPASSED, authorized **NO**, MIN_LOAD boiler / **OT-00211**.

**Say:** “CASCADE is the morning story. inject_04 is the same rule on another unit: recorded bypass is visible; we do not call bypass_interlock; UNKNOWN is not authorized.”

Then go back to CASCADE-001 before the close.

---

## Step 7 — Close in one sentence

Point at **EXECUTE=FALSE** and **DO_NOT_ISOLATE**.

> Isolation now can become the incident. We showed the bypass, the SOC demand, and the process warning together. The app drafts DO_NOT_ISOLATE. It will not write the PLC.

| The screen **did** | The screen **must not** |
|---|---|
| Show BYPASSED + authorized NO | Treat HIGH as isolate-execute |
| Keep process context UNKNOWN | Coerce UNKNOWN to NORMAL |
| Draft DO_NOT_ISOLATE, execute No | Show an Execute Isolation button |
| Name Process Eng + Safety + VP Ops | Let SOC self-authorize |
| Refuse bypass_interlock (tier 4) | Turn “observe bypass” into a bypass tool |
| Distinguish SOC SUPPRESSED from SIS | Suppress a trip because the ticket is SUPPRESSED |

---

## Plain-English click path (print this)

1. Open the app. Persona **FDE** / **Full**.
2. **Control Tower** → point at **61** barriers degraded.
3. Scenario rail → **CASCADE-001**. Read **SOC VS PE DISSENT** and **EXECUTE=FALSE**.
4. Walk 08:38 bypass → 08:47 SOC isolate → 08:50 PE warning.
5. **Safety vs Security** → row **PLT-10-SAFE-07** / **PLT-10-U06** / **BYPASSED** / authorized **NO**.
6. If the red Q3 error appears, ignore it and stay on the table.
7. **Recommendation Gate** → **Request draft packet**.
8. Read **DO_NOT_ISOLATE**, **Execute No**, **Authorize disabled**.
9. “We did not isolate. Isolating now could be the incident.”

---

## 90-second version

1. CASCADE-001.  
2. Safety vs Security: **PLT-10-SAFE-07 BYPASSED / NO**.  
3. Recommendation Gate → draft **DO_NOT_ISOLATE**, execute **No**.  
4. “08:47 SOC vs 08:50 process. Highest alert is not isolate. No PLC write.”

---

## If someone asks “so what do we do?”

- **SOC:** do not execute isolate from HIGH. The draft is DO_NOT_ISOLATE until process and safety sign.
- **Process:** MIN_LOAD is the safe-state on the packet. Abrupt isolation may destabilize PLT-10-U06.
- **Safety:** recorded bypass stays visible. Nobody bypasses an interlock from this UI.
- **Executives:** value is **unsafe isolate avoided**, not speed-to-isolate.

---

## Forbidden lines in this workflow

- “Click isolate.”
- “HIGH means we pull it off the network.”
- “The bypass is already there, so we can bypass the SIS.”
- “UNKNOWN is close enough to authorized / normal.”
- “SOC SUPPRESSED means suppress the trip.”
- Any PLC / SIS / interlock write.

---

## Screenshot index

| File | What it shows |
|---|---|
| `screenshots/safety/live-01-tower.png` | Control Tower, 61 degraded barriers |
| `screenshots/safety/live-02-cascade-tower.png` | CASCADE-001 badges, SOC vs PE |
| `screenshots/safety/live-03-safety-cascade.png` | Conflict board, PLT-10-SAFE-07 BYPASSED |
| `screenshots/safety/live-04-safety-scrolled.png` | Same board, full page |
| `screenshots/safety/live-06-safety-after-search.png` | After Search — table still the evidence |
| `screenshots/safety/live-05-recommend.png` | Gate before packet |
| `screenshots/safety/live-07-draft-packet.png` | **DO_NOT_ISOLATE**, execute No, Authorize disabled |
