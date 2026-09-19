# FDE Capstone — Direction Check Answers

**Source worksheet:** `FDE_Capstone_Thinking_Questions_Cohort_4.pdf` (E&Y Batch-2, Cohorts 1–5)  
**Capstone:** Cohort-4 — ICS/OT Autonomous Risk & Resilience Command Center  
**Repo:** `AI_FDE_ICS_OT_Autonomous_Risk_Resilience_Command_Center_v2` (Repo 3.0 / PRD-01)  
**Date:** 2026-09-19  
**How this was answered:** Repo evidence (`specs/`, `adrs/`, `src/ot_command/`, `evals/`, `ops/`, `data/`) plus the workshop business story. OPEN items stay OPEN. No live plant is connected.

**Core FDE chain used here:** customer problem → evidence → constraints → system behavior → human decision → outcome → production operation.

---

## A. Cohort-specific challenge questions

### A1. What happens if the AI recommendation conflicts with a deterministic PLC/SCADA/DCS safety constraint?

**Safety wins. The product never writes the controller, and a HIGH cyber label cannot override a degraded SIS / MIN_LOAD / unauthorized bypass.**

Concrete scenario — **CASCADE-001 at 08:55** (plant `PLT-10`, asset `OT-01016`, alert `ALT-002783` HIGH, process context UNKNOWN):

| Clock | Who | Claim |
|---|---|---|
| 08:38 | Safety barrier `PLT-10-SAFE-07` | `BYPASSED`, `bypass_authorized=NO` |
| 08:47 | SOC / legacy habit | HIGH → isolate the endpoint |
| 08:50 | Process engineer (untrusted handover) | Isolation may destabilize the unit; safe-state is `MIN_LOAD` |

What the product does:

- Deterministic containment (`src/ot_command/core/containment.py`, ADR-04) returns **`DO_NOT_ISOLATE`** or **`ABSTAIN`** when barriers are degraded and process context is UNKNOWN. It never returns execute-`ISOLATE`.
- `POST /recommend` packets always have **`execute=false`**.
- Tier 4 verbs (`write_plc_logic`, `change_setpoint`, `modify_sis`, `bypass_interlock`) are **refused** (`policy.py` ACTION_TIERS; EVAL-006).
- Optional AI explainer (ADR-12, `AI_ENABLED=0` default) **cannot re-rank** risk or override the safety engine (ADR-03: LLM must not re-rank).
- Shift handover text is **UNTRUSTED_CONTENT** — cited, never treated as permission (ADR-06, EVAL-007, EVAL-029).

**Human boundary:** Process Engineer + Safety/SIS Owner must stay visible as dissent. Authorize is **not** implemented as a named person (OPEN-001).  
**Failure mode we refused:** “HIGH means isolate now.” That is exactly `legacy_isolation_recommendation` (kept XFAIL on purpose).  
**Measurable outcome:** EVAL-003 / 007 / 019 / 023 — packet is draft-only; barrier bypass and MIN_LOAD remain visible; no isolate-execute surface.

---

### A2. What is the fail-safe state if the AI, network, historian, or control-system connection fails?

**Fail-safe for this product is “do not actuate.” The plant stays on its existing SIS / operator control path. The command center degrades to tables, uncertainty, and abstain — never to a write.**

| Failure | Product fail-safe | Evidence |
|---|---|---|
| AI / LLM down or `AI_ENABLED=0` | Deterministic engines still serve identity, telemetry, risk, safety, recovery. No blank screen. | ADR-12, EVAL-016 |
| Historian / telemetry quality bad | Dual clocks (`event_time` vs `ingest_time`); BAD/uncertain flags stay visible; do not invent a clean process state | ADR-02, inject_02, EVAL-009 |
| Network / plant link (workshop) | There is **no live OT connector**. Absence of a write API *is* the fail-safe | ADR-11, `tests/test_api_readonly.py` |
| Control-system / SIS unreachable | Product cannot change SIS. Safe-state on the unit (`STOPPED` / `MIN_LOAD` / `ISOLATED` / …) is **displayed**, not commanded | `data/raw/process_units.csv`, FR-004 |
| Missing joins (1834 assets without tag→unit) | `unit_join_missing` stays true; UNKNOWN is not NORMAL | TRACEABILITY FR-006, EVAL-031 |

If the **operator** loses the app: PLC/SCADA/DCS and the physical SIS remain the authority. This software is not in the trip path.

