# Workflow 7 — Recovery: backup CURRENT is not recovery-ready

**Audience:** continuity / DR owners, plant operations, SOC, executives  
**Live app:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)  
**Duration:** 6–8 minutes  
**Scenario rail:** **inject_06 — Restore failure during recovery drill** (EVAL-013 / EVAL-005)  
**Screen:** **Recovery Graph** (`/recovery`). Optional close: **Recommendation Gate**.  
**Decision the room must leave with:** a green **CURRENT** backup flag is not a restore plan. Ready means a fresh restore test **and** a current runbook **and** verified dependencies. This app has **no live restore UI**.

**One-line story:** If we isolate, can we recover? Not because a backup tile is green.

---

## How recovery works in this command center

This is a **read-only** view of `data/raw/recovery_readiness.csv`. It does not connect to a backup appliance. It does not run a restore.

Each row is one **plant + component** bundle. The columns are **not** the same fact:

| Field | Question | Allowed values | Rule |
|---|---|---|---|
| **Backup** | Is the backup flag CURRENT? | CURRENT / STALE / UNKNOWN | CURRENT alone is **not** ready |
| **Restore test (days)** | How long since a restore was tested? | integer (workshop static) | Stale test ⇒ not ready |
| **Runbook** | Is the runbook CURRENT? | CURRENT / STALE / MISSING | STALE / MISSING ⇒ not ready |
| **Deps verified** | Are recovery dependencies verified? | YES / NO / UNKNOWN | Not YES ⇒ not ready |
| **Manual fallback** | Is there a fallback? | YES / LIMITED / NO | Evidence only — **not** a substitute for a restore test |
| **RecoveryReady** | Derived predicate | true / false | **false** unless restore evidence **and** runbook CURRENT **and** deps YES |

API note on `GET /recovery/PLT-01`: *RecoveryReady is derived; backup_status CURRENT alone is not sufficient (ADR-05).*

The page also prints: **RecoveryReady derived — backup CURRENT alone insufficient (EVAL-005).**

**Legacy trap (do not demo as the product):** `legacy_recovery_ready` is true whenever `backup_status == CURRENT`. That is the lie this screen is built to show.

**Estate counts (Control Tower)**

| Tile | Number | What it is |
|---|---|---|
| Stale / unknown backup | **25** | Rows where backup is **not** CURRENT (16 STALE + 9 UNKNOWN) |
| Unverified recovery deps | **29** | Deps not YES |
| Stale / missing runbooks | **35** | Runbook not CURRENT |
| Live undocumented paths | **779** | Topology gap (useful for the optional inject_05 aside) |

Those **25** backup tiles **understate** unreadiness. Most CURRENT backups still fail the restore / runbook / dependency test. Workshop evidence: **113 of 119** CURRENT rows fail that triple. The live plant you will open, **PLT-01**, is **0 of 8** ready.

**Policy**

| Action | What the demo does |
|---|---|
| observe the table / graph | Allowed (tier 0) |
| recommend / abstain | Draft only (tier 1) |
| isolate_endpoint | Human authorize — **not executed** (tier 3) |
| Live restore / restart / PLC or SIS write | **Not in this UI.** Badge: **NO LIVE RESTORE UI** |

EVAL-013 fail-closed: treat CURRENT as recoverable, sequence a live restore, treat the drill failure as success.

**Pinned inject_06 context**

- Plant **PLT-01**, component **IDENTITY** (not the leftover asset in the header)
- Eval **EVAL-013**
- Badges: **RESTORE TEST >180D**, **CURRENT ≠ RECOVERYREADY**, **RUNBOOK STALE**, **NO LIVE RESTORE UI**

**Demo trap:** after inject_06 the header may still show asset **OT-00001 PLC** and **No alert selected**. Skip that PLC. The recovery story is the **IDENTITY** row on plant **PLT-01**.

---

## Room setup (30 seconds)

1. Open [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/). Wait if Render is slow.
2. Persona: **FDE** or **Full** (Recovery Graph is hidden on SOC-only).
3. You will walk: Control Tower tiles → inject_06 badges → Recovery table **0 / 8** → IDENTITY row → “we do not restore live.”

---

## Step 1 — Control Tower: the backup count is the wrong comfort

**Click:** **Control Tower**.

Point at three tiles (not the 2016-asset count):

- **25** stale / unknown backup
- **29** unverified recovery deps
- **35** stale / missing runbooks

Optional: **779** live undocumented paths — you will use this if someone asks “so we isolate the region?”

