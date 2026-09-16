# AI-specific incident response

| Symptom | Detect | Respond |
|---|---|---|
| Agent loop / max 12 steps | `GET /ops/slo` `agent_loop.alert` | Abort; war room; `AI_ENABLED=0` |
| Prompt injection / tool misuse | Trace `dropped_tool_calls`; EVAL-014/027 | Keep packet ABSTAIN; do not retry forbidden tools |
| Model timeout / vendor outage | Empty explanation + fallback tables | EVAL-016 path; engines stay |
| Hidden CoT as authority | Trace `hidden_cot_as_authority` | Fail the packet; packet JSON is the argument |
| Eval leakage | `restricted_answer_key/` must stay absent | CI `verify_repo.py` |

Do not add isolate/PLC tools “behind a flag” as the response.
