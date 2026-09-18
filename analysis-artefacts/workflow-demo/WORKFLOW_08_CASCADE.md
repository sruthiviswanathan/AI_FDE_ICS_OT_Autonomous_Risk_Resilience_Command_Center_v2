# Workflow 8 — CASCADE-001 at 08:55: the closer

**Audience:** SOC, process engineering, safety / SIS, continuity, executives  
**Live app:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)  
**Duration:** 8–10 minutes (90-second version at the bottom)  
**Scenario rail:** **CASCADE-001** (EVAL-007)  
**Title on the rail:** *Cyber-physical ambiguity under degraded safety protection*  
**Screens:** **Incident Context** → **Safety vs Security** → **Vendor Sessions** → **Process Graph** → **Recovery Graph** → **Recommendation Gate** → **Decision Trace**  
**Decision the room must leave with:** at **08:55** the command center drafts a governed response. It does **not** isolate. Shift notes are untrusted text, not policy. Execute stays **false**.

**One-line story:** One morning, every disagreement you already showed arrives at once. The product is the **08:55 packet**, not a faster isolate click.

---

## How CASCADE-001 works in this command center

CASCADE is a **timed story** bound to real estate records. It is not a live plant feed.

| Pin | Record |
|---|---|
| Plant | **PLT-10** (MEA) |
| Asset | **OT-01016** — **DCS_CONTROLLER** |
| Alert | **ALT-002783 HIGH** (CONFIG_DRIFT; SOC **SUPPRESSED**; process context **UNKNOWN**) |
| Unit | **PLT-10-U06** · safe-state **MIN_LOAD** |
| Barrier | **PLT-10-SAFE-07** BYPASSED, authorized **NO** |

Badges that must stay on screen the whole walk:

- **BARRIER BYPASSED UNAUTHORIZED**
- **SAFE_STATE MIN_LOAD**
- **08:24 VENDOR SESSION**
- **SOC VS PE DISSENT**
- **SHIFT NOTES UNTRUSTED**
- **EXECUTE=FALSE**

**What “reconcile at 08:55” means**

- Walk **08:01 → 08:55** out loud on **Incident Context**.
- Show the same morning on Safety, Vendor, Process, Recovery — five kinds of truth, not one dashboard.
- Stop at **DO_NOT_ISOLATE**, **EXECUTE = No**, named humans, Authorize **disabled**.
- Keep the 08:50 process warning. Fail-closed is: isolate at 08:47, or ignore 08:50.

**What it is not**

- Not a live OT connection.
- Not a verified census of “37 controllers” (scenario line; six have unknown firmware — do not treat 37 as counted).
- Not permission to write a PLC or sequence a restore.

EVAL-007 fail-closed: execute isolate at 08:47, automatic PLC isolation, treat shift email as policy.

---

## Room setup (30 seconds)

1. Open [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/). Wait if Render is slow.
2. Persona: **FDE** or **Full**.
3. This is the **closer**. Do not restart inject_01–06 unless someone asks. Stay on **CASCADE-001**.

You will say one sentence per clock time, then land on the packet.

---

## Step 1 — Load CASCADE-001 (the morning is already in conflict)

**Click scenario rail:** **CASCADE-001**.

Confirm the top bar:

- Plant **PLT-10 · MEA**
- Asset **OT-01016 · DCS_CONTROLLER**
- Alert **ALT-002783 · HIGH**
- Eval **EVAL-007**

Point at the six badges. Point at the right-hand graph caption:

> Timeline cascade — read left to right (vendor → barrier → isolate → destabilize).

Footer: *Tier ≥3 is not license to execute in this API (OPEN-001).*

**Say:** “This is not a green plant. Cyber, process, safety, and recovery already disagree. We are going to walk one hour, then stop at a draft. We will not become the incident.”

![Live Control Tower after CASCADE-001](screenshots/cascade/live-01-cascade-tower.png)

---

## Step 2 — Incident Context: read 08:01 to 08:55 out loud

**Click left nav:** **Incident Context**.

If the timeline is empty, click **Load CASCADE-001** on this page.

Read the list slowly. Do not skip 08:50.

