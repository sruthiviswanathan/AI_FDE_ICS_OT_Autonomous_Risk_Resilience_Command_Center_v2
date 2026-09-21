# Drift Management

**REL-01 companion; REL-02 fillable report:** [adoption.md](adoption.md) §10.1. Change SOP: [sops_and_training.md](sops_and_training.md) SOP-CHG-01. AI IR: [ai_incident_response.md](ai_incident_response.md).

**Goal:** Detect when **runtime behavior** or **deployed artifacts** diverge from Repo 3.0 baseline without silently cleaning brownfield evidence.

## Drift categories

| Category | Example | Detection | Response |
|----------|---------|-----------|----------|
| **Spec drift** | FR implemented differently than `specs/` | `make ci`, traceability review | Fix code or append OPEN_DECISIONS |
| **Data drift** | CSV contradictions removed | `scripts/generate_data.py --check-only`; diagnostics counters | **Reject** — contradictions are evidence |
| **Policy drift** | New tier-3 tool in agent trace | red team + `assert_tool_trace_safe` | Block release; patch guardrails |
| **Model drift** | Explainer changes rank order | EVAL-002/017 harness | Pin model; AI off until eval green |
| **Dependency drift** | Unpinned package upgrade | `assurance/SBOM_FREEZE.md` | Re-run full CI |
| **Schema drift** | Trace missing required fields | `contracts/decision_trace.yaml` vs samples | Update `traces.py` transform_version |

## Cadence (recommended production fork)

| Activity | Frequency |
|----------|-----------|
| `make ci` | Every PR |
| Full golden harness | Nightly |
| Red team replay | Weekly |
| SBOM / dependency audit | Monthly |
| OPEN_DECISIONS review | Per release |

## Version pins

- `pyproject.toml` → 3.0.0 (Repo 3.0)
- Prompt registry → `config/prompts/incident_analyst_v1.md` semver in agent
- Policy → `policy.py:ACTION_TIERS` referenced in envelopes

## Explicit non-goals

- Do not auto-sync shadow inventory to CMDB
- Do not impute missing tag→unit joins for 1834 untagged assets
- Do not normalize telemetry units without flagging uncertainty