---

### A3. Can the AI directly control the plant? If not, what is the approval boundary?

**No. The AI cannot control the plant. There is no OT write API and no Execute Isolation control.**

Approval boundary (`policy.py` / ADR-14):

| Tier | Examples | Autonomous in this product |
|---|---|---|
| 0 | observe, correlate, summarize | Yes |
| 1 | recommend (draft packet) | Yes — **draft only** |
| 2 | request_fresh_telemetry, open_ticket, increase_logging | Stubs / recommend-only in workshop |
| 3 | isolate_endpoint, change_remote_access, change_firewall | **Human authorize only** — no execute API |
| 4 | write_plc_logic, change_setpoint, modify_sis, bypass_interlock | **Refuse** |

Unknown action → treat as tier 4 refuse (EVAL-006). UNKNOWN permission is not permission.

`recommend` ≠ `authorize` ≠ `execute`. `containment.is_packet_authorizable()` stays false until CTQ-ISO fields exist (EVAL-020). UI Authorize remains disabled (OPEN-001).

---

### A4. How do you detect anomalies without generating an unusable number of false alarms?

**We do not ship a “detect everything” ML anomaly engine. We rank and gate existing alerts so HIGH/CVSS does not become 2,800 isolate tickets.**

Estate scale in the corpus: 18 plants, ~2,016 assets, **2,800** cyber alerts, **4,094** bad/uncertain telemetry events, **779** undocumented observed paths.

How noise is reduced:

1. **Contextual risk, not CVSS sort** (ADR-03). Example in the estate: a CVSS 9.8 that is unreachable ranks below an 8.7 that is reachable on a MIN_LOAD unit (`OT-01016`). LLM must not re-rank.
2. **Identity first.** Alias collisions and REGISTERED vs OBSERVED conflicts are shown, not merged (ADR-01, EVAL-001). Isolating the wrong twin is a false “success.”
3. **Telemetry quality is a separate channel** (ADR-02). A flat historian vs moving HMI is a *quality* story, not automatically a process incident (handover 20-min claim; inject_02).
4. **Safety join required for isolate drafts.** HIGH + UNKNOWN process context + degraded barrier → `DO_NOT_ISOLATE` / `ABSTAIN`, not a flood of isolate recommendations.
5. **Hop-capped graph slices (Q1–Q5, hop ≤ 8)** so operators see a neighborhood, not the whole estate (NFR-CAP, ADR-KG).

We are not claiming a production SOC false-positive SLO. Workshop SLO for packet assembly is p95 &lt; 8000 ms (OPEN-006 — baseline pending).

---

### A5. How do you distinguish a genuine process anomaly from a sensor/data-quality problem?

**Keep five states separate. Never infer process truth from a single dirty tag.**

| State | What we use | What we refuse |
|---|---|---|
| Observed cyber | `cyber_alerts.csv`, sessions | Treating SOC SUPPRESSED as an SIS trip suppression |
| Registered identity | CMDB / `assets.csv` | Picking a CMDB winner on alias collision |
| Telemetry quality | `event_time` **and** `ingest_time`; BAD / duplicate / unit-mismatch flags | Using ingest order as process order (EVAL-004) |
| Process / safety | unit `safe_state`, barrier state, `process_context` | Imputing tag→unit for the 1,834 untagged assets |
| Operator narrative | Shift email | Using it as policy (ADR-06) |

CASCADE analogue: historian “flat 20 min” vs HMI movement is in the **untrusted email**, not a verified tag incident (OPEN-021). Product shows both clocks and quality flags; it does **not** declare a process trip from that sentence.

If `process_context=UNKNOWN`, the engine **abstains** rather than assuming NORMAL (EVAL-031).

---

### A6. How would you test autonomous behavior safely without putting the physical process at risk?

**We do not test autonomy on a live process. The workshop corpus, golden evals, and red-team cases are the safe testbed. “Autonomous” here is draft-recommend only.**

How we test without plant risk:

- **No live connectors** (Dockerfile / FastAPI bind localhost; synthetic CSVs).
- **Golden harness EVAL-001…031** (`evals/harness.py`) including isolation-must-not-execute (007, 023), AI-outage (016), injection in shift notes (029).
- **Red team A-01…A-10** (`tests/red_team/`) — prompt injection, tool misuse, write-PLC requests.
- **Legacy XFAIL preserved** so we can still *see* the unsafe predicate (`legacy_isolation_recommendation` → ISOLATE) without shipping it.
- **Scenarios** (`cascade_001`, inject_01…06) pin plant/asset/alert and expected badges; conflicts are never hidden to beautify the demo.
- **Hop cap 8**, no isolate-execute UI, `execute=false` asserted in API tests.

