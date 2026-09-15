# SDD-04 — SCQA problem frame, root cause, value

**Prompt:** SDD-04 | OM-3 Problem, root cause, value  
**Depends on:** SDD-01 CHARTER, SDD-02 CURRENT_STATE, SDD-03 matrix/top15 (present)  
**Date:** 2026-09-15  
**FDE capabilities evidenced (OM 3 homes):** C03, C05, C07, C12, C13, C14 Analyse, C55 (criteria design; measurement is OM 19)  
**Not this prompt:** use-case go/no-go (SDD-05); architecture (SDD-09); agents; KG/RAG.

---

## Evidence used / assumptions / unknowns / what this artifact did not conclude

### Evidence used (file / field / count / id)

| Source | Used as |
|---|---|
| `docs/05_kpis_baseline.md` | 18 named KPIs |
| `VERIFICATION.md` | 200, 5, 779, 120, 4094, 47, 61, 73, 244, 137, 128, 25, 29, 35; 3 passed / 3 xfailed |
| SDD-03 `matrix.csv` / `top15.md` | Cell IDs; traces OT-00211, OT-01016, OT-00528; EVAL-001…006 |
| SDD-02 waste W1–W11 | DMAIC Analyse |
| SDD-01 CHARTER §1–3 | Client vs FDE ask; five states |
| `data/manifest.json` | 18 plants; 2016 assets; 31224 telemetry; 2800 alerts; 144 recovery |
| `src/ot_command/legacy/risk.py` | CVSS rank; backup flag; safety-blind isolate |
| `src/ot_command/core/policy.py` | ACTION_TIERS unused by isolate |
| `docs/06_security_safety_assurance.md` | Recommendation quality bar; forbidden writes |

### Assumptions

1. VERIFICATION.md counts remain the before-intervention snapshot.
2. Workshop CTQ tolerances in §7 are **this prompt’s stated workshop bars**, not a named-sponsor signature (OPEN-001).
3. Tag→unit join covers **182/2016** assets (OPEN-020); process-impact KPIs are subset-limited.
4. No architecture is implied by “truth layer” or “decisioning” — those are problem outcomes, not product choices.

### Unknowns

OPEN-001 named humans; OPEN-006 unmeasured clocks/cost; OPEN-012 case key; OPEN-018 Unit 04 plant; OPEN-020 tag coverage; “actionable incident” still undefined.

### What this artifact did not conclude

- Did not select KG, RAG, digital twin, agents, or a vendor model.
- Did not rank sites or CVSS as operational priority.
- Did not set production plant thresholds beyond workshop CTQs given in the prompt.
- Did not close eval gates (SDD-08) or use-case go/no-go (SDD-05).

---

## 1. Situation (C03)

The fictional company operates **18** industrial sites across five regions (`plants.csv`: NA/EU/APAC 4, LATAM/MEA 3) with mixed-generation OT labels (PLC/DCS/SCADA/HMI/historian/SIS/CMMS/SOC/vendor access — `docs/01_domain_context.md`).

Leadership asked for a global **autonomous risk and resilience command center** (`participant/CHALLENGE_BRIEF.md`). The estate already produces many dashboards and **2800** cyber alerts, **6500** enterprise events, **14** diagnostic integers, and a FastAPI `/diagnostics` — and still has **no trusted cyber-physical truth**.

Five statements that must stay distinct: **observed**, **registered**, **operational interpretation**, **safety**, **decision authority** (SDD-01). Forensic tension: cyber state ≠ operational state ≠ safety state ≠ resilience state (`README.md`).

Grain (manifest seed `20260910`): 2016 assets, 216 process units, 450 safety barriers, 144 recovery rows. Synthetic workshop; not live plant control (`README.md`).

---

## 2. Complication — symptoms vs root causes (C07)

Quantify symptoms first (`VERIFICATION.md` unless noted):

