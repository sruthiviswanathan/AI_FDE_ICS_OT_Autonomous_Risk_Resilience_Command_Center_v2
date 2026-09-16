# BCDR — Business Continuity / Disaster Recovery

**Scope:** Command center **advisory service** and evidence store — not plant OT recovery (see `recovery.py` for plant component readiness views).

## Tier definitions (workshop)

| Tier | RTO target | Scope |
|------|------------|-------|
| T0 | 0 min | AI-disabled deterministic engines (identity, risk, safety, recovery tables) |
| T1 | 4 h | Read-only API + eval harness on standby host |
| T2 | 24 h | Full Repo 3.0 restore from git + SBOM-pinned image |

Plant RTO hours remain in `data/raw/recovery_readiness.csv` — **RecoveryReady** is derived, not `backup_status` alone (ADR-05).

## Backup objects

| Object | Location | Notes |
|--------|----------|-------|
| Bronze evidence | `data/raw`, `data/telemetry`, `data/shadow` | Immutable workshop seed — do not “clean” |
| Decision traces | `data/local/decision_traces.jsonl` | Runtime append-only; gitignored |
| Specs / ADRs | `specs/`, `adrs/` | Source of truth for behavior |
| Container image | Dockerfile + `requirements.txt` | Pin in `assurance/SBOM_FREEZE.md` |

## Failover procedure

1. Deploy last known-good image to standby.
2. Mount same bronze `data/` volume (contradictions preserved).
3. Set `AI_ENABLED=0`.
4. Run `make ci`.
5. Resume advisory POST `/recommend` — still no OT execute.

## DR test evidence gap

OPEN-027: restore-test days in CSV are not independently attested backup blobs. Do not claim live DR proof from this repo alone.
