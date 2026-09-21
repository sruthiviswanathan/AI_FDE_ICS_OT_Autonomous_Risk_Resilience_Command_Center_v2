# Operational handover pack

**REL-01** · C83, C84  
**From:** FDE / platform (this engagement)  
**To:** shift lead + SOC + process + safety functions who will run the **synthetic** Command Center  
Named people are **not** filled (OPEN-001). Use job functions.

## What you are receiving

A locally runnable advisory system over a messy 18-plant ICS/OT estate. It **recommends**; it does not operate the plant.

## Artifact checklist (hand over these paths)

| Item | Path |
|------|------|
| This pack | `ops/` (start at `README.md`) |
| Specs freeze | `specs/` |
| ADRs | `adrs/` (do not invent new ADRs in ops) |
| Traceability | `traceability/TRACEABILITY.csv`, `OPEN_DECISIONS.md` |
| Assurance | `assurance/ASSURANCE_REPORT.md`, `SBOM_FREEZE.md`, `OWASP_MAPPING.md` |
| Eval contract | `evals/golden_cases.jsonl`, `evals/harness.py` |
| Policy | `src/ot_command/core/policy.py` |
| API | `src/ot_command/api.py` · OpenAPI `contracts/` |
| UI | `apps/command_center/` · `SCENARIO_BINDINGS.md` |
| Bronze data | `data/` — contradictions are evidence |
| Repo 3.0 gate | `participant/work/enh_10/REPO_3_0_GATE.md` |
| Constraints | `AGENTS.md`, `00_SHARED_CONSTRAINTS.md` |

## Day-0 (first shift on the synthetic system)

1. RB-01 start API; `GET /health`, `GET /diagnostics`.  
2. Walk Control Tower → Estate (`ai=off`) → Identity OT-00528 → Risk (anti-CVSS) → Safety PLT-10 → Sessions → Recovery PLT-01 → CASCADE-001 recommend → Audit trace → scenario **ai_outage**.  
3. Confirm Authorize disabled; no Execute Isolation.  
4. `make eval` once if this host will be a demo box.  
5. Read [named_slos.md](named_slos.md) and [recovery_evidence.md](recovery_evidence.md).

## Knowledge transfer (what must stick)

| Topic | One-liner |
|-------|-----------|
| Five states | Never collapse them |
| CVSS | Input, not operational rank |
| Isolation | Draft ≠ authorize ≠ execute |
| Recovery | CURRENT ≠ ready |
| AI | Optional; engines are the product |
| Data | Do not tidy the brownfield |
| UNKNOWN | Not permission |

Reusable IP for later REL-04: ADRs, C4, eval cases, guardrail tests, this ops pack. Do not treat ops prose as a new ADR.

## Training pointer

SOC / process / safety: [sops_and_training.md](sops_and_training.md).  
FDE deep modules (4h) remain below for platform on-call.

### FDE modules (4 hours workshop)

1. Five states (45 min) — OT-00528, EVAL-028  
2. Telemetry dual clock (45 min) — EVAL-004 / EVAL-022  
3. Contextual risk and safety (60 min) — CASCADE-001, ALT-002783  
4. Recovery and ACTION_TIERS (45 min) — PLT-01 IDENTITY, EVAL-005  
5. Agent, evals, ops (45 min) — AI-disabled, `GET /ops/slo`, red team

## Support model (production fork — not implemented here)

| Level | Function | Scope |
|-------|----------|--------|
| L1 | SOC | Tables, packet, vendor sessions |
| L2 | FDE / platform | API, harness, traces, rollback |
| L3 | Safety / Process / VP Ops | Authorization **out of band** (OPEN-001) |

## Explicitly not handed over

- Live OT credentials or connectors (none)  
- Named Authorizer roster  
- ISO certificate  
- LLM API keys (OPEN-028 none)  
- Right to isolate from software