| Symptom (what leadership feels) | Count | Cell IDs |
|---|---|---|
| Asset registered ACTIVE vs observed OFFLINE/UNSEEN | **200** / 2016 = 9.92% | L4-Inconsistency |
| Undocumented ∩ observed-24h network paths | **779** / 3780 | L2-Friction |
| Telemetry BAD or UNCERTAIN | **4094** / 31224 = 13.11% | L3-Imperfection |
| Alias collisions | **5** | L4-Inconsistency, EVAL-001 |
| Safety barriers not ACTIVE | **61** / 450 | L7-Imperfection |
| Proof-test not CURRENT | **73** / 450 | L7-Volatility |
| CMMS CLOSED ≠ field RETURNED_TO_SERVICE | **244** / 1250 | L8-Inconsistency |
| Unapproved remote sessions | **137** / 700 | L6-Uncertainty |
| MFA not confirmed | **128** / 700 | L6-Uncertainty |
| Backup flag not CURRENT | **25** / 144 | L10-Imperfection |
| CURRENT backup that is still not recovery-ready | **113 / 119** (SDD-03; restore/runbook/dep) | L10-Inconsistency, EVAL-005 |
| HIGH+CRITICAL alerts that legacy would **ISOLATE** | **860** (525 process_context UNKNOWN) | L11-Imperfection, L6-Friction |
| Unsafe-isolation join (MIN_LOAD or non-ACTIVE barrier) | **32** alerts (18 MIN_LOAD) | EVAL-003 |
| Empty enterprise `correlation_id` | **3251 / 6500** | L9-Inconsistency |

**Three encoded policies** turn those disagreements into **wrong decisions** (`risk.py`; 3 XFAIL):

1. `legacy_rank` sorts **CVSS alone** (EVAL-002: VUL-00706 cvss 9.8 reachable NO LOW vs OT-01016 VUL-00098 cvss 8.7 reachable YES MIN_LOAD).
2. `legacy_isolation_recommendation` returns **ISOLATE** for HIGH/CRITICAL with no safe-state or role (CASCADE-001 08:47 vs 08:50; handover min stable load).
3. `legacy_recovery_ready` is true iff `backup_status == CURRENT` (PLT-01 IDENTITY CURRENT, restore **360** days, runbook STALE).

### Root causes (not “lack of AI”)

| ID | Root cause | Evidence | Not a root cause (symptom) |
|---|---|---|---|
| RC-A | **No identity object** that keeps five states separate and aliases non-unique | L4-Inconsistency; 200 conflicts; 5 collisions; 99 RETIRED∩ONLINE (OT-00528); 182/2016 tagged | “We need another CMDB dashboard” |
| RC-B | **No process/safety join** on the decision path | L5-Friction; L7-Friction; diagnostics does not read `process_units` / `safety_barriers` / `cyber_alerts` | 4094 dirty tags (quality defect, not the isolate bug) |
| RC-C | **Decision policy hard-codes the wrong question** (score, isolate, ready) | L1-Imperfection; W2; W4; W8 | 860 ISOLATE strings (output of RC-C) |
| RC-D | **Authority exists as a dict and is not applied** | L1-Hidden Dependency; L12-Inconsistency; `ACTION_TIERS` isolate_endpoint=3 unused | Unnamed humans (OPEN-001) are a **gap**, not the code defect |
| RC-E | **No case / uncertainty / evidence package** for a governed recommendation | L9 empty correlation; L11 no uncertainty object; `/diagnostics` ints only; EVAL stubs | Alert volume 2800 (load, not cause of safety-blind rule) |

Five states disagree **because RC-A/B**. Wrong recommendations **because RC-C/D**. Autonomy would **scale RC-C** (L12-Imperfection).

---

## 3. Question (one sentence)

Can we establish trustworthy, safety-bounded, authority-aware risk and resilience **decisioning** — with disagreements visible, isolation drafts gated by safety-state and named role, and recovery judged on restore-test + runbook + dependencies — **before any autonomy is switched on**?

---

## 4. Client ask vs FDE ask vs 90-day vs 12-month vs moonshot

Moonshot is **not** autonomous isolation.

| Horizon | Statement | Evidence / bound |
|---|---|---|
| **Exact client ask** | Global **autonomous** risk and resilience command center | CHALLENGE_BRIEF; docs/01 |
| **Real FDE ask** | Trusted cyber-physical **decision support**: visible disagreement, contextual risk (not CVSS-only), safety-aware recommendations, proven recovery, HITL for tier ≥3, evals before agents | SDD-01 mandate; docs/06; AGENTS.md |
| **90-day target (workshop)** | Freeze baseline; keep contradictions; ship **visibility** of the 200/779/4094/61/244/137 gaps; isolation **drafts** 100% show `safe_state` + required role; recovery **drafts** never equal CURRENT-only; 0 PLC-write paths; EVAL-001…006 specified (not necessarily all green on a modern path yet); **no** agent enablement | This SCQA CTQs; SDD-03 packs; Phase 0 3 pass / 3 xfail **preserved** |
| **12-month target** | A **governed recommendation** path that can outrank high CVSS with process/safety/recovery context; identity conflicts remain **visible** (not cleaned); restore-test+runbook+deps required for “ready”; named-role HITL on consequential drafts; eval gates in CI on the **modern** path; legacy `legacy_*` still comparable | Challenge-brief deliverable list minus live OT; SDD-08/ENH later — **no tech pick here** |
| **Earned moonshot** | Command-center **speed** with trustworthy joins and authority-aware advice that operators will use without automation bias — still **advisory**. Earned only after CTQs hold. | docs/06 recommendation bar |
| **Not the moonshot** | Autonomous isolation, PLC/SIS/interlock writes, trip suppression, silent inventory cleanup | docs/06; L12-Complexity |