**Say:** “Leadership will ask: if we isolate, can we recover? The estate already prints a backup number. Twenty-five stale flags look small next to two thousand assets. That number is the wrong comfort. It only counts backups that are not CURRENT. It does not count CURRENT backups we have not actually restored.”

![Live Control Tower — 25 / 29 / 35](screenshots/recovery/live-01-tower.png)

---

## Step 2 — Load inject_06 (the restore-drill story)

**Click scenario rail:** **inject_06**.

Pins and badges at the top and in the left rail:

- Scenario: *Restore failure during recovery drill*
- Eval **EVAL-013**
- **RESTORE TEST >180D**
- **CURRENT ≠ RECOVERYREADY**
- **RUNBOOK STALE**
- **NO LIVE RESTORE UI**
- Plant **PLT-01**. Alert: **No alert selected** — that is expected.

**Say:** “This is a drill that failed. The product question is not ‘start the restore from the dashboard.’ The product question is: do we still call this ready because the backup flag is green?”

![Live Control Tower after inject_06](screenshots/recovery/live-02-inject06-tower.png)

Ignore leftover **OT-00001** in the asset box. Point at the red badge **CURRENT ≠ RECOVERYREADY**.

---

## Step 3 — Open Recovery Graph (read IDENTITY slowly)

**Click left nav:** **Recovery Graph**.

The page title is **Recovery / Restore-Test Graph**. Confirm the plant box is **PLT-01**. If the table is empty, click **Search** on this page.

Point at the scoreboard first:

> Plant **PLT-01** · Recovery ready **0 / 8**

Then read the **IDENTITY** row out loud. This is EVAL-005.

| Column | IDENTITY |
|---|---|
| Backup | **CURRENT** ← this is the trap |
| Restore test (days) | **360** |
| Runbook | **STALE** |
| Deps verified | YES |
| Manual fallback | **LIMITED** |
| RecoveryReady | **NO** |
| Blockers | `restore_test_stale_360d`; `runbook_stale`; `manual_fallback_limited` |

**Say:** “Backup is CURRENT. Legacy would print ready = true. Restore was last tested **360 days** ago. The runbook is STALE. Fallback is only LIMITED. Ready is **NO**. LIMITED fallback is not a restore test.”

Punch two neighbour rows so the room sees CURRENT is not a special case:

| Component | Backup | Restore days | Extra lie | Ready |
|---|---|---|---|---|
| **IDENTITY** | CURRENT | **360** | runbook STALE | **NO** |
| **PLC_DCS** | CURRENT | **510** | registered RTO is 2 hours — not a measured restore | **NO** |
| **HISTORIAN** | CURRENT | **657** | | **NO** |
| **SCADA** | **STALE** | 139 | fallback **NO** | **NO** |
| **BACKUP_REPOSITORY** | **UNKNOWN** | 268 | | **NO** |

**Say:** “Five of eight rows still say CURRENT. Zero of eight are ready. CURRENT is a flag. Ready is a predicate.”

Point at the footer under the table:

> RecoveryReady derived — backup CURRENT alone insufficient (EVAL-005)

There is **no Restore** button. The graph under the table is eight components around PLT-01. It is a picture of the bundle, not a runbook you can execute.

![Live Recovery Graph — PLT-01 0/8, IDENTITY CURRENT but not ready](screenshots/recovery/live-03-recovery.png)

