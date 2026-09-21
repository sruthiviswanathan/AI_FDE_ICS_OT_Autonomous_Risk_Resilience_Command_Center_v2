# REL-03 — Benefits, variance, leakage, TCO

**Before snapshot:** `VERIFICATION.md` + SDD-04 §6 (workshop date 2026-09-15, seed `20260910`).  
**After snapshot:** modern engines + Command Center as of Repo 3.0 / app / REL-02 — **same bronze files**.  
**Rule:** inventory/telemetry/safety **counts stay**. What moved is **decision quality and visibility**. Plant MTT and $ are **BASELINE_PENDING** (OPEN-006). Do not fabricate outcomes.

Value hypothesis (SDD-04): value is **unsafe-recommendation avoided**, **time-to-justified-confidence** (when measurable), and **disagreement inspectable** — not dashboard count or isolate speed.

---

## 1. Before / after KPI table

| KPI (`docs/05`) | Before | After (this repo) | Variance | Honest limitation |
|-----------------|--------|-------------------|----------|-------------------|
| Asset inventory disagreement | **200** / 2016 (9.92%) | **200** — still queryable | **0 count** (intended) | CTQ-ID: drop would be a **fail** |
| Alias collisions | **5** | **5** visible; no CMDB winner | 0 | EVAL-001 |
| Unknown/unowned (`owner=Unknown`) | **343** (17.01%) | **343** | 0 | Do not fill with a default team |
| Telemetry BAD/UNCERTAIN | **4094** / 31224 (13.11%) | **4094**; quality flags remain | 0 | No BAD→GOOD imputation |
| Undocumented paths | **779** | **779**; hop cap 8 on graphs | 0 | Not a rank bug |
| Safety not ACTIVE | **61** / 450 | **61**; bypass shown; UNKNOWN ≠ YES | 0 | Aging clock still pending |
| Unapproved remote sessions | **137** / 700 | **137** shown; no VPN kill | 0 | Display ≠ containment |
| MFA not confirmed | **128** | **128** | 0 | |
| Backup not CURRENT | **25** / 144 | **25** | 0 | Diagnostics still this integer |
| CURRENT but not RecoveryReady | **113 / 119** | Predicate now **false** without restore∧runbook∧deps | **Decision** changed; row counts kept | EVAL-005; PLT-01 IDENTITY 360d |
| Legacy HIGH/CRIT → ISOLATE strings | **860** (525 context UNKNOWN) | Modern packet **not** safety-blind ISOLATE; `execute=false` | Unsafe isolate **withheld** on eval fixtures | 860 strings remain in bronze |
| Unsafe-isolation joins | **32** mined | Draft ≠ execute on those joins (EVAL-003) | Upper bound of **interest**, not a $ saving | |
| Remote approval compliance | 563/700 (80.4%) | Unchanged records | 0 | UNKNOWN counted non-compliant |
| Runbook CURRENT | 109/144 (75.7%) | Unchanged; CURRENT ≠ tested | 0 | |
| Restore-test freshness | p50 **376d**; >180d **114** | Used in RecoveryReady | Visibility | 180d is **workshop** bar, not OPEN-022 close |
| Stale config proxy | 1581/2016 `backup_age_days>90` | Unchanged | 0 | Official formula BASELINE_PENDING |
| MTT contextualize | BASELINE_PENDING | Still **unmeasured** | — | OPEN-006 |
| Alerts per actionable incident | BASELINE_PENDING | Still undefined incident object | — | OPEN-012 |
| Safety-bypass **aging** | Count 61; aging pending | Count unchanged | — | No bypass timestamp |
| Vuln-to-process coverage | Limited; 182/2016 tagged | Contextual rank uses joins when present | Not a diagnostic | OPEN-020 |
| Time to confidence / safe containment rec / degraded duration / FP escalation / approval latency | BASELINE_PENDING | Tabletop stopwatch **not yet run** | — | Do not invent minutes |
| Decision evidence completeness | **0%** of `/diagnostics` ints | Packets carry evidence, impact, authority **roles**, `execute=false` | **Structural complete** on `POST /recommend` | Completeness ≠ named approval |
| AI cost per analyzed incident | No meter | Meter **exists**; tokens **0** at default | $ **not claimed** | OPEN-006 / OPEN-028 |

