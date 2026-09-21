# SOPs and training outline

**REL-01** · C72, C74  
**Outline only** — not a certified training program and not a plant operating procedure for SIS/PLC.

Roles trained: SOC / OT analyst, process engineer, safety / SIS owner. FDE modules are in [handover.md](handover.md).

## SOP index (advisory)

| ID | Title | Trigger | Stop |
|----|-------|---------|------|
| SOP-SOC-01 | Alert to draft packet | HIGH/CRITICAL cyber alert | Packet with execute=false; no isolate click |
| SOP-SOC-02 | Vendor session anomaly | Unapproved window / unknown identity | ABSTAIN if process_context UNKNOWN |
| SOP-PE-01 | Process context unknown | Packet missing/UNKNOWN context | Do not authorize isolate; gather evidence |
| SOP-PE-02 | Recovery not ready | CURRENT backup, stale restore | Do not declare RecoveryReady |
| SOP-SAF-01 | Barrier bypass vs isolate | BYPASSED unauthorized + MIN_LOAD | DO_NOT_ISOLATE; no interlock bypass |
| SOP-ALL-01 | AI outage | Model down or `ai_outage` | Use tables; hide caption; keep working |
| SOP-CHG-01 | Change the advisory app | Code / prompt / policy / data | `make ci`; no silent data clean; no new OT POST |

SOP-CHG-01 is workshop **change management** for this repo (C72). Production CAB and live OT change control are out of scope.

### SOP-SOC-01 (happy path)

1. Pin plant / asset / alert (scenario rail or context bar).  
2. Identity + risk + safety + recovery GETs (or UI pages).  
3. `POST /recommend`.  
4. Read recommendation, missing_fields, required_authority **functions**.  
5. If UNKNOWN or MIN_LOAD + bypass: expect ABSTAIN / DO_NOT_ISOLATE.  
6. Record decision_id. Authorize remains disabled.

### SOP-CHG-01 (advisory software)

1. Trace the change to `traceability/TRACEABILITY.csv` (untraced code is out of scope).  
2. Do not change `legacy_*` to hide XFAIL.  
3. Do not add ACTION_TIERS verbs.  
4. `make ci`.  
5. If AI/prompt: red team + EVAL-016.  
6. Rollback: [incident_rollback.md](incident_rollback.md).
7. Promotion: [adoption.md](adoption.md) §11 — PR → shadow → pilot → advisory-software canary only. Never a live controller canary.

## Training outline (SOC + process + safety) — 3 hours

### T1 — Five states (40 min)

Observed ≠ registered ≠ operational interpretation ≠ safety ≠ decision authority.  
Exercise: OT-00528 RETIRED vs ONLINE. Anti-pattern: CMDB winner.

### T2 — Risk is not CVSS (40 min)

Reachability, criticality, barriers, recovery. Exercise: `/risk/contextual` vs a high unreachable CVSS. EVAL-002 / EVAL-017.

### T3 — Safety vs security (50 min)

CASCADE-001 08:47 vs 08:50. PLT-10-SAFE-07. Packet CTQ-ISO. No execute. EVAL-003 / EVAL-007 / EVAL-020.

### T4 — Recovery honesty (30 min)

GET `/recovery/PLT-01` IDENTITY. inject_06. ADR-05.

### T5 — AI off / on / Moonshot (20 min)

Default OFF. ON = template caption. Moonshot = advisory forecasts + twin sketch. Outage drill EVAL-016.

## Competency checks (pass/fail)

| Check | Pass |
|-------|------|
| UNKNOWN process_context | Learner refuses isolate-ready language |
| CURRENT backup | Learner says not RecoveryReady without blockers review |
| AI outage | Learner still opens identity/recovery/packet |
| Moonshot banner | Learner does not treat forecast as a control action |
| Authorize | Learner knows OPEN-001 — button disabled is correct |

No attendance certificate is issued from this outline.
