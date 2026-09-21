# Named SLOs — advisory service (workshop)

**REL-01** · C68 · Normative source: `specs/14_delivery_spec.md` and `participant/work/sdd_15/SDD-14_delivery_spec/DELIVERY_SPEC.md` §12.  
**Runtime:** `GET /ops/slo` · `src/ot_command/core/ops.py`  
**Not:** plant operator SLAs, MTT-contextualize dollars, or a close of **OPEN-006 / OPEN-022**.

These are **synthetic engineering** targets for the local 18-plant files. Error budget is **0** on safety-class SLOs. Do not invent additional thresholds.

## Named SLOs

| ID | Statement | Target | Error budget | How measured | On breach |
|----|-----------|--------|--------------|--------------|-----------|
| **SLO-OT** | Zero OT execute actions in software | 0 violations | **0** | Traces `execute=true`; red team; `GET /ops/slo` | Immediate rollback of any execute-adjacent route; keep `AI_ENABLED=0`; do not “compensate” with more automation |
| **SLO-CTQ0** | Zero forbidden write routes | 0 routes | **0** | `tests/test_api_readonly.py` forbidden POST scan (`/isolate`, `/plc`, `/sis`, `/setpoint`, `/bypass`, `/firewall`) | Remove route; `make ci`; do not ship |
| **SLO-ISO** | Isolation drafts include `safe_state` and required authority when recommendation is `ISOLATE_DRAFT` | 100% | **0** | `containment.is_packet_authorizable`; EVAL-003, EVAL-020 | Packet must ABSTAIN / DO_NOT_ISOLATE; Authorize stays disabled |
| **SLO-EVAL** | Golden `must_not` cases pass | 100% of EVAL-001…031 must_not | **0** | `make eval` / `evals/harness.py` | Block release; do not hide XFAIL on `legacy_*` by deleting tests |
| **SLO-LAT** | p95 packet assembly **without dropping safety/identity joins** | p95 &lt; 8000 ms | TBD (OPEN-006) | Trace `latency_ms`; `GET /ops/slo` | **Never** skip joins to make latency green (NFR-LAT / EVAL-025). Status may be UNKNOWN if no traces |
| **SLO-HEALTH** | Advisory API remains available for gold GETs | `/health` and `/diagnostics` stay GET-only and up | workshop | `GET /health` `status=ok`; FR-013 | Restart API; AI-disabled tables must still render (EVAL-016) |

SLO-HEALTH is the FR-013 availability pin (`traceability/TRACEABILITY.csv`). It is not a plant uptime SLA.

## Error-budget policy

| Class | IDs | Budget | Meaning |
|-------|-----|--------|---------|
| Safety / control | SLO-OT, SLO-CTQ0, SLO-ISO, SLO-EVAL | **0** | One violation is a stop-ship for the advisory service. There is no “burn 1% and keep automating.” |
| Latency | SLO-LAT | TBD | Watch only. Fast-but-wrong is a **counter-metric** (EVAL-026). |
| Availability (API) | SLO-HEALTH | workshop | Fail over to last image with `AI_ENABLED=0`; bronze `data/` unchanged |

## What these SLOs are not

- Not a promise that plants recover in `rto_hours` from `recovery_readiness.csv`.
- Not permission to isolate when the packet is `ABSTAIN` / `DO_NOT_ISOLATE`.
- Not a model-quality SLA (OPEN-028: provider `none`). Caption/Moonshot are templates + CSV joins.

## Shift-lead check (2 minutes)

```text
GET /health          → status ok, mode synthetic-read-only
GET /ops/slo         → SLO-OT OK, SLO-CTQ0 OK
GET /diagnostics     → counters still show conflicts (do not “fix” data)
```

If SLO-OT is BREACH: treat as **S1** in [ai_incident_response.md](ai_incident_response.md) / [incident_rollback.md](incident_rollback.md).
