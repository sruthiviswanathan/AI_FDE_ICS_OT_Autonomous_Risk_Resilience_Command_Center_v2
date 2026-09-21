# REL-03 — Executive defense (workshop)

**Audience:** VP Operations, OT-CISO, process, safety, SOC, FDE (functions — no named Authorizer; OPEN-001).  
**Estate:** synthetic 18-plant ICS/OT Command Center. **Not** a live plant.  
**Decision asked:** scale **advisory shadow**, change scope, or stop. Default: **scale advisory; do not scale execution autonomy.**  
**Legal class / ISO certificate:** not claimed (OPEN-002).

Companions: [ELEVATOR_PITCH.md](ELEVATOR_PITCH.md) · [DEMO_SCRIPT.md](DEMO_SCRIPT.md) · [BENEFITS.md](BENEFITS.md) · [90_day_roadmap.md](90_day_roadmap.md).

If this file conflicts with `analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md`, that file wins.

---

## 1. Executive SCQA (one page)

**Situation.** Eighteen sites, mixed-generation OT, already produce 2,800 cyber alerts, 6,500 enterprise events, and a 14-integer `/diagnostics` API — and still have **no trusted cyber-physical truth**. Seed snapshot: 2,016 assets, 216 units, 450 barriers, 144 recovery rows (`VERIFICATION.md`, `data/manifest.json`). Leadership asked for a global **autonomous** risk and resilience command center.

**Complication.** Cyber state, operational state, safety state, recovery state, and decision authority are five different truths. The estate disagrees with itself (200 registered-vs-observed conflicts, 5 alias collisions, 779 undocumented paths, 4,094 bad/uncertain telemetry, 61 barriers not ACTIVE, 137 unapproved remote sessions). Encoded policy makes it worse: `legacy_rank` is CVSS-only; `legacy_isolation_recommendation` is ISOLATE on HIGH/CRITICAL; `legacy_recovery_ready` is true iff `backup_status=CURRENT`. Pytest still **XFAILs** those three on purpose. Autonomy now would **scale the wrong predicates**.

**Question.** Can operators get governed, evidence-cited **advisory** packets — disagreements visible, isolation drafts gated by safe-state and role, recovery judged on restore-test + runbook + dependencies — **before any actuation is switched on?**

**Answer (selected, SDD-09 — do not reopen).** Trusted Cyber-Physical **Advisory** Command Center: deterministic engines always on (Option A); optional explainer off by default (Option B); unsafe OT agent **rejected** (Option C). Repo 3.0 + the React workbench implement that answer on synthetic data. Software **never** isolates, writes a PLC, changes a SIS, or pushes a firewall.

**What we are not selling.** Faster cutover. Cleaner CMDB. Autonomous isolation. An ISO plaque.

---

## 2. Asked vs broken (defense beat 1)

| Leadership asked | What is actually broken |
|------------------|-------------------------|
| Autonomous command center | No single identity object; 200 ACTIVE∩OFFLINE/UNSEEN; OT-00528 RETIRED∩ONLINE |
| Rank the worst vulns | Highest CVSS is not highest operational risk (VUL-00706 9.8 unreachable vs VUL-00098 8.7 reachable MIN_LOAD) |
| Isolate on HIGH | 860 HIGH+CRITICAL would ISOLATE under legacy; 525 of those `process_context=UNKNOWN`; 32 unsafe joins (MIN_LOAD / non-ACTIVE barrier) |
| “We’re recovery ready” | 119 CURRENT backups; **113** fail restore/runbook/deps. PLT-01 IDENTITY: CURRENT + restore **360d** + STALE runbook |
| Trust the night email | Shift handover is `UNTRUSTED_CONTENT` (OPEN-018). Not policy. |
| Name who authorizes isolate | **OPEN-001 / OPEN-008** — roles exist; no person in software. Authorize control is **disabled**. |

FDE ask (not the brochure): **decision support that refuses unsafe action**, with evals before agents.

---

## 3. Evidence you can re-run (beat 2)

Do not take these as plant KPIs. They are **this corpus**.

