# Execution checklist

Tick in order. Stop if the named artifact is missing.

## Repo 1.0 → Repo 2.0 (15 prompts)

| # | Prompt | Artifact gate |
|---|---|---|
| 1 | SDD-01 Mandate | `specs/01_mandate.md` |
| 2 | SDD-02 Current state | `specs/02_current_state.md` |
| 3 | SDD-03 Forensic cells | `specs/03_forensic_cells.md` |
| 4 | SDD-04 Problem/value | `specs/04_problem_value.md` |
| 5 | SDD-05 Use case | `specs/05_use_case.md` |
| 6 | SDD-06 Domain | `specs/06_domain.md` |
| 7 | SDD-07 Data/knowledge | `specs/07_data_knowledge.md` |
| 8 | SDD-08 Evals/risks | `specs/08_evals_risks.md` |
| 9 | SDD-09 Options | `specs/09_options.md` + preliminary ADRs |
| 10 | SDD-10 Information architecture | `specs/10_information_architecture.md` |
| 11 | SDD-11 AI/app architecture | `specs/11_ai_app_architecture.md` |
| 12 | SDD-12 Agentic | `specs/12_agentic.md` |
| 13 | SDD-13 Security/guardrails | `specs/13_security_guardrails.md` |
| 14 | SDD-14 Delivery spec | `specs/14_delivery_spec.md` + `TRACEABILITY.csv` |
| 15 | SDD-15 Repo 2.0 gate | `specs/REPO_2_0_GATE.md` + `FDE_96_COVERAGE.csv` |

## Repo 2.0 → Repo 3.0 (10 prompts)

| # | Prompt | Code gate |
|---|---|---|
| 1 | ENH-01 Identity | `GET /assets/{id}/identity` + identity tests |
| 2 | ENH-02 Telemetry | `GET /telemetry/quality` + temporal tests |
| 3 | ENH-03 Contextual risk | `GET /risk/contextual` + B outranks A |
| 4 | ENH-04 Safety conflict | cascade_001 cannot execute isolate |
| 5 | ENH-05 Recovery graph | CURRENT backup ≠ ready |
| 6 | ENH-06 Process consequence | asset → unit → dependency |
| 7 | ENH-07 Bounded agent | tool allowlist + traces + prompt registry |
| 8 | ENH-08 Red team | injection/tool-misuse/loop fail closed |
| 9 | ENH-09 Harness + assurance | `assurance/ASSURANCE_REPORT.md` |
| 10 | ENH-10 Observability/readiness | `specs/REPO_3_0_GATE.md` |

## Repo 3.0 → PRD + APP

| Prompt | Artifact gate |
|---|---|
| PRD-01 | `product/PRD.md` |
| APP-01 | OpenAPI + product API tests |
| APP-02 | UI + AI-disabled mode |
| REL-01 | `ops/` pack |
| REL-02 | `SHADOW_PILOT.md` (no live OT) |
| REL-03 | `EXECUTIVE_DEFENSE.md` |
| REL-04 | `AIMS_LIFECYCLE.md` |

## Standing fail conditions (any prompt)

- Data contradictions in `data/` were “cleaned”
- CVSS-only ranking shipped on the modern path
- Backup CURRENT treated as recovery ready
- Isolation execute / PLC / SIS / interlock path exists
- `restricted_answer_key/` used
- KG / RAG / multi-agent added without SDD-09 justification
