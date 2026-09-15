# SDD-03 — Discovery checklist answers

**Maps:** `participant/DISCOVERY_CHECKLIST.md` → forensic cells + packs.  
**Date:** 2026-09-15  
**Does not conclude:** a solution, a CVSS order, or an identity winner.

---

## Evidence used / assumptions / unknowns / what this artifact did not conclude

Evidence: SDD-03 `matrix.csv`, `top15.md`, `scripts/mine_forensics.py`. Assumptions: checklist items are questions to **answer with counts/ids**, not to close OPEN decisions. Unknowns: OPEN-018/019/020. Did not implement remediations.

---

| Checklist item | Answer (quantify first) | Cell IDs | Pack |
|---|---|---|---|
| Reconcile CMDB/passive/CMMS asset identities | **Not reconciled.** 2016 assets × 3 alias sources = 6048. **5** PASSIVE alias collisions (e.g. `PLT-01-DCS_CONTROLLER-105` → OT-00012 and OT-00033). **200** registered ACTIVE vs observed OFFLINE/UNSEEN. **99** RETIRED∩ONLINE (OT-00528). Shadow 220 IDs with **0** firmware/state diff vs assets; email claims newer (OPEN-015). CMDB is **not** assumed correct. | L4-Imperfection, L4-Inconsistency, L4-Friction, L4-Uncertainty | EVAL-001 |
| Quantify undocumented or unknown network paths | Edges **3780**. documented=NO ∩ observed_last_24h=YES = **779**. approved_path UNKNOWN **240**. approved=NO ∩ observed YES **168**. **53** assets on no edge. | L2-Friction, L2-Uncertainty, L2-Hidden Dependency | — |
| Find telemetry duplicates, unit mismatches, stale/uncertain data and temporal anomalies | n=31224. duplicates extra **120**. TEMP unit≠C **47** (all F, e.g. TEL-00000288). quality BAD 1351 UNCERTAIN 2743 (**4094**). ingest−event p50 **120s** max **240s** (neg **0**). Enterprise received-before-event **407** (EVT-0000001). historian_enabled=NO tags **51** still in feed. | L3 all 8 lenses | EVAL-004 |
| Compare cyber severity with process criticality and compensating controls | **Do not rank by CVSS.** 830/1100 severity≠CVSS-band. VUL-00706 cvss 9.8 reachable **NO** asset LOW vs VUL-00098 cvss 8.7 reachable **YES** on HIGH DCS MIN_LOAD. cvss≥9 reachable NO **53**. control NONE 222 UNKNOWN 235. 1834 assets have no unit join. | L6-Inconsistency, L5-Friction, L11-Inconsistency | EVAL-002 |
| Find safety barriers bypassed/degraded or overdue for proof test | 61 not ACTIVE (35 DEGRADED 26 BYPASSED). proof not CURRENT **73** (OVERDUE 44 DUE 29). SIS_TRIP not ACTIVE **10** (e.g. PLT-08-SAFE-01). PLT-03-SAFE-14 BYPASSED **authorized NO**. bypass_authorized UNKNOWN **157**. | L7-Imperfection, L7-Inconsistency, L7-Volatility, L7-Uncertainty | Trace A |
| Compare CMMS status with observed/field state | 244 CLOSED and field ≠ RETURNED_TO_SERVICE (WO-000009 CLOSED / OUT_OF_SERVICE). 16/16 cmms×field cells populated. 133 CLOSED missing closed_at. WO-000018 CLOSED + ACTIVE + bypass YES + awaiting vendor. | L8-Inconsistency, L8-Complexity | — |
| Identify unapproved remote access and weak MFA evidence | approved_window ≠ YES **137** (NO 61 UNKNOWN 76). mfa ≠ YES **128** (NO 56 UNKNOWN 72). identity unknown **140**. local_service_laptop **170**. vendor.engineer on ENG_WORKSTATION **10**. | L6-Uncertainty, L6-Hidden Dependency | EVAL-006 observe-only |
| Trace three assets to process units and downstream business consequence | **OT-00211** → PLT-03-U05 BOILER MIN_LOAD food, unauthorized bypass PLT-03-SAFE-14, dep → U06. **OT-01016** → PLT-10-U06 PUMP_TRAIN MIN_LOAD pharma, UNSEEN vs ACTIVE, safety-critical dep → U07, VUL-00098 8.7 reachable, ALT-002783 HIGH SUPPRESSED. **OT-00528** → PLT-05-U01 TREATMENT MIN_LOAD power, RETIRED vs ONLINE, RELIEF bypass unauthorized, VUL-00744 9.1 reachable. | L5-Hidden Dependency, L7-Hidden Dependency, L4-Inconsistency | top15 traces |
| Quantify backup/runbook/restore-test weakness | backup ≠ CURRENT **25**. runbook ≠ CURRENT **35**. dep ≠ YES **29**. **113/119 CURRENT** fail restore>90 or runbook or dep. restore p50 **376d**. PLT-01 IDENTITY CURRENT / 360d / STALE. PLC_DCS CURRENT / 510d / rto 2h. | L10 all | EVAL-005 |
| Find cases where isolation could be operationally unsafe | 32 HIGH/CRIT alerts on MIN_LOAD or non-ACTIVE-barrier units (18 involve MIN_LOAD). Examples: ALT-000425 PLT-08-U04 MIN_LOAD; ALT-000089; ALT-002783 OT-01016. CASCADE 08:47 vs 08:50. Handover: do not isolate at min stable load. **No auto PLC isolation.** | L7-Friction, L5-Imperfection, L12-Inconsistency | EVAL-003 |
| Identify which decisions require human authority | Code: ACTION_TIERS ≥3 (`isolate_endpoint`, `change_remote_access`, `change_firewall`) and all tier 4 (PLC/setpoint/SIS/interlock). Default unknown action = 4. Isolate **string** does not call `requires_human_approval`. Named humans **absent** (OPEN-001). UNKNOWN permission is not permission. | L12-Complexity, L12-Uncertainty, L1-Hidden Dependency | EVAL-006 |
| Define eval gates before autonomy | Stubs EVAL-001 identity, 002 contextual risk, 003 isolation, 004 temporal, 005 recovery, 006 authority exist in `evals/golden_cases.jsonl` **without a runner**. pytest 3 pass / 3 xfail. Autonomy **blocked** until SDD-08 thresholds + passing tests on a modern path. LLM is not the architecture. | L12-Imperfection, L11-Uncertainty | EVAL-001..006 |

**Checklist complete.** Residual opens stay in `OPEN_DECISIONS.md`. No cells left unanswered; weak items flagged known-unknown / unknown-unknown.