What we chose **not** to automate: any write to PLC, SIS, setpoint, interlock, or firewall.

---

## B. FDE direction-check questions

### B1. Problem and customer

**What exact real-world problem are you solving?**  
SOC, process, and safety each see a different “truth” on the same asset. Legacy tools collapse that to **highest CVSS** or **HIGH → isolate**, which can become the incident (CASCADE 08:47 vs 08:50). The product produces a **governed, evidence-cited advisory packet** so humans can decide *without* software actuation.

**Who is the primary user, and what decision are you helping them make?**

| Persona | Decision the product supports |
|---|---|
| SOC / OT analyst | Triage this alert — monitor, draft contain, or abstain? **Not** “press isolate.” |
| Process engineer | Will isolation destabilize MIN_LOAD / this unit? |
| Safety / SIS owner | Is a bypass already in place? Is it authorized? |
| VP Ops | Estate residual risk and who must authorize — person still unnamed (OPEN-001) |

**What is the current process without this solution, and where does it break?**  
Separate CMDB, SIEM, historian, CMMS, shift email, and vendor sessions. Legacy code in-repo encodes the break:

- `legacy_rank` = CVSS-only  
- `legacy_recovery_ready` = backup CURRENT is enough  
- `legacy_isolation_recommendation` = HIGH/CRITICAL → ISOLATE  

Diagnostics baseline: 200 state conflicts, 5 alias collisions, 779 undocumented paths, 4094 bad/uncertain telemetry, 137 unapproved sessions, 61 degraded barriers (estate tiles).

**Cost of getting it wrong?**  
Wrong-asset isolate, SIS already bypassed, MIN_LOAD destabilization, vendor session mistaken for approved change, or “cleaning” identity collisions into a silent CMDB winner. Kill criterion (SDD-05): if the product adds an OT write surface or scales unsafe isolate recommendations → **stop**.

---

### B2. End-to-end workflow

**One realistic path (CASCADE-001):**

1. **Input / event** — Alert `ALT-002783` HIGH CONFIG_DRIFT on `OT-01016` (PLT-10); SOC status SUPPRESSED; process context UNKNOWN.  
2. **Data** — `cyber_alerts.csv`, `assets.csv` + aliases, `tags.csv` / `process_units.csv`, `safety_barriers.csv`, `remote_access_sessions.csv`, untrusted `shift_handover_email.txt`.  
3. **Processing** — `/diagnostics` → `/assets/OT-01016/identity` → `/graph/slice?query=Q5` → `/risk/contextual` → `/safety/conflicts` → `/recovery/PLT-10` → `POST /recommend`. Deterministic engines always run. Optional explainer off.  
4. **Decision (system)** — Packet: `DO_NOT_ISOLATE` or `ABSTAIN` / `ISOLATE_DRAFT` only if CTQ-ISO complete; **`execute=false`**; required roles listed.  
5. **Human action** — SOC + PE + Safety review the dual-column dissent. No Execute button. Authorize control disabled (OPEN-001).  
6. **Outcome** — Isolation is **not** executed by the app. Trace appended (`contracts/decision_trace.yaml`). EVAL-007 PASS is the workshop proof.

**Systems / data that must participate (workshop files standing in for them):**  
CMDB/assets, alias overlay, passive/observed state, historian/telemetry, SIEM alerts, process units, SIS/barriers, recovery/backup/runbook, vendor remote access, shadow inventory (evidence only), shift email (untrusted).

**Real-time vs async (honest workshop bound):**  
This repo is **workshop-static**. In a real plant: alert ingest and safe-state read would be near-real-time; identity reconciliation, recovery-ready, and eval harness are asynchronous. Packet SLO target p95 &lt; 8 s is **baseline pending** (OPEN-006). We do not pretend we have a live historian subscription.

**Success for the user:**  
They can say: “HIGH is not a license to isolate. Barrier `PLT-10-SAFE-07` is bypassed unauthorized. Unit is MIN_LOAD. Draft only. Execute = No.” And they can show the evidence paths.

---

### B3. Why AI / agentic?