---

## 5. Causal chain (C07)

```text
Leadership wants autonomy
        |
        v
No single cyber-physical truth (Situation)
        |
        +-- RC-A identity/states/aliases not reconcilable
        |      --> 200 conflicts, 5 collisions, 343 owner Unknown
        |      --> wrong asset in any downstream decision
        +-- RC-B process/safety/recovery not on the path
        |      --> 1834/2016 untagged; 525/860 high alerts context UNKNOWN
        |      --> 32 unsafe isolate joins hidden from code
        +-- RC-C hard-coded policy (CVSS / HIGH=ISOLATE / CURRENT=ready)
        |      --> XFAIL trio; VUL-00706 outranks OT-01016; 113 CURRENT lies
        +-- RC-D ACTION_TIERS unused; no named approver
        |      --> recommend-time ISOLATE without approval
        +-- RC-E no case key, no uncertainty object, stub evals
               --> 3251 empty correlation_id; /diagnostics ints; EVAL jsonl unused
        |
        v
SOC and process engineering argue (CASCADE 08:47 vs 08:50)
        |
        v
Autonomy now would scale unsafe recommendations  (stop condition)
```

### Five Whys (isolate example — EVAL-003)

1. Why might a unit trip? SOC isolation draft on HIGH (`legacy_isolation_recommendation`).
2. Why did software say ISOLATE? Severity ∈ {HIGH, CRITICAL} only (RC-C).
3. Why was safe-state ignored? `process_units.safe_state` unread (RC-B); 54 MIN_LOAD units.
4. Why was a bypassed barrier ignored? `safety_barriers` unread (L7-Friction); e.g. PLT-03-SAFE-14 authorized NO.
5. Why no human gate? `requires_human_approval` not called (RC-D); OPEN-001 unnamed.

Root: **policy + missing join + unwired authority**, not “need an LLM.”

### Five Whys (recovery example — EVAL-005)

1. Why is leadership told “ready”? `legacy_recovery_ready("CURRENT")` is True.
2. Why is that false for PLT-01 IDENTITY? restore 360d, runbook STALE.
3. Why doesn’t diagnostics catch it? It counts backup ≠ CURRENT only (25), not restore days (L10-Friction).
4. Why was the function written that way? Hard-coded flag (RC-C).
5. Why would AI make it worse? It would cite the boolean as evidence (naive-AI in L10-Inconsistency).

---

## 6. Baseline dataset — each `docs/05` KPI (C05)

Use VERIFICATION.md where the diagnostic matches the named KPI. Workshop snapshot date: 2026-09-15. Population is synthetic seed `20260910`.

