# How to demonstrate Control Tower

Plain-English click path for stakeholders.

**App:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)

You are showing that **we do not trust the picture yet**. This screen is inventory and disagreement. It is **not** a healthy-plant badge and **not** a permission to isolate.

If the page is slow, wait about a minute.

The longer script with screenshots is in [`WORKFLOW_01_CONTROL_TOWER.md`](WORKFLOW_01_CONTROL_TOWER.md).

---

## Before you start

1. At the top, set the persona to **FDE** or **Full**.
2. On the left, under **Scenario rail**, click **Nominal**.
3. Rule you will repeat: **SLO-OT OK means we did not execute. It does not mean the estate is healthy.**

---

## Step 1 — Show what this app is

1. Stay on **Control Tower**.
2. Point at the top: **synthetic-read-only**, **deterministic engines**, **workshop-static**.
3. Point at **SLO-OT: OK**.
4. Say this:

> Leadership asked for an autonomous command center. First we prove the picture is not trusted. This is a workbench. It is not a plant controller.

---

## Step 2 — Read five disagreement tiles

Ignore the **2016 assets** number for a moment. Point at:

- **200** state conflicts — we cannot always name the box  
- **4094** bad / uncertain telemetry — we cannot always trust the historian  
- **61** barriers degraded — protection is already messy  
- **137** unapproved remote sessions — someone may already be inside  
- **25** stale / unknown backups — and this number still **understates** recovery problems  

Say this:

> These are joins, not a CVSS leaderboard. This is why the other workflows exist.

---

## Step 3 — 18/18 plants are elevated

1. Scroll to **Estate posture**.
2. Read: **18/18 plants elevated · 2016 assets · 2800 alerts · 860 HC (inventory)**.
3. Point at the five red pills on a plant card: **cyber · process · safety · recovery · evidence**.
4. Say this:

> Composite is OK only when every layer is OK. Worst layer wins. Eighteen red cards is disagreement, not “isolate the company.” 860 HIGH/CRITICAL is a count, not the ticket order.

5. Skip leftover asset **OT-00001** and alert **ALT-001744 LOW** in the header. That is not the estate story.
6. If you see **CTX UNKNOWN** on a HIGH incident, say: “Unknown is not normal. We do not isolate from a blank.”

---

## Step 4 — Open Estate Dashboard

1. On the left, click **Estate Dashboard**.
2. Read the banner: inventory signals, **not contextual risk rank**.
3. Read the five layer boxes (cyber queue, process disagreement, safety bypass, recovery credibility, evidence / identity).
4. Scroll to the plant table. Every composite is **NOT OK**.
5. Optional: point at **PLT-11** if recovery is green while other pills are red — still **NOT OK**.
6. Say this:

> We keep five truths. We do not paint one green dashboard over them.

---

## Step 5 — Optional KPI page

1. Click **KPI Before/After**.
2. Point at **SLO-OT execute violations = OK** (must remain OK).
3. Point at **SLO-LAT = BASELINE_PENDING**. Do not claim a speed win.
4. Say this:

> Value is disagreement made visible and unsafe action refused — not isolate-speed.

---

## Step 6 — Close in one sentence

> We do not trust the picture yet. Eighteen plants disagree with themselves. The app may show that. It may not write the plant.

---

## If someone asks “so what do we do?”

- **Executives:** do not buy another dashboard. Buy trusted joins and a gate that can refuse.
- **SOC:** HIGH on this page is inventory. Ranking is a later screen.
- **Plant / safety:** your layer can keep composite NOT OK. That is intended.
- **Everyone:** next demo is a named conflict (identity), not execute.

---

## 90-second version

1. Nominal. Synthetic, read-only. SLO-OT OK ≠ healthy.  
2. Tiles **200 / 4094 / 61 / 137 / 25**.  
3. **18/18** elevated — five layers, worst wins.  
4. “Not another dashboard. Not isolate.”
