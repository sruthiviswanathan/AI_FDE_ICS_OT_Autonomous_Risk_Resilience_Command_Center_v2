# REL-03 — 90-day ask

**Status:** forward roadmap after Repo 3.0 + app + REL-01/02 ops.  
**Does not reopen** SDD-09. Does not add ACTION_TIERS verbs, OT write APIs, or named Authorizers in software.  
**SDD-14 §15 seed (done):** days 1–30 truth engines · 31–60 evals/agent-advisory · 61–90 shadow ops. That workshop seed is **complete**. This file is the **next** 90 days for leadership.

Default recommendation: **scale advisory shadow; do not scale execution autonomy.**

---

## Hard gates (every week)

These are not plant SLAs (OPEN-006). They are ship gates.

| Gate | Hold |
|------|------|
| SLO-OT / SLO-CTQ0 | 0 execute; 0 new OT POST |
| SLO-EVAL | EVAL-001…031 = 31/31 |
| Red team | A-01…A-10 pass |
| CTQ-ID | diagnostics counters must not collapse |
| AI-disabled | `ai_outage` / `AI_ENABLED=0` still usable (EVAL-016) |
| Autonomy ceiling | recommend only until REL-04 review (`ops/adoption.md` §4) |

**Moonshot** (forecast UI, `execute=false`) may stay visible to Full/FDE/SOC **only while** those gates hold. If any gate fails: `ai=off`, Moonshot hidden, engines stay.

---

## Days 1–30 — Scale the advisory, not the plant

| Work | Output | Not this month |
|------|--------|----------------|
| Nightly shadow replay (`evals/harness.py`) | Digest next to traces | Plant network |
| HITL tabletop, four **functions** | Override/workaround log (`ops/adoption.md` §6) | Named people invented in git |
| Chaos drills CH-05 CASCADE + CH-06 AI outage before every demo | PASS/FAIL record | Live region isolate |
| Ask leadership to **name** Authorizer people **outside** this repo | Process note; OPEN-001 **stays open in software** | Enable Authorize button |
| Keep `AI_ENABLED=0` default | Token cost 0 | Hosted model pin (OPEN-028) |

Success this slice: tabletop uses the packet instead of the CRITICAL banner. Failure: SOC auto-block request, or “just isolate 10% of PLT-10.”

---

## Days 31–60 — Measure what OPEN-006 left pending (no invented $)

| Work | Output | Bound |
|------|--------|-------|
| Stopwatch **time-to-confidence** on CASCADE tabletop | Minutes or UNKNOWN | Do not backfill a baseline |
| Count missed bypass (PLT-10-SAFE-07 not surfaced) | Adoption field; must not rise | Not a plant aging KPI |
| Optional explainer `ai=on` in **advisory software canary** only | Caption vs packet disagreement log | Caption must not re-rank (ADR-13) |
| FinOps meters already in `GET /ops/cost-per-incident` | Report template (`ops/adoption.md` §10.2) | Dollar threshold still unsigned |
| Do not optimize SLO-LAT by skipping joins | EVAL-025 / EVAL-026 | Fast-but-wrong = fail |

If a fork wants a hosted model: stop canary until OPEN-028 is an accepted **pin** and harness still 31/31.

---

## Days 61–90 — Management review, not actuation

Vehicle: **REL-04** (scale / change / restrict / suspend / retire). This slice only **feeds** it.

| Work | Output |
|------|--------|
| CAPA register template from tabletop FAILs | REL-04 |
| Drift report vs `assurance/SBOM_FREEZE.md` | Fill `ops/adoption.md` §10.1 |
| Decision: remain advisory · name Authorizers in operating model · or **stop** | Exec one-pager |
| Moonshot “more visibility” | Only if gates still hold; still `execute=false` |
| Retirement **plan** (workshop) | REL-04 — not an action on real systems |

**Stop the 90 days** if: write surface appears; data cleaned to beautify KPIs; legal class claimed (OPEN-002); live controller canary.

---

## What we are asking leadership for (explicit)

1. **Decision:** scale advisory shadow (YES) / scale execute (NO).  
2. **People:** name the humans who may authorize tier ≥3 **in your process**. Software will still not execute.  
3. **Clocks:** allow tabletop timing so OPEN-006 can move from BASELINE_PENDING to measured-on-synthetic — still not a plant MTT.  
4. **Money:** do not demand a $/incident target this quarter; meters exist; harm of unsafe isolate is **not a line item**.  
5. **Moonshot:** keep it earned. No twin-to-plant.

---

## 12-month (not this ask)

Governed recommendation path stays modern-default; `legacy_*` remains comparable; identity conflicts remain **visible**; named-role HITL on consequential drafts. Still no live OT in this repo (OPEN-003).

## Not the moonshot

Autonomous isolation, PLC/SIS/interlock writes, trip suppression, silent inventory cleanup, SOC auto-block, firewall push.
