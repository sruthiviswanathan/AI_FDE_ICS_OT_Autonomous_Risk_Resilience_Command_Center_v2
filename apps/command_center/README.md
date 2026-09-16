# Command Center (APP-02)

Synthetic **command-room workbench**, not a chatbot. **No live OT.** IsolationExecution does not exist. CURRENT backup is not RecoveryReady. Highest CVSS is not highest operational risk.

## Local run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
set PYTHONPATH=src
set AI_ENABLED=0
python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/ui

Health: http://127.0.0.1:8000/health (`mode: synthetic-read-only`, `ai_enabled`, `live_ot: false`).

Regenerate fixtures (APP-01):

```bash
PYTHONPATH=src python scripts/generate_command_center_fixtures.py
```

## Behaviour
- 15 PRD screens; provenance side panel on every view
- AI explainer checkbox default **off** (EVAL-016 tables remain)
- Draft packet via `POST /recommend` only; refuse path for PLC/SIS demand
- No Execute Isolation / Write PLC controls
- Inject rail = fixture replay (`inject_01`…`06`, cascade_001, AI outage)
- Shift notes labelled UNTRUSTED
- Sessions: `GET /access/sessions` (not all-plants dump; not VPN disable)

No real OT connectors or secrets.
