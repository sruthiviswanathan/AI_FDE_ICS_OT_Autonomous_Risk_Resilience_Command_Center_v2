# How to demonstrate Moonshot (advisory forecast)

Plain-English click path for stakeholders.

**App (local):** [http://127.0.0.1:5173](http://127.0.0.1:5173)  
**Hosted fallback:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)

You are showing that Moonshot is **not** the plant taking itself offline. It is an **advisory forecast layer** on top of the Command Center.

In one sentence: *the system can guess what might matter next, let you rehearse an isolation in a lab sketch, and still refuse to touch the plant.*

If the page is slow, wait about a minute, then hard-refresh once.

---

## What the three AI buttons mean

The **AI** control is in the top-right of the header.

| Click | What the client sees | What it is |
|---|---|---|
| **OFF** | Tables, maps, draft packet | Engines only. Safe default. |
| **ON** | A short **Advisory caption** | A cited summary. Not a decision. |
| **MOONSHOT** | Caption **plus** a ranked forecast table | Hypotheses. Still not a control action. |

If anyone asks “will this isolate the unit?” the answer is **no**. There is no Execute button on Moonshot.

---

## Before you start

1. Open [http://127.0.0.1:5173](http://127.0.0.1:5173).
2. At the top, set **Persona** to **Full workshop view**.
3. Confirm the badge says **AI-DISABLED**.
4. On the left, under **Scenario rail**, click **Nominal**.
5. Confirm mode is **synthetic-read-only**.

Do **not** click **Authorize**. It is disabled on purpose.

Backup URL if you get lost:

`http://127.0.0.1:5173/estate?persona=full&ai=off`

---

## The story you are telling (about 8 minutes)

A SOC analyst sees a high alert at plant **PLT-10** and wants to isolate. Safety is already degraded. Process context is unknown. Moonshot can **forecast** that tension and **rehearse** isolate in a twin lab. The engines still say **do not isolate**.

Pins you will keep pointing at:

- Plant **PLT-10**, asset **OT-01016**, alert **ALT-002783**
- Unit **PLT-10-U06**, barrier **PLT-10-SAFE-07**, safe-state **MIN_LOAD**

Rule you will repeat: **Moonshot may forecast. The twin may sketch. The packet is still the engines. Execute stays no.**

---

## Step 1 — Start with AI off

1. On the left, click **Estate Dashboard**.
2. Point at the plant pills / map. There is no caption and no forecast table.
3. Say this:

> This is the 18-plant estate as it is. Inventories already disagree. This screen is advice, not a control-room write path. AI is off, so you are looking at engines only.

---

## Step 2 — Turn AI on

1. In the header **AI** control, click **ON**.
2. The badge should change to **AI-ON**.
3. Point at the **Advisory caption** box. Estate numbers do **not** change.
4. Say this:

> AI on is a cited caption of the current slice. It does not replace the tables. If the caption and the engines ever disagree, keep the engines.

---

## Step 3 — Load the golden incident

1. On the left, under **Scenario rail**, click **CASCADE-001**.
2. Check the top: **PLT-10**, **OT-01016**, **ALT-002783**.
3. Read the badges: Barrier BYPASSED unauthorized, safe_state MIN_LOAD, 08:24 vendor session, SOC vs PE dissent, shift notes UNTRUSTED, **execute=false**.
4. On the left, click **Incident Context**.
5. If the list is empty, click **Load CASCADE-001**.
6. Read these times out loud:

| Time | What it means |
|---|---|
| 08:24 | A vendor session is on the network |
| 08:38 | A safety barrier is bypassed |
| 08:47 | SOC wants isolate |
| 08:50 | Process says abrupt isolate may destabilize (MIN_LOAD) |
| 08:55 | This product only drafts advice |

7. Say this:

> 08:47 is a demand. 08:50 is dissent. Software does not take the unit.

---

## Step 4 — Turn on Moonshot

1. In the header **AI** control, click **MOONSHOT**.
2. The badge should turn orange: **MOONSHOT**.
3. Stay on **Estate Dashboard** or click **Recommendation Gate**. The Moonshot panel appears under the caption.
4. Point at the orange banner first:

> **ADVISORY FORECAST — NOT A CONTROL ACTION**

5. Walk three rows. Do not spend time on every line.

| Row | Category | Action | What to say |
|---|---|---|---|
| 1 | **UNKNOWN_PROCESS_CONTEXT** | **ABSTAIN** | We do not know process context. Unknown is not permission to isolate. |
| 2 | **SAFETY_BYPASS_AGING** on **PLT-10-SAFE-07** | **ABSTAIN** | Protection is already bypassed without authorization. Isolate is not automatically safer. |
| 3 | **VENDOR_SESSION_PLUS_WRITE_ALERT** (session **RA-00025**) | **ABSTAIN** | Someone may already be on the network. We can show that. We cannot disable VPN from this screen. |

Optional fourth row if they ask “what is the strongest this goes?”:

- **IDENTITY_CONFLICT_REACHABLE** → **RECOMMEND_CONTAINMENT_REVIEW** — still not execute.

6. Say this:

> Moonshot may only say MONITOR, RECOMMEND_CONTAINMENT_REVIEW, or ABSTAIN. It cannot say isolate. Execute stays false. There is no Authorize or Execute on this panel.

---

## Step 5 — Rehearse isolate in the twin lab

1. On the Moonshot table, find **UNKNOWN_PROCESS_CONTEXT** or **VENDOR_SESSION_PLUS_WRITE_ALERT**.
2. Click **Load in twin**.
3. You land on **Inject / Simulation**. The twin lab card is visible.
4. Click **isolate_preview** (it is often already selected).
5. Wait for **lab_result**. It should read **UNSAFE_ISOLATION**.
6. Point at:
   - detail: CASCADE isolate_preview at 08:50 MIN_LOAD with unauthorized barrier bypass — unsafe
   - `execute=false`
   - `apply_to_plant=false`
7. Optionally click **do_nothing**, **increase_logging**, and **open_ticket** once, then go back to **isolate_preview**.
8. Say this:

> This is a consequence sketch, not a certified plant twin. We can rehearse isolate. We cannot apply it to the plant. There is no write-to-PLC path.

9. Click **Create approval packet**. That takes you to **Recommendation Gate**. Twin green does **not** auto-approve anything.

---

## Step 6 — Show the engine still owns the decision

1. You should already be on **Recommendation Gate**. If not, click it on the left.
2. Confirm pins: **PLT-10 · OT-01016 · ALT-002783**.
3. Click **Request draft packet**.
4. Wait for the workflow steps to light up.
5. Read:
   - Recommendation: **DO_NOT_ISOLATE** or **ABSTAIN**
   - Execute: **false**
   - Safe state: **MIN_LOAD**
   - Authorizable: **false**
   - Authorize: **disabled**
6. Point at the footer: no Execute Isolation, no Write PLC, no Modify SIS.
7. Say this:

> Moonshot can forecast. The twin can sketch. The packet is still the engines. 08:55 is a draft. The unit stayed up.

---

## Step 7 — Prove it still works when AI is down

1. On the left, under **Scenario rail**, click **AI outage**.
2. Stay on Control Tower or Recommendation Gate.
3. Point at:
   - Header AI control **disabled**
   - Caption gone
   - Moonshot table gone
   - Estate tables / draft path **still there**
4. Say this:

> If the model is down and this board goes blank, we failed. Advice is the engines. AI is optional narration.

5. Return: scenario rail **CASCADE-001**, header **MOONSHOT**.

---

## Step 8 — Close the ask

1. Click **KPI Before/After**, then **Executive Brief**.
2. Say this:

> We are not selling autonomous isolation. The 90-day ask is an advisory shadow: humans still authorize, Moonshot stays earned, execute stays off. Do not canary a controller.

If they ask for “just isolate the bad VLAN,” say: that control is not in this product, on purpose.

---

## Optional contrast (20 seconds)

1. Change **Persona** to **Executive**.
2. The **MOONSHOT** button disappears. Executives get the brief, not the forecast toy.
3. Switch back to **Full workshop view** before the next click.

---

## 90-second version

Paste this URL:

`http://127.0.0.1:5173/estate?persona=full&scenario=cascade_001&ai=moonshot`

Then only do:

1. Banner: **NOT A CONTROL ACTION**.
2. Row **UNKNOWN_PROCESS_CONTEXT** → **ABSTAIN**.
3. **Load in twin** → **isolate_preview** → **UNSAFE_ISOLATION**.
4. **Create approval packet** → **Request draft packet** → Execute **false**, Authorize **disabled**.
5. Scenario **AI outage** → tables remain, Moonshot hides.

---

## Lost-screen recovery

| You want | Paste this |
|---|---|
| Clean start, AI off | http://127.0.0.1:5173/estate?persona=full&ai=off |
| Moonshot on CASCADE | http://127.0.0.1:5173/estate?persona=full&scenario=cascade_001&ai=moonshot |
| Twin lab | http://127.0.0.1:5173/simulation?persona=full&scenario=cascade_001&ai=moonshot |
| Draft packet | http://127.0.0.1:5173/recommend?persona=full&scenario=cascade_001&ai=moonshot |

Use **5173** for the live UI. **8000** is the API (it can also show the built UI, but 5173 is the demo screen).

---

## What not to do on stage

- Do not click **Authorize** (disabled; naming an authorizer is still an open client decision).
- Do not promise “apply twin to plant” (that button does not exist).
- Do not say SLO-OT green means the plant is healthy (it means **this software did not execute on OT**).
- Do not hide conflicts or clean the inventory.
- Do not rank by CVSS as if that were operational risk.
- Do not demo live controller writes — this app cannot do them.
- Do not treat the Executive persona as permission. It is a view filter only.
