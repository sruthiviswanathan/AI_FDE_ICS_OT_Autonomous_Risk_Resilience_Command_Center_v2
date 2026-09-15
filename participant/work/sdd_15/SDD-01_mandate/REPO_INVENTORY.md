# SDD-01 — Repo inventory (as-is, no modernization)

**Prompt:** SDD-01 | OM-1  
**Date:** 2026-09-15  
**Does not conclude:** target architecture, identity winner, or that packaging version `2.0.0` means the product logic is modernized.

---

## Evidence used / assumptions / unknowns / what this artifact did not conclude

### Evidence used

- Directory listing of `data/`, `contracts/`, `src/`, `tests/`, `evals/`, `scenarios/` (Glob + direct reads).
- Module reads: `api.py`, `cli.py`, `diagnostics.py`, `repository.py`, `legacy/risk.py`, `core/policy.py`, `__init__.py`.
- Contracts: `asset_api_v1.yaml`, `asset_api_v2.yaml`, `telemetry_event_schema.json` vs first records of `tag_telemetry.jsonl`.
- Tests: `tests/test_baseline.py`, `tests/test_known_legacy_defects.py`; `VERIFICATION.md` pytest block; `participant/work/00_setup/phase0_check.md` (3 passed, 3 xfailed).
- Packaging: `pyproject.toml` version `2.0.0`; `api.py` FastAPI version `2.0.0`; `data/manifest.json` `repo_version` `2.0.0`; `__init__.py` `__version__ = "0.1.0"`; `docs/07_v2_audit_and_changelog.md` claims version metadata normalized to 2.0.0.
- `scripts/verify_repo.py` required files: README, AGENTS, requirements, pyproject, Dockerfile, Makefile, `data/manifest.json` — all exist. `data/ot_legacy.db` exists (614400 bytes); 6 tables; integrity ok.
- `evals/README.md` eval dimensions vs actual tests.

### Assumptions

- Inventory describes **this working tree**, not a future Repo 2.0 layout (`specs/` is created at SDD-15).
- `.venv/` and `.pytest_cache/` are local environment, not engagement evidence.

### Unknowns

- Whether `__version__` 0.1.0 vs 2.0.0 is an intentional brownfield packaging contradiction or an accidental leftover after `docs/07` remediation (`OPEN-010`).
- Whether SQLite is generated from CSV or independently maintained (`OPEN-007`).
- Whether FastAPI is intended to implement asset API v1, v2, both, or neither (`OPEN-009` related).

### What this artifact did not conclude

- Did not change code, tests, or data.
- Did not treat XFAIL as accidental failure; they are documented product defects (`VERIFICATION.md`).
- Did not select a contract as canonical.

---

## 1. Tree (engagement-relevant; not `.venv`)

```text
AI_FDE_ICS_OT_Autonomous_Risk_Resilience_Command_Center_v2/
  AGENTS.md
  README.md
  VERIFICATION.md
  LICENSE.txt
  pyproject.toml
  requirements.txt
  Dockerfile
  Makefile
  .env.example
  checksums.sha256
  contracts/
    asset_api_v1.yaml
    asset_api_v2.yaml
    telemetry_event_schema.json
  data/
    manifest.json
    ot_legacy.db
    raw/          (12 files: assets, aliases, edges, units, deps, vulns, barriers,
                   work_orders, remote_access, recovery, cyber_alerts, enterprise_events.jsonl)
    reference/    (plants.csv, vendors.csv, tags.csv)
    telemetry/    (tag_telemetry.jsonl)
    shadow/       (ot_asset_inventory_FINAL_v8.csv, risk_acceptance_tracker.csv, shift_handover_email.txt)
  docs/           (01–07)
  evals/          (README.md, golden_cases.jsonl)
  scenarios/      (cascade_001.json, inject_01.md … inject_06.md)
  src/ot_command/
    __init__.py
    api.py
    cli.py
    diagnostics.py
    repository.py
    core/policy.py
    legacy/risk.py
  tests/
    test_baseline.py
    test_known_legacy_defects.py
  scripts/
    generate_data.py      (--check-only only; does not regenerate)
    verify_repo.py
  tools/
    inspect_repo.py       (prints run_diagnostics)
  participant/
    CHALLENGE_BRIEF.md
    DISCOVERY_CHECKLIST.md
    work/00_setup/phase0_check.md
    work/sdd_15/          (this SDD-01 output)
```

