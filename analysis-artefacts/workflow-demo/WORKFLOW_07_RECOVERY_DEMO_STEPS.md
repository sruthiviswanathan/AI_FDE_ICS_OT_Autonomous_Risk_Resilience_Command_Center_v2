# How to demonstrate recovery

Plain-English click path for stakeholders.

**App:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)

You are showing that a **CURRENT backup is not recovery-ready**. This screen **flags** missing restore tests and stale runbooks. It does **not** run a restore.

If the page is slow, wait about a minute.

The longer script with screenshots is in [`WORKFLOW_07_RECOVERY.md`](WORKFLOW_07_RECOVERY.md).

---

## Before you start

1. At the top, set the persona to **FDE** or **Full**. Recovery Graph is hidden on SOC-only.
2. Remember three things you will read on the IDENTITY row: **Backup**, **Restore test (days)**, **Runbook**.
3. Rule you will repeat: **CURRENT is not ready.**

---

## Step 1 — Show that “backup green” is the wrong comfort

1. Stay on **Control Tower**.
2. Point at three tiles:
   - **25** stale / unknown backups
   - **29** unverified recovery deps
   - **35** stale / missing runbooks
3. Say this:

> If we isolate, can we recover? Twenty-five stale backups look small. That number only counts flags that are not CURRENT. It does not count CURRENT backups we have not actually restored.

---

## Step 2 — Load the restore-drill story

1. On the left, under **Scenario rail**, click **inject_06**.
2. Check the badges: **restore test >180d**, **CURRENT ≠ RecoveryReady**, **runbook STALE**, **no live restore UI**.
3. Plant is **PLT-01**. Alert may say **No alert selected**. That is OK.
4. Skip leftover asset **OT-00001**. The story is component **IDENTITY**, not that PLC.
5. Say this:

> This is a drill that failed. We are not going to start a restore from the dashboard. We are going to see whether CURRENT still gets called ready.

---

## Step 3 — Open Recovery Graph

1. On the left, click **Recovery Graph**.
2. Confirm plant **PLT-01**. If the table is empty, click **Search** on this page.
3. Point at the scoreboard: **Recovery ready 0 / 8**.
4. Read the **IDENTITY** row slowly:

**IDENTITY**

- Backup: **CURRENT**  
- Restore test: **360** days  
- Runbook: **STALE**  
- Deps: YES  
- Fallback: **LIMITED**  
- RecoveryReady: **NO**

Say: “Legacy would say ready because backup is CURRENT. Restore is a year old. Runbook is stale. Ready is no. LIMITED fallback is not a restore test.”

5. Optional extra row: **PLC_DCS** is also CURRENT with a **510**-day restore. A two-hour RTO on paper is not a tested restore.
6. Repeat: **CURRENT is not ready.**

---

## Step 4 — Do not restore live from the demo

Say this while still on the table:

> There is no Restore button. Humans orchestrate recovery. This app must not sequence a live restore. Do not treat the failed drill as a passed DR test.

If someone asks about isolating a region (inject_05):

> PLT-01 SCADA on this same table is already STALE with no fallback. Undocumented paths are 779 on the tower. We do not isolate the region from this screen.

---

## Step 5 — Request a draft (it should abstain)

1. On the left, click **Recommendation Gate**.
2. Confirm **PLT-01**. Alert may say **No alert selected**. Leftover **OT-00001** is still not IDENTITY — say that.
3. Click **Request draft packet**.
4. Read:
   - Recommendation: **ABSTAIN**
   - Execute: **No**
   - Process context: **UNKNOWN**
   - Missing: unit join / safe-state
   - Authorize: **disabled**
5. Say this:

> No alert, UNKNOWN context — the engine abstains. It does not start a restore. The recovery table already said ready is false.

---

## Step 6 — Close in one sentence

> Backup is CURRENT. Restore is 360 days old. Runbook is STALE. Ready is false. We did not restore live.

---

## If someone asks “so what do we do?”

- **DR / continuity:** schedule a **tested** restore of IDENTITY. A CURRENT flag is not that test.
- **Plant:** a STALE runbook means the restore procedure may not be usable tonight.
- **SOC:** do not isolate “because we have backups.” Ask RecoveryReady, not BackupCurrent.
- **Leadership:** value is false recoverability avoided, not “we clicked restore.”

---

## 90-second version

1. inject_06 — CURRENT ≠ ready, no live restore.  
2. Recovery Graph: PLT-01 **0 / 8**; IDENTITY CURRENT / 360 / STALE / **NO**.  
3. Draft **ABSTAIN**.  
4. “A green backup flag is not a restore.”
