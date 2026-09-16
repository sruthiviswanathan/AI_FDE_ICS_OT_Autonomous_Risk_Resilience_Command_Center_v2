# UI verification (APP-02)

Browser MCP was not available. Verification used HTTP against local uvicorn (`AI_ENABLED=0`).

## Evidence used
`.venv\Scripts\python.exe -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000`

## Checks executed (2026-09-16)

| Probe | Result |
|---|---|
| GET `/health` | 200 `mode=synthetic-read-only` `ai_enabled=false` `live_ot=false` `ui=/ui` |
| GET `/ui` | 200, 15 `data-screen` sections, no `Isolate now` / `>Write PLC<` |
| GET `/ui/static/app.css` `/ui/static/app.js` | 200 |
| GET `/ui/fixtures/command_center_fixtures.json` | 200 `invented_fields=false` |
| GET `/access/sessions?plant_id=PLT-10` | 200 `change_remote_access_execute=false` `all_plants_export=false` |
| POST `/recommend` action=recommend | 200 `executed=false` `ot_action=false` rec=ABSTAIN (OT-01016 MIN_LOAD) |
| POST `/recommend` action=write_plc_logic | 200 `permit.allowed=false` `executed=false` |
| GET `/identity/conflicts` | winner=null, 5 alias collisions |
| GET `/recovery/PLT-01` | `recovery_ready=false` |
| GET `/risk/contextual?limit=200` | `cvss_is_sort_key=false`; VUL-00098 present (rank 138); VUL-00706 not in top 200 |

Did not click through a real browser (no browser tool in this session). Pytest `tests/test_command_center_ui.py` covers forbidden control labels.
