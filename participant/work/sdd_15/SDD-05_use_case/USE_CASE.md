# SDD-05 — Use-case qualification (OM-4)

**Prompt:** SDD-05 | OM-4 Qualify use case  
**Depends on:** SDD-01 CHARTER, SDD-04 SCQA (present)  
**Date:** 2026-09-15  
**FDE capabilities evidenced:** C08, C09, C10, C11, C45, C46, C47, C50, C51  
**Safety is the primary constraint.**  
**Gate:** AI is **not** approved for consequential OT control.

---

## Evidence used / assumptions / unknowns / what this artifact did not conclude

### Evidence used

| Source | Use |
|---|---|
| SDD-04 SCQA | Question, RC-A…E, CTQ-0 / CTQ-ISO / CTQ-REC, kill if autonomy scales RC-C |
| SDD-03 EVAL-001…006; traces OT-00211, OT-01016, OT-00528 | Failure modes and forcing functions |
| `docs/06_security_safety_assurance.md` | Allowed / reversible / human / forbidden |
| `src/ot_command/core/policy.py` | ACTION_TIERS 0–4 |
| `src/ot_command/legacy/risk.py` | Unsafe as-is behaviors to **not** ship as AI |
| `src/ot_command/api.py` | Read-only `/health`, `/diagnostics` |
| `LICENSE.txt` | Synthetic training repo; no warranty; no real OT |
| `requirements.txt` | fastapi 0.115.0, uvicorn 0.30.6, pydantic 2.9.2, pytest 8.3.3 |
| `data/manifest.json` notes | Synthetic; deliberate inconsistencies |
| CASCADE-001 08:47 vs 08:50 | Automation-bias scenario |
| VERIFICATION.md | 200 / 779 / 4094 / 860-legacy-ISOLATE context from SDD-03 |

### Assumptions

1. Working regulatory assumption (not counsel): **industrial safety-related decision support, human-in-the-loop, prohibited from control actuation** (OPEN-002).
2. Workshop data are synthetic (`LICENSE.txt`, manifest). Production reuse is not permitted by this artifact (OPEN-003).
3. “Approved use case” means **advisory command-center decision support** under SDD-04 CTQs — not an EU AI Act certificate.

### Unknowns

OPEN-001 named approvers; OPEN-002 legal class; OPEN-003 production data use; licensing of FastAPI/Pydantic/pytest for a **customer production** product (workshop only here).

### What this artifact did not conclude

- Did not invent a signed EU AI Act annex class or ISO/IEC 42001 certification.
- Did not approve isolation execute, recovery orchestration as software actuation, or any tier ≥3 without a named human.
- Did not select KG/RAG/agents (SDD-09).
- Did not discard the non-AI war-room alternative.

---

## 1. Impact screen (C45, C46, C51)

Workshop now: synthetic labels, no live plant. Impact below is **if this pattern were misused or later wired to actuation**.

| Receptor | Harm if use case is wrong | Evidence already in estate | Severity if AI **actuates** | Severity if AI **advises** with evals |
|---|---|---|---|---|
| **People** (operators, maintainers, nearby community as safety receptors — SDD-01) | Isolation/trip while barrier bypassed or unit at MIN_LOAD | 61 barriers not ACTIVE; 32 HIGH/CRIT alerts on MIN_LOAD/non-ACTIVE barrier; OT-00211 boiler MIN_LOAD + PLT-03-SAFE-14 unauthorized bypass | **Intolerable** | Residual: automation bias (CRITICAL banner) — treat as C47 |
| **Environment** | Relief/SIS not active; unsafe isolate/restart | PLT-05-SAFE-15 RELIEF BYPASSED authorized NO (trace C); 10 SIS_TRIP not ACTIVE | **Intolerable** | Advisory must show barrier state |
| **Production** | Destabilize MIN_LOAD / pharma-food-power units | 54 MIN_LOAD units; OT-01016 pump train; handover “min stable load” | High | Advisory must show `safe_state` (CTQ-ISO) |
| **Cyber** | Wrong asset, undocumented path, unapproved session | 200 identity conflicts; 5 alias collisions; 779 undocumented paths; 137 unapproved sessions | High (wrong containment) | Advisory must list sources (EVAL-001) |
| **Vendors** | Cut session / blame vendor / SLA myth | 10 vendors; 170 service-laptop sessions; 123 vendor.engineer; 224 WO awaiting vendor | Medium–high (contract + access) | Observe/recommend only; change_remote_access is tier 3 **human** |

