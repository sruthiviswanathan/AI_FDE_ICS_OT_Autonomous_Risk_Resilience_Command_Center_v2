# Runtime Data Layer — APP-01

The command center UI must consume the **read-only product API** (`src/ot_command/api.py`), which loads estate data at runtime via `src/ot_command/core/data_layer.py`.

## Canonical sources (playbook logical names)

| Logical name | Repo path | API introspection |
|--------------|-----------|-------------------|
| `assets.csv` | `data/raw/assets.csv` | `GET /data/sources` |
| `telemetry.jsonl` | `data/telemetry/tag_telemetry.jsonl` | same |
| `vulnerabilities.csv` | `data/raw/vulnerabilities.csv` | same |
| `safety_barriers.csv` | `data/raw/safety_barriers.csv` | same |
| `recovery_readiness.csv` | `data/raw/recovery_readiness.csv` | same |
| `vendor_sessions.csv` | `data/raw/remote_access_sessions.csv` | same |

Derived views are built at request time (cached in-process): assets-by-id, recovery-by-plant, degraded barriers, vendor session anomalies, estate summary.

## UI rule

**Do not depend on acceptance-test fixtures** under `tests/` or `evals/` for runtime data. Fixtures are for harness/APP-AT verification only.

## Product API

- OpenAPI: `contracts/openapi_command_center.yaml`
- Health: `GET /health` → `{ status, mode, api_version }`
- Estate summary: `GET /data/views/estate`
- Vendor sessions: `GET /data/views/vendor-sessions`

Legacy asset contracts remain at `contracts/asset_api_v1.yaml` and `contracts/asset_api_v2.yaml`.

## Local run

```bash
make run
# API at http://127.0.0.1:8000/docs
```

Optional override: `OT_DATA_ROOT=/path/to/estate` (defaults to repo root).