**Counts already frozen in Phase 0 / VERIFICATION.md:** diagnostics 14 keys; pytest 3 passed + 3 xfailed.

`scripts/generate_data.py --check-only` (Phase 0): `{"seed": 20260910, "missing": [], "status": "ok"}`. The script **does not generate** data; it only checks `manifest.json` paths exist.

---

## 2. Module responsibilities (as-is)

| Module | Responsibility today | Does not do |
|---|---|---|
| `repository.py` | `rows(rel)` CSV DictReader; `jsonl(rel)` JSON lines; ROOT = repo root | Auth, schema validation, provenance |
| `diagnostics.py` `run_diagnostics()` | 14 heuristic counters over assets, aliases, edges, telemetry, safety, work, access, recovery | Vulns, process units, alerts, enterprise events, shadow, restore-test days |
| `legacy/risk.py` | `legacy_risk_score`, `legacy_rank` (CVSS desc), `legacy_recovery_ready` (backup CURRENT), `legacy_isolation_recommendation` (HIGH/CRITICAL → ISOLATE) | Process, safety, reachability, authority |
| `core/policy.py` | `ACTION_TIERS` dict; `requires_human_approval` if tier ≥ 3 | Not imported by isolation/rank/recovery |
| `api.py` | FastAPI title `Synthetic ICS/OT Risk & Resilience API` v2.0.0; `GET /health`; `GET /diagnostics` | No `/assets`, no write routes |
| `cli.py` | `python -m ot_command.cli diagnostics` | Other commands |
| `__init__.py` | `__version__ = "0.1.0"` | — |

**API surface (complete):**

- `GET /health` → `{'status':'ok','mode':'synthetic-read-only'}`
- `GET /diagnostics` → `run_diagnostics()` JSON

Dockerfile CMD runs uvicorn on 0.0.0.0:8000. `.env.example` has `APP_HOST`, `APP_PORT`, `LOG_LEVEL` and states no production credentials.

---

## 3. Contract drift

### 3.1 Asset API v1 vs v2 (unimplemented)

| | `contracts/asset_api_v1.yaml` | `contracts/asset_api_v2.yaml` |
|---|---|---|
| Title | Legacy Asset API v1 | Legacy Asset API v2 |
| Path | `/assets/{id}` | `/ot-assets/{asset_id}` |
| Field convention (comment only) | `assetId`, `fwVersion`, `operationalState` | `asset_id`, `firmware`, `observed_state` |
| Implemented in `api.py`? | **No** | **No** |

`data/raw/assets.csv` uses `asset_id`, `firmware`, `observed_state` (v2-like names) **and also** `registered_state` (not in either comment). Five-state split is therefore **not** represented in either contract.

### 3.2 Telemetry schema vs records

`contracts/telemetry_event_schema.json` **required:** `event_id`, `tag_id`, `event_time`, `value`, `unit`, `quality`.  
**properties:** those six only. **Missing from schema:** `ingest_time`, `source`, `asset_id`.

Actual `data/telemetry/tag_telemetry.jsonl` record `TEL-00000000`:

- has `asset_id` = `OT-00058`
- has `ingest_time` = `2026-09-01T00:00:14` vs `event_time` = `2026-09-01T00:00:00`
- has `source` = `HISTORIAN`

EVAL-004 stub requires event vs ingest/received time. The **contract cannot express** the temporal fields the eval and the data already use.

`data/raw/enterprise_events.jsonl` uses `received_time` (not `ingest_time`). EVT-0000001: `event_time` `2026-10-05T17:48:00` vs `received_time` `2026-10-05T17:47:35` (received **before** event).

### 3.3 Version metadata split

| Location | Value |
|---|---|
| `pyproject.toml` `[project].version` | `2.0.0` |
| `src/ot_command/api.py` FastAPI `version=` | `2.0.0` |
| `data/manifest.json` `repo_version` | `2.0.0` |
| `src/ot_command/__init__.py` `__version__` | **`0.1.0`** |
| `docs/07_v2_audit_and_changelog.md` | Claims version metadata normalized to 2.0.0 |

This is inventory evidence. Canonical product version is **OPEN-010**. Do not silently “fix” `__version__` in SDD-01.

### 3.4 Diagnostics vs SQLite vs CSV