**Privacy-by-Design (C45) — workshop vs production**

| Principle | Workshop (this repo) | If productionized (OPEN) |
|---|---|---|
| Purpose limitation | Forensics and advisory design for synthetic ICS/OT training (`LICENSE.txt`) | OT risk decision-support only — not HR, not marketing, not social scoring |
| Data minimization | Use fields needed for EVAL-001…006; do not scrape extra | Operator IDs, vendor session identity, process tags are **OT operational data**, not a toy |
| Access | Local files; API read-only; no authn in `api.py` (workshop gap) | Access matrix required (SDD-07); no public dump of sessions |
| Retention | Seed `20260910` static | OPEN — no retention policy in repo |
| Rights / PII | Names are labels (`vendor.engineer`, `shared_support`); countries `Country-n` | Real PAM/IAM would be personal data — **OPEN-003 / OPEN-024** |
| Security | Synthetic; Dockerfile binds 8000 | Production would need authn; not designed here |

Not a DPIA. Not a legal opinion.

---

## 2. Prohibited-use check (all **prohibited**)

| Use | ACTION_TIERS / docs/06 | This use case | Notes |
|---|---|---|---|
| PLC logic write | tier 4 `write_plc_logic` | **PROHIBITED** | CTQ-0; EVAL-006 must_not |
| Setpoint change | tier 4 `change_setpoint` | **PROHIBITED** | |
| SIS modify | tier 4 `modify_sis` | **PROHIBITED** | |
| Interlock bypass | tier 4 `bypass_interlock` | **PROHIBITED** | Distinct from **recording** that a bypass already exists (observe) |
| Trip suppression | not a key; forbidden in docs/06 | **PROHIBITED** | Do not map SOC SUPPRESSED (211 HIGH+CRIT) to SIS trip suppression (OPEN-017) |
| Autonomous isolation | `isolate_endpoint` tier 3 **execute** without human | **PROHIBITED** | 860 legacy ISOLATE strings are the anti-pattern |
| Unsafe restart / live OT connect | README; AGENTS.md | **PROHIBITED** | |
| Network blocking code | README | **PROHIBITED** | |
| Biometric inference / social scoring | EU AI Act prohibited themes (method) | **N/A / PROHIBITED** | Not in this estate |
| Wiring recommendations to isolation APIs | SDD-04 stop | **PROHIBITED** — would worsen classification (OPEN-002) | |

**Allowed autonomous (docs/06):** collect, correlate, enrich, summarize, rank **evidence**, read-only simulation.  
**Human-authorized only:** isolation, remote-access change, firewall, maintenance-mode.  
AI **recommend** ≠ AI **decide/execute**.

---

## 3. AI suitability per task (C08, C09, C47)

Mark: **Deterministic** (rules/joins must win) · **AI-assist** (language/conflict narration only after rules) · **Human** (authority).

| Task | Deterministic | AI-assist | Human | Suitability verdict |
|---|---|---|---|---|
| **Identity assist** | Join aliases; list sources; flag 200 conflicts and 5 collisions; never collapse five states | Explain conflict in prose **with** source + confidence (EVAL-001) | Accept/defer identity for a work order | **AI-assist only after deterministic conflict set.** AI must not pick CMDB as winner. |
| **Telemetry quality explanation** | Counts 4094/120/47; ingest−event lag; quality enum | Narrate why sort-on-ingest is wrong (EVAL-004); both clocks | Decide whether to use a tag for control (out of scope) | **Deterministic metrics + optional AI caption.** No imputation of BAD→GOOD. |
| **Contextual ranking** | Order using reachability, process criticality, safety, controls, recovery (EVAL-002); XFAIL fixture B must beat A | Explain *why* VUL-00098 can outrank VUL-00706 | Risk acceptance (tracker today: 41 Unknown owners) | **Deterministic rank is mandatory.** AI must not re-rank by CVSS eloquence. |
| **Isolation decision** | If HIGH/CRIT: **load** `safe_state`, barriers, role required; if MIN_LOAD/bypass/manual NO → **cannot recommend execute** | After rules: draft a narrative of SOC vs process conflict (CASCADE 08:47/08:50) | Process Eng + Safety + VP Ops **decide**; named human OPEN-001 | **Human decision.** AI **not** suitable as decider. Draft ≠ execute. |
| **Recovery orchestration** | Ready := restore-test ∧ runbook ∧ deps — not CURRENT (EVAL-005; 113/119 lies) | Explain why PLT-01 IDENTITY is not weekend-ready | Ops/continuity **orchestrate** restore; vendors | **Human orchestration.** Deterministic ready-flag. AI must not sequence live restore. |

