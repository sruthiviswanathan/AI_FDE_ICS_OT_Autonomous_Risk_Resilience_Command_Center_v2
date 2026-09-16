# TEST_PLAN — ENH-01 (tests before implementation)

**Prompt:** ENH-01 | TESTS BEFORE IMPLEMENTATION  
**OM:** 14 (Engineer)  
**FDE capabilities:** C31 (Software engineering), C49/C52 (TEVV prep)  
**Date:** 2026-09-16

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
- `specs/14_delivery_spec.md` FR-001…014, NFR-SAFE, SLO-EVAL
- `specs/08_evals_risks.md` EVAL-001…031 must_not ship blockers
- `evals/golden_cases.jsonl` — 31 cases (EVAL-001…031)
- `tests/test_known_legacy_defects.py` — 3 strict XFAIL on `legacy_*`
- `src/ot_command/core/policy.py` — ACTION_TIERS pin (tier 4 unknown default)
- `traceability/TRACEABILITY.csv` — planned_code under `modern/` (OPEN-030 mapping)
- Seeded counts: alias collisions ≥5, state conflicts ≥200, bad telemetry ≥4094, duplicates ≥120, unit mismatches ≥47

### Assumptions
1. New tests target **`ot_command.core.*`** per capstone ENH-01; TRACEABILITY `modern/` paths are deferred naming (OPEN-030).
2. Stubs raise `NotImplementedError` until ENH-02…07 implement engines.
3. Legacy XFAIL tests remain strict evidence of Repo 1.0 defects.
4. `tests/helpers/` is test-only; not traced as production code.

### Unknowns
OPEN-001 (named Authorizer), OPEN-006 (latency/cost thresholds), OPEN-028 (model), OPEN-029 (API authn). Tests do not invent thresholds or people.

### Did not conclude
Did not implement production engines. Did not add gold API routes. Did not delete XFAIL tests. Did not clean `data/` contradictions.

---

## Scope

| Module under test | Test file | Primary evals | ENH implementer |
|---|---|---|---|
| `core.identity` | `tests/test_identity.py` | EVAL-001 | ENH-02 |
| `core.telemetry` | `tests/test_telemetry_temporal.py` | EVAL-004, 009, 015, 022 | ENH-03 |
| `core.risk` | `tests/test_contextual_risk.py` | EVAL-002, 017 | ENH-04 |
| `core.containment` | `tests/test_isolation_policy.py` | EVAL-003, 019, 031 | ENH-05 |
| `core.recovery` | `tests/test_recovery.py` | EVAL-005, 018 | ENH-06 |
| `core.authority` | `tests/test_authority.py` | EVAL-006 | ENH-07 |
| `core.guardrails` | `tests/test_denied_control.py` | EVAL-014, 023, 027, 030 | ENH-07 |
| `api.py` gold GETs | `tests/test_api_readonly.py` | EVAL-016, FR-013 | ENH-02…07 |
| Golden loader | `tests/test_golden_loader.py` | EVAL-001…031 load | ENH-09 harness |
| `legacy.*` (unchanged) | `tests/test_known_legacy_defects.py` | EVAL-017…019 | remain XFAIL |

---

## Pass / fail expectations (this prompt)

| Category | Expected now | Reason |
|---|---|---|
| Baseline + SDD layout | PASS | unchanged Repo 2.0 gate |
| Legacy XFAIL | XFAIL (strict) | brownfield evidence preserved |
| Golden loader helpers | PASS | helper only |
| `policy.py` assertions in denied_control | PASS | existing pin |
| Core engine tests | **FAIL** | `NotImplementedError` until ENH-02+ |
| Gold GET route tests | **FAIL** | 404 until routes wired |

**Gate rule:** ENH-01 passes when new tests exist, assert the right contracts, and fail for missing implementation — not import errors or weakened assertions.

---

## Safety constraints encoded in tests

- No PLC write, SIS change, setpoint, interlock bypass, or isolate-execute paths (CTQ-0).
- Highest CVSS must not win when reachability/criticality disagree (EVAL-002/017).
- `CURRENT` backup ≠ RecoveryReady (EVAL-018/005).
- CRITICAL/HIGH severity alone ≠ bare ISOLATE (EVAL-019/003/031).
- Unknown ACTION_TIERS action → tier 4 refuse (EVAL-006).
- CMDB is not identity winner (EVAL-001).

---

## Run

```bash
python -m pytest -q
python scripts/check_sdd_gates.py
python scripts/verify_repo.py
```

**Next prompt:** ENH-02 — implement `core.identity` and pass identity tests.
