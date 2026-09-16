# ICS/OT Command Center — APP-02

React operator workbench (control-room density, not chatbot-first). Consumes the read-only product API only — no acceptance-test fixtures at runtime.

## Design pack (APP-00)

| File | Purpose |
|------|---------|
| [APP_FLOW.md](APP_FLOW.md) | Journeys, workflows, navigation |
| [UI_WIREFRAMES.md](UI_WIREFRAMES.md) | Layout and card hierarchy |
| [SCREEN_SPECIFICATIONS.md](SCREEN_SPECIFICATIONS.md) | 15 PRD screens |
| [DATA_LAYER.md](DATA_LAYER.md) | APP-01 runtime data abstraction |
| [SCENARIO_BINDINGS.md](SCENARIO_BINDINGS.md) | APP-03 golden scenario rail |

## Scenario rail (APP-03)

Left nav **Scenario rail** loads `GET /scenarios/catalog`. Selecting a scenario applies plant/asset/alert context and expected badges (`scenario_bindings.json`). Conflicts are never hidden.

## Prerequisites

Complete **one-time backend setup** from the repo root first:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

- **Python 3.11+** — FastAPI backend (`src/ot_command/api.py`)
- **Node.js 18+** and **npm** — Vite + React frontend (this directory)

See also the root [`README.md`](../../README.md) for diagnostics, tests, and CI commands.

## Run backend (BE)

From the **repo root** with the virtual environment activated:

```bash
# Windows (PowerShell)
$env:PYTHONPATH="src"
python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000 --reload

# Linux/macOS
PYTHONPATH=src python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000 --reload
```

Or: `make run` from the repo root.

Confirm the API before starting the UI:

```bash
curl http://127.0.0.1:8000/health
```

## Run frontend (FE)

**Development** (hot reload + API proxy) — use **two terminals**:

```bash
# Terminal 1 — backend (repo root)
PYTHONPATH=src python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000

# Terminal 2 — frontend (this directory)
cd apps/command_center
npm install
npm run dev
```

Open **http://127.0.0.1:5173** — Vite proxies `/api/*` to the backend (default `http://127.0.0.1:8000`).

| Script | Purpose |
|--------|---------|
| `npm run dev` | Dev server on port 5173 with `/api` proxy |
| `npm run build` | Production bundle → `dist/` |
| `npm run preview` | Preview the production build locally |

Environment variables (see `.env.example`):

- `VITE_API_URL=/api` — fetch prefix in dev (default in `.env.development`)
- `VITE_DEV_API_TARGET` — backend URL for the Vite proxy (override in `.env.development.local`)

**Port conflict (Windows):** If `--port 8000` fails (`WinError 10013`) or `/health` lacks `api_version`, another service may own 8000. Run BE on 8001 and create `.env.development.local`:

```env
VITE_DEV_API_TARGET=http://127.0.0.1:8001
```

Restart `npm run dev` after changing env files.

## Integrated mode (BE serves built FE)

Single port — no Vite dev server:

```bash
cd apps/command_center && npm install && npm run build
cd ../..
PYTHONPATH=src python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000**

## Stack

- React 18 + React Router 6 + Vite 5 + TypeScript
- API client: `src/api/client.ts` → `contracts/openapi_command_center.yaml`
- Global: incident context bar, AI toggle (default OFF), provenance/retrieval drawer

## Constraints

- No execute isolation, PLC, SIS, or bypass controls
- AI-disabled path shows deterministic engine tables (ADR-12)
- Shift notes and inject narrative marked UNTRUSTED
- UI verification: [product/UI_VERIFICATION.md](../../product/UI_VERIFICATION.md)
