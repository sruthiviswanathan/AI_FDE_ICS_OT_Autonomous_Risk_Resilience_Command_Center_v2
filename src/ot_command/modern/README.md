# `ot_command.modern` — parallel path (empty of business logic)

Repo 2.0 placeholder. ENH-01…10 implement engines **beside** `ot_command.legacy`, not as a rewrite of it.

## Rules
- Do not change `legacy_rank` / `legacy_recovery_ready` / `legacy_isolation_recommendation`.
- Do not add OT write APIs or isolate-execute tools.
- Untraced modules are out of scope (`traceability/TRACEABILITY.csv`).
- Engines in `ot_command.core`: identity, telemetry, risk, containment, recovery, authority, agent, guardrails. Isolation is never execute. CURRENT backup is not RecoveryReady. POST /recommend is a packet, not an OT action.

## Planned modules (not present yet)
identity.py · telemetry.py · risk.py · safety.py · recovery.py · graph_slice.py · packet.py · traces.py · ai_disabled.py · provenance.py · authority.py · agent.py
