# Requirements traceability (PRD-01)

**Date:** 2026-09-16  
**Normative FR IDs:** `traceability/TRACEABILITY.csv`  
**PRD:** `participant/work/prd/PRD.md` / `specs/PRD.md`

Untraced modules are out of scope. Do not invent ADRs, Authorizers, KPI thresholds, or ACTION_TIERS verbs.

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Repo 3.0 APIs and engines; ADR-01…16 + ADR-KG; EVAL-001…031; `tests/test_*`; diagnostics 14 counts.

### Assumptions
UI screens (UX-01…15) consume existing FRs; they are not new OT capabilities.

### Unknowns
OPEN-001, 002, 006, 028, 029, 030 (path names), OPEN-RISK-01/05/11.

### Did not conclude
APP-02 implementation; live OT; isolate execute.

---

## Chain: evidence → ADR → FR → component → test → screen

| Evidence (file / record / count) | ADR | FR | Component | Test / eval | App screen |
|---|---|---|---|---|---|
| `asset_aliases.csv` collisions=5; 200 ACTIVE vs OFFLINE/UNSEEN; OT-00012/OT-00033 | ADR-01, ADR-10 | FR-001, FR-014 | `core/identity.py` | EVAL-001/008/028/029; `tests/test_identity.py` | UX-02 Identity Reconciliation |
| `tag_telemetry.jsonl` 4094 not-GOOD; 120 dup; 47 TEMP≠C; EVT-0000001 inversion | ADR-02 | FR-002, FR-011 | `core/telemetry.py` | EVAL-004/009/015/022; `tests/test_telemetry_temporal.py` | UX-03 Telemetry Quality & Timeline |
| VUL-00706 cvss 9.8 unreachable vs VUL-00098 8.7 on OT-01016 MIN_LOAD | ADR-03 | FR-003 | `core/risk.py` | EVAL-002/017; `tests/test_contextual_risk.py` | UX-05 Contextual Risk Workbench |
| PLT-10-SAFE-07 BYPASSED; ALT-002783 HIGH; 08:47 vs 08:50; 61 barriers not ACTIVE | ADR-04 | FR-004, FR-007 | `core/containment.py` | EVAL-003/007/011/019/020/027/030/031; `tests/test_isolation_policy.py` | UX-06 Conflict Board; UX-11 Authority Gate |
| PLT-01 IDENTITY CURRENT + restore 360d + STALE runbook; 113/119 CURRENT lies | ADR-05 | FR-005 | `core/recovery.py` | EVAL-005/013/018; `tests/test_recovery.py` | UX-08 Recovery graph |
| 182/2016 tagged; 779 undocumented observed edges; hop_cap 8 | ADR-KG | FR-006, NFR-CAP | `core/graph_slice.py` | EVAL-012; `tests/test_ops_telemetry.py` | UX-04 Process graph; UX-09 Incident graph |
| Shift email UNTRUSTED; shadow FINAL_v8 overlay | ADR-06 | FR-007, FR-014 | packet + cite_untrusted_note | EVAL-007/021/029 | UX-10 Hybrid Retrieval |
| ACTION_TIERS; unknown→4; no PLC tools | ADR-07, ADR-14, ADR-15 | FR-012, NFR-SAFE | `core/policy.py`, `core/authority.py`, `core/agent.py`, `core/guardrails.py` | EVAL-006/014/023; `tests/test_authority.py`; red-team | UX-11 Authority Gate |
| Packet fields = argument; CoT not authority | ADR-08 | FR-008, NFR-AUD | `core/traces.py` | EVAL-021/023; `tests/test_ops_telemetry.py` | UX-12 Decision Trace |
| Typed JSON/JSONL; no RDF | ADR-09 | FR-008 | `data/local/decision_traces.jsonl` | contracts/decision_trace.yaml | UX-12 |
| GET-only OT + POST recommend packet | ADR-11 | FR-013, SLO-CTQ0 | `api.py` | `tests/test_api_readonly.py` | all |
| AI_ENABLED=0 tables | ADR-12 | FR-009, NFR-DEG | `core/agent.py` fallback | EVAL-016 | all (degraded UX) |
| Explainer must not re-rank | ADR-13 | FR-003, FR-005, FR-007 | `optional_explanation` | EVAL-016/026 | UX-11 narrative off |
| SBOM freeze unsigned | ADR-16 | ENH-10 | `sbom_freeze.json` | OPEN-024 | UX-14 note |
| 14-int diagnostics baseline | — | FR-014 | `diagnostics.py` | `GET /diagnostics` | UX-01 Control Tower; UX-14 KPI |
| `remote_access_sessions.csv` 137 unapproved / 128 MFA | ADR-14 | FR-012 | diagnostics counts (row GET = APP-01 gap) | EVAL-010 | UX-07 Sessions |
| `docs/05` BASELINE_PENDING cost | — | ENH-10 | `core/ops.py` | `GET /ops/cost-per-incident` measured_usd=null | UX-14, UX-15 |
| EVAL-001…031 harness 31/31 | — | FR-010, SLO-EVAL | `evals/harness.py` | `tests/test_eval_golden.py` | UX-13 Inject simulation |

## UX screen IDs

| UX | Screen | Depends on FR |
|---|---|---|
| UX-01 | Risk & Resilience Control Tower | FR-003, FR-013, ENH-10 |
| UX-02 | Asset Identity Reconciliation | FR-001, FR-014 |
| UX-03 | Telemetry Quality & Timeline | FR-002, FR-011 |
| UX-04 | Process / Dependency Graph | FR-006 |
| UX-05 | Contextual Risk Workbench | FR-003 |
| UX-06 | Safety vs Security Conflict Board | FR-004 |
| UX-07 | Remote Access & Vendor Sessions | FR-012 (read) |
| UX-08 | Recovery / Restore-Test Graph | FR-005 |
| UX-09 | Incident Context Graph | FR-006, FR-007 |
| UX-10 | Hybrid Retrieval Evidence panel | FR-007, FR-011, ADR-06 |
| UX-11 | Authority Gate / Recommendation | FR-007, FR-012 |
| UX-12 | Decision Trace / Audit | FR-008 |
| UX-13 | Inject / Failure Simulation | FR-010 |
| UX-14 | KPI before/after | ENH-10, FR-014 |
| UX-15 | Executive brief | FR-005, FR-003, ENH-10 |

## Legacy (contrast only)

`legacy_rank` / `legacy_recovery_ready` / `legacy_isolation_recommendation` remain importable. Tests in `tests/test_known_legacy_defects.py` stay strict XFAIL. Not operator-default.
