# Handover & Training Outline

## Handover package (FDE → operations / product)

| Artifact | Location |
|----------|----------|
| Specs freeze | `specs/` |
| ADRs | `adrs/` |
| Assurance case | `assurance/ASSURANCE_REPORT.md` |
| Ops runbooks | `ops/*.md` |
| Eval contract | `evals/golden_cases.jsonl` |
| Gate record | `participant/work/enh_10/REPO_3_0_GATE.md` |
| Open decisions | `traceability/OPEN_DECISIONS.md` |

## Training modules (4 hours workshop)

### Module 1 — Five states (45 min)
- Registered vs Observed vs Operational interpretation vs Safety vs Decision authority
- Exercise: reconcile OT-00528 RETIRED vs ONLINE (EVAL-028)
- **Anti-pattern:** treating CMDB or shadow spreadsheet as winner

### Module 2 — Telemetry & temporal (45 min)
- Dual clock: event_time vs ingest_time
- Unit mismatch (F vs C on TEMP tags)
- Exercise: EVAL-004 / EVAL-022

### Module 3 — Contextual risk & safety (60 min)
- Why CVSS alone fails (VUL-00706 vs VUL-00098)
- Isolation packet CTQ-ISO fields; no execute
- CASCADE-001 walkthrough (08:47 vs 08:50)
- Exercise: assess ALT-002783 / OT-01016

### Module 4 — Recovery & authority (45 min)
- RecoveryReady ≠ backup CURRENT
- ACTION_TIERS; tier 0 observe vs tier 4 refuse
- Exercise: PLT-01 IDENTITY not ready (EVAL-005)

### Module 5 — Agent, evals, ops (45 min)
- AI-disabled demo; `POST /recommend` trace review
- Run `make eval`; read `GET /ops/slo`
- Red-team examples (ignore safety, trip suppression)

## Competency checks

- Participant can explain why UNKNOWN process_context blocks execute-ready isolate
- Participant can run diagnostics + recommend workflow without LLM
- Participant identifies untrusted shift handover email in packet constraints

## Support model (production fork — not in repo)

- L1: SOC triage with deterministic tables
- L2: FDE / platform on-call for harness regressions
- L3: Safety / Process Engineering for authorization decisions (OPEN-001)
