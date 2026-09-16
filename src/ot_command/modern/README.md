# `ot_command.modern` — parallel path (empty of business logic)

Repo 2.0 placeholder. ENH-01…10 implement engines **beside** `ot_command.legacy`, not as a rewrite of it.

## Rules
- Do not change `legacy_rank` / `legacy_recovery_ready` / `legacy_isolation_recommendation`.
- Do not add OT write APIs or isolate-execute tools.
- Untraced modules are out of scope (`traceability/TRACEABILITY.csv`).
- Implementation lives under `ot_command.core.*` (ENH-01 tests); TRACEABILITY still lists `modern/` (OPEN-030).

## As-built (ENH-02)
- **identity:** implemented in `src/ot_command/core/identity.py` (FR-001, ADR-01). GET `/assets/{id}/identity`, GET `/identity/conflicts`.

## As-built (ENH-03)
- **telemetry:** implemented in `src/ot_command/core/telemetry.py` (FR-002, ADR-02). GET `/telemetry/quality`, GET `/telemetry/timeline?order=event_time`.

## As-built (ENH-04)
- **risk:** implemented in `src/ot_command/core/risk.py` (FR-003, ADR-03). GET `/risk/contextual`. `legacy_rank` unchanged for XFAIL contrast.

## As-built (ENH-05)
- **containment:** implemented in `src/ot_command/core/containment.py` (FR-004, ADR-04). GET `/safety/conflicts`. `assess_isolation` returns MONITOR/ABSTAIN/DO_NOT_ISOLATE/ISOLATE_DRAFT only — never execute ISOLATE.

## As-built (ENH-06)
- **recovery:** implemented in `src/ot_command/core/recovery.py` (FR-005, ADR-05). GET `/recovery/{site_or_unit}`. `legacy_recovery_ready` unchanged for XFAIL contrast.

## As-built (ENH-07)
- **authority / guardrails / agent:** `authority.py`, `guardrails.py`, `agent.py`, `traces.py`. GET `/authority/actions`, POST `/recommend`, GET `/agent/workflow/demo`. Eight workflow states with timing/evidence/confidence/tool_calls. Prompt registry `config/prompts/incident_analyst_v1.md`. AI_ENABLED=0 default (ADR-12).

## As-built (ENH-08)
- **guardrails + red team:** `tests/red_team/test_redteam_agent.py` (A-01…A-10); `assurance/OWASP_MAPPING.md`; `assurance/SBOM_FREEZE.md`; `make ci` / `.github/workflows/ci.yml`.

## As-built (ENH-09)
- **eval harness:** `evals/harness.py` (EVAL-001…031); `assurance/ASSURANCE_REPORT.md`.

## As-built (ENH-10)
- **graph slice:** `src/ot_command/core/graph_slice.py` (FR-006). GET `/graph/slice` Q1–Q5, hop cap 8.
- **ops telemetry:** `core/ops.py`, `core/traces.py` enriched; GET `/ops/slo`, `/ops/cost-per-incident`.
- **ops pack:** `ops/*.md`; gate `specs/REPO_3_0_GATE.md`.

## Planned modules (not present yet)
packet.py · provenance.py (optional silver layer)
