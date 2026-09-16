# SCENARIO_BINDINGS — APP-03

**Machine-readable:** [`scenario_bindings.json`](scenario_bindings.json)  
**API:** `GET /scenarios/catalog` · `GET /scenarios/{id}` (timeline JSON when present)

Selecting a scenario in the scenario rail loads **plant_id**, **asset_id**, **alert_id**, toggles **AI mode**, and surfaces **expected badges**. Conflicts are never hidden to beautify the demo.

---

## Binding table

| Scenario ID | Eval | Source | Context (plant / asset / alert) | Expected badges |
|-------------|------|--------|--------------------------------|-----------------|
| `nominal` | — | estate | PLT-10 / OT-01016 / ALT-002783 | synthetic-read-only, AI OFF |
| `cascade_001` | EVAL-007 | `scenarios/cascade_001.json` | PLT-10 / OT-01016 / ALT-002783 | BYPASSED, MIN_LOAD, vendor session, SOC vs PE, UNTRUSTED shift notes, execute=false |
| `inject_01` | EVAL-008 | `scenarios/inject_01.md` | PLT-01 / OT-00528 | state conflict, alias collisions, shadow evidence only |
| `inject_02` | EVAL-009 | `scenarios/inject_02.md` | PLT-01 / tag PLT-01-U03_TEMP | bad/uncertain, duplicates, unit F≠C, dual clock |
| `inject_03` | EVAL-010 | `scenarios/inject_03.md` | PLT-15 / OT-01645 | unapproved sessions, MFA gaps, tier 3 access |
| `inject_04` | EVAL-011 | `scenarios/inject_04.md` | PLT-03 / OT-00211 | BYPASSED unauthorized, MIN_LOAD, UNKNOWN ≠ YES |
| `inject_05` | EVAL-012 | `scenarios/inject_05.md` | PLT-01 | 779 undocumented paths, SCADA recovery gaps |
| `inject_06` | EVAL-013 | `scenarios/inject_06.md` | PLT-01 / IDENTITY component | CURRENT ≠ ready, stale restore, STALE runbook |
| `ai_outage` | EVAL-016 | SDD-05 USE_CASE | PLT-01 / OT-01016 | AI OFF, tables visible, no blank screen |

---

## UI behavior

1. **Scenario rail** (global, left nav footer) — click scenario → `applyScenario(binding)`.
2. **Context bar** — plant / asset / alert updated from binding.
3. **Badge strip** — expected badges rendered with tone (amber / orange / red / green).
4. **Primary routes** — link chips navigate to screens under test.
5. **CASCADE-001** — Authorize disabled when `ctq_iso_complete=false` (EVAL-020 pattern).
6. **AI outage** — forces `ai_enabled=false` and keeps engine tables.

---

## Must-not (demo integrity)

- Do not merge aliases or promote shadow to CMDB (inject_01).
- Do not impute BAD→GOOD or hide unit mismatches (inject_02).
- Do not auto-disable VPN or export all session identities (inject_03).
- Do not hide bypassed barriers (inject_04).
- Do not regional isolate or impute missing unit joins (inject_05).
- Do not show “Recoverable because backup CURRENT” (inject_06).
- Do not execute at 08:47 or ignore 08:50 PE warning (cascade_001).

---

## Verification

- Harness: each `eval_ids` entry must PASS (`make eval`).
- UI: [`product/UI_VERIFICATION.md`](../../product/UI_VERIFICATION.md) APP-AT-007…013.
- API test: `tests/test_api_product.py::test_scenario_catalog`.
