# How to demonstrate CASCADE-001 (the closer)

Plain-English click path for stakeholders.

**App:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)

You are showing **one morning** where identity, vendor access, telemetry, safety, process, and recovery all disagree. At **08:55** the app drafts a response. It does **not** isolate.

If the page is slow, wait about a minute.

The longer script with screenshots is in [`WORKFLOW_08_CASCADE.md`](WORKFLOW_08_CASCADE.md).

---

## Before you start

1. At the top, set the persona to **FDE** or **Full**.
2. Stay on **CASCADE-001**. Do not bounce through inject_01–06 unless someone asks.
3. Rule you will repeat: **08:47 is a demand. 08:55 is the decision. Execute stays no.**

Pins you will keep pointing at:

- Plant **PLT-10**, asset **OT-01016**, alert **ALT-002783 HIGH**
- Unit **PLT-10-U06**, barrier **PLT-10-SAFE-07**, safe-state **MIN_LOAD**

---

## Step 1 — Load the morning

1. On the left, under **Scenario rail**, click **CASCADE-001**.
2. Check the top: **PLT-10**, **OT-01016 DCS_CONTROLLER**, **ALT-002783 HIGH**.
3. Read the badges: barrier bypassed unauthorized, MIN_LOAD, 08:24 vendor session, SOC vs PE dissent, shift notes UNTRUSTED, **execute=false**.
4. Say this:

> This is one hour in a plant that already disagrees with itself. We will walk the clock, then stop at a draft. We will not become the incident.

---

## Step 2 — Read the clock on Incident Context

1. On the left, click **Incident Context**.
2. If the list is empty, click **Load CASCADE-001**.
3. Read these four times out loud (you can paraphrase the others):

- **08:24** — a vendor session is already on the engineering workstation.  
- **08:38** — a safety barrier is recorded bypassed.  
- **08:47** — SOC says isolate now.  
- **08:50** — process engineering says that may destabilize the unit.  
- **08:55** — the command center must recommend a **safe governed** response.

4. Point at the red box **Shift handover UNTRUSTED**.
5. Say this:

> That email talks about Unit 04. This morning is Unit 06. Even the line that says “do not isolate near minimum stable load” is still untrusted text. It is not policy.

---

## Step 3 — Four proof screens (one sentence each)

Keep CASCADE pinned.

**Safety vs Security**

1. Click **Safety vs Security**.
2. Point at **PLT-10-SAFE-07** on **PLT-10-U06**: **BYPASSED**, authorized **NO**.
3. If a red **Q3** error appears, ignore it. The table is enough.
4. Say: “Protection is already degraded. Isolate is not automatically safer.”

**Vendor Sessions**

1. Click **Vendor Sessions**.
2. Table is **PLT-10** only. Point at **RA-00025** — approved window **NO**.
3. Say: “Someone is already inside. We do not kill VPN from this screen.”

**Process Graph**

1. Click **Process Graph**.
2. Point at the dashed line onto **OT-01016** (observed **UNSEEN**).
3. Point at **Forbidden: regional isolate action**.
4. Say: “Blast radius is unknown. We do not isolate the region.”

**Recovery Graph**

1. Click **Recovery Graph**.
2. Point at **PLT-10 · 0 / 8** ready.
3. Say: “If we isolate, we still cannot claim a tested restore. CURRENT is not ready.”

---

## Step 4 — Request the 08:55 packet

1. Click **Recommendation Gate**.
2. Confirm **PLT-10**, **OT-01016**, **ALT-002783**.
3. Click **Request draft packet**.
4. Read:
   - Recommendation: **DO_NOT_ISOLATE**
   - Execute: **No**
   - Safe state: **MIN_LOAD**
   - Process context: **UNKNOWN**
   - Required humans: Process Engineer, Safety/SIS Owner, VP Operations
   - Authorize: **disabled**
5. Say this:

> SOC wanted isolate at 08:47. Process warned at 08:50. The packet at 08:55 is DO_NOT_ISOLATE. There is no isolate button.

---

## Step 5 — Show the audit row

1. Click **Decision Trace**.
2. Point at **Zero OT execute actions in software**.
3. Point at the row **CASCADE-001 triage** → **DO_NOT_ISOLATE** → Execute **No**.
4. Point at **0** tokens.
5. Say this:

> The refusal is inspectable. We did not need a model to keep execute false.

---

## Step 6 — Close in one sentence

> At 08:55 we showed bypass, vendor session, untrusted notes, and recovery not ready together. The packet is DO_NOT_ISOLATE. We did not isolate.

---

## If someone asks “so what do we do?”

- **SOC:** keep the HIGH alert; do not execute isolate from this UI.
- **Process / Safety:** you are named on the packet. Unit is MIN_LOAD. Bypass is unauthorized.
- **Leadership:** the win is unsafe isolate avoided, not a faster cut.

Optional last click: **Executive Brief** (“no execute controls”) or **AI outage** (tables stay up, tier 4 still refused).

---

## 90-second version

1. CASCADE-001 — six badges, execute=false.  
2. Incident: 08:47 vs 08:50; shift notes UNTRUSTED.  
3. Safety bypassed; vendor already on PLT-10; recovery 0/8.  
4. Draft **DO_NOT_ISOLATE**.  
5. “The command center reconciled the morning. It did not become the incident.”