Related after (not in docs/05 list): SLO-OT OK; SLO-EVAL 31/31; red team 17/17; CASCADE wall ~132 ms / 7 tools (workshop hardware, not a plant SLA).

---

## 2. Variance (what actually moved)

| Moved | Did not move |
|-------|----------------|
| Default rank is contextual (EVAL-002/017) | 14 diagnostic integers |
| Isolation draft CTQ-ISO fields; CASCADE ≠ bare ISOLATE | `legacy_*` behavior (XFAIL kept) |
| RecoveryReady ≠ CURRENT | Bronze contradictions |
| AI-disabled path usable | Named Authorizer (OPEN-001) |
| Traces + cost/SLO endpoints | Live OT, plant MTT, legal class |

**DMAIC Improve (C14):** we changed the **decision path** (RC-C/D), not the messy inputs (RC-A symptoms stay visible). Control charts for plant outcomes are **not** this repo.

---

## 3. Value leakage (named)

A “win” on the left that is actually a loss.

| Leakage name | Bad win | Why it leaks | Already a temptation |
|--------------|---------|--------------|----------------------|
| **Rank-speed leakage** | Lower latency by skipping safety/process joins | Uncertainty hidden; EVAL-002 fails | EVAL-026 disqualifies the shortcut |
| **Alert-volume leakage** | Fewer tickets / more SUPPRESSED HIGH | Bypass and MIN_LOAD never reviewed | 211 HIGH+CRIT already SUPPRESSED (OPEN-017) |
| **Inventory-clean leakage** | Disagreement rate ↓ by deleting aliases/shadow | Forensic problem disappears; CTQ-ID fail | 5 collisions; OPEN-015 |
| **Backup-badge leakage** | CURRENT % ↑ | Restore-test still stale | 113/119 CURRENT lies |
| **Isolate-throughput leakage** | More or faster ISOLATE drafts | Process trips / MIN_LOAD destabilization | 860 strings; 32 unsafe joins |
| **Owner-fill leakage** | Unknown owner → default team | Authority faked | 343 Unknown; 41 tracker Unknown |
| **Caption-authority leakage** | Moonshot/caption treated as control | Automation bias | ADR-13; banner NOT A CONTROL ACTION |
| **SLO-OT leakage** | “Plant healthy” because SLO-OT OK | Confuses product CTQ with process state | Header badge |
| **Twin-promote leakage** | Green lab `isolate_preview` → plant | CASCADE is UNSAFE_ISOLATION | Twin is `lab_result` only |

**Explicit failures (SDD-04):** faster isolate that increases process trips = failure. Cleaner inventory that hides aliases = failure.

---

## 4. Counter-metrics (dashboard fields that must not be gamed)

| Counter | Direction that is a **fail** if it “improves” |
|---------|-----------------------------------------------|
| Time to isolation **execute** / raw ISOLATE rate | Down (faster) |
| Inventory disagreement rate via deletes | Down |
| Alert volume without bypass review | Down |
| Backup CURRENT % without restore | Up |
| Mean time to contextualize via skipped joins | Down |
| AI incidents processed (CVSS-sorted) | Up |
| `traces_execute_true` | Any > 0 |
| `moonshot_execute_clicks` | Any > 0 |
| Missed bypass detections | Up |
| Diagnostics counters vs VERIFICATION.md | Collapse |

Adoption counters that **may** rise and still be healthy: SOC disagreement with isolate on CASCADE (engines ABSTAIN). See `ops/adoption.md` §12.

---

## 5. Waste vs SDD-02 register (Improve, not a plant kaizen)

