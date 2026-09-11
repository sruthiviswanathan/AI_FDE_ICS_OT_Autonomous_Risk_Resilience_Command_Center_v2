# AGENTS.md

Treat this as a production brownfield discovery and modernization engagement, not a greenfield rewrite.

- Preserve evidence before changing behavior.
- Never assume CMDB, passive discovery, historian, SCADA, CMMS, SIEM or operator notes are authoritative by name alone.
- Separate **observed state**, **registered state**, **operational interpretation**, **safety state**, and **decision authority**.
- Do not connect to real OT systems or produce code that writes to controllers.
- Any consequential target-state action must be bounded by policy, safety constraints and human authority.
- Build tests/evals before introducing agentic automation.
- `restricted_answer_key/` is out-of-bounds for participants unless explicitly authorized.

Suggested path: inventory → topology → asset identity → telemetry quality → process dependencies → cyber/safety context → recovery dependencies → decision/authority model → evals → intervention.