`run_diagnostics()` reads **CSV/JSONL**, not `data/ot_legacy.db`. SQLite tables duplicate six CSV grains with matching row counts. Not proven independent.

---

## 4. Test taxonomy

### 4.1 Passing (3) — `tests/test_baseline.py`

| Test | Asserts | What it does **not** prove |
|---|---|---|
| `test_diagnostics_detect_seeded_imperfections` | alias_collisions > 0; undocumented_network_paths > 0; duplicate_telemetry_packets > 0 | Exact VERIFICATION.md counts; identity reconciliation |
| `test_safety_critical_actions_require_human_approval` | `write_plc_logic` and `modify_sis` require approval; `summarize` does not | Isolation recommendation gated; unknown actions; docs/06 verbs absent from dict |
| `test_recovery_gaps_exist` | `recovery_unverified_dependencies` > 0 | That CURRENT backup is not treated as ready (that is XFAIL) |

### 4.2 Expected failure / XFAIL strict (3) — `tests/test_known_legacy_defects.py`

| Test | Reason string | Legacy behavior preserved |
|---|---|---|
| `test_contextual_risk_should_outrank_highest_cvss` | ranking uses CVSS alone | `legacy_rank` sorts by `cvss`; fixture A cvss 9.8 LOW unreachable vs B 6.5 CRITICAL reachable — A still wins |
| `test_stale_restore_test_should_not_be_recovery_ready` | trusts backup flag | `legacy_recovery_ready('CURRENT')` is True |
| `test_high_alert_should_not_always_trigger_isolation` | safety-blind | `legacy_isolation_recommendation('CRITICAL')` == `ISOLATE` |

Phase 0 / VERIFICATION.md: **3 passed, 3 xfailed**. These are product defects to keep visible until Repo 3.0 remediations, not to delete now.

### 4.3 Missing tests (eval dimensions in `evals/README.md` with no pytest)

| Dimension | Stub only? | Executable test? |
|---|---|---|
| Identity correctness | EVAL-001 | **No** |
| Evidence grounding | listed in README | **No** |
| Temporal correctness | EVAL-004 | **No** |
| Unit correctness | README; diagnostics counts 47 TEMP mismatches | **No unit test** |
| Process-context correctness | README | **No** |
| Safety-policy compliance | EVAL-003; XFAIL isolation | No **passing** modern isolator |
| Authority enforcement | EVAL-006; baseline PLC/SIS | No test that isolation requires approval |
| Tool trajectory / side effects | README | **No** |
| Uncertainty communication | README | **No** |
| Recovery reasoning | EVAL-005; XFAIL backup | No passing recovery graph test |
| Latency and cost | README | **No** |
| `GET /health` | — | **No** |
| Asset API v1/v2 | contracts exist | **No** (routes missing) |
| Inject 01–06 | markdown titles | **No** harness |
| CASCADE-001 | JSON timeline | **No** |

Golden cases `EVAL-001`…`EVAL-006` exist as JSONL rows with `must_include` / `must_not`. There is **no runner**. Expanding them is later (SDD-08 / ENH-09), not this prompt.

---

## 5. What diagnostics measure vs what files exist (gap list, not a design)

| File exists | Used by `run_diagnostics()`? |
|---|---|
| assets, aliases, edges, telemetry, safety, work_orders, remote_access, recovery | Yes |
| vulnerabilities, process_units, process_dependencies, cyber_alerts, enterprise_events | **No** |
| plants, vendors, tags | **No** |
| shadow spreadsheet, risk tracker, shift email | **No** |
| SQLite copy | **No** |
| `recovery_readiness.last_restore_test_days` | **No** (file used; this field unused) |
| `safety_barriers.bypass_authorized` | **No** |

This is current-state inventory for SDD-02, not a proposed architecture.

---

## 6. Safety surface of this codebase

| Question | Evidence |
|---|---|
| PLC write route? | None in `api.py` |
| Live OT connector? | None; README + `.env.example` |
| Isolation execute? | String `"ISOLATE"` in `legacy_isolation_recommendation` only |
| Policy enforced on recommendations? | **No** |

---

## 7. Inventory gate

SDD-01 required this file: tree, module responsibilities, contract drift (asset v1/v2; telemetry missing ingest_time/source/asset_id), test taxonomy (pass vs XFAIL vs missing).

**PASS** as inventory. No code modernized.
