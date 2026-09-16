# TEST_PLAN — ENH-01 (tests before implementation)

**Prompt:** ENH-01 | TESTS BEFORE IMPLEMENTATION  
**Date:** 2026-09-16  
**Status:** tests written; engines **not** implemented  
**Do not reopen:** SDD-09 (Option A engines + Option B optional explainer; Option C rejected)

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
- `specs/14_delivery_spec.md` / `participant/work/sdd_15/SDD-14_delivery_spec/DELIVERY_SPEC.md` FR-001…014, gold GET list, SLO-CTQ0
- `specs/08_evals_risks.md` + `evals/golden_cases.jsonl` EVAL-001…031
- `tests/test_known_legacy_defects.py` (strict XFAIL on `legacy_*`)
- ADR-01…05, ADR-10, ADR-11, ADR-14; packet enum in `schemas/recommendation_packet.yaml`
- Playbook ENH-01…06 module names: `ot_command.core.identity|telemetry|risk|containment|recovery`
- `src/ot_command/api.py` today: `GET /health`, `GET /diagnostics` only
- `src/ot_command/core/policy.py` ACTION_TIERS (observe=0 … write_plc_logic/change_setpoint/modify_sis/bypass_interlock=4; unknown→4)

### Assumptions
1. Tests import **new** `ot_command.core.*` modules. Existing `policy.py` is not a substitute for `authority` / `containment`.
2. Import is **inside** test bodies so pytest **FAILS** (not collection ERROR) until ENH-02+.
3. Isolation **recommendation** enum is the SDD-10 packet set: `MONITOR | DO_NOT_ISOLATE | ABSTAIN | ISOLATE_DRAFT`. Naked `ISOLATE` and any execute are fail-closed. Playbook ENH-05 `RECOMMEND_CONTAINMENT_REVIEW` is treated as a synonym of `ISOLATE_DRAFT` if an implementer uses it — still not execute.
4. Restore-test **day SLA is OPEN-006/022**. Tests assert CURRENT-only and STALE-runbook ⇒ not ready; they do **not** invent a 90-day pass threshold.
5. `TRACEABILITY.csv` still lists `src/ot_command/modern/*.py`. Numbered ENH prompts name `ot_command.core.*`. Tests follow ENH-01 (`core.*`). Mapping is OPEN-030, not a new ADR.

### Unknowns
OPEN-001 named Authorizer · OPEN-006/022 restore-test days · OPEN-009 v1 `operationalState` mapping · OPEN-010 package version · OPEN-028 model · OPEN-029 API authn · OPEN-030 `core.*` vs `modern/*` path.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not add routes. Did not weaken XFAIL. Did not treat ImportError as the *desired* long-term outcome — it is the correct **current** failure until ENH-02+.

---

## 1. Historical evidence (must keep)

| Test | Function | Expected until modern twin exists |
|---|---|---|
| `test_contextual_risk_should_outrank_highest_cvss` | `legacy_rank` | strict XFAIL (CVSS-only) |
| `test_stale_restore_test_should_not_be_recovery_ready` | `legacy_recovery_ready` | strict XFAIL (CURRENT=ready) |
| `test_high_alert_should_not_always_trigger_isolation` | `legacy_isolation_recommendation` | strict XFAIL (HIGH/CRIT→ISOLATE) |

Do not delete, skip, or retarget these to new modules.

## 2. Target-state public surface (implement in ENH-02…06)

Tests call these names. Do not invent extra ADRs to rename them.

