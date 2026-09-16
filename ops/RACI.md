# RACI (workshop)

People are **roles**, not named Authorizers (OPEN-001). This table does not grant OT execute.

| Activity | SOC | Process Eng | Safety/SIS | VP Ops | FDE / platform | Incident Analyst (agent) |
|---|---|---|---|---|---|---|
| Observe / correlate / summarize | A | C | C | I | C | R (tier 0) |
| Draft IsolationRecommendation | C | C | C | I | R | R (tier 1 draft) |
| Authorize tier ≥3 | C | C | C | A* | I | **None** |
| Execute isolate / PLC / SIS | — | — | — | — | — | **Forbidden** |
| Recovery orchestration | I | C | C | A | I | Observe blockers only |
| Eval / prompt change | I | I | I | I | A | — |
| AI-disabled war room | A | A | A | A | C | Off |

\*Authorize remains unnamed until OPEN-001; software still must not execute after a click.

R = responsible · A = accountable · C = consulted · I = informed.
