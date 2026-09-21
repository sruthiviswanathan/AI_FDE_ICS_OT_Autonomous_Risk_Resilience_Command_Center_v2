# Ops pack — workshop / synthetic release (REL-01–02; REL-04 in release/)

**Audience:** shift lead, SOC analyst, process engineer, safety owner, FDE on-call.  
**Scope:** operate the **advisory Command Center** on the synthetic 18-plant estate. Not live plant operations.  
**Grade:** workshop evidence pack. **Not** an ISO/IEC 42001 certificate, EU AI Act conformity declaration, or production CAB sign-off.

If a later instruction conflicts with `analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md`, that file wins. Software in this repo **never** executes isolation, PLC writes, SIS changes, setpoints, or interlock bypasses.

## How to use this pack

1. Start here. Then [RACI](RACI.md) (who decides) and [named SLOs](named_slos.md) (what must not break).
2. Operate from [runbooks](runbooks.md) and [SOPs / training](sops_and_training.md).
3. On failure: [incident / rollback](incident_rollback.md) then [AI-specific IR](ai_incident_response.md) if the explainer/agent is involved.
4. Continuity: [BC/DR](bcdr.md) and [recovery evidence](recovery_evidence.md) (ENH recovery engine, ADR-05).
5. Oversight: [AI-system record](ai_system_record.md), [transparency](transparency.md), [dashboards / alerts](dashboards_alerts.md).
6. Progressive delivery (advisory only): [adoption](adoption.md) — shadow vs tabletop pilot vs **software** canary. Never a live controller canary.
7. Handover / go-live (synthetic): [handover](handover.md), [production-readiness checklist](production_readiness_checklist.md), [technical documentation](technical_documentation.md).
8. Lifecycle (paper): [AIMS lifecycle](../participant/work/release/AIMS_LIFECYCLE.md) — restrict-to-advisory; retirement is a **plan**, not a teardown of `data/` or plants.

A shift lead should be able to start the API, diagnose a plant, draft a packet, and fail closed **without** reading `specs/`.

## Document index

| Document | Purpose | FDE cell |
|----------|---------|----------|
| [RACI.md](RACI.md) | Observe / recommend / authorize / execute; AI incident roles | C80–C82 |
| [named_slos.md](named_slos.md) | Named SLOs and error budgets (SDD-14) | C68 |
| [dashboards_alerts.md](dashboards_alerts.md) | Ops dashboards and alert design | C65, C67 |
| [runbooks.md](runbooks.md) | Diagnose, failover, eval, injects | C67 |
| [incident_rollback.md](incident_rollback.md) | Software incident and rollback | C69 |
| [ai_incident_response.md](ai_incident_response.md) | Prompt injection, tool-misuse, loop | C70 |
| [bcdr.md](bcdr.md) | Advisory service continuity | C71 |
| [recovery_evidence.md](recovery_evidence.md) | How to read `GET /recovery/{plant}` | C71 |
| [sops_and_training.md](sops_and_training.md) | SOP outline + training | C74, C72 |
| [handover.md](handover.md) | Operational handover pack | C83, C84 |
| [production_readiness_checklist.md](production_readiness_checklist.md) | Pre-release checklist | C85 |
| [ai_system_record.md](ai_system_record.md) | Intended purpose, oversight, limits | C48 method |
| [transparency.md](transparency.md) | What traces exist; what is not logged | C66 |
| [technical_documentation.md](technical_documentation.md) | Start, APIs, flags, UI | C67 |
| [finops_cost_dashboard.md](finops_cost_dashboard.md) | Cost-per-incident meters | OPEN-006 |
| [drift_management.md](drift_management.md) | Spec / data / policy / model drift | C92 |
| [adoption.md](adoption.md) | Shadow / pilot / advisory canary; templates | C28, C64, C73, C86, C91, C92 |
| [AIMS_LIFECYCLE.md](../participant/work/release/AIMS_LIFECYCLE.md) | Management review, CAPA, retire plan, reusable IP | C48, C91, C93 |
| [render_deployment.md](render_deployment.md) | Demo host (synthetic, unauthenticated) | OPEN-029 |

## Runtime evidence (as-built)

| Signal | Where |
|--------|--------|
| Health / diagnostics | `GET /health`, `GET /diagnostics` |
| SLO synthesis | `GET /ops/slo` (`src/ot_command/core/ops.py`) |
| FinOps meters | `GET /ops/cost-per-incident` |
| Decision traces | `data/local/decision_traces.jsonl` · schema `contracts/decision_trace.yaml` |
| Recovery view | `GET /recovery/{site_or_unit}` · engine `src/ot_command/core/recovery.py` |
| Policy | `src/ot_command/core/policy.py` ACTION_TIERS |
| AI default | `AI_ENABLED=0` (ADR-12) |

## Hard rules (every runbook inherits these)

- UNKNOWN permission is not permission.
- Highest CVSS is not highest operational risk.
- `backup_status=CURRENT` is not RecoveryReady (ADR-05).
- Draft packet ≠ authorize ≠ execute. Named Authorizer is **OPEN-001**.
- Do not clean `data/` contradictions.
- Do not invent ISO certificate IDs or plant SLA dollars (OPEN-006).
