# How to demonstrate identity reconciliation

Plain-English click path for stakeholders.

**App:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)

You are showing that **one name can mean two different things**, and the app **does not pick a winner**.

If the page is slow, wait about a minute (Render is waking up).

The longer script with screenshots is in [`WORKFLOW_02_IDENTITY_RECONCILIATION.md`](WORKFLOW_02_IDENTITY_RECONCILIATION.md).

---

## Before you start

1. At the top, set the persona to **FDE** or **Full**.
2. Leave conflicts visible. Do not hide red or amber items to make the screen look clean.

---

## Step 1 — Show that the estate already disagrees

1. Stay on **Control Tower** (the home screen).
2. Point at two tiles:
   - **200** state conflicts
   - **5** alias collisions
3. Say this:

> Leadership asked for a command center. The estate already has dashboards. What it does not have is one trusted list of assets. Two hundred assets say one thing in the register and another thing when observed.

Do **not** say the plant is healthy because the app loaded.

---

## Step 2 — Load the identity story

1. On the left, under **Scenario rail**, click **inject_01**.
2. Look at the badges that appear. They should mention:
   - **RETIRED vs ONLINE (OT-00528)**
   - **200 state conflicts**
   - **5 alias collisions**
   - **shadow FINAL_v8 evidence only**
3. Say this:

> This scenario does not invent a pretty plant. It pins a real inventory mismatch we already have in the data.

---

## Step 3 — Open Identity — and skip the first happy card

1. On the left, click **Identity Reconciliation**.
2. The first asset card is often **OT-00001**. It looks fine: ACTIVE and ONLINE, no conflict.
3. Say this out loud so people do not get the wrong idea:

> This first card is the clean row. If I stop here, I am lying. The story is in the Conflicts table and in Search.

---

## Step 4 — Same name, two controllers

Stay on plant **PLT-01**.

1. Scroll to the **Conflicts** table.
2. Find **OT-00012**, type **ALIAS_COLLISION**.
3. Point at the name **PLT-01-DCS_CONTROLLER-105**.
4. Show that this one name points to **two IDs**:
   - **OT-00012** — ACTIVE, ONLINE, critical, owned by Vendor
   - **OT-00033** — RETIRED, OFFLINE, medium, owned by Maintenance
5. In the **Asset** dropdown, pick **OT-00012**, click **Search**. Then pick **OT-00033** and Search again.
6. On both cards, point at:
   - **CMDB winner = No**
   - **Merged = No**
7. Say this:

> SOC has one controller name on the ticket. The estate has two different assets. We list both. We do not merge them. The CMDB is not automatically right.

---

## Step 5 — The “retired” sensor that is still online

This is the punchline.

1. Change the **Plant** dropdown to **PLT-05**.  
   OT-00528 lives on plant 5, even though inject_01 may still show plant 1. That mismatch is part of the demo.
2. In **Asset**, choose **OT-00528**, then click **Search**.
3. Read the card slowly:
   - Registered: **RETIRED**
   - Observed: **ONLINE**
   - Type: **SENSOR**
   - Criticality: **CRITICAL**
   - **CMDB winner = No**
4. Say this:

> The register says this sensor is retired. The plant still sees it online. If we hide retired assets, we go blind. We keep both truths on screen.

---

## Step 6 — Show why this is not “just an inventory problem”

Do **not** click anything that sounds like isolate or execute.

1. Open **Contextual Risk**. Keep **OT-00528**.
   - Point at **VUL-00744**: score **9.1**, reachable **YES**.
   - Say: “A retired label did not remove a reachable vulnerability.”
2. Open **Safety vs Security**. Plant **PLT-05**.
   - Point at **PLT-05-SAFE-15**: **BYPASSED**, authorized **NO**.
   - Say: “Cyber, process, and safety are three different truths. Identity is how we hold them together.”

---

## Step 7 — Close in one sentence

Go back to **Identity Reconciliation** and say:

> Reconciliation here means: show the disagreement, cite the sources, and refuse to pick a winner. Named humans still decide. This app will not merge IDs or isolate a plant from a name.

---

## If someone asks “so what do we do?”

Answer only this:

- **SOC:** do not open an isolate ticket on the name `DCS-105` until you know **which** ID.
- **CMDB owner:** you are **not** the automatic winner.
- **Plant / operations:** is OT-00528 supposed to still be live?
- **Safety:** the bypass on PLT-05 is a separate fact. It is not fixed by cleaning inventory.

---

## 90-second version

1. Control Tower → **200** and **5**.
2. Click **inject_01**.
3. Identity → skip OT-00001.
4. Show **OT-00012** and **OT-00033** share one name.
5. Search **OT-00528** → RETIRED and ONLINE.
6. “We do not merge. We do not isolate. We hand a bundle to people.”
