# Command Center (APP-02 / APP-03)

Synthetic **command-room workbench**, not a chatbot. **No live OT.** IsolationExecution does not exist. CURRENT backup is not RecoveryReady. Highest CVSS is not highest operational risk.

Open this when the API is up: **http://127.0.0.1:8000/ui**

`GET /` is intentionally empty (404). The product surface is `/ui`.

## Run (Windows PowerShell)

From the repository root (`AI_FDE_ICS_OT_Autonomous_Risk_Resilience_Command_Center_v2`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$env:PYTHONPATH = "src"
$env:AI_ENABLED = "0"
python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

Without activating the venv:

```powershell
$env:PYTHONPATH = "src"
$env:AI_ENABLED = "0"
.\.venv\Scripts\python.exe -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

Then:

| URL | What it is |
|---|---|
| http://127.0.0.1:8000/ui | Command room (15 screens + scenario rail) |
| http://127.0.0.1:8000/health | `mode: synthetic-read-only`, `ai_enabled`, `live_ot: false` |
| http://127.0.0.1:8000/docs | FastAPI OpenAPI (advisory GETs + `POST /recommend`) |

Stop with `Ctrl+C` in the uvicorn terminal.

If port 8000 is already bound, either use that existing process or pick another port:

```powershell
python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8001
```

`PYTHONPATH=src` is required so `ot_command` imports from `src/`. `AI_ENABLED=0` is the default and the EVAL-016 path: tables stay visible; the explainer stays off unless the UI checkbox is turned on.

## Run (Linux / macOS)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
export AI_ENABLED=0
python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

Makefile equivalent (Git Bash / WSL / make available): `make run`.

## Docker (advisory only)

```bash
docker build -t ot-command .
docker run --rm -p 8000:8000 -e AI_ENABLED=0 ot-command
```

No model credentials. No OT connectors. Image CMD is uvicorn on `0.0.0.0:8000`.

## First-time data check (optional)

Fixtures under `apps/command_center/fixtures/` are already committed. To confirm the estate seed and regenerate the demo slice:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts\generate_data.py --check-only
.\.venv\Scripts\python.exe scripts\generate_command_center_fixtures.py
```

UI tests:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m pytest -q tests\test_command_center_ui.py
```

## What you should see

1. Header: `ICS/OT Command Room · synthetic · read-only`, pills `mode=synthetic-read-only` `live_ot=false` `ai_enabled=false`.
2. **Scenario** select (APP-03): EVAL-001…006, inject_01…06, cascade_001, EVAL-014, EVAL-016. Expected badges vs struck-through must_not. Conflicts are not hidden (`SCENARIO_BINDINGS.md`).
3. Left nav: 15 PRD screens (Control Tower → Executive).
4. Right **Provenance** panel on every view.
5. AI explainer checkbox **off** by default.
6. Authority screen: **Draft packet** / **Submit control-demand text**. No Execute Isolation / Write PLC controls.

## Behaviour
- 15 PRD screens; provenance side panel on every view
- AI explainer checkbox default **off** (EVAL-016 tables remain)
- Draft packet via `POST /recommend` only; refuse path for PLC/SIS demand
- No Execute Isolation / Write PLC controls
- Inject rail = fixture replay (`inject_01`…`06`, cascade_001, AI outage)
- Scenario rail loads plant/asset/alert + expected/must_not badges. Conflicts are not hidden.
- Shift notes labelled UNTRUSTED
- Sessions: `GET /access/sessions` (not all-plants dump; not VPN disable)

No real OT connectors or secrets.