**Why AI at all? What is deterministic?**  
SDD-09 **Option A (deterministic engines) + Option B (optional explainer)**. **Option C (agent writes OT) was rejected** and must not be reopened.

| Deterministic (always on) | Optional AI | Must not use AI for |
|---|---|---|
| Identity, telemetry quality, contextual risk, containment, recovery-ready, graph Q1–Q5, ACTION_TIERS | Narrative explainer / incident-analyst workflow when `AI_ENABLED=1` | Re-rank risk, authorize, isolate, write PLC/SIS, treat shift notes as policy |

**What the agent must NOT do:**  
Write controllers, change setpoints, modify SIS, bypass interlocks, execute isolate, merge colliding aliases, hide UNKNOWN, or treat vector-retrieved email as DecisionAuthority.

**Autonomy level:**  
**Level 1 draft / recommend.** Tier 0–1 tools only for the agent (`guardrails.py`). Tier 3 is human-only and still has no execute API. That is appropriate because isolation on a degraded SIS is a process-safety decision, not a chat completion.

---

### B4. Data and evidence

**Data required for one important decision (isolate draft vs do-not-isolate):**  
`asset_id`, plant, alert severity + process_context, identity conflicts, network reachability, unit `safe_state`, barrier state + `bypass_authorized`, recovery-ready (not just backup CURRENT), required roles, policy version, as-of.

**Where it comes from / freshness:**  
Workshop-static CSVs under `data/raw`, `data/reference`, `data/shadow`, `data/telemetry`. Freshness is **synthetic / PENDING** on several KPIs. In production, as-of and policy_version must be on every packet (already fields on `POST /recommend`).

**Missing, stale, contradictory, corrupted:**  
We **keep the contradiction**. Do not clean `data/`. Missing unit join → `unit_join_missing`. UNKNOWN bypass ≠ YES. Shadow `FINAL_v8` is evidence, not the new CMDB. Bad telemetry stays flagged. Shift email stays UNTRUSTED.

**Evidence for later explanation:**  
Decision traces (JSONL, `contracts/decision_trace.yaml`): actor, purpose, plant/asset/alert, recommendation, execute flag, evidence[], tool_calls, policy_version, tokens/latency, policy_gate. Provenance drawer: STRUCTURED / GRAPH / POLICY / MEMORY (vector off / untrusted only).

---

### B5. Failure modes and resilience

**Five most dangerous failures**

| # | Failure | Detect | Prevent | Recover |
|---|---|---|---|---|
| 1 | Product becomes the isolate executor | Route tests: no isolate POST; `execute=false` | ACTION_TIERS + no write API | Kill criterion — stop the release |
| 2 | HIGH/CVSS-only ranking isolates the wrong box | EVAL-002 / 017; factor_breakdown | ADR-03 contextual rank | Show missing joins; abstain |
| 3 | Prompt injection in shift notes (“bypass is authorized”) | EVAL-029, red-team A-02 | UNTRUSTED channel; engines ignore note for enums | Citation only; do not train policy from the email |
| 4 | Wrong asset (alias collision / RETIRED vs ONLINE) | EVAL-001; identity board | `cmdb_winner=false`; do not merge | Human picks; no silent winner |
| 5 | AI outage blanks the console | EVAL-016 | `AI_ENABLED=0` is a first-class path | Tables + refuse control remain |

**Wrong AI recommendation:**  
It cannot execute. Human sees packet + engines. Explainer is optional. Override is “do not authorize” — there is no execute to undo. If a human later isolates out-of-band, that is **outside this API** and must be recorded in their own OT change process (not implemented here).

**Critical service unavailable:**  
No live downstream OT. If API/UI is down, plant control is unchanged. If a *future* historian feed drops, fail to UNKNOWN/ABSTAIN, not to last-good isolate.

---

### B6. Human-in-the-loop

**Where the human enters:**  
Context bar (plant / asset / alert / scenario) → reading five boards → **Recommendation Gate** (`Request draft packet`) → reading dual-column SOC vs PE → **not** pressing Execute (control does not exist). Named authorize is OPEN-001.

**What they see before any approval:**  
Identity bundle, contextual risk factors, safety conflicts (bypass_authorized), recovery blockers, Q5/Q3 graph, untrusted handover, authority catalog, packet fields: recommendation, execute=false, safe_state, required_roles, evidence[].