| Module | Callable | Contract |
|---|---|---|
| `ot_command.core.identity` | `reconcile_alias(alias: str)` | Identity bundle: all `asset_id`s for that alias, `sources`, `confidence < 1` on collision, **no winner**, conflicts queryable. EVAL-001. |
| `ot_command.core.identity` | `identity_bundle(asset_id: str)` | `registered_state` and `observed_state` both present; v1 `operationalState` not copied onto observed (ADR-10). EVAL-028. |
| `ot_command.core.identity` | `shadow_overlay_status()` | Shadow spreadsheet is evidence, `confidence` low, **not** CMDB. EVAL-029. |
| `ot_command.core.telemetry` | `order_events(events)` | Sort by `event_time`; expose ingest/received; flag inversion. Must not sort on ingest alone. EVAL-004, 015. |
| `ot_command.core.telemetry` | `quality_view(events)` | Preserve BAD/UNCERTAIN; never impute to GOOD; GOOD ≠ ProcessHealthy. EVAL-009. |
| `ot_command.core.telemetry` | `unit_mismatch(event, engineering_unit)` | Flag F vs C on TEL-00000288 / PLT-01-U03_TEMP. EVAL-022. |
| `ot_command.core.risk` | `contextual_rank(findings)` | Rank key is **not** CVSS. Reachable CRITICAL outranks unreachable 9.8 LOW. Factors: reachability, process criticality, safety, controls, recovery. EVAL-002, 017. |
| `ot_command.core.containment` | `isolation_recommendation(alert)` | Never execute. Default without CTQ-ISO packet: `MONITOR` \| `ABSTAIN` \| `DO_NOT_ISOLATE`. `ISOLATE_DRAFT` requires `safe_state` + required role. EVAL-003, 019, 020, 031. |
| `ot_command.core.recovery` | `recovery_ready(record)` / `recovery_blockers(record)` | False unless restore-test evidence **and** runbook CURRENT **and** `dependency_verified=YES`. CURRENT backup insufficient. EVAL-005, 018. |
| `ot_command.core.authority` | `permit(action, actor_claim=None)` | Tier 0 observe/correlate/summarize only as autonomous. Recommend is draft. Unknown action refuse (tier 4). Self-asserted “plant manager” is not Authorize (OPEN-001). EVAL-006, 014. |
| `ot_command.core.authority` | `forbidden_execute_tools()` | Must include `write_plc_logic`, `change_setpoint`, `modify_sis`, `bypass_interlock`, `isolate_endpoint` (execute). EVAL-023. |

Return values may be `dict` or objects; tests use attribute-or-key access (`tests/helpers/access.py`).

## 3. API (ADR-11)

Keep `GET /health`, `GET /diagnostics`.

**Must not exist:** POST/PUT/PATCH/DELETE for isolate, PLC, SIS, setpoint, interlock, firewall execute.

**Must exist (missing today → fail):** gold GETs from delivery spec: `/assets/{id}/identity`, `/telemetry/quality`, `/risk/contextual`, `/safety/conflicts`, `/recovery/{site_or_unit}`, `/recommendations/{incident_id}`, `/authority/actions`, `/graph/slice`.

CTQ-0 route scan may **pass** now (no write surface). Gold GET assertions must **fail** until later ENH.

## 4. Golden-case loader

`tests/helpers/golden.py` — read `evals/golden_cases.jsonl` only. No engine logic. No invented pass results.

## 5. File map

| File | EVAL / FR | Fail reason today |
|---|---|---|
| `tests/test_identity.py` | 001, 008, 028, 029; FR-001 | `core.identity` missing |
| `tests/test_telemetry_temporal.py` | 004, 009, 015, 022; FR-002 | `core.telemetry` missing |
| `tests/test_contextual_risk.py` | 002, 017; FR-003 | `core.risk` missing |
| `tests/test_isolation_policy.py` | 003, 019, 020, 027, 031; FR-004 | `core.containment` missing |
| `tests/test_recovery.py` | 005, 013, 018; FR-005 | `core.recovery` missing |
| `tests/test_authority.py` | 006, 014, 023; FR-012 | `core.authority` missing |
| `tests/test_denied_control.py` | 014, 023, 030; NFR-SAFE | `core.authority` missing |
| `tests/test_api_readonly.py` | FR-013, SLO-CTQ0 | gold GETs missing; write-scan may pass |
| `tests/test_golden_loader.py` | FR-010 | loader presence test may pass |

## 6. Gate for this prompt

- New engine tests **FAIL** (ImportError in body or unmet assertion). Not XFAIL. Not skip.
- Legacy XFAIL still **xfail**.
- Baseline diagnostics tests still **pass**.
- Do not add `pytest.raises(ImportError)` as the assertion (that would pass now and invert TDD).
- Do not implement `src/ot_command/core/{identity,telemetry,risk,containment,recovery,authority}.py`.

**Next prompt:** ENH-02 (identity engine).