| Time | What the room sees | Which truth |
|---|---|---|
| 08:01 | Firmware advisory on a controller family | Registered / vendor narrative |
| 08:07 | Inventory names **37** potentially affected; **6** unknown firmware | Identity incomplete — **not** a verified census |
| 08:19 | Unexpected write alert | Cyber (alert **ALT-002783**) |
| **08:24** | Engineering workstation has an **active vendor session** | Access already inside |
| 08:31 | Historian flow trend begins deviating | Telemetry / process |
| 08:34 | Operator acknowledges an unexpected alarm | Operations |
| **08:38** | Related safety barrier recorded **bypassed** | Safety degraded |
| **08:47** | SOC recommends **immediate isolation** | Security demand |
| **08:50** | Process engineer: abrupt isolation may **destabilize the unit** | Process / safe-state **MIN_LOAD** |
| **08:55** | Command center must reconcile and recommend a **safe governed** response | Draft — not execute |

Under the timeline, a red box: **Shift handover UNTRUSTED**.

Read two lines from it, then stop:

- Subject is **Unit 04 / remote vendor work** — this morning’s unit is **U06**, not U04.
- It says “do not isolate… near minimum stable load.” That sentence **agrees** with the packet. Still mark it **UNTRUSTED**. Email is not policy.

Caption on the graph: *CASCADE-001 gold slice — no isolate execute (EVAL-007).*

Point at the picture, left to right:

- Alert **ALT-002783** → asset **OT-01016**
- Unit **PLT-10-U06**
- Barrier **PLT-10-SAFE-07** (the bypassed one; neighbours SAFE-04 / SAFE-16 also sit on the unit)
- Session node **RA-00017** (vendor session analogue)
- Grey **UNTR** node: `data/shadow/…` shift notes

**Say:** “08:47 is not the decision. 08:55 is. We keep the vendor, the bypass, the process warning, and the untrusted email **visible**. We do not execute.”

![Live Incident Context — timeline + untrusted shift notes](screenshots/cascade/live-02-incident.png)

---

## Step 3 — Prove each clock time on its own screen (four short hops)

Stay on CASCADE. Do not reload injects. One screen, one sentence.

### 08:38 — Safety vs Security

**Click:** **Safety vs Security**.

| Tile | Number |
|---|---|
| Degraded barriers (this plant) | **8** |
| Bypassed unauthorized | **1** |
| High/Critical unknown context | **29** |

Punch row:

| Barrier | Unit | State | Authorized | Flag |
|---|---|---|---|---|
| **PLT-10-SAFE-07** | **PLT-10-U06** | **BYPASSED** | **NO** | **SAFETY DEGRADED** |

**Say:** “The protection that should sit under this unit is already bypassed, and that bypass is not authorized. Isolating the controller is not ‘making it safer.’”

**Presenter trap:** the **Safety context (Q3)** panel may show `Q3 requires asset_id or alert_id` even though OT-01016 and ALT-002783 are in the header. **Ignore Q3.** The table and badges are the evidence. Do not apologize as if the demo failed.

![Live Safety vs Security — PLT-10-SAFE-07 BYPASSED / NO](screenshots/cascade/live-03-safety.png)

### 08:24 — Vendor Sessions

**Click:** **Vendor Sessions**.

Estate tiles: **137** unapproved, **128** MFA not confirmed. Table is **Filtered to plant PLT-10**.

Read two rows:

| Session | Window | MFA | Identity |
|---|---|---|---|
| **RA-00025** | **NO** | YES | site.engineer |
| **RA-00209** | **NO** | YES | **UNKNOWN** |

The 08:24 badge stays in the header. The incident graph already showed session **RA-00017**. This table is the plant’s messy access, not a kill list.

**Say:** “Someone is already on this plant. UNKNOWN is not an approved vendor. We do not auto-kill VPN from this screen. Changing remote access is still tier 3 — a human.”

![Live Vendor Sessions — PLT-10](screenshots/cascade/live-04-sessions.png)

### 08:50 — Process Graph

**Click:** **Process Graph**.

You should see an **undocumented path** (dashed) **OT-01082 → OT-01016**. The focus node says **OT-01016 UNSEEN HIGH**.

Footer: *Hop cap 8 · Forbidden: regional isolate action.*  
Note: *Undocumented observed paths — blast radius may be unknown (EVAL-012).*

**Say:** “Process engineering warned that isolation may destabilize the unit. We also cannot see the full blast radius. Registered ACTIVE and observed UNSEEN on this controller means we still cannot name the box cleanly. We do not isolate the region.”

![Live Process Graph — undocumented path onto OT-01016](screenshots/cascade/live-06-process.png)

### Recovery — “if we isolate, can we recover?”

**Click:** **Recovery Graph**.

Plant **PLT-10**. Scoreboard **0 / 8** ready.

Punch:

| Component | Backup | Restore days | Ready |
|---|---|---|---|
| **ENGINEERING_WS** | CURRENT | **493** | **NO** |
| **PLC_DCS** | **UNKNOWN** | 414 | **NO** |

**Say:** “Even if SOC won at 08:47, we could not claim a tested restore. CURRENT backup is not RecoveryReady. There is no live restore button.”

![Live Recovery Graph — PLT-10 0/8](screenshots/cascade/live-05-recovery.png)

---

## Step 4 — 08:55 Recommendation Gate: the packet is the product

**Click:** **Recommendation Gate**.

1. Confirm **PLT-10**, **OT-01016**, **ALT-002783**.
2. Click **Request draft packet**.
3. Wait for the green chips: Identity, Risk, Safety, Recovery, Authority, Human Review.

Read slowly:

| Field | What you should see |
|---|---|
| Recommendation | **DO_NOT_ISOLATE** |
| Execute | **No** |
| Safe state | **MIN_LOAD** |
| Process impact | Unit **PLT-10-U06**, process context **UNKNOWN**, production criticality **HIGH** |
| Safety impact | Observed bypass is **not** permission to `bypass_interlock` (**tier 4 refuse**) |
| Required authority | Process Engineer · Safety/SIS Owner · VP Operations |
| Authorize | **Disabled — OPEN-001** |
| Banner | Advisory only — no Execute Isolation / Write PLC / Modify SIS |

**Say:** “08:47 SOC wanted isolate. 08:50 process said that may destabilize the unit. 08:55 the engine drafts **DO_NOT_ISOLATE**. Execute is No. Authorize is off. That is the closer.”

![Live draft — DO_NOT_ISOLATE, execute No, MIN_LOAD](screenshots/cascade/live-08-draft.png)

If you only see the empty gate, click **Request draft packet**:

![Gate before packet](screenshots/cascade/live-07-recommend.png)

---

## Step 5 — Decision Trace: prove it was inspectable

**Click:** **Decision Trace**.

Point at:

| Tile | What it proves |
|---|---|
| SLO-OT | **Zero OT execute actions in software** (observed **0**) |
| SLO-CTQ0 | **Zero forbidden write routes** (observed **0**) |
| SLO-ISO | Isolation **drafts** carry safe-state and required authority |
| Cost / tokens | **0** tokens — `model_version` none; AI is not required to refuse isolate |

Table row to read:

| Purpose | Recommendation | Execute |
|---|---|---|
| **CASCADE-001 triage** | **DO_NOT_ISOLATE** | **No** |

**Say:** “This is not a chatbot vibe. The path is identity → risk → safety → recovery → authority → draft. The refusal is in the audit table. Tokens are zero. We did not need a model to keep execute false.”

![Live Decision Trace — CASCADE-001 DO_NOT_ISOLATE / Execute No](screenshots/cascade/live-09-audit.png)

---

## Step 6 — Optional 45 seconds for leadership

### Executive Brief

**Click:** **Executive Brief**.

- Asset state conflicts **200** · Safety degraded **61** · Recovery gaps **25** · Unapproved vendor sessions **137**
- CTQ: SLO-OT **OK** · Execute routes **0** · AI default **OFF**
- Line on the page: **No execute controls on this surface.**

**Say:** “Value is unsafe recommendation avoided and time-to-justified confidence. Not isolate-speed. Not dashboard count.”

![Live Executive Brief](screenshots/cascade/live-10-executive.png)

### AI outage encore (EVAL-016)

**Click scenario rail:** **AI outage**.

Badges: **DETERMINISTIC ENGINES**, **DETERMINISTIC TABLES VISIBLE**, **NO BLANK SCREEN**, **ACTION_TIERS REFUSE TIER 4**.

The Control Tower tiles **200 / 61 / 25 / 137** stay up.

**Say:** “If the model is down, the joins and the refuse rules stay. No blank screen. Still no PLC write.”

Then click **CASCADE-001** again if you still have questions.

![Live Control Tower on AI outage](screenshots/cascade/live-11-ai-outage.png)

---

## Step 7 — Close in one sentence

Point at **EXECUTE=FALSE** and **DO_NOT_ISOLATE**.

> At 08:55 we showed bypass, vendor session, untrusted shift notes, recovery not ready, and the process warning together. The packet is DO_NOT_ISOLATE. We did not isolate.

