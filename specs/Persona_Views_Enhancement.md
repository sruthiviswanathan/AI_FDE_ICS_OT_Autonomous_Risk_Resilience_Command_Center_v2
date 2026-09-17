# Enhanced Prompt: Persona-Based Command Center Views

## Context

You are working on the **AI FDE ICS/OT Autonomous Risk Resilience Command Center v2** — a brownfield OT advisory application (not a greenfield rewrite). The React frontend lives in `apps/command_center/`; the FastAPI backend in `src/ot_command/`. Data is workshop-static CSV under `data/`.

**Read first:**
- `AGENTS.md`
- `.cursor/rules/sdd.mdc` and `.cursor/rules/ot-fde.mdc`
- `apps/command_center/SCREEN_SPECIFICATIONS.md` (S01–S15 — each screen already lists personas)
- `apps/command_center/APP_FLOW.md` (journeys 2.1–2.5 per persona)
- `specs/PRD.md` §1.2 (Users / personas), §2 (Roles and decision authority)
- `contracts/openapi_command_center.yaml`

**Hard constraints (do not violate):**
- Persona views are **navigation and presentation filters only** — not authentication, not authorization (OPEN-029: no production API auth in Repo 1.0).
- Do not invent named Authorizers, legal class, KPI pass thresholds, or ACTION_TIERS verbs.
- Do not reopen SDD-09. Do not change `legacy_*` behavior, delete XFAIL tests, or clean `data/` contradictions.
- Do not add OT write routes, isolate-execute surfaces, SIS bypass, or PLC write capabilities.
- **UNKNOWN permission is not permission** — switching persona must never enable Execute / Authorize / tier-3 actions.
- ADR-12 / EVAL-016: deterministic tables and packets remain visible regardless of persona or narrative toggle.
- CASCADE-001 dissent (08:47 SOC vs 08:50 PE) and safety bypass rows must **never be hidden** by persona filtering (EVAL-007, APP-AT-011).
- Untraced modules are out of scope (`traceability/TRACEABILITY.csv`).

---

## Task Overview

Implement **persona-based views** so operators see a focused command center tailored to their role, while preserving a **Full workshop view** escape hatch for demos and FDE use.

| # | Feature | Priority |
|---|---------|----------|
| 1 | Persona registry + selector (global chrome) | High |
| 2 | Filtered navigation rail per persona | High |
| 3 | Persona-specific default landing routes | High |
| 4 | Context bar + drawer defaults per persona | Medium |
| 5 | Screen-level card emphasis (within existing layouts) | Medium |
| 6 | Deep-link / persist persona (`?persona=` + localStorage) | Medium |

Work incrementally. No backend authority model changes unless a read-only `/personas/catalog` introspection endpoint is explicitly traced. Prefer frontend config derived from existing screen specs.

---

## Persona Model

| Persona ID | UI label | Default route |
|------------|----------|---------------|
| `soc_analyst` | SOC / OT Analyst | `/` |
| `process_engineer` | Process Engineer | `/process` |
| `safety_owner` | Safety / SIS Owner | `/safety` |
| `executive` | Executive / VP Ops | `/executive` |
| `fde` | FDE / Platform | `/` |
| `full` | Full workshop view | `/` |

---

## Definition of Done

1. Five workshop personas + Full view are selectable and persist.
2. Nav, landing route, and context bar match persona intent from PRD/APP_FLOW.
3. Incident-critical evidence remains visible across personas.
4. No new OT action surfaces; authority model unchanged.

---

## Suggested Implementation Order

```
1. Persona registry + AppContext persona state + usePersona hook
2. Refactor NAV to data-driven + filtered render in Shell
3. Persona selector in topbar + localStorage/URL persist
4. Route guard + default landing redirects
5. Context bar + drawer defaults per persona
6. Scenario rail banner + optional screen emphasis
7. Tests + APP_FLOW.md update
```
