# BC / DR (tabletop)

Workshop continuity for the **advisory** service, not a plant outage.

- RecoveryReady requires restore-test evidence, CURRENT runbook, and `dependency_verified=YES`. CURRENT backup is not ready (ADR-05).
- Restore-test day SLA is OPEN-006/022 — do not invent 90 days.
- No live restore orchestration from this API.
- Chaos drill = fixture replay (`scenarios/inject_06.md`, EVAL-013) + war-room checklist.
- Bronze `data/` remains the evidence store; do not promote shadow spreadsheets.

Plant DR remains site ownership. This repo does not connect to controllers.
