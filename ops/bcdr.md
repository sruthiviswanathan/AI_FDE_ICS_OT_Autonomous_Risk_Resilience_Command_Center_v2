# BC/DR — advisory service continuity

**REL-01** · C71  
**Scope:** Command Center **software and evidence store**. Plant OT recovery is a **view** (ENH recovery engine), not a drill you run on live controllers from this repo.

Plant component RTO hours in `data/raw/recovery_readiness.csv` are registered claims. **RecoveryReady** is derived (ADR-05). OPEN-027: restore-test days are not independently attested backup blobs.

## Tiers (workshop — advisory service)

| Tier | Target | What fails over | What does not |
|------|--------|-----------------|---------------|
| **T0** | Immediate | Deterministic engines with `AI_ENABLED=0` (identity, risk, safety, recovery tables, draft packet) | Explainer, Moonshot caption |
| **T1** | Hours (workshop: restore host + `make ci`) | Read-only API + eval harness on standby | Live plant connectivity (none exists) |
| **T2** | Next business day (workshop) | Full tree from git + SBOM-pinned image | Plant IDENTITY restore just because CSV says CURRENT |

These T0–T2 numbers are **service restoration intent**, not a new KPI threshold and not OPEN-006 MTT.

## Backup objects

| Object | Location | Rule |
|--------|----------|------|
| Bronze estate | `data/raw`, `data/telemetry`, `data/reference`, `data/shadow` | Immutable seed — do not clean contradictions |
| Decision traces | `data/local/decision_traces.jsonl` | Runtime append-only; often gitignored — copy off-box in a production fork |
| Specs / ADRs | `specs/`, `adrs/` | Behavior source of truth |
| Policy | `src/ot_command/core/policy.py` | ACTION_TIERS freeze |
| Image / deps | `Dockerfile`, `requirements.txt`, `assurance/SBOM_FREEZE.md` | Pin before restore |
| Eval contract | `evals/golden_cases.jsonl` | Must still pass after restore |

## Failover procedure (advisory)

1. Deploy last known-good image (or `git checkout` SHA).
2. Mount the **same** bronze `data/` (contradictions preserved).
3. `AI_ENABLED=0`.
4. `make ci`.
5. Resume `GET` gold routes and `POST /recommend` — still no OT execute.
6. Optional UI: confirm `ai_outage` scenario is not a blank screen.

## DR test evidence (honest)

| Claim | Evidence in this repo | Gap |
|-------|----------------------|-----|
| Engines survive AI loss | EVAL-016; UI AI outage | Not a plant blackstart |
| RecoveryReady ≠ CURRENT | EVAL-005, EVAL-018; `GET /recovery/PLT-01` | CSV restore days ≠ tape restore (OPEN-027) |
| Chaos | Tabletop + fixture replay inject_05 / inject_06 / `make eval` | **Not** a plant outage |

How to read plant recovery rows: [recovery_evidence.md](recovery_evidence.md).

## RTO/RPO (do not fabricate plant SLAs)

| Item | Workshop statement |
|------|-------------------|
| Advisory API RPO | Bronze files in git + local traces (traces may lag if not copied) |
| Advisory API RTO | Restart process / last image (T0–T1) |
| Plant component RTO | Column `rto_hours` in CSV — **registered**, not proven |
| Plant restore-test freshness | Engine flag if `last_restore_test_days` &gt; 180 | OPEN-006/022 plant SLA unset |

## What BC/DR must never include

- “Apply twin result to plant”
- Automatic isolation as a continuity action
- Silent promotion of shadow inventory during restore
