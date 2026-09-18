# How to demonstrate vendor access

Plain-English click path for stakeholders.

**App:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)

You are showing that **someone is already on the network**, so “isolate now” is not the first move. This screen **flags** bad sessions. It does **not** kill VPN.

If the page is slow, wait about a minute.

The longer script with screenshots is in [`WORKFLOW_06_VENDOR_ACCESS.md`](WORKFLOW_06_VENDOR_ACCESS.md).

---

## Before you start

1. At the top, set the persona to **FDE** or **Full**.
2. Remember three columns you will read on every row: **Approved window**, **MFA**, **Identity**.
3. Rule you will repeat: **UNKNOWN is not approval.**

---

## Step 1 — Show that access is already messy

1. Stay on **Control Tower**.
2. Point at three tiles:
   - **137** unapproved remote sessions
   - **128** sessions without confirmed MFA
   - **337** vendor session anomalies
3. Say this:

> Before we talk isolate, look at who may already be inside. If we cut a path while a vendor laptop is on a safety PLC, we can make the morning worse.

---

## Step 2 — Load the vendor story

1. On the left, under **Scenario rail**, click **inject_03**.
2. Check the top: plant **PLT-15**, asset **OT-01645** — it is a **SAFETY_PLC**.
3. Point at the badges: unapproved ≥137, MFA gaps ≥128, **change_remote_access tier 3**, **UNKNOWN identity ≠ approval**.
4. Say this:

> The pinned box is a safety PLC. Vendor access is not an IT hygiene slide.

---

## Step 3 — Open Vendor Sessions

1. On the left, click **Vendor Sessions**.
2. The big numbers **137** and **128** are the **estate**. The table is **this plant only (PLT-15)**. Say both.
3. Read two rows slowly:

**RA-00038**

- Approved window: YES  
- MFA: **UNKNOWN**  
- Identity: **UNKNOWN**

Say: “A green window does not make this a known person.”

**RA-00210**

- Approved window: **NO**  
- MFA: YES  
- Identity: site.engineer

Say: “This one is outside the approved window. Still not a kill button.”

4. Repeat: **UNKNOWN is not an approved vendor.**

---

## Step 4 — Do not kill VPN from the demo

Say this while still on the table:

> Changing remote access is tier 3 — a human must authorize it. This app must not auto-disable vendor VPN. We also do not paste the whole company’s session list onto a slide. Plant-filtered is enough.

---

## Step 5 — Request a draft (it should abstain)

1. On the left, click **Recommendation Gate**.
2. Confirm **PLT-15** and **OT-01645**. Alert may say **No alert selected**. That is OK.
3. Click **Request draft packet**.
4. Read:
   - Recommendation: **ABSTAIN**
   - Execute: **No**
   - Process context: **UNKNOWN**
   - Missing: unit join / safe-state
   - Authorize: **disabled**
5. Say this:

> No alert, UNKNOWN context, missing process join — the engine abstains. It does not cut the vendor. Named humans still own access change.

---

## Step 6 — Close in one sentence

> Someone is already on the network. We showed the sessions. We did not kill VPN. UNKNOWN is not permission.

---

## If someone asks “so what do we do?”

- **SOC / IAM:** confirm the window with the real vendor owner. Do not treat unknown as a person.
- **Plant:** should a safety PLC have remote access right now?
- **Safety:** do not kill a path to a safety PLC from a dashboard.
- **Leadership:** value is unsafe access-change avoided, not “we blocked VPN live.”

---

## 90-second version

1. inject_03 — safety PLC pinned.  
2. Vendor Sessions: **137** / **128**; **RA-00210** window NO; **RA-00038** identity UNKNOWN.  
3. Draft **ABSTAIN**.  
4. “We recommend. We do not cut the vendor.”