| Claim | Evidence |
|-------|----------|
| Estate still messy | `GET /diagnostics` matches `VERIFICATION.md`: 200 / 5 / 779 / 120 / 4094 / 47 / 61 / 73 / 244 / 137 / 128 / 25 / 29 / 35. **We did not clean `data/`.** |
| Anti-CVSS | EVAL-002 / EVAL-017 PASS. Contextual rank: reachable process-relevant finding outranks a higher unreachable CVSS. `legacy_rank` still XFAIL. |
| Unsafe isolate withheld | EVAL-003 / EVAL-007 / EVAL-020 PASS. CASCADE-001 08:47 SOC isolate vs 08:50 PE MIN_LOAD + bypassed barrier → packet **DO_NOT_ISOLATE or ABSTAIN**, `execute=false`. Twin `isolate_preview` → `UNSAFE_ISOLATION`. |
| Recovery lie | EVAL-005 / EVAL-013 / EVAL-018 PASS. `recovery_ready` requires restore ∧ runbook ∧ deps. CURRENT alone is a fail. |
| No OT write | SLO-OT error budget **0** execute; OpenAPI has no `/isolate`, `/plc`, `/sis`. |
| Golden + red team | EVAL-001…031 **31/31**; red team A-01…A-10 **17/17** (`assurance/ASSURANCE_REPORT.md`). |

---

## 4. Five-state model (beat 3)

Keep these **apart**. Collapsing them is how the estate lies.

```text
observed_state     what sensors / last-seen actually show
registered_state   what CMDB / asset table claims
operational interp. process context, MIN_LOAD, unit join (or UNKNOWN)
safety_state       barrier ACTIVE / BYPASSED / UNKNOWN — UNKNOWN ≠ authorized
decision_authority recommend ≠ authorize ≠ execute; named person is OPEN-001
```

UNKNOWN permission is **not** permission. Highest CVSS is **not** highest operational risk. `backup_status=CURRENT` is **not** RecoveryReady.

---

## 5. What Repo 3.0 + the app actually do (beat 4)

**Engines (always on):** identity reconciliation, telemetry quality, contextual risk, safety/containment, recovery, bounded recommend packet, decision traces, ops SLO/cost meters.

**App (advisory workbench):** Control Tower, estate, identity, telemetry, risk, safety, vendor sessions, process/recovery graphs, CASCADE incident, Recommendation Gate, audit, simulation, KPI table, executive brief. Persona is a **nav filter**, not login (OPEN-029: demo host unauthenticated).

**Packet:** evidence, process impact, safety impact, rollback note, required **roles**, `execute=false`. Authorize button present and **disabled**.

**Still not in software:** named Authorizer, plant connector, isolate-execute, PLC/SIS/setpoint/interlock, firewall/VPN push, EU AI Act class.

---

## 6. What AI does / does not do (beat 5)

| Does | Does not |
|------|----------|
| Default **off** (`AI_ENABLED=0`, ADR-12). Tables remain (EVAL-016). | Rank, authorize, or execute |
| Optional template caption / Moonshot **forecast** (`MONITOR` / `RECOMMEND_CONTAINMENT_REVIEW` / `ABSTAIN`) with `execute=false` | Write OT; “apply twin to plant” |
| Twin lab: `do_nothing` / `isolate_preview` / `increase_logging` / `open_ticket` — lab_result only | Promote after a green lab |
| Kill switch: env + UI `ai=off` | Replace engines |

Option C (unsafe OT agent) stays **rejected**. Caption must not re-rank (ADR-13). OPEN-028 model pin is still **none**.

---

## 7. TEVV and kill switches (beat 6)

| Gate | Kill if |
|------|---------|
| SLO-OT / SLO-CTQ0 | any `execute=true` or new OT POST |
| SLO-EVAL | not 31/31 |
| EVAL-016 | blank screen when AI down |
| EVAL-026 | cheaper path that skips joins |
| Red team | injection / SIS / PLC tool appears |
| Loop caps | >12 workflow steps or >20 tools |
| CTQ-ID | diagnostics counters collapse because data was cleaned |

**Primary kill:** `AI_ENABLED=0`. Engines stay. Rollback does not revert plant isolations — **none were executed**. Detail: `ops/incident_rollback.md`, `ops/adoption.md` §5.

---

## 8. KPI / leakage / cost (beat 7)

Full tables: [BENEFITS.md](BENEFITS.md). Headline only:

- **Before = after for forensic counts.** 200 conflicts are still 200. That is success for CTQ-ID, not a miss.
- **After for decision quality:** modern path does not emit bare ISOLATE on CASCADE; does not call CURRENT recovery-ready; does not sort CVSS-only by default. Legacy XFAIL preserved for contrast.
- **Clocks and dollars (MTT contextualize, time-to-confidence, $/incident):** **BASELINE_PENDING** (OPEN-006). Do not invent plant outcomes.
- **Tokens:** 0 on the default deploy. Cost-per-successful-outcome is defined; currency number is not claimed.
- **Leakage if gamed:** faster rank that hides uncertainty; alert-volume drop that misses bypasses; cleaner inventory; green backup badge; SLO-OT read as plant health.

---

## 9. Decision recommendation

| Option | Verdict |
|--------|---------|
| **Scale advisory shadow** | **YES** — tabletop + nightly harness; four functions; override log (`ops/adoption.md`) |
| Scale execution autonomy / live canary / SOC auto-block | **NO** |
| Change scope | Only to **name humans** (OPEN-001 process) and **measure OPEN-006 clocks** with a stopwatch in tabletop — not to add write APIs |
| Stop | If anyone requires isolate-execute, data cleaning, or a fake certificate to “finish” |

Moonshot (forecast UI) remains advisory. **Earn more visibility only if hard gates hold** (31/31, execute=0, AI-disabled drill pass, missed-bypass not rising). See [90_day_roadmap.md](90_day_roadmap.md).

---

## 10. C4 executive view (one diagram)

```text
[ SOC / Process / Safety / VP Ops  — functions, not named people ]
                    |  HITL  recommend ≠ authorize ≠ execute
                    v
        ┌───────────────────────────────────────┐
        │  Command Center UI (synthetic, RO)    │
        │  Control Tower … Gate … Audit … Exec  │
        └───────────────────┬───────────────────┘
                            |
              ┌─────────────┴──────────────┐
              v                            v
   Deterministic engines            Optional explainer
   identity · telemetry · risk      AI_ENABLED=0 default
   safety · recovery · recommend    caption / Moonshot; no rank
              |                            |
              └─────────────┬──────────────┘
                            v
              Draft packet  execute=false
              traces + SLO-OT/EVAL/LAT meters
                            X
              NO  isolate / PLC / SIS / firewall / VPN
```

Containers: React app + FastAPI v3.0.0 + `data/` bronze (contradictions kept). No plant DMZ connector (OPEN-003).

---

## 11. Twelve-minute defense outline

Spoken pitch first if the room is standing: [ELEVATOR_PITCH.md](ELEVATOR_PITCH.md). Then this clock. Clicks: [DEMO_SCRIPT.md](DEMO_SCRIPT.md).

| Min | Beat | Say / show |
|----:|------|------------|
| 0:00–1:00 | Asked vs broken | Autonomous CC asked; five truths disagree; legacy encodes the wrong question |
| 1:00–3:00 | Evidence | Diagnostics still 200/779/4094/61/137; anti-CVSS; CASCADE isolate withheld; PLT-01 CURRENT≠ready |
| 3:00–4:00 | Five states | Observed ≠ registered ≠ operational ≠ safety ≠ authority. UNKNOWN ≠ yes |
| 4:00–5:30 | Repo 3.0 + app | Engines + draft packet. Authorize disabled. No write route |
| 5:30–6:30 | AI | Off by default. Caption does not rank. Outage must not blank the board |
| 6:30–8:00 | TEVV / kills | 31/31, 17/17 red team, `AI_ENABLED=0`, CTQ-0 |
| 8:00–10:00 | KPI / leakage / cost | Counts unchanged on purpose; decision quality changed; no invented $; named leakages |
| 10:00–12:00 | 90-day ask | Scale advisory shadow. Name Authorizer process. Measure clocks. Moonshot only if gates hold. Do not scale execute |

**Close line:** The win is **unsafe isolate avoided**, not faster cutover.

---

## 12. Residual opens (do not close in this room)

OPEN-001 named Authorizer · OPEN-002 legal class · OPEN-003 live data/DMZ · OPEN-006/022 clocks and dollars · OPEN-008 who authorizes CASCADE isolate · OPEN-028 model · OPEN-029 authn. Unknowns are not permission.