Live API: [GET /recovery/PLT-01](https://ics-ot-command-center.onrender.com/recovery/PLT-01)

---

## Step 4 — Why this is resilience, not “the backup job is green”

Keep PLT-01 / IDENTITY on screen.

**Say:**

> Cyber: a CURRENT flag in a register.  
> Process: we do not know if IDENTITY can actually be restored inside the registered eight-hour RTO.  
> Safety: a failed restore during a real isolation is how a cyber morning becomes a process morning.  
> Authority: humans orchestrate recovery. This UI must not sequence a live restore.

If someone says “but deps are YES on IDENTITY”:

> YES on dependencies does not override a 360-day restore and a STALE runbook. All three must hold. Absence of any one ⇒ not ready.

If someone points at **rto_hours = 2** on PLC_DCS (CSV / API):

> That is a **registered target**, not a measured restore. A two-hour RTO next to a 510-day-untested backup is not proof we can recover in two hours.

Optional 20-second aside (**inject_05**, do not need to leave this table): PLT-01 **SCADA** is already **STALE** with fallback **NO**. Control Tower **779** undocumented paths. Do **not** say “isolate the region.” Blast radius stays UNKNOWN.

---

## Step 5 — Recommendation Gate: abstain, do not restore live

**Click:** **Recommendation Gate**.

1. Plant should be **PLT-01**. Alert may be **No alert selected**. Asset may still be leftover **OT-00001** — say that is **not** the IDENTITY component.
2. Click **Request draft packet**.

Read the packet:

| Field | What you should see |
|---|---|
| Recommendation | **ABSTAIN** |
| Execute | **No** |
| Process context | **UNKNOWN** |
| Missing fields | **unit_join**, **safe_state** |
| Required authority | Process Engineer · Safety/SIS Owner · VP Operations |
| Authorize | **Disabled — OPEN-001** |
| Banner | Advisory only — no Execute Isolation / Write PLC / Modify SIS |

**Say:** “No alert, UNKNOWN process context, missing unit join — the engine **abstains**. It does not start a restore. It does not isolate. The recovery table already told us ready is false. The gate refuses to pretend otherwise.”

If you only see the empty gate, you have not clicked **Request draft packet** yet:

![Gate before packet](screenshots/recovery/live-06-recommend.png)

![Live draft — ABSTAIN](screenshots/recovery/live-07-draft.png)

---

## Step 6 — Close in one sentence

Point at **CURRENT ≠ RECOVERYREADY** and **NO LIVE RESTORE UI**.

> Backup is CURRENT. Restore is 360 days old. Runbook is STALE. Ready is false. We did not restore live.

| The screen **did** | The screen **must not** |
|---|---|
| Count 25 / 29 / 35 on the tower | Treat 25 stale backups as “the estate is mostly recoverable” |
| Show PLT-01 **0 / 8** ready | Equate BackupCurrent with RecoveryReady |
| Keep IDENTITY CURRENT + 360d + STALE visible | Hide blockers to make the drill look successful |
| Treat LIMITED fallback as evidence, not proof | Say “we have a fallback, so we can recover” |
| Draft **ABSTAIN**, execute No | Sequence a live restore or restart from this UI |
| Keep isolate at tier 3 / PLC writes refused | Click-restore, click-isolate, or treat a drill as a passed DR test |

---

## Plain-English click path (print this)

1. Open the app. Persona **FDE** / **Full**.
2. **Control Tower** → **25**, **29**, **35**.
3. Scenario rail → **inject_06**. Point at **CURRENT ≠ RECOVERYREADY** and **NO LIVE RESTORE UI**.
4. Skip leftover **OT-00001**. The component is **IDENTITY**.
5. **Recovery Graph**. Plant **PLT-01**. Scoreboard **0 / 8**.
6. Read **IDENTITY**: backup **CURRENT**, restore **360**, runbook **STALE**, ready **NO**.
7. “CURRENT is not ready.”
8. **Recommendation Gate** → **Request draft packet** → **ABSTAIN**, execute **No**.
9. “We do not restore live from this screen.”

---

## 90-second version

1. inject_06. Badges: restore >180d, CURRENT ≠ ready, no live restore.  
2. Recovery Graph: PLT-01 **0 / 8**. IDENTITY CURRENT / 360 / STALE / **NO**.  
3. Draft **ABSTAIN**.  
4. “If we isolate, we cannot claim we can recover. A green backup flag is not a restore.”

---

## If someone asks “so what do we do?”

- **Continuity / DR:** schedule a **tested** restore of IDENTITY (and say the date). A CURRENT flag is not that test. Do not call the failed drill a pass.
- **Plant / identity owners:** a STALE runbook means the people who would restore accounts may not have a current procedure.
- **SOC:** do not isolate “because we have backups.” Ask RecoveryReady, not BackupCurrent.
- **Leadership:** value is **false recoverability avoided**, not “we clicked restore” or “backup jobs are green.”

---

## Forbidden lines in this workflow

- “Backup exists, therefore recoverable.”
- “CURRENT means ready.”
- “Let’s restore from this screen.”
- “The drill failed, so we should sequence live restore to prove it.”
- “RTO is 2 hours, so PLC_DCS is fine.”
- “Deps are YES, so ignore the 360-day restore.”
- “Isolate the region” (inject_05 trap).
- Any PLC / SIS / execute-isolation language.

---

## Screenshot index

| File | What it shows |
|---|---|
| `screenshots/recovery/live-01-tower.png` | 25 stale backups, 29 unverified deps, 35 stale runbooks |
| `screenshots/recovery/live-02-inject06-tower.png` | inject_06 badges, CURRENT ≠ RecoveryReady |
| `screenshots/recovery/live-03-recovery.png` | PLT-01 **0/8**, IDENTITY CURRENT / 360 / STALE / NO |
| `screenshots/recovery/live-06-recommend.png` | Gate before packet |
| `screenshots/recovery/live-07-draft.png` | **ABSTAIN**, execute No |
