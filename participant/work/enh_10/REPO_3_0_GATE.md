# ENH-10 — Repo 3.0 gate

**Prompt:** ENH-10 | MATERIALIZE REPO 3.0  
**Date:** 2026-09-16  
**FDE capabilities:** C58, C65, C66, C85 (C23 graph slice closed this increment)  
**Not this prompt:** customer UI (PRD/APP); live plant deploy; named Authorizers; signed SBOM.

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
- Playbook ENH-10 paste; companion `REPO_3.0_ENH_01_TO_10.md`
- Engines in `src/ot_command/core/` (identity, telemetry, risk, containment, recovery, graph_slice, authority, agent, guardrails, traces, ops)
- Gold GETs including `/graph/slice`; `GET /ops/slo`; `GET /ops/cost-per-incident`; POST `/recommend` packet only
- `evals/harness.py` EVAL-001…031 (ENH-09: 31 PASS)
- `assurance/ASSURANCE_REPORT.md`; `ops/` pack; `contracts/decision_trace.yaml`
- `tests/test_known_legacy_defects.py` still strict xfail on `legacy_*`
- Dockerfile `AI_ENABLED=0`; traces gitignored under `data/local/`

### Assumptions
1. Production-oriented means workshop-operable advisory software, not a connected plant.
2. Cost per analyzed incident may be traced (tokens, count) without inventing USD (OPEN-006).
3. RACI uses roles only (OPEN-001).

### Unknowns
OPEN-001, OPEN-002, OPEN-006/022, OPEN-024, OPEN-028, OPEN-029, OPEN-RISK-01/05/11.

### Did not conclude
PRD text; App UI; isolate execute; live restore orchestration; legal classification.

## Comparison vs SDD slide (Repo 1.0 → 2.0 → 3.0)

| Dimension | Repo 1.0 (before) | Repo 2.0 (SDD-15) | Repo 3.0 (this prompt) |
|---|---|---|---|
| Stage | Brownfield simulation | **Modernized** (structure only) | **Modernized** (engines + ops) |
| Nature | Runnable diagnostics + seeded defects | **SDD-aligned** | **Production-oriented** synthetic |
| Specs | Participant worktree / scattered `docs/` | **Structured** `specs/01`…`14` + `adrs/` | **Refined** + as-built C4 + ops pack |
| Controls | AGENTS.md + ot-fde.mdc | **Traceability + gates** | **Stronger governance**: guardrails, decision traces, SBOM freeze |
| Validation | 3 passed / 3 xfailed | **Spec-aligned** | **Readiness-focused** (harness 31/31, assurance, ops telemetry) |
| Outcome | Discoverable mess | **Improved repo** | **PRD + App ready** (UI not built here) |

## Confirmations

| Claim | Evidence |
|---|---|
| No live OT write / isolate-execute | `tests/test_api_readonly.py`; forbidden tools; POST `/recommend` is a packet |
| Data contradictions not cleaned | `data/raw` and `data/shadow` not rewritten this increment |
| Legacy XFAIL only against `legacy_*` | `tests/test_known_legacy_defects.py` |
| Graph slice hop_cap 8, no estate dump | `src/ot_command/core/graph_slice.py`; gold GET `/graph/slice` |
| Decision traces implemented | `data/local/decision_traces.jsonl` (gitignored); `contracts/decision_trace.yaml` |
| AI-disabled still traces policy_gate | `tests/test_ops_telemetry.py` |
| Cost dashboard does not invent USD | `GET /ops/cost-per-incident` `measured_usd=null` |
| As-built C4 | `specs/as_built_c4.md`, `docs/as_built_c4.md`, `src/ot_command/modern/AS_BUILT_C4.md` |

**Gate:** PASS. pytest **73 passed / 3 xfailed** (`legacy_*` only). `scripts/check_sdd_gates.py` → SDD_GATE_OK (63 paths, 31 eval cases). `verify_repo.py` → VERIFY_OK.

**Next:** PRD-01