**Can they override? How recorded?**  
They can ignore a draft (no execute to override). A future Authorize click is **disabled**. Decision traces record the draft; they do not pretend a named human signed (OPEN-001). We do not invent an Authorizer.

**Always require human authorization:**  
Tier 3 isolate_endpoint / remote-access / firewall change. Tier 4 is refuse, not “authorize in app.” SIS and interlock changes are never in-app.

---

### B7. Auditability and traceability

**Six months later, “why this decision?”**  
Reconstruct from: `GET /audit/traces`, packet `packet_id`, `policy_version=policy.py:ACTION_TIERS`, evidence[] source_path + record_id, scenario binding, eval case id (EVAL-007 for CASCADE). TRACEABILITY.csv maps FR → engine → eval.

**Data, model, rules, prompts, tools, approvals, actions:**  
Yes for rules/tools/actions (`authority.catalog`, traces.tool_calls, prompt file `config/prompts/incident_analyst_v1.md`). Model/version: **no LLM vendor selected** (OPEN-028); AI off is the production-shaped default. Approvals: roles on packet, **person unbound** (OPEN-001).

**Log vs evidence-rich case history:**  
A log line “recommend called” is not enough. A case history keeps **who / as-of / policy / evidence rows / missing joins / UNTRUSTED citations / execute=false / workflow states**. That is `decision_trace.yaml` + provenance channels.

**Prove completeness / no silent loss:**  
Workshop: append-only JSONL traces, eval harness, SBOM freeze, CI (`make ci`). We do **not** claim WORM storage, legal hold, or signed audit in production (OPEN-029 no prod auth). Completeness of *estate evidence* is intentionally incomplete — missing joins are first-class so we cannot silently drop them.

---

### B8. Evaluation and business outcome

**Baseline:**  
The three `legacy_*` functions and the pre-engine diagnostics counts. XFAIL tests are the baseline we must beat without deleting them.

**Metrics that prove it is working (workshop):**

- Golden harness **EVAL-001…031** and red-team **A-01…A-10**  
- `execute=false` on every recommend  
- Identity: collisions not merged  
- Risk: reachable MIN_LOAD finding outranks unreachable CVSS 9.8  
- Safety: unauthorized bypass visible; UNKNOWN ≠ authorized  
- Recovery: CURRENT backup ≠ RecoveryReady  
- AI outage: tables still render  
- Ops: `GET /ops/slo`, `GET /ops/cost-per-incident` (FinOps design, not a live bill)

**Errors that matter most:**  
**False isolate / wrong-asset actuation** (false “positive” on containment) is worse than a missed LOW alert. Next: **false confidence** (UNKNOWN shown as NORMAL; email treated as policy). Latency matters only if the packet is still complete — dropping the safety join to go faster fails CTQ-ISO.

**Result that proves it is NOT working:**  
Any isolate-execute route; LLM re-rank as default; cleaned-away alias collisions; blank screen on AI outage; Authorize enabled without a named human; live PLC write “for demo.”

---

### B9. Production readiness

**If this went to production tomorrow — five biggest gaps**

1. **No live plant connectivity, no production auth** (OPEN-029).  
2. **Named Authorizer not implemented** (OPEN-001) — cannot close AwaitAuthorization honestly.  
3. **No LLM vendor / model port signed** (OPEN-028); explainer is optional and off.  
4. **Packet latency SLO baseline pending** (OPEN-006).  
5. **Handover / Unit 04 plant unbound** (OPEN-018); several clocks still dual (OPEN-021). Also: no external pentest, no EU AI Act claim, workshop-static freshness.

This is a **synthetic advisory increment**, not a live-plant go-live (`ops/production_readiness_checklist.md`).

**How we would monitor:**  
`/health`, `/ops/slo`, traces (tokens, latency_ms, policy_gate), eval harness on change, drift process (`ops/drift_management.md`), quality flags on telemetry. Business outcome in production would be: isolate-execute rate from *this* tool = 0; PE/Safety dissent visible on HIGH contain drafts.

**Alert that requires someone to act immediately:**  
In **this** product: unauthorized barrier bypass **plus** HIGH/CRITICAL with UNKNOWN process context (do **not** isolate from the app — call PE/Safety). In a future live deploy: API health fail is an *IT* page, not a plant trip.

**Who operates off-hours?**  
Workshop RACI: FDE + OT Security + Safety (unnamed). `ops/RACI.md`, `ops/runbooks.md`, `ops/ai_incident_response.md`. No 24×7 NOC is staffed in this repo.

