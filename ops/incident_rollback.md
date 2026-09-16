# Incident rollback (software)

This API **cannot** roll back a plant. IsolationExecution does not exist.

| Layer | Rollback |
|---|---|
| Explainer / agent | `AI_ENABLED=0` |
| Prompt | Revert `prompt_id` only after eval gate EVAL-006/014/016/023 |
| Packet | Supersede with a new `decision_id`; do not rewrite bronze |
| Data | Do not “clean” `data/` contradictions to hide the incident |
| OT | Out of band; human + site procedures only |

Feature-flag off is the software rollback. There is no isolate-execute flag to turn off because the tool is not registered.