| KPI | Formula (as-is / working) | Source | Population | Snapshot | Limitation |
|---|---|---|---|---|---|
| Asset inventory disagreement rate | `registered_state=ACTIVE` AND `observed_state∈{OFFLINE,UNSEEN}` / N assets | `assets.csv`; diagnostics `asset_state_conflicts` | 2016 | **200 (9.92%)** VERIFICATION | Omits alias collisions (5), RETIRED∩ONLINE (99), shadow |
| Unknown/unowned asset rate | `owner=Unknown` / N | `assets.owner` | 2016 | **343 (17.01%)** | Label ≠ proven unowned; empty owner = 0 |
| Telemetry bad/uncertain quality rate | `quality ≠ GOOD` / N events | `tag_telemetry.jsonl`; `telemetry_bad_or_uncertain` | 31224 | **4094 (13.11%)** VERIFICATION | Extra: 120 dups; 47 TEMP≠C |
| Stale configuration rate | **No catalogue formula.** Proxy only: `backup_age_days > 90` / N | `assets.backup_age_days` | 2016 | Proxy **1581 (78.4%)**; official **BASELINE_PENDING** | N=90 not in docs/05 (OPEN-022) |
| Mean time to contextualize an OT alert | time from `cyber_alerts.timestamp` to first package with identity+process+safety+uncertainty | no clock in product | 2800 alerts | **BASELINE_PENDING** | 525/860 HIGH+CRIT already context UNKNOWN |
| Alerts per actionable incident | N alerts / N incidents meeting evidence bar | `cyber_alerts.csv` | 2800 | **BASELINE_PENDING** (OPEN-006) | “Actionable” undefined; 1735/2800 process_context UNKNOWN |
| Safety-bypass aging | days since bypass (need a date field) | `safety_barriers.csv` | 450 | **Count 61** not ACTIVE (VERIFICATION); **aging BASELINE_PENDING** | No bypass timestamp; 157 authorized UNKNOWN |
| Vulnerability-to-process-impact coverage | findings with unit_id + production_criticality + reachable + barrier state / 1100 | `vulnerabilities.csv` ⋈ `tags.csv` | 1100 | **Not a diagnostic.** Tagged assets only **182/2016** (OPEN-020) | Most vulns `units=[]` |
| Remote-session approval compliance | `approved_window=YES` / 700 | `remote_access_sessions.csv`; unapproved **137** VERIFICATION | 700 | **563 (80.4%)** | UNKNOWN 76 counted non-compliant |
| Restore-test freshness | share with `last_restore_test_days` ≤ workshop bar **or** report distribution | `recovery_readiness.csv` | 144 | p50 **376 d**; >180d **114**; **not** in diagnostics | Legacy ignores field; bar not in docs/05 |
| Recovery runbook completeness | `runbook_status=CURRENT` / 144 | same; VERIFICATION **35** not CURRENT | 144 | **109 (75.7%)** | CURRENT ≠ tested |
| Time to cyber-physical incident confidence | clock to evidence-complete package | none | — | **BASELINE_PENDING** | No case id (OPEN-012) |
| Time to safe containment recommendation | clock to draft with safe_state+role (not execute) | none; isolate is safety-blind | 860 ISOLATE strings | **BASELINE_PENDING** | Must not optimize “time to ISOLATE” |
| Degraded-operation duration | dwell in DEGRADED/bypass | none | — | **BASELINE_PENDING** | WO field DEGRADED 313 is a count not a duration |
| False-positive escalation rate | escalations that fail EVAL-002/003 / escalations | none | — | **BASELINE_PENDING** | 211 HIGH+CRIT already SUPPRESSED (OPEN-017) |
| Decision evidence completeness | share of drafts with docs/06 fields: evidence, freshness, uncertainty, process, safety, rollback, authority | API emits none of these | — | **0% of API outputs** (working) | `/diagnostics` ints only |
| Human approval latency for consequential actions | time from draft to named approval for tier ≥3 | none; no named humans | — | **BASELINE_PENDING** | OPEN-001 |
| AI cost per analyzed incident / avoided escalation | see §12 | none | — | **BASELINE_PENDING** | No FinOps meter |

Related VERIFICATION measures **not** named in docs/05 but part of the baseline snapshot: alias_collisions **5**; undocumented_network_paths **779**; duplicate_telemetry_packets **120**; telemetry_unit_mismatches **47**; recovery_unverified_dependencies **29**.

---

## 7. KPI tree and CTQs (C12, C13)

```text
Value: unsafe-recommendation avoided + time-to-confidence reduced
        + disagreement made visible (not hidden)
   |
   +-- Safety / authority CTQs (hard)
   |     0 PLC-write paths
   |     0 SIS / setpoint / interlock / trip-suppression paths
   |     100% isolation DRAFTS show safety-state + required role
   |     Isolation EXECUTE = 0 in this repo
   |
   +-- Truth CTQs
   |     Identity conflicts VISIBLE (do not hide aliases)
   |     Five states not collapsed
   |     Telemetry quality + event vs ingest shown
   |
   +-- Recovery CTQ
   |     "Ready" requires restore-test AND runbook AND deps
   |     (CURRENT backup alone is failure)
   |
   +-- Risk CTQ
         Contextual rank can outrank highest CVSS (EVAL-002)
```

### Workshop CTQ tolerances (prompt-specified; not plant-signed)