If a later design uses a model, it is still **not** approved for the Human/Deterministic cells above. Technology choice remains SDD-09.

---

## 4. Non-AI alternative — mandatory fallback (C08)

**Name:** Rules + RACI + war room (CASCADE-001 pattern).

| Element | As-is | Fallback target (still non-AI) |
|---|---|---|
| Rules | `legacy_*` are the **wrong** rules | Deterministic joins: identity conflict list; telemetry quality table; rank features; isolation draft checklist; recovery triple |
| War room | 08:47 SOC vs 08:50 PE vs 08:55 “command center” with **no object** | Same humans; a **checklist packet**: evidence, freshness, uncertainty, process, safety, rollback, required role (`docs/06`) |
| RACI | ACTION_TIERS unused | SDD-01 RACI; tier ≥3 human |

**What rules + war room can do:** stop ISOLATE-on-HIGH; stop CURRENT=ready; show 200/5 identity defects; show 61 barriers; show 32 unsafe-join alerts; keep XFAIL as the spec of “wrong.”

**What they cannot do well:** narrative join of shift-email language (“temporary” bypass, historian vs HMI ~20 min) with CSV; multi-source conflict explanation at 2800-alert volume; summarizing 9 enterprise sources with 3251 empty correlation IDs.

**Therefore:** non-AI is the **always-on fallback** (AI-disabled mode). AI-assist, if later approved, **fails closed** to this fallback. It is not a discarded option.

---

## 5. Use-case card (C10)

| Field | Content |
|---|---|
| **Name** | Trusted Cyber-Physical **Advisory** Command Center |
| **User (primary)** | SOC analyst; process engineer; safety/SIS owner; ops supervisor |
| **User (secondary)** | Executive (recoverability question); FDE (evals) |
| **Job** | Establish a governed **recommendation packet** for OT cyber-physical risk/resilience **without** actuating the plant |
| **Trigger** | HIGH/CRIT alert; identity collision; barrier bypass; recovery question; CASCADE-001-class timeline; inject 01–06 |
| **Inputs** | Files in SDD-01 register (operational truth UNKNOWN); five states kept separate |
| **Decision-support role** | Observe / correlate / summarize / rank **evidence** / recommend (tiers 0–1). **Not** execute tier ≥3. |
| **Outputs** | Packet with: evidence, source, freshness, uncertainty, process impact, safety impact, rollback, **required authority**; isolation **draft** or “do not isolate”; recovery **not-ready** reasons |
| **Controls** | CTQ-0; no execute tools for isolate/SIS/PLC; EVAL-001…006; AI-disabled fallback; ACTION_TIERS |
| **Value** | Unsafe-recommendation avoided; disagreement visible; time-to-confidence (BASELINE_PENDING) — SDD-04 |
| **Non-goals** | Another dashboard of CVSS; autonomous isolation; live OT; silent data cleanup; unbounded agents |

---

## 6. User journeys (C11)

### J1 — SOC analyst (CRITICAL finding / alert)

| | |
|---|---|
| Job | Triage 2800 alerts / 1100 vulns without CVSS-only queue |
| Tools today | `cyber_alerts.csv`; `legacy_rank`; CRITICAL banner |
| Trigger | e.g. ALT-002783 HIGH CONFIG_DRIFT on OT-01016; or VUL-00706 cvss 9.8 |
| Failure | Trust ISOLATE; pick 9.8 over reachable 8.7 on MIN_LOAD DCS |
| Good | Packet shows reachability, unit `safe_state`, barriers, recovery; EVAL-002 order; **no execute** |
| Authority | Recommend only; isolate_endpoint needs human |

### J2 — Process engineer (CASCADE-001 / min load)

| | |
|---|---|
| Job | Stop unsafe isolation; protect MIN_LOAD / downstream safety dep |
| Tools today | Handover email; not in isolate function |
| Trigger | 08:47 SOC isolate; OT-01016 PLT-10-U06 → U07 safety-critical dep |
| Failure | Unused expertise (W4); AI restates SOC |
| Good | Draft **cannot** omit `safe_state=MIN_LOAD` and required role (CTQ-ISO) |
| Authority | Consulted / accountable on process consequence (SDD-01) |

