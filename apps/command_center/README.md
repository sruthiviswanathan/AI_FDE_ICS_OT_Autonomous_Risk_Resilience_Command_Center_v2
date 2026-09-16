# Command Center — APP-00 design pack

Design artifacts for the OT command-room workbench (APP-02 implementation).

| File | Purpose |
|------|---------|
| [APP_FLOW.md](APP_FLOW.md) | Journeys, workflows, navigation |
| [UI_WIREFRAMES.md](UI_WIREFRAMES.md) | ASCII wireframes, dashboard layout |
| [SCREEN_SPECIFICATIONS.md](SCREEN_SPECIFICATIONS.md) | Per-screen spec tied to PRD §12 |

**Constraints:** No chatbot-first UX. No execute-isolation or PLC/SIS controls. AI-disabled path is first-class.  
**Build contract:** `specs/PRD.md`, `specs/APP_ACCEPTANCE_TESTS.md`, read-only API (`src/ot_command/api.py`).