| ID | CTQ | Tolerance (workshop) | Today | Counter if gamed |
|---|---|---|---|---|
| CTQ-0 | PLC-write / SIS / setpoint / interlock paths | **0** routes | **0** in `api.py` | Adding a write “behind a flag” = fail |
| CTQ-ISO | Isolation **drafts** show `safe_state` + required role | **100%** | **0%** (`legacy_isolation_recommendation` has neither) | Drafts that omit role to go faster = fail |
| CTQ-ID | Identity conflicts visible | Conflicts remain queryable; aliases not deleted | 200 + 5 collisions visible | “Cleaner inventory” that drops collisions = fail |
| CTQ-REC | Recovery ready | restore-test + runbook + deps all required | 119 CURRENT would pass legacy; **113** fail the CTQ | Green backup badge = fail |
| CTQ-CVSS | Operational rank | Must include reachability, process, safety, controls, recovery | `legacy_rank` CVSS only | Sort cvss then sprinkle text = fail |

Tolerances for rates (9.92% disagreement, 13.11% dirty telemetry) are **not** set here — reducing them is value only if conflicts remain visible. Numeric improve targets wait SDD-08 / named owner.

---

## 8. Value hypothesis and assumptions (C12, C13)

**Hypothesis:** Value is created when the program **avoids unsafe recommendations**, **shortens time-to-justified confidence**, and **makes inventory/telemetry/safety/recovery disagreement inspectable** — not when dashboard count or isolate speed increases.

Assumptions (if false, hypothesis fails):

| A# | Assumption | Risk if false |
|---|---|---|
| A1 | Operators and SOC will use a slower, evidence-complete draft over a CRITICAL banner | Automation bias (CASCADE 08:47) |
| A2 | Process engineering and Safety remain in the isolation-draft path | W4 unused expertise continues |
| A3 | Contradictory records are preserved | Cleaning removes the problem (CTQ-ID) |
| A4 | Workshop synthetic metrics predict the **shape** of value, not live-plant dollars | OPEN-003 |
| A5 | Evals EVAL-001…006 are the definition of “successful analysis” | Cost metric has no denominator |
| A6 | No architecture is required to **state** this value | SDD-09 still required to pick how |

---

## 9. Counter-metrics (failure if they “improve” the wrong way)

| Counter-metric | Bad “win” | Evidence it is already a temptation |
|---|---|---|
| Time to isolation **execute** or raw ISOLATE rate | Faster isolate that increases process trips / MIN_LOAD destabilization | 860 ISOLATE strings; 32 unsafe joins; handover min load |
| Inventory disagreement rate | Cleaner CMDB that **hides** aliases/collisions/shadow | 5 collisions; OPEN-015 spreadsheet; EVAL-001 must_not CMDB always correct |
| Alert volume down | SUPPRESS HIGH/CRIT without safety review | 211 HIGH+CRIT SUPPRESSED (OPEN-017); ALT-002783 |
| Backup CURRENT % | More CURRENT flags without restore tests | 113/119 CURRENT lies |
| Mean time to contextualize | Skip safety/process join to go faster | 525/860 context UNKNOWN |
| AI incidents processed | High throughput of CVSS-sorted tickets | `legacy_rank` |
| Owner Unknown rate | Fill Unknown with a default team name | 343 Unknown; 41 tracker Unknown |

**Explicit failures named in the prompt:** faster isolate that increases process trips = failure; cleaner inventory that hides aliases = failure.

---

## 10. Success / failure / stop conditions (C55 design)

### Success (engagement, before autonomy)

- Question in §3 answered **yes** with evidence: drafts carry safety-state + role; recovery CTQ-REC holds on the modern path; identity conflicts remain visible; CTQ-0 holds; EVAL-001…006 are runnable specs.
- Baseline in §6 is the **before** snapshot; after-metrics come later (OM 19).
- Legacy XFAIL tests **still xfail** until a parallel function is proven (do not delete defects).

### Failure

- Ranking still CVSS-only on the path that operators see.
- Isolation still automatic or safety-blind.
- Data “cleaned.”
- Agent writes a control action (PLC/SIS/interlock/setpoint/trip suppression/unsafe isolate).
- Counter-metrics in §9 move “the right way” for a dashboard and the wrong way for the plant.

### Stop / kill (return to earlier OM or halt autonomy)

- Any PLC-write or SIS path appears in code.
- Isolation **execute** implemented.
- Named human authority still missing **and** software proceeds as if approved (OPEN-001 violated).
- Eval stubs treated as passing gates.
- Sponsor insists moonshot = autonomous isolation.

Go/no-go for **AI as a product** is SDD-05. This section is engagement success, not use-case classification.

