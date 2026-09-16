# AGENTS.md

Treat this as a production brownfield discovery and modernization engagement, not a greenfield rewrite.

- Preserve evidence before changing behavior.
- Never assume CMDB, passive discovery, historian, SCADA, CMMS, SIEM or operator notes are authoritative by name alone.
- Separate **observed state**, **registered state**, **operational interpretation**, **safety state**, and **decision authority**.
- Do not connect to real OT systems or produce code that writes to controllers.
- Any consequential target-state action must be bounded by policy, safety constraints and human authority.
- Build tests/evals before introducing agentic automation.
- `restricted_answer_key/` is out-of-bounds for participants unless explicitly authorized.
- Specs in `specs/` and ADRs in `adrs/` constrain code. Do not invent ADRs. Untraced modules are out of scope (`traceability/TRACEABILITY.csv`).
- Do not reopen SDD-09. Do not change `legacy_*` behavior, delete XFAIL tests, or clean `data/` contradictions.

Suggested path: SDD-01…15 (done) → ENH-01…10 (parallel modern engines) → PRD-01 → APP-01/02 → REL-01…04.

Discovery order if re-entering the estate: inventory → topology → asset identity → telemetry quality → process dependencies → cyber/safety context → recovery dependencies → decision/authority model → evals → intervention.