| Waste | Root or symptom (SDD-04) | After (software) |
|-------|--------------------------|------------------|
| W1 Waiting on identity | Root RC-A | Conflicts **queryable**; no CMDB winner. Wait remains if humans skip Identity page |
| W2 Extra processing CVSS-only | Root RC-C | Default contextual rank; CVSS-only is a **warn** mode |
| W3 Telemetry/CMMS defects | Symptom | Flags remain; not imputed |
| W4 Unused PE/safety expertise | Root RC-B/D | Packet lists roles; Authorize still disabled (OPEN-001) |
| W5 Handoffs / tribal email | Symptom RC-E | Traces exist; email stays UNTRUSTED |
| W6 Overproduction of ISOLATE | Symptom RC-C | Modern path withholds unsafe isolate on evals; 860 bronze strings **kept** |
| W7 Undocumented paths | Exposure | Drawn with hop cap; no regional isolate control |
| W8 Defective recovery processing | Root RC-C | RecoveryReady predicate |
| W9 Waiting on vendor | Symptom | Sessions visible; no auto-disable |
| W10 Duplicate contracts / unused policy | Root RC-D | ACTION_TIERS applied to recommend; unused execute tools **not added** |
| W11 Shadow vs spreadsheet | UU | Overlay; do not pick a winner |

---

## 6. TCO and cost-to-value (workshop)

Assumptions from SDD-09: one FDE; local/synthetic host; no production IAM; LLM off or none; 90-day **workshop** already spent on this repo; harm of unsafe isolate **not monetized** (intolerable, not a line item). **No plant $.**

| Element | Status-quo war room | Advisory CC (as-built A+B) | Unsafe agent (rejected) |
|---------|---------------------|----------------------------|-------------------------|
| Software | `/diagnostics` 14 ints | Engines + evals + UI in this repo | Unbounded review/legal |
| Human time | High rework on identity + unused PE | Joins cut **re-work of the wrong answer**; HITL remains | Fake-low then incident |
| Tokens | 0 | **0** default (`provider=none`) | Tool loops |
| TEVV | 3 XFAIL only | 31/31 + 17/17 red team | Cannot ship |
| Residual harm | Wrong advice, no write path | OPEN-RISK-11 (UI isolate pressure) — execute still absent | **Intolerable** |

**Cost-to-value (qualitative):** value = avoided unsafe isolate on CASCADE-class mornings + visible disagreement. Cost = FDE-weeks already in repo + **$0** model on default deploy. A hosted model is optional later (OPEN-028) and is **disqualified** if it wins EVAL-002 by omitting joins.

Buy a GRC/OT-cyber dashboard: **rejected for this estate** unless the same engines are still built. Partner SIEM isolate-execute: **rejected**.

---

## 7. Cost per successful outcome

**Name:** AI cost per analyzed incident / avoided escalation (`docs/05`).

| Piece | Workshop definition | Number |
|-------|---------------------|--------|
| Successful outcome | Packet (or harness case) that meets EVAL must_include **or** HIGH/CRIT where legacy would ISOLATE **and** join is MIN_LOAD / non-ACTIVE barrier **and** draft `execute=false` | Denominator = eval cases + tabletop packets; **not** raw 2800 alerts |
| Avoided escalation (narrow) | Those 32 unsafe-join candidates are an **upper bound of interest** | **Not** a claimed saving of 32 events |
| Cost numerator | Tokens × unit cost + attributed analyst/FDE hours | Tokens **0**; hours **not metered**; unit cost **0.0** until OPEN-028 |
| Formula | `Cost_period / Successful_outcomes_period` | Currency **BASELINE_PENDING** |
| Counter | Do not optimize cost per **legacy ISOLATE emitted** | Would reward W6 |

Until leadership times a tabletop and optionally pins a model, report: **meters exist, dollars do not.**

API: `GET /ops/cost-per-incident` · `GET /ops/slo`.

---

## 8. Unintended effects (watch list)

- Operators treat Authorize-disabled as “the system already approved.”  
- Executive persona never sees Moonshot — good — but may infer the SOC view is “the AI.”  
- Hop cap 8 hides longer cascades (correct bound, incomplete graph).  
- Persona filter is not authorization (OPEN-029).  
- Render demo is unauthenticated — not a production release.

---

## 9. Realisation verdict

| Claim | Status |
|-------|--------|
| Benefits realisation (workshop decision quality) | **Evidenced** on eval fixtures + UI packet |
| Plant outcome realisation (MTT, $) | **Gap** — OPEN-006 |
| Scale advisory | **Recommended** |
| Scale execute | **Not realised; not recommended** |