---

## 11. DMAIC Analyse — SDD-02 wastes: root vs symptom (C14)

Define/Measure were SDD-02. Analyse maps wastes W1–W11 to RC-A…E.

| Waste | Root cause or symptom? | Mapping |
|---|---|---|
| W1 Waiting on identity | **Root (RC-A)** | 200 conflicts; 5 collisions; 343 Unknown |
| W2 Extra processing CVSS-only | **Root (RC-C)** | `legacy_rank` |
| W3 Defects (telemetry/CMMS/clocks) | **Symptom + contributor** | Dirty data worsens RC-B joins; does not create HIGH=ISOLATE |
| W4 Unused expertise | **Root (RC-B + RC-D)** | Process/safety unread; no HITL on isolate |
| W5 Handoffs / tribal | **Symptom of RC-A/E** | Email/spreadsheet/tracker because no case object |
| W6 Overproduction of ISOLATE | **Symptom of RC-C** | 860 strings |
| W7 Undocumented paths | **Contributor (exposure)** | 779; not the ranking bug |
| W8 Defective recovery processing | **Root (RC-C)** | CURRENT flag |
| W9 Waiting on vendor | **Symptom** | 224 awaiting vendor; 64 CLOSED |
| W10 Duplicate contracts / unused policy | **Root (RC-D)** | ACTION_TIERS unused; API v1/v2 |
| W11 Shadow email vs spreadsheet | **Symptom / UU** | OPEN-015; do not pick a winner |

Improve/Control are **not** this prompt (no solution selected).

---

## 12. Cost-per-successful-outcome metric design (C55)

KPI name (`docs/05`): **AI cost per analyzed incident / avoided escalation**.

**Baseline: BASELINE_PENDING** — no labor, token, or infra meter in the repo; `/diagnostics` has no cost field.

### Working design (not a number)

| Element | Definition | Workshop notes |
|---|---|---|
| Outcome (denominator, “successful”) | Count of **analyzed incidents** that meet EVAL-001…006 must_include **or** **avoided escalations**: isolation drafts that would have been ISOLATE under legacy but are withheld/rewritten because of safe-state/role (EVAL-003) | Do not use raw 2800 alerts as denominator |
| Avoided escalation (narrow) | HIGH/CRIT alert where legacy would ISOLATE **and** joined unit is MIN_LOAD or barrier not ACTIVE **and** draft ≠ execute | 32 mined candidates are the **upper bound of interest**, not a claimed saving |
| Cost (numerator) | FDE/analyst hours + compute/API cost attributed to those successful outcomes in a period | Unmetered today |
| Formula | `Cost_period / Successful_outcomes_period` | Dimension: currency or hours per outcome |
| Counter | Cost per **legacy ISOLATE emitted** must not be optimized | Would reward W6 |
| Limitation | No incident object (OPEN-012); no FinOps (OPEN-006) | Do not invent $ |

Until meters exist, report **BASELINE_PENDING** plus the structural counts above (860 legacy ISOLATE; 32 unsafe-join).

---

## OM-3 capability evidence

| ID | Capability | Where |
|---|---|---|
| C03 | Problem framing | §1–4 SCQA; qualification continues SDD-05 |
| C05 | Baseline KPIs before intervention | §6 |
| C07 | Root-cause analysis | §2, §5, cell IDs |
| C12 | Business-value engineering | §7–8, §10 |
| C13 | Benefits / value tree / counter-metrics | §7–9 |
| C14 | DMAIC Analyse | §11 (D/M in SDD-02) |
| C55 | Business-outcome evaluation (design) | §10, §12; measurement OM 19 |

---

## Gate (SDD-04)

| Criterion | Result |
|---|---|
| SCQA with one-sentence question | **PASS** §3 |
| Root causes ≠ symptoms; cell IDs cited | **PASS** RC-A…E |
| All 18 docs/05 KPIs have formula/source/population/limitation | **PASS** §6 |
| CTQs include 0 PLC-write, 100% isolation-draft safety+role, visible identity, restore+runbook+deps | **PASS** §7 |
| Counter-metrics include faster-isolate trips and hidden aliases | **PASS** §9 |
| No KG/RAG/agent as the answer | **PASS** |
| Moonshot ≠ autonomous isolation | **PASS** §4 |

**Output to next:** evidence-backed problem and baseline. SDD-05 may qualify whether AI is justified **per task**. SDD-05 must not invent a legal class or enable control actuation.
