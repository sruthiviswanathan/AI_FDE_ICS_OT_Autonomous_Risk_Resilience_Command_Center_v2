# 30-Minute Demo Plan — ICS/OT Autonomous Risk & Resilience Command Center v2

**Audience:** Business stakeholders, technical architects, AI architects  
**Demo length:** 30 minutes  
**Target client pain points:** *(Customize — mapped below to documented repo business pains: unplanned downtime risk, audit/readiness gaps, SOC–plant conflict, untrusted operational picture.)*

---

## App understanding (brief)

This is a **synthetic, locally runnable simulation** of an 18-plant multinational ICS/OT estate where cyber, operational, safety, and resilience views **do not agree** — by design. Today's runnable product is a **read-only advisory foundation**: a CLI and API that aggregate **14 brownfield health signals** (inventory conflicts, bad telemetry, safety bypasses, recovery gaps, remote-access issues, and more) from seeded, contradictory data. It **observes and recommends**; it never writes to controllers, blocks networks, or executes isolation. The core value proposition is a path to a **Trusted Cyber-Physical Advisory Command Center** — governed, human-in-the-loop decision support that replaces CVSS-only dashboards and safety-blind automation with evidence-based, policy-bounded recommendations.

---

## Top 5 features to demo

### 1. Brownfield Estate Diagnostics (14-signal command snapshot)

**Feature:** One command aggregates 14 cross-domain brownfield signals across all 18 plants.

**Why it matters here:** Leadership already has dashboards — but none answer "what is actually wrong across cyber, operations, safety, and recovery?" This directly addresses **untrusted situational awareness** and **audit readiness** (you can show measurable gaps, not opinions).

**Demo workflow:**

1. Open terminal in the project folder; show `data/manifest.json` — **18 plants**, ~2,000 assets, ~31K telemetry records (estate scale in one screen).
2. Run `python scripts/generate_data.py --check-only` — show data integrity passes on the seeded brownfield dataset.
3. Run `python -m ot_command.cli diagnostics` — display the JSON output with all 14 counts.
4. Highlight four headline numbers: **200** assets registered ACTIVE but observed OFFLINE/UNSEEN; **61** safety barriers bypassed/degraded; **4,094** bad/uncertain telemetry records; **244** stale/unknown backups.
5. Say: "This is not a greenfield demo — these contradictions are the real problem we're built to investigate, not hide."

**Talking point:** "In thirty seconds you see what your SIEM, CMDB, and historian cannot agree on — across the whole estate."

---

### 2. Identity & state reconciliation (why 'ACTIVE' ≠ 'actually there')

**Feature:** Diagnostics surface asset identity conflicts — registered vs. observed state, alias collisions, and maintenance field mismatches.

**Why it matters here:** You cannot cut downtime or pass an audit if you don't know **what exists** and **what state it's in**. This hits **inventory truth**, **maintenance/CMMS alignment**, and **incident response accuracy**.

**Demo workflow:**

1. Return to diagnostics output; zoom into `asset_state_conflicts` (200), `alias_collisions` (5), `maintenance_state_conflicts` (128).
2. Open `data/raw/assets.csv` — filter/show one row where `registered_state=ACTIVE` and `observed_state=OFFLINE` or `UNSEEN`.
3. Open `data/raw/asset_aliases.csv` — show one alias that maps to more than one asset (collision).
4. Open `data/raw/work_orders.csv` — show one row where CMMS says CLOSED but field status is not RETURNED_TO_SERVICE.
5. Tie back: "If we isolate or patch the wrong asset ID, we create downtime — not reduce risk."

**Talking point:** "We stop treating the CMDB as gospel and show you where field reality, telemetry, and maintenance records diverge."

---

### 3. Legacy risk ranking — the CVSS trap (modernization target)

**Feature:** `legacy_rank` intentionally ranks findings by CVSS alone — a known defect preserved for modernization.

**Why it matters here:** SOC queues driven by score alone **misallocate effort**, extend **unplanned downtime** (wrong asset prioritized), and weaken **audit defensibility** ("why did we patch that first?").

**Demo workflow:**

1. Open `src/ot_command/legacy/risk.py` — show `legacy_rank` sorts by CVSS only.
2. Run `pytest tests/test_known_legacy_defects.py -v` — show the **expected failure (XFAIL)**: a CVSS 9.8 LOW/unreachable finding outranks a CVSS 6.5 CRITICAL/reachable one.
3. Walk through the test data: Asset A (high CVSS, low criticality) vs. Asset B (lower CVSS, critical and reachable).
4. State the target (from specs): **contextual risk** joins reachability, process criticality, safety barriers, and recovery — not CVSS alone.
5. Close: "This is what you have today in many estates; our modern engines are spec'd to replace this logic — safely."

**Talking point:** "Highest CVSS is not highest operational risk — and your current ranking logic proves it in one test."

---

### 4. Safety-blind containment vs. governed action tiers

**Feature:** `legacy_isolation_recommendation` always says ISOLATE on HIGH/CRITICAL alerts; `ACTION_TIERS` in policy code bounds what software may even *recommend* vs. what requires human approval — with OT writes and isolation **execute** permanently forbidden.

**Why it matters here:** Addresses **safe response** (avoid destabilizing a unit), **governance for AI/automation**, and **audit/regulatory** questions about who can do what.

**Demo workflow:**