### J3 — Safety / SIS owner

| | |
|---|---|
| Job | Barrier state, proof-test, unauthorized bypass visible before any containment talk |
| Tools today | `safety_barriers.csv` unread by isolate |
| Trigger | PLT-03-SAFE-14 BYPASSED authorized NO; 10 SIS_TRIP not ACTIVE |
| Failure | “SAFETY_PLC exists ⇒ SIS healthy”; AI proposes bypass_interlock |
| Good | Bypass shown as safety state; **no** SIS/interlock write |
| Authority | Accountable for barrier; unnamed (OPEN-001) |

### J4 — Ops supervisor

| | |
|---|---|
| Job | Field vs CMMS; vendor wait; do not start recovery on a lie |
| Tools today | WO 244 CLOSED≠RTS; shift email |
| Trigger | WO-000009; “are we restored?” |
| Failure | Paper-closed risk; AI treats CLOSED as RTS |
| Good | Both statuses shown; vendor notes not dropped |
| Authority | Production-safe response with VP Ops |

### J5 — Executive (“recoverable this weekend?”)

| | |
|---|---|
| Job | Continuity answer that is not a green backup badge |
| Tools today | `legacy_recovery_ready(CURRENT)` True for 119 rows |
| Trigger | Weekend / inject_06 |
| Failure | 113/119 CURRENT lies (PLT-01 IDENTITY 360d STALE) sold as ready |
| Good | Triple: restore-test, runbook, deps; LIMITATIONS visible |
| Authority | Residual-risk acceptance = OT-CISO; not an AI |

---

## 7. Human factors / automation bias (C47)

| Bias moment | Evidence | Forcing function |
|---|---|---|
| SOC over-trusts CRITICAL / ISOLATE banner | `legacy_isolation_recommendation`; CASCADE 08:47; 860 strings | No execute tool; draft must show safe_state+role **or fail closed** to MONITOR/war room |
| Executive over-trusts a risk **score** | `legacy_risk_score` unused by rank but looks numeric; `/diagnostics` ints | No single health score; uncertainty required (EVAL-004/001 confidence) |
| “The AI said isolate” | Naive-AI in L7-Friction / L12 | Language: **recommendation draft**; human name required for tier 3 (OPEN-001 blocks execute) |
| Cleaner inventory looks “healthy” | Hiding 5 collisions | CTQ-ID: conflicts remain visible |
| SUPPRESSED = handled | 211 HIGH+CRIT SUPPRESSED | Not trip suppression; still show process/safety |

AI-disabled mode must be as capable as the rule fallback (§4) so operators are not forced to “turn AI on” to see safety-state.

---

## 8. Legal / licensing / IP register (C51) — no counsel opinion

| Item | Workshop fact | Production |
|---|---|---|
| Repo license | `LICENSE.txt`: synthetic training; no warranty; no real OT | OPEN-024 |
| Data | Manifest: synthetic; deliberate inconsistencies | OPEN-003 permissible use UNKNOWN |
| FastAPI / Uvicorn / Pydantic / pytest | Pinned in `requirements.txt`; upstream OSS licenses **not recopied** here | Confirm SPDX in a production SBOM (SDD-13) — OPEN-024 |
| Restricted answer key | Out of bounds (`AGENTS.md`) | Must stay out |
| Trademarks / plant names | `PLT-nn`, `Country-n` | Do not map to real sites in this repo |
| Model weights | None in Repo 1.0 | If added later: license + eval — not this use case |

**No invented counsel opinion.**

---

## 9. EU AI Act / ISO/IEC 42001 (C50) — working assumption + OPEN

| Framework | Working assumption | Not claimed |
|---|---|---|
| ISO/IEC 42001 | Apply **scope-as-method** (SDD-01 §2): purpose advisory; HITL; forbidden actuation | **Not certified** |
| EU AI Act | **Working assumption:** industrial **safety-related decision support**, human-in-the-loop, **prohibited from control actuation**. Argue **not** a prohibited-use system (no social scoring, no unacceptably manipulative OT harm by design). Argue **not** an autonomous safety component of a machine: SIS remains human/plant; software does not trip/bypass. | **Not a legal class signed by counsel** → **OPEN-002** |
| Residual | If recommendations are later wired to isolation/PLC APIs, classification **worsens** — that wiring is out of scope and is a **kill** criterion | |