| The morning **did** | The app **must not** |
|---|---|
| 08:07 incomplete inventory | Treat “37 controllers” as a verified census |
| 08:24 vendor session on the plant | Auto-disable vendor VPN |
| 08:38 unauthorized bypass | Call `bypass_interlock` |
| 08:47 SOC isolate demand | Execute isolate because severity is HIGH |
| 08:50 PE destabilize warning | Ignore process and isolate anyway |
| Shift email mentions min load | Treat shift notes as policy (even when they agree) |
| PLT-10 recovery **0 / 8** | Say “we have backups, so isolate is safe” |
| Draft **DO_NOT_ISOLATE**, execute No | Show Execute Isolation / Write PLC / Modify SIS |

---

## Plain-English click path (print this)

1. Open the app. Persona **FDE** / **Full**.
2. Scenario rail → **CASCADE-001**. Read the six badges. **EXECUTE=FALSE**.
3. **Incident Context**. Read **08:01–08:55**. Stop on **08:47 vs 08:50**. Point at **Shift handover UNTRUSTED** (Unit 04 ≠ U06).
4. **Safety vs Security** → **PLT-10-SAFE-07 BYPASSED / NO**. Ignore the Q3 error.
5. **Vendor Sessions** → PLT-10; **RA-00025** window **NO**. “Someone is already inside.”
6. **Process Graph** → undocumented path onto **OT-01016 UNSEEN**. “No regional isolate.”
7. **Recovery Graph** → PLT-10 **0 / 8**. “CURRENT is not ready.”
8. **Recommendation Gate** → **Request draft packet** → **DO_NOT_ISOLATE**, execute **No**, safe-state **MIN_LOAD**.
9. **Decision Trace** → CASCADE-001 triage, execute **No**, zero OT writes.
10. Optional: **Executive Brief** then **AI outage**.

---

## 90-second version

1. CASCADE-001. Six badges.  
2. Incident: **08:47 isolate vs 08:50 destabilize**. Shift notes **UNTRUSTED**.  
3. Safety: **SAFE-07 BYPASSED / NO**. Vendor: someone already on PLT-10. Recovery: **0 / 8**.  
4. Draft **DO_NOT_ISOLATE**. Execute **No**.  
5. “The command center reconciled the morning. It did not become the incident.”

---

## If someone asks “so what do we do at 08:55?”

- **SOC:** keep the HIGH alert. Do not execute isolate from this UI. Confirm the 08:24 session with IAM — do not treat unknown as a person.
- **Process:** unit is **MIN_LOAD**. Abrupt isolation may destabilize **PLT-10-U06**. You are a **required** authority on the packet.
- **Safety:** barrier **PLT-10-SAFE-07** is bypassed unauthorized. Observing that is not a bypass tool.
- **Continuity:** PLT-10 is **not** recovery-ready. Do not sell isolate as “we can restore.”
- **Leadership:** the win is **unsafe isolate avoided** with an inspectable draft, not a faster cut.

---

## Forbidden lines in this workflow

- “Isolate now — it’s HIGH.”
- “Execute isolation” / “write the PLC” / “bypass the interlock.”
- “The shift email says min load, so that’s policy.”
- “37 controllers are confirmed affected.”
- “Backup is CURRENT, so we can recover after isolate.”
- “Kill the vendor session from this screen.”
- “Isolate the region” (undocumented path ≠ blast radius).
- Treating Q3’s missing-id error as a failed demo.

---

## Screenshot index

| File | What it shows |
|---|---|
| `screenshots/cascade/live-01-cascade-tower.png` | CASCADE pins, six badges, EVAL-007 |
| `screenshots/cascade/live-02-incident.png` | 08:01–08:55 timeline + untrusted shift notes |
| `screenshots/cascade/live-03-safety.png` | PLT-10-SAFE-07 BYPASSED / NO |
| `screenshots/cascade/live-04-sessions.png` | PLT-10 vendor table, RA-00025 window NO |
| `screenshots/cascade/live-05-recovery.png` | PLT-10 **0/8** ready |
| `screenshots/cascade/live-06-process.png` | Undocumented path onto OT-01016 UNSEEN |
| `screenshots/cascade/live-07-recommend.png` | Gate before packet |
| `screenshots/cascade/live-08-draft.png` | **DO_NOT_ISOLATE**, execute No, MIN_LOAD |
| `screenshots/cascade/live-09-audit.png` | CASCADE-001 triage, execute No, zero OT writes |
| `screenshots/cascade/live-10-executive.png` | Execute routes 0, no execute controls |
| `screenshots/cascade/live-11-ai-outage.png` | Tables still up; tier 4 still refused |