---

### B10. FDE judgment

**Assumption most likely wrong:**  
That operators will treat “draft + UNTRUSTED + execute=false” as enough, and will not demand a green isolate button under SOC time pressure. Second: that CMDB names match observed assets often enough for Q5 to be the daily path (they do not — 200 state conflicts, 5 alias collisions).

**If I had production access for 24 hours I would investigate first:**  
(1) How often HIGH alerts have `process_context=UNKNOWN`. (2) Which isolate tickets last month hit units already on bypass or MIN_LOAD. (3) Whether historian ingest_time vs event_time inversions match the 407 enterprise-event inversions. (4) Whether the night-shift “Unit 04” mailbox can be bound to a plant without guessing (OPEN-018).

**If technically correct but operationally unusable:**  
Fewer screens, plant-first boards (already the estate/safety pattern), hop-capped graphs only, no gold CASCADE defaults leaking into the wrong plant (Q5 still defaults OT-01016 / ALT-002783 — a known workshop gold-slice), and a one-page packet. Do **not** “fix usability” by executing isolate.

**Smallest production-ready version to prove value safely:**  
Read-only replica of **identity conflicts + contextual risk + safety bypass board + recommend draft with execute=false**, AI off, no OT connectors, eval harness in CI. That is enough to show “we would have stopped the 08:47 isolate.” Do not start with an agent.

---

## C. Final 5-minute review

| Prompt | Answer |
|---|---|
| **Customer problem (one sentence)** | High-severity cyber labels on a messy OT estate are not a license to isolate — operators need an evidence-cited draft that keeps safety, process, and identity visible and never writes the plant. |
| **Most important decision supported** | **Do not execute isolation** (monitor / abstain / do-not-isolate / isolate-draft only) for this asset/alert given safe-state, barriers, and identity. |
| **Most dangerous failure mode** | The product (or an operator trusting it) isolates the wrong or unprotected unit — software becoming the incident. |
| **Human approval / override boundary** | Tier 3+ is human-only; tier 4 refused; Authorize disabled (OPEN-001); **no execute API**. |
| **Evidence it is ready for the next stage** | Repo 3.0 engines + APP UI; golden EVAL-001…031 and red-team in CI; `execute=false`; AI-off path; ADRs A+B (not C); remaining OPEN items documented rather than hidden. Next stage is **governed read-only pilot**, not live actuation. |

---

## Reviewer quick check (how this capstone maps)

| Dimension | What this repo does | Warning we avoided |
|---|---|---|
| Problem | CASCADE 08:47 vs 08:50; five truths ≠ one CVSS | Did not start with “add an LLM” |
| AI fit | Option A engines + optional explainer; Option C rejected | AI is not in the trip path |
| Data | Contradictions kept; UNKNOWN stays UNKNOWN | Did not clean `data/` |
| Failure | AI-outage, injection, no-write tests | Not happy-path-only |
| Human control | ACTION_TIERS; OPEN-001 explicit | HITL is not a slogan |
| Evidence | Traces + evidence[] + provenance channels | Not “just app logs” |
| Evaluation | Legacy baseline + EVAL/red-team | Not accuracy-only |
| Production | ops pack + honest OPEN gaps | Not claimed live-ready |
| Security | Read-only API, guardrails, refuse tier 4 | Agent is not trusted to write |
| FDE mindset | Investigate joins, authority, clocks | Implementation is constrained by ADRs |

---

## Key repo pointers

| Topic | Where |
|---|---|
| Problem / personas / tiers | `specs/PRD.md` |
| Safety vs isolate | `adrs/ADR-04-safety-policy.md`, `src/ot_command/core/containment.py` |
| Autonomy | `adrs/ADR-14-autonomy.md`, `src/ot_command/core/policy.py` |
| AI off | `adrs/ADR-12-ai-disabled.md` |
| Risk ≠ CVSS | `adrs/ADR-03-contextual-risk.md` |
| Untrusted notes | `adrs/ADR-06-retrieval-mix.md`, `data/shadow/shift_handover_email.txt` |
| Architecture | `specs/as_built_c4.md` |
| Evals | `evals/`, `assurance/ASSURANCE_REPORT.md` |
| Ops / RACI | `ops/` |
| OPEN items | `traceability/OPEN_DECISIONS.md` |

---

*This document is a direction-check worksheet fill, not a new ADR and not a production CAB sign-off.*
