# `ot_command.modern` — parallel path (no business logic here)

Repo 3.0 pointer. ENH-01…10 engines live in `ot_command.core`, **beside** `ot_command.legacy`, not as a rewrite of it.

## Rules
- Do not change `legacy_rank` / `legacy_recovery_ready` / `legacy_isolation_recommendation`.
- Do not add OT write APIs or isolate-execute tools.
- Untraced modules are out of scope (`traceability/TRACEABILITY.csv`).
- Isolation is never execute. CURRENT backup is not RecoveryReady. POST `/recommend` is a packet, not an OT action.

## As-built
See `AS_BUILT_C4.md` (canonical: `specs/as_built_c4.md`).
