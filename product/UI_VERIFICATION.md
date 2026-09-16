# UI verification (APP-02)

Browser MCP was not available. Verification used HTTP against local uvicorn (`AI_ENABLED=0`) plus pytest.

The workbench is React (`apps/command_center/src/`). FastAPI still serves `/ui` and the Vite build at `/ui/static/app.js`.

## Evidence used
Existing local uvicorn on `127.0.0.1:8001` (and `8000`). After UI edits: `cd apps/command_center && npm run build`.

## Checks executed (2026-09-16)

| Probe | Result |
|---|---|
| GET `/health` | 200 `mode=synthetic-read-only` `ai_enabled=false` `live_ot=false` `ui=/ui` |
| GET `/ui` | 200 React shell (`#root`, `type="module"` `/ui/static/app.js`); no `Execute Isolation` / `Write PLC` |
| GET `/ui/static/app.css` `/ui/static/app.js` | 200; JS `text/javascript` (React 18 bundled IIFE/ES) |
| GET `/ui/fixtures/command_center_fixtures.json` | 200 |
| GET `/ui/fixtures/scenario_bindings.json` | 200 |
| GET `/lookup?q=ALT-002783` | 200 |
| GET `/graph/slice?hops=4&plant_id=PLT-10` | 200 |
| GET `/identity/conflicts` | 200 |
| GET `/diagnostics` `/ops/slo` | 200 |
| `python scripts/check_sdd_gates.py` | `SDD_GATE_OK` (`index.html` + `static/app.js` still present) |
| `pytest tests/test_command_center_ui.py` | 11 passed (15 `data-screen` in `src/`, no execute controls) |
| full pytest | 87 passed, 3 xfailed (legacy XFAIL unchanged) |

Did not click through a real browser (no browser tool in this session). Hard-refresh `/ui` to pick up the module bundle.
