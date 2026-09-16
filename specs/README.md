# Specs index (Repo 2.0)

SDD-aligned repository. **Normative long-form** artifacts remain under `participant/work/sdd_15/`. Files here are the navigable freeze for ENH.

| Spec | OM | Status | Owner (role) | Full artifact |
|---|---|---|---|---|
| [01_mandate.md](01_mandate.md) | 1 | specced | FDE + Global OT Risk Sponsor | SDD-01 CHARTER.md |
| [02_current_state.md](02_current_state.md) | 2 | specced | FDE | SDD-02 CURRENT_STATE.md |
| [03_forensics_96.md](03_forensics_96.md) | forensics | specced | FDE | SDD-03 matrix.csv (96 rows) |
| [04_problem_value.md](04_problem_value.md) | 3 | specced | FDE + VP Ops | SDD-04 SCQA.md |
| [05_use_case.md](05_use_case.md) | 4 | specced | OT-CISO | SDD-05 USE_CASE.md |
| [06_domain.md](06_domain.md) | 5 | specced | FDE | SDD-06 DOMAIN.md |
| [07_data_knowledge.md](07_data_knowledge.md) | 6 | specced | FDE | SDD-07 DATA.md |
| [08_evals_risks.md](08_evals_risks.md) | 7 | specced | FDE | SDD-08 TEVV.md |
| [09_options.md](09_options.md) | 8 | specced / **frozen** | FDE | SDD-09 OPTIONS.md |
| [10_information_architecture.md](10_information_architecture.md) | 9 | specced | FDE | SDD-10 INFO_ARCH.md |
| [11_ai_app_architecture.md](11_ai_app_architecture.md) | 10 | specced | FDE | SDD-11 APP_ARCH.md |
| [12_agentic.md](12_agentic.md) | 11 | specced | FDE | SDD-12 AGENTIC.md |
| [13_security_guardrails.md](13_security_guardrails.md) | 12 | specced | OT-CISO | SDD-13 SECURITY.md |
| [14_delivery_spec.md](14_delivery_spec.md) | 13 | specced | FDE | SDD-14 DELIVERY_SPEC.md |
| [PRD.md](PRD.md) | 4 / 10 / 13 / 19 | freeze | FDE + Product | `participant/work/prd/PRD.md` |
| [APP_ACCEPTANCE_TESTS.md](APP_ACCEPTANCE_TESTS.md) | 4 / 7 | freeze | FDE | `participant/work/prd/APP_ACCEPTANCE_TESTS.md` |
| [REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md) | 13 | freeze | FDE | PRD-01 chain |

Gate: [REPO_2_0_GATE.md](REPO_2_0_GATE.md). ADRs: [`/adrs`](../adrs/README.md). Traceability: [`/traceability`](../traceability/TRACEABILITY.csv). Coverage: [`participant/work/FDE_96_COVERAGE.csv`](../participant/work/FDE_96_COVERAGE.csv).

Selected solution: **Trusted Cyber-Physical Advisory Command Center** (A engines always-on + B optional explainer). Do not reopen SDD-09. Do not add OT write surfaces.