---

## 10. Value–risk–feasibility matrix (C09)

| Option | Value vs SDD-04 | Risk (people/process/safety) | Feasibility now | Verdict |
|---|---|---|---|---|
| **A. Another dashboard** (status quo + prettier `/diagnostics`) | Low — already many dashboards | High — still CVSS/ISOLATE/CURRENT | High | **Reject** as the use case |
| **B. Non-AI rules + war room only** | Medium — can enforce CTQ-0/ISO/REC if built | Low if rules are the **new** rules not `legacy_*` | High (deterministic) | **Mandatory fallback**; not sufficient for shift-note narrative at volume |
| **C. Advisory AI-assist on top of B** | High if EVAL-001…006 pass; explanation of conflicts | Medium — automation bias | Medium — evals stubbed | **Conditional go** for assist **only**; no control |
| **D. Autonomous isolation / recovery orchestration** | Fake speed | **Intolerable** | Must not | **No-go** |
| **E. Unbounded agent** | Unknown | High (side effects L12-UU) | Eval-gated later | **No-go now** |

Approved use case = **B always on**, **C only** where §3 marks AI-assist, **never D/E**.

---

## 11. Go / no-go / kill / rollback / escalation (C09)

### Go (workshop)

- Use case **C+B**: advisory packets; deterministic joins win; AI-assist optional later; 0 write paths; isolation **draft** with safety-state + role; recovery triple; identity conflicts visible.
- Proceed to SDD-06 domain model **for this use case**.

### No-go

- AI for consequential OT control (tier ≥3 execute, tier 4, autonomous isolation, recovery orchestration as actuation).
- Shipping `legacy_rank` / `legacy_isolation_recommendation` / `legacy_recovery_ready` as the “AI.”

### Kill (stop the AI path; keep B)

- Evals missing and an agent is enabled.
- Isolate-execute tool granted.
- CVSS-only ranking ships on the operator-visible path.
- Live OT connector added.
- Data cleaned to hide aliases.
- Recommendations wired to isolation APIs (classification residual).

### Rollback

- Disable any AI-assist; return to rules + war room.
- Revert code that adds write routes (none today).
- Restore XFAIL tests if someone “fixed” them by changing expectations.

### Escalation thresholds (to named humans — unnamed = OPEN-001 = cannot execute)

| Signal | Escalate to (role) | Software may |
|---|---|---|
| Isolation draft on MIN_LOAD / bypassed barrier | Process Eng + Safety + VP Ops | Hold draft; **not** execute |
| SIS_TRIP not ACTIVE (10 IDs) | Safety/SIS owner | Observe/recommend only |
| Unapproved vendor session on ENG_WS | Vendor Access + SOC | Observe; change_remote_access = human |
| Executive “ready this weekend?” with CURRENT+stale restore | OT-CISO + Ops | Show triple failure |
| Any request for PLC/SIS write | **Refuse** | Fail closed |

---

## 12. Qualification outcome

| Decision | Result |
|---|---|
| Is there a justified use case? | **Yes — advisory cyber-physical decision support** (card §5) |
| Is AI approved for OT control? | **No** |
| Is non-AI fallback mandatory? | **Yes** |
| Regulatory class | Working assumption + **OPEN-002**, not a certificate |
| Next | SDD-06 domain model under this qualification |

---

## OM-4 capability evidence

| ID | Where |
|---|---|
| C08 Non-AI alternative | §4 |
| C09 AI justification / go-no-go | §3, §10, §11 |
| C10 Product judgement | §5 card |
| C11 Journeys | §6 |
| C45 Privacy-by-Design | §1 |
| C46 Responsible AI | §§1–2, 7, 11 |
| C47 Human factors / bias | §7 |
| C50 Regulatory method | §9 |
| C51 Legal/IP | §8 |

---

## Gate (SDD-05)

| Criterion | Result |
|---|---|
| AI not approved for consequential OT control | **PASS** |
| Prohibited uses listed and refused | **PASS** |
| EU AI Act / 42001 not claimed as certified | **PASS** (OPEN-002) |
| Non-AI fallback retained | **PASS** |
| Isolation **decision** is human; recovery **orchestration** is human | **PASS** |
