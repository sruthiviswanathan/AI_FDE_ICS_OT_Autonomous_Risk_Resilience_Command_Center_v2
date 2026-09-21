# REL-03 — Demo script (12 minutes)

**Tone:** FDE on the board, not a vendor. Describe only what is implemented.  
**Host:** local `apps/command_center` or the synthetic Render demo. Cold start can take 30–60s.  
**Persona:** **Full workshop view**. Do **not** click Authorize (disabled — OPEN-001).  
**Mode:** `synthetic-read-only`. Header may show AI OFF (default).  

Click-path (required): **Control Tower → identity conflict → anti-CVSS → safety vs SOC isolate → vendor session → recovery not ready → cascade_001 08:55 → trace → AI outage → exec KPIs.**

If the API is unreachable, hard-refresh once. Fallback: `/docs` on the same host.

---

## Before the clock

1. Persona = Full workshop view.  
2. Scenario rail visible. Start on **Nominal**.  
3. Confirm footer: workshop-static freshness. SLO-OT OK means **the product did not execute on OT**, not “the plant is healthy.”

---

## 0:00–1:00 — Control Tower (asked vs broken)

**Stay:** `/` Control Tower. Scenario **Nominal**.

**Point:** Mode badge · Deterministic engines · SLO-OT · estate diagnostic strip.

**Say:** Leadership asked for an autonomous command center. What we have is an 18-plant estate that already disagrees with itself. This UI is advisory. There is no isolate button that does anything.

**Do not say:** The fleet is healthy because SLO-OT is green.

---

## 1:00–2:00 — Identity conflict

**Click:** Scenario **inject_01** (identity). Nav **Identity Reconciliation**.

**Point:** Registered vs observed. Alias collisions. `cmdb_winner=false`. OT-00528 (or the pinned asset) RETIRED vs ONLINE if shown.

**Say:** Two inventories, two truths. Software must not pick a CMDB winner. Cleaning this list would hide the problem.

---

## 2:00–3:00 — Anti-CVSS

**Click:** **Contextual Risk**. Keep plant pin if the rail set one; otherwise stay on the estate rank.

**Point:** Default **Contextual rank**. Row **VUL-00098 / OT-01016** (reachable, process-relevant) vs a higher-CVSS unreachable finding. Optional: **CVSS-only (warn)** amber banner, then switch back.

**Say:** A 9.8 that cannot reach the unit is not the first ticket. CVSS is an input. Ranking by CVSS alone is the legacy defect we kept as XFAIL.

---

## 3:00–4:30 — Safety vs SOC isolate

**Click:** Scenario **CASCADE-001**. **Safety vs Security**.

**Point:** PLT-10-SAFE-07 · unit PLT-10-U06 · BYPASSED · authorized **NO**. UNKNOWN bypass stays UNKNOWN.

**Say:** SOC will want isolate because the alert is HIGH. Protection is already degraded. Isolate is not automatically safer. This screen cannot bypass a SIS.

---

## 4:30–5:30 — Vendor session

**Click:** **Vendor Sessions**. Filter **PLT-10** if not already pinned.

**Point:** Unapproved / MFA-not-confirmed tiles (corpus: **137** / **128**). Example session **RA-00025** approved window **NO**.

**Say:** Someone may already be on the network. We can show that. We cannot disable VPN. That is a tier-3 human action with no execute API.

---

## 5:30–6:30 — Recovery not ready

**Click:** **Recovery Graph**. Prefer **inject_06** or plant **PLT-01** IDENTITY if the rail offers it; else PLT-10 scoreboard (workshop: **0 / 8** ready).

**Point:** A row with backup **CURRENT** and RecoveryReady **NO**. Restore-test days, STALE runbook, unverified deps.

**Say:** If we isolate, can we recover? Not because a flag is green. Ready means tested restore, current runbook, verified dependencies. PLT-01 IDENTITY is CURRENT with a 360-day restore test. There is no live restore button.

---

## 6:30–8:30 — cascade_001 08:55 (the packet)

**Click:** Scenario **CASCADE-001**. **Incident Context** (Load CASCADE-001 if empty). Read times:

| Time | What the room sees |
|------|--------------------|
| 08:24 | Vendor session |
| 08:38 | Barrier bypassed |
| 08:47 | SOC recommends isolate |
| 08:50 | Process: abrupt isolate may destabilize (MIN_LOAD) |
| 08:55 | Governed **draft** — this is the product |

Shift email: **UNTRUSTED**. Not PLT-10 policy.

**Click:** **Recommendation Gate**. Confirm pins **PLT-10 · OT-01016 · ALT-002783**. **Request draft packet.** Wait the eight engine states.

**Read:** Recommendation **DO_NOT_ISOLATE** or **ABSTAIN**. Execute **false**. Safe state **MIN_LOAD**. Authorizable **false**. Required authority = **roles only**. Authorize **disabled**. Footer: no Execute Isolation / Write PLC / Modify SIS.

**Say:** 08:47 is a demand. 08:50 is dissent. 08:55 is a draft. Software did not take the unit.

---

## 8:30–9:30 — Trace

**Click:** **Decision Trace** (`/audit`).

**Point:** SLO-OT · cost card (tokens **0** with AI off) · last row: purpose CASCADE-001 triage, **Execute = false**.

**Say:** If we cannot show the row, we do not have a decision. Hidden chain-of-thought is not a control.

---

## 9:30–10:30 — AI outage

**Click:** Scenario **AI outage** (`ai_outage`). Stay on Control Tower or Recommendation Gate.

**Point:** Tables and draft path remain. Caption / Moonshot **hidden**. Header AI control **disabled**. Engines still run.

**Say:** If the model is down and the board goes blank, we failed EVAL-016. Advice is the engines. AI is optional narration.

Optional 10s: `?ai=moonshot` only on Full/FDE/SOC **after** returning to CASCADE — banner **NOT A CONTROL ACTION**. Skip if time is tight. Executive persona keeps Moonshot off.

---

## 10:30–12:00 — Exec KPIs and the ask

**Click:** **KPI Before/After** (`/kpi`) then **Executive Brief** (`/executive`).

**Point:** Diagnostic counts **unchanged** (conflicts still counted). CTQ strip: SLO-OT, SLO-EVAL, AI default OFF, execute routes **0**. Footer: no execute on this surface.

**Say:** After does not mean “200 went to zero.” After means the draft no longer isolates blind, no longer calls CURRENT ready, and no longer sorts CVSS-only. Clocks and dollars are still OPEN-006 — we will not invent them in this room.

**Close (90-day):** Scale **advisory shadow**. Name Authorizer **people in your process**, not in this repo. Measure time-to-confidence with a stopwatch in tabletop. Moonshot only if 31/31, execute stays false, and AI-disabled drill still passes. Do not scale isolation execute. Do not canary a controller.

---

## If time slips

Keep: CASCADE 08:55 packet → AI outage → exec CTQs. Cut: identity and vendor.

## What not to demo

Twin **apply to plant**. Authorize. Any “isolate region” control (does not exist). Cleaning diagnostics. Live OT.
