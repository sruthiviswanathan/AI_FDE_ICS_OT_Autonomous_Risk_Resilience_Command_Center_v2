# How to demonstrate contextual risk

Plain-English click path for stakeholders.

**App:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)

You are showing that **the highest CVSS is not automatically the plant’s biggest problem**.

If the page is slow, wait about a minute.

The longer script with screenshots is in [`WORKFLOW_04_CONTEXTUAL_RISK.md`](WORKFLOW_04_CONTEXTUAL_RISK.md).

---

## Before you start

1. At the top, set the persona to **FDE** or **Full**.
2. You will use two findings. Write them on a slide or a notepad:

| | Scanner favourite | Plant problem |
|---|---|---|
| ID | **VUL-00706** on **OT-00654** | **VUL-00098** on **OT-01016** |
| CVSS | **9.8** | **8.7** |
| Can it reach the plant? | **NO** | **YES** |
| Contextual score | **40.6** | **87.4** |

---

## Step 1 — Control Tower is not a CVE leaderboard

1. Stay on **Control Tower**.
2. Point at the diagnostic tiles. They are identity, telemetry, safety, recovery — not “top CVSS.”
3. Say this:

> This wall is disagreement, not a CVE leaderboard. Highest scanner score is not the same as operational risk.

---

## Step 2 — Pin the plant finding

1. On the left, under **Scenario rail**, click **CASCADE-001**.
2. Check the top bar: plant **PLT-10**, asset **OT-01016**, alert **ALT-002783**.
3. Point at **execute=false**.
4. Say this:

> We are about to rank the finding on this controller. Not the scariest CVE in the whole catalogue.

---

## Step 3 — Open Contextual Risk

1. On the left, click **Contextual Risk**.
2. Leave the mode on **Contextual rank (default)**. Do not start on CVSS-only.
3. You will probably see **only one row**: **VUL-00098**. That is normal. The scenario pinned one asset, and this workshop shows one finding per asset.

Say this:

> If I stopped on this one row, I have the plant finding. I still need the 9.8 for contrast. That is a second search.

---

## Step 4 — Read the plant problem out loud

Point at **VUL-00098**:

- CVSS **8.7** (labelled input)
- Reach **YES**
- Criticality **HIGH**
- Score **87.4**

Point at the cards underneath:

- Reachability **35 points** — can it get there?
- Process criticality **30 points** — does the unit matter?
- CVSS **17.4 points** — “input only, not the sort key”
- Recovery **DEGRADED** — a green backup flag is not recovery-ready

Say this:

> Reachability and process criticality outweigh the scanner score. 8.7 is not small. It is just not why this row is first for the plant.

---

## Step 5 — Show the 9.8 that should not win

1. In **Asset**, search or select **OT-00654**.
2. You should see **VUL-00706**:
   - CVSS **9.8**
   - Reach **NO**
   - Criticality **LOW**
   - Score **40.6**
3. Say this:

> Legacy ranking would put 9.8 first. This engine gives it 40.6 because it cannot reach the plant. The 8.7 that can reach a HIGH unit scores 87.4. Highest CVSS is not the plant’s problem.

Optional extra: set Plant to **PLT-10**, Asset to **All assets (plant-wide)**, click Search. A finding with CVSS **6.0** can sit above an **8.7**. Even clearer that CVSS is not the sort key.

---

## Step 6 — Show the old habit, then switch back

1. Click **CVSS-only (warn)**.
2. Read the amber banner: **CVSS-only sort is anti-pattern**.
3. Say this:

> This toggle exists to show the old habit. It is a warning, not the product.
4. Click **Contextual rank (default)** again before you leave.

---

## Step 7 — Close in one sentence

Point at **execute=false** and say:

> We ranked which finding to talk about. We did not isolate. The 9.8 that cannot get there is not ticket one.

---

## If someone asks “so what do we do?”

- **SOC:** do not open the 9.8 first just because the scanner said CRITICAL.
- **Process:** OT-01016 is reachable and HIGH — that is the conversation, still not an isolate button.
- **Leadership:** ticket order follows plant consequence, not CVSS descending.
- **Nobody:** the AI does not get to reshuffle this list.

---

## 90-second version

1. CASCADE-001 → **Contextual Risk**.  
2. **VUL-00098**: 8.7, reachable YES, score **87.4**.  
3. Search **OT-00654** / **VUL-00706**: 9.8, reachable NO, score **40.6**.  
4. “Highest CVSS is not the plant’s problem. No isolate.”