1. In `legacy/risk.py`, show `legacy_isolation_recommendation('CRITICAL')` returns `"ISOLATE"` regardless of safety context.
2. Show the second XFAIL test — high severity should **not** always trigger isolation.
3. Open `scenarios/cascade_001.json` — read the timeline: SOC recommends isolation at 08:47; process engineer warns abrupt isolation may destabilize the unit at 08:50; safety barrier bypassed at 08:38.
4. Open `src/ot_command/core/policy.py` — walk ACTION_TIERS 0–4: observe/correlate at tier 0; recommend at tier 1; isolate_endpoint at tier 3 (human approval); write_plc_logic / modify_sis / bypass_interlock at tier 4 (never executable).
5. Emphasize SDD-09: **Option C (unsafe autonomous OT agent) was rejected**; Option A deterministic engines + optional explainer only.

**Talking point:** "We don't automate plant control — we govern recommendations so the wrong button never exists in software."

---

### 5. Read-only advisory API + AI-optional resilience

**Feature:** FastAPI exposes `GET /health` and `GET /diagnostics` only — synthetic, read-only. Core diagnostics work with AI disabled (`AI_ENABLED=0` per ADR-12).

**Why it matters here:** Technical and AI architects care about **integration without OT write risk**; business cares about **continuity during outages** and **audit evidence** that the system never becomes a control path.

**Demo workflow:**

1. Start API: `uvicorn ot_command.api:app --reload` (with `PYTHONPATH=src`).
2. Browser: hit `/health` — show `synthetic-read-only` mode.
3. Browser: hit `/diagnostics` — same 14 signals as CLI, JSON for SOC/dashboard integration.
4. Reference ADR-12: if AI/LLM is down, **identity, telemetry, and recovery tables still work** — no blank screen.
5. Close with target vision from specs: modern engines in `src/ot_command/modern/` (placeholder today) — identity, contextual risk, safety policy, recovery, advisory packets — all **recommend-only**.

**Talking point:** "Your command center keeps working when the model goes quiet — because the engines are deterministic; AI explains, it doesn't decide alone."

---

## Suggested running order (30 minutes)

| Segment | Feature | Time | Narrative role |
|--------|---------|------|----------------|
| **Open** | Estate scale + 14-signal diagnostics | **6 min** | "Here's the multinational estate and why dashboards disagree." |
| **Build 1** | Identity & state reconciliation | **6 min** | "You can't act on assets you can't trust." |
| **Build 2** | Legacy CVSS ranking (XFAIL) | **5 min** | "Today's logic prioritizes the wrong fights." |
| **Build 3** | CASCADE-001 + ACTION_TIERS | **7 min** | "Security and safety can conflict — here's how we govern response." |
| **Close** | Read-only API + AI-optional path | **6 min** | "Safe to integrate, safe to audit, safe when AI is off." |

**Arc:** Problem (no trusted truth) → Evidence (14 signals + data rows) → Failure mode (legacy logic) → Governance (tiers + rejected unsafe autonomy) → Production posture (read-only API, deterministic core).

---

## Prep checklist

### Before the demo

- [ ] Python venv created; `pip install -r requirements.txt`
- [ ] Set `PYTHONPATH=src` (or install package editable)
- [ ] Pre-run: `python scripts/generate_data.py --check-only` and `python -m ot_command.cli diagnostics` — capture output in a buffer in case live run hiccups
- [ ] Pre-run: `pytest tests/test_known_legacy_defects.py -v` — confirm 3 passed / 3 xfailed baseline
- [ ] Have browser tab ready for `http://127.0.0.1:8000/diagnostics` after starting uvicorn
- [ ] Pre-open: `data/manifest.json`, one example row each from `assets.csv`, `work_orders.csv`, `cascade_001.json`, `policy.py`
- [ ] Prepare one slide or verbal line: **modern engines are spec'd, not yet live** — avoid overselling

### Likely client questions — be ready

1. **"Can this isolate a compromised PLC automatically?"** — No. Isolation execute is not a software action; `isolate_endpoint` is tier 3 (human approval) and the API is read-only. Recommendations only.
2. **"How is this different from our SIEM/GRC?"** — SIEM sees cyber alerts; this correlates **cyber + operational state + safety barriers + recovery readiness** from the same brownfield evidence. Diagnostics already show conflicts SIEM cannot resolve alone.
3. **"What if we don't trust AI in OT?"** — Align with ADR-12: `AI_ENABLED=0` still delivers diagnostics and tables; Option A deterministic engines are always-on; Option B explainer is optional. Option C unsafe agent was explicitly rejected.

---

## Confirm before demo

These are **specified or narrated in the repo** but **not runnable as live product features today** — do not demo as if they work:

| Item | Status |
|------|--------|
| Modern engines (contextual risk, identity resolution, advisory packets) | Placeholder in `src/ot_command/modern/` |
| Web UI / executive dashboard | Not in repo; CLI + API only |
| CASCADE-001 as a live "play scenario" button | JSON narrative only — use as story, not simulation |
| Eval harness pass/fail run | `golden_cases.jsonl` exists; execution is future ENH work |
| Named human authorizers for tier-3 actions | OPEN decision — roles only, no named people |

---

*Customize client pain points in the header when known (e.g., "Q1 audit," "72-hour downtime target," "board mandate on AI governance") to tighten talking points and reorder features.*
