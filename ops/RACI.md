# RACI — Synthetic ICS/OT Command Center (Repo 3.0)

**Scope:** Workshop / synthetic estate only. No live plant operations from this repository.

Roles are **unnamed placeholders** until OPEN-001 closes (named Authorizer).

| Activity | FDE / Platform | SOC / OT Security | Process Engineer | Safety / SIS Owner | VP Operations | Plant OT |
|----------|----------------|-------------------|------------------|--------------------|--------------|----------|
| Identity reconciliation review | R/A | C | C | I | I | C |
| Telemetry quality triage | R/A | C | C | I | I | C |
| Contextual risk ranking | R/A | C | C | C | I | I |
| Isolation **recommendation** draft | R | C | C | C | A | I |
| Isolation **execute** | — | — | — | — | A | R |
| Recovery readiness assessment | R/A | I | C | I | A | C |
| Vendor session review | R | A | I | I | C | I |
| Eval harness / assurance | R/A | I | I | I | C | I |
| AI feature flag (AI_ENABLED) | R/A | C | I | I | A | I |
| Production deployment decision | C | C | C | C | A | C |

**Legend:** R = Responsible · A = Accountable · C = Consulted · I = Informed

**Hard rules (ADR-04, ADR-11, ADR-12):**
- Software in this repo **never** executes tier 3/4 OT actions.
- `POST /recommend` returns packets only; human authority is out-of-band (OPEN-001).
- AI-disabled path (`AI_ENABLED=0`) must remain operable (EVAL-016).
