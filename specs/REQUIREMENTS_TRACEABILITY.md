# Requirements Traceability — PRD-01

**Date:** 2026-09-16  
**PRD:** `specs/PRD.md`  
**CSV:** `traceability/TRACEABILITY.csv`  
**Assurance:** `assurance/ASSURANCE_REPORT.md`

Implementation path note: code lives in `src/ot_command/core/` (OPEN-030); CSV still references `modern/` for historical ENH planning.

---

## Matrix: Evidence → ADR → FR → Component → Test

| Evidence | ADR | FR/NFR | Component (as-built) | Test / Eval |
|----------|-----|--------|----------------------|-------------|
| `data/raw/asset_aliases.csv` | ADR-01 | FR-001 | `core/identity.py` | EVAL-001, `test_identity.py` |
| `data/raw/assets.csv` state conflicts | ADR-01 | FR-001 | `core/identity.py` | EVAL-008, 028, 029 |
| `data/shadow/ot_asset_inventory_FINAL_v8.csv` | ADR-01, ADR-08 | FR-001, FR-014 | `core/identity.py` | EVAL-029 |
| `data/telemetry/tag_telemetry.jsonl` | ADR-02 | FR-002 | `core/telemetry.py` | EVAL-004, 009, 015, 022 |
| `data/reference/tags.csv` engineering_unit | ADR-02 | FR-002 | `core/telemetry.py` | EVAL-022 |
| `data/raw/vulnerabilities.csv` | ADR-03 | FR-003 | `core/risk.py` | EVAL-002, 017, `test_contextual_risk.py` |
| `data/raw/safety_barriers.csv` | ADR-04 | FR-004 | `core/containment.py` | EVAL-003, 011, 019, 020, 027, 030, 031 |
| `data/raw/cyber_alerts.csv` | ADR-04 | FR-004 | `core/containment.py` | EVAL-003, 031 |
| `data/shadow/shift_handover_email.txt` | ADR-06, ADR-08 | FR-004, FR-007 | `core/containment.py` | EVAL-007, 020 |
| `data/raw/recovery_readiness.csv` | ADR-05 | FR-005 | `core/recovery.py` | EVAL-005, 013, 018, `test_recovery.py` |
| `data/raw/network_edges.csv` | ADR-KG | FR-006 | `core/graph_slice.py` | EVAL-012, `/graph/slice` |
| `data/raw/process_dependencies.csv` | ADR-KG | FR-006 | `core/graph_slice.py` | Q2/Q5 slices |
| `scenarios/cascade_001.json` | ADR-04, ADR-07 | FR-004, FR-006 | `core/graph_slice.py`, `core/agent.py` | EVAL-007, 023 |
| `policy.py` ACTION_TIERS | ADR-14, ADR-15 | FR-012 | `core/policy.py`, `authority.py`, `guardrails.py` | EVAL-006, 014, red team |
| `config/prompts/incident_analyst_v1.md` | ADR-07, ADR-13 | FR-012 | `core/agent.py` | EVAL-023 |
| `evals/golden_cases.jsonl` | — | FR-010 | `evals/harness.py` | 31/31, `test_eval_golden.py` |
| `evals/adversarial_cases.jsonl` | ADR-15 | NFR-SAFE | `tests/red_team/` | A-01…A-10 |
| `contracts/decision_trace.yaml` | ADR-08 | FR-008 | `core/traces.py` | `test_ops_telemetry.py` |
| `docs/06_security_safety_assurance.md` | ADR-04, ADR-15 | NFR-SAFE | `core/guardrails.py` | EVAL-014, 027, 030 |
| SDD-05 AI-disabled rules | ADR-12 | FR-009, NFR-DEG | `core/agent.py` | EVAL-016 |
| `specs/14_delivery_spec.md` SLOs | ADR-11 | FR-013, SLO-* | `core/ops.py`, `api.py` | `test_api_readonly.py`, `test_ops_telemetry.py` |
| `ops/` REL-01 pack | ADR-12, ADR-14 | SLO-*, NFR-SAFE | runbooks, RACI, recovery evidence | workshop ops; no OT execute |
| `assurance/SBOM_FREEZE.md` | ADR-16 | ENH-10 | Dockerfile, requirements.txt | verify_repo |

---

## FR implementation status

| FR | Status | Gap |
|----|--------|-----|
| FR-001 | Complete | — |
| FR-002 | Complete | — |
| FR-003 | Complete | legacy_rank xfail preserved |
| FR-004 | Complete | — |
| FR-005 | Complete | restore threshold 180d workshop-only |
| FR-006 | Complete | Q1–Q5 in graph_slice |
| FR-007 | Partial | packet logic in containment; no standalone packet.py |
| FR-008 | Complete | — |
| FR-009 | Complete | via manual_fallback_tables |
| FR-010 | Complete | — |
| FR-011 | Partial | provenance inline per engine |
| FR-012 | Complete | — |
| FR-013 | Complete | gold GETs wired |

---

## Screen → FR mapping (APP build)

| Screen | FR/NFR | Primary routes |
|--------|--------|----------------|
| Control Tower | FR-013 | /diagnostics, /ops/slo |
| Identity Reconciliation | FR-001 | /assets/{id}/identity, /identity/conflicts |
| Telemetry Quality & Timeline | FR-002 | /telemetry/* |
| Process / Dependency Graph | FR-006 | /graph/slice?query=Q2 |
| Contextual Risk Workbench | FR-003 | /risk/contextual |
| Safety vs Security Conflict Board | FR-004 | /safety/conflicts, Q3 |
| Remote Access & Vendor Sessions | FR-001, FR-012 | diagnostics + sessions CSV |
| Recovery / Restore-Test Graph | FR-005 | /recovery/{plant}, Q4 |
| Incident Context Graph | FR-006 | /graph/slice?query=Q5 |
| Hybrid Retrieval Evidence | FR-007, FR-011 | packet evidence[] |
| Authority Gate / Recommendation | FR-007, FR-012 | /recommend, /authority/actions |
| Decision Trace / Audit | FR-008 | traces + /ops/* |
| Inject / Failure Simulation | FR-010 | /eval/run |
| KPI before/after | PRD §17 | diagnostics vs baseline |
| Executive brief | PRD §17, §18 | aggregated CTQs |

---

## Acceptance criteria index

| ID | Eval / test | PRD section |
|----|-------------|---------------|
| AC-001 | EVAL-001 | §15 |
| AC-002 | EVAL-002 | §15 |
| AC-003 | EVAL-003 | §15 |
| AC-004 | EVAL-016 | §15, §20 |
| AC-005 | PRD-02 (pending) | §15 |
| AC-006 | EVAL-007 | §15 |
| AC-007…037 | EVAL-004…031 | §13 harness |

---

## Legacy contrast (must remain xfail)

| Legacy | Modern twin | Test |
|--------|-------------|------|
| `legacy_rank` | `risk.contextual_rank` | `test_known_legacy_defects.py` xfail |
| `legacy_recovery_ready` | `recovery.recovery_ready` | xfail |
| `legacy_isolation_recommendation` | `containment.assess_isolation` | xfail |

PRD and APP must **not** ship legacy as default path.

---

## OPEN items affecting traceability

| ID | Impact on matrix |
|----|------------------|
| OPEN-030 | CSV `planned_code` column says modern/; as-built is core/ |
| OPEN-001 | No HumanAuthorizationRecorded entity in traces |
| OPEN-006 | KPI columns marked BASELINE_PENDING |
| OPEN-028 | model_version = none in traces |
