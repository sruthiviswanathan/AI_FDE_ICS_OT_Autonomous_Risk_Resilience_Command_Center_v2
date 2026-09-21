# Recovery evidence — ENH recovery engine (ADR-05)

**REL-01** · C71  
**As-built code:** `src/ot_command/core/recovery.py` (FR-005). TRACEABILITY lists this increment as **ENH-05**; the REL-01 playbook line “using ENH-06” refers to the **recovery evidence surface**, not the graph-slice engine (graph slice is TRACEABILITY ENH-06 / FR-006).  
**API:** `GET /recovery/{site_or_unit}` — plant id (`PLT-01`) or unit id (`PLT-10-U06` maps to `PLT-10`).  
**There is no `GET /recovery/gaps` route in this repo.** Gaps are the component rows where `recovery_ready=false`.

Do not treat this file as a live restore runbook. Chaos is **tabletop + fixture replay**.

## How to read the payload

```text
GET /recovery/PLT-01
```

| Field | Meaning |
|-------|---------|
| `component_count` | Rows for that plant (8 components in the seed) |
| `recovery_ready_count` | How many pass the **derived** predicate |
| `components[].backup_status` | Registered backup claim (`CURRENT` is not sufficient) |
| `components[].last_restore_test_days` | Stale if **&gt; 180** in this engine (workshop threshold; not OPEN-006/022) |
| `components[].runbook_status` | Must be `CURRENT` to be ready |
| `components[].dependency_verified` | Must be `YES` |
| `components[].manual_fallback` | Must be `YES` (LIMITED / NO → blocker) |
| `components[].recovery_ready` | Engine output |
| `components[].blockers` | Why not ready (e.g. `restore_test_stale_360d`, `runbook_stale`) |
| `components[].provenance` | `data/raw/recovery_readiness.csv`, grain plant+component |
| `note` | Repeats ADR-05 |

**Worked seed — PLT-01 IDENTITY (EVAL-005 / inject_06)**

From `data/raw/recovery_readiness.csv`: backup **CURRENT**, restore **360** days, runbook **STALE**, manual_fallback **LIMITED**.  
Expect `recovery_ready=false` and blockers including restore-test stale and runbook. Legacy `legacy_recovery_ready` would lie if it keys only on CURRENT — that path stays XFAIL on purpose.

## Estate-wide “gaps” without a dedicated route

Shift lead procedure:

1. For each plant `PLT-01` … `PLT-18`, `GET /recovery/{id}` (or UI Recovery Graph per plant).
2. List components with `recovery_ready=false`.
3. Do **not** sort plants by CVSS or by “backup CURRENT count.”
4. Diagnostics `recovery_stale_or_unknown_backup` counts CURRENT-missing only — **not** the full RecoveryReady predicate. Prefer the GET view.

Moonshot category `RESTORE_TEST_ROT` (forecasts) flags CURRENT + restore-test **&gt;90d** as an advisory hypothesis. The **authoritative** ready/not-ready bit remains this engine (180d + runbook + deps + fallback). If they disagree, keep the engine.

## Chaos / resilience drill (not a plant outage)

| Step | Action | Pass |
|------|--------|------|
| 1 | Load scenario **inject_05** (EVAL-012) | Undocumented paths visible; no regional isolate control |
| 2 | Load **inject_06** (EVAL-013) | IDENTITY not ready despite CURRENT |
| 3 | `make eval` | EVAL-005, EVAL-013, EVAL-018 PASS |
| 4 | Tabletop: “SCADA outage at PLT-01 — do we isolate the region?” | Answer: **no**. Hop cap 8; blast radius may be UNKNOWN |
| 5 | Tabletop: “Backups CURRENT — restore now?” | Answer: **not from this UI**. OPEN-027 |

Record the drill in the handover log: date, eval digest, `recovery_ready_count` for PLT-01, participants’ **functions** (not invented names).

## Related tests

- `tests/test_recovery.py` — EVAL-018 CURRENT-only false; EVAL-005 IDENTITY not ready
- UI: `apps/command_center/src/pages/RecoveryPage.tsx`

## Honest limitations

- No attested backup blobs in git.
- No plant blackstart.
- `rto_hours` is a CSV field, not a measured SLA.
