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

## Local run

**Development** (hot reload + API proxy):

```bash
# Terminal 1 — from repo root
PYTHONPATH=src python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000

# Terminal 2
cd apps/command_center
npm install
npm run dev
```

Open http://127.0.0.1:5173 — Vite proxies `/api/*` to port 8000.

**Integrated** (single port):

```bash
cd apps/command_center && npm install && npm run build
cd ../..
PYTHONPATH=src python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000

## Stack

- React 18 + React Router 6 + Vite 5 + TypeScript
- API client: `src/api/client.ts` → `contracts/openapi_command_center.yaml`
- Global: incident context bar, AI toggle (default OFF), provenance/retrieval drawer

## Constraints

- No execute isolation, PLC, SIS, or bypass controls
- AI-disabled path shows deterministic engine tables (ADR-12)
- Shift notes and inject narrative marked UNTRUSTED
- UI verification: [product/UI_VERIFICATION.md](../../product/UI_VERIFICATION.md)
