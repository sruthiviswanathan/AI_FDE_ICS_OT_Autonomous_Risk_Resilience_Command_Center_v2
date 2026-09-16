# Command Center (APP-02 / APP-03)

Synthetic **command-room workbench**, not a chatbot. **No live OT.** IsolationExecution does not exist. CURRENT backup is not RecoveryReady. Highest CVSS is not highest operational risk.

The workbench is **React only**. Edit `src/` (JSX/CSS). There is no hand-written vanilla JS in this tree.

| Path | Role |
|---|---|
| `src/` | React source (edit here) |
| `index.html` | Vite dev entry |
| `static/` | **Generated** by `npm run build` — do not edit `static/app.js` |
| `fixtures/` | Demo/scenario JSON for the workbench |

## Start the React app

API must be up (or `npm start` will launch it). From `apps/command_center`:

```powershell
npm install
npm start
```

That opens **http://127.0.0.1:5173** (Vite + React, with hot reload). API calls are proxied to uvicorn (`OT_API_ORIGIN`, default `http://127.0.0.1:8001`).

| Command | What it does |
|---|---|
| `npm start` / `npm run dev` | **Starts** the React UI at http://127.0.0.1:5173 |
| `npm run build` | Compiles `src/` into `static/app.js` for FastAPI `/ui`. Does not open a browser. |

Workshop / Docker without Node uses FastAPI **http://127.0.0.1:8000/ui** — run `npm run build` first so `static/app.js` exists (Docker image builds it automatically).

`GET /` is intentionally empty (404). The product surface is the React app (`npm start`) or `/ui`.

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

`PYTHONPATH=src` is required so `ot_command` imports from `src/`. `AI_ENABLED=0` is the default and the EVAL-016 path: tables stay visible. `AI_ENABLED=1` only attaches a **placeholder sentence** to the recommend packet. It does not start a model.

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

1. Header: `ICS/OT Command Room · synthetic · read-only`, pills `mode=synthetic-read-only` `live_ot=false` `explainer=omitted` (or `placeholder` — that is not a model).
2. **Scenario** select (APP-03): EVAL-001…006, inject_01…06, cascade_001, EVAL-014, EVAL-016. Expected badges vs struck-through must_not. Conflicts are not hidden (`SCENARIO_BINDINGS.md`).
3. Left nav: 15 PRD screens (Control Tower → Executive). **Work as** role landings (SOC / Process Eng / Safety / Ops / Exec / FDE) jump to the first useful screen.
4. **Look up** binds a session-local case (alias / asset / plant / alert / finding / tag). Collisions stay unmerged. Clear case returns to demo slices; estate conflicts stay visible.
5. Right **Provenance** panel on every view.
6. Process graph is drawn (hop-capped SVG). Incident screen shows the CASCADE analogue clock. Authority keeps a HITL queue of drafts (roles, not named people; no execute).
7. **Show explainer text** checkbox **off** by default. That is a placeholder sentence, not a chatbot.
8. Authority screen: **Draft packet** / **Submit control-demand text**. No Execute Isolation / Write PLC controls.

## Behaviour
- 15 PRD screens; provenance side panel on every view
- Session-local case via Look up / scenario rail (OPEN-012 durable correlation stays open)
- Role landings; graph drawing; CASCADE analogue timeline; HITL queue (no execute)
- Placeholder explainer checkbox default **off** (EVAL-016 tables remain). Env flag is still `AI_ENABLED`; the product is not an LLM.
- Draft packet via `POST /recommend` only; refuse path for PLC/SIS demand
- No Execute Isolation / Write PLC controls
- Inject rail = fixture replay (`inject_01`…`06`, cascade_001, explainer-outage EVAL-016)
- Scenario rail loads plant/asset/alert + expected/must_not badges. Conflicts are not hidden.
- Shift notes labelled UNTRUSTED
- Sessions: `GET /access/sessions` (not all-plants dump; not VPN disable)

No real OT connectors or secrets.
