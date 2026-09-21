# How to demonstrate safety vs security

Plain-English click path for stakeholders.

**App:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)

You are showing that **“isolate now” can become the incident**. A HIGH SOC alert is not a license to pull a controller off the network.

If the page is slow, wait about a minute.

The longer script with screenshots is in [`WORKFLOW_05_SAFETY_VS_SECURITY.md`](WORKFLOW_05_SAFETY_VS_SECURITY.md).

---

## Before you start

1. At the top, set the persona to **FDE** or **Full**.
2. Remember the two times you will say out loud:
   - **08:47** — SOC says isolate.
   - **08:50** — Process engineer says that may destabilize the unit.

---

## Step 1 — Show that protection is already degraded

1. Stay on **Control Tower**.
2. Point at **61** barriers degraded (and **73** proof tests due if you have a second).
3. Say this:

> Security is not the only clock. If we isolate from a HIGH label, we may hit a unit that is already running with a bypass.

---

## Step 2 — Load the morning story

1. On the left, under **Scenario rail**, click **CASCADE-001**.
2. Check the top: plant **PLT-10**, asset **OT-01016**, alert **ALT-002783 HIGH**.
3. Point at the badges: **barrier bypassed unauthorized**, **safe-state MIN_LOAD**, **SOC vs PE dissent**, **execute=false**.
4. Say this:

> At 08:38 the barrier is recorded bypassed. At 08:47 SOC wants isolate. At 08:50 process says wait. We must not become the incident.

---

## Step 3 — Open the conflict board

1. On the left, click **Safety vs Security**.
2. For PLT-10, point at:
   - Degraded barriers **8**
   - Bypassed unauthorized **1**
3. Read the table row slowly:
   - Barrier **PLT-10-SAFE-07**
   - Unit **PLT-10-U06**
   - State **BYPASSED**
   - Bypass authorized **NO**
4. Say this:

> The protection on this unit is already bypassed, and nobody authorized it. Isolating the controller now is not making it safer.

**If a red error appears under “Safety context (Q3)”:** ignore it. The **table** is the evidence. Do not stop the demo.

---

## Step 4 — Name both truths

Keep the same screen and say:

> SOC sees a HIGH alert. Safety sees an unauthorized bypass and MIN_LOAD. Process context is UNKNOWN — that is not NORMAL. Legacy would isolate on HIGH. This board refuses to hide the conflict.

---

## Step 5 — Prove there is no isolate button

1. On the left, click **Recommendation Gate**.
2. Confirm **OT-01016** and **ALT-002783** are still selected.
3. Click **Request draft packet**. Wait for the chips to turn green.
4. Read the packet:
   - Recommendation: **DO_NOT_ISOLATE**
   - Execute: **No**
   - Safe state: **MIN_LOAD**
   - Required people: Process Engineer, Safety/SIS Owner, VP Operations
   - Authorize: **disabled**
5. Point at the banner: advisory only — no Execute Isolation, no Write PLC, no Modify SIS.
6. Say this:

> SOC wanted isolate. The packet is DO_NOT_ISOLATE. Seeing a bypass is not permission to bypass an interlock. This app will not write the plant.

---

## Step 6 — Close in one sentence

Point at **execute=false** and say:

> Isolate now can become the incident. We showed both truths. We drafted DO_NOT_ISOLATE. We did not pull the controller.

---

## If someone asks “so what do we do?”

- **SOC:** do not execute isolate from HIGH.
- **Process:** MIN_LOAD — abrupt isolation may destabilize the unit.
- **Safety:** keep the bypass visible; nobody bypasses SIS from this screen.
- **Leadership:** value is unsafe isolate avoided, not speed-to-isolate.

---

## 90-second version

1. CASCADE-001.  
2. Safety vs Security: **PLT-10-SAFE-07 BYPASSED / NO**.  
3. Recommendation Gate → **DO_NOT_ISOLATE**, execute **No**.  
4. “08:47 vs 08:50. We do not isolate.”
