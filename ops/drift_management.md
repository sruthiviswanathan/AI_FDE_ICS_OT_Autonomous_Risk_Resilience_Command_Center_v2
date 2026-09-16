# Drift management

| Drift | Detect | Respond |
|---|---|---|
| Prompt / `prompt_id` | Registry status vs eval gate | Block activate until EVAL-006/014/016/023 |
| Policy / ACTION_TIERS | Diff `policy.py` | Do not add execute verbs |
| Model substitution | ADR-13 | Must not change rank / RecoveryReady / isolation enum |
| Bronze CSV “cleanup” | Git diff `data/` | Reject — contradictions are evidence (FR-014) |
| Shadow spreadsheet as CMDB | EVAL-029 | Overlay only, confidence low |
| Restore-test age | recovery blockers | Do not invent a day SLA (OPEN-006/022) |

Traces are audit, not a silent policy memory (ASI06).
