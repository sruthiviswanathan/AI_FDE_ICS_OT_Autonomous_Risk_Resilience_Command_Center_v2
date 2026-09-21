# Operational RACI — Synthetic ICS/OT Command Center

**REL-01** · C80–C82 · ADR-04, ADR-11, ADR-12, ADR-14  
**Scope:** workshop / synthetic estate. No live plant operations from this repository.  
**Roles are job functions, not named people.** Named Authorizer is **OPEN-001** — do not invent a person or badge number.

## Decision split (frozen)

| Band | What | Software in this repo | Human |
|------|------|------------------------|--------|
| **Observe** | Collect, correlate, tables, graphs | R — engines / GET APIs | C |
| **Recommend** | Draft packet, ranked evidence, caption | R — `POST /recommend`, optional template caption | C |
| **Authorize** | Accept a consequential OT action | **None** — UI Authorize is disabled | A (unnamed until OPEN-001) |
| **Execute** | Isolate, firewall, remote-access change, PLC/SIS/setpoint/interlock | **Forbidden** | Plant OT under human authority only; **not from this app** |

ACTION_TIERS (`src/ot_command/core/policy.py`): observe/correlate/summarize = 0; recommend = 1; request_fresh_telemetry / open_ticket / increase_logging = 2 (design-only); isolate_endpoint / change_remote_access / change_firewall = 3 (human); write_plc_logic / change_setpoint / modify_sis / bypass_interlock = 4 (refuse). Unknown action = 4.

## Activity RACI

| Activity | FDE / Platform | SOC / OT Security | Process Engineer | Safety / SIS Owner | VP Operations | Plant OT |
|----------|----------------|-------------------|------------------|--------------------|---------------|----------|
| Start / health of advisory API | R/A | I | I | I | I | I |
| Identity reconciliation review | R | C | C | I | I | C |
| Telemetry quality triage | R | C | C | I | I | C |
| Contextual risk ranking (not CVSS-only) | R | C | C | C | I | I |
| Safety vs security conflict review | C | C | C | A | I | C |
| Isolation **recommendation** draft | R | C | C | C | I | I |
| Isolation **authorize** | — | C | C | C | A | C |
| Isolation **execute** | — | — | — | — | A | R |
| Recovery readiness assessment | R | I | C | I | A | C |
| Vendor session review | R | A | I | I | C | I |
| Eval harness / assurance gate | R/A | I | I | I | C | I |
| AI feature flag (`AI_ENABLED`) | R | C | I | I | A | I |
| AI incident (S1–S4) | R | C | I | C | A | I |
| Advisory service rollback | R/A | C | I | I | A | I |
| Synthetic deploy decision | C | C | C | C | A | C |

**Legend:** R = Responsible · A = Accountable · C = Consulted · I = Informed · — = no role (software must not perform)

## AI incident roles (when explainer/agent is in path)

| Role | Does | Does not |
|------|------|----------|
| FDE / Platform | Set `AI_ENABLED=0`; preserve traces; re-run `make ci` / red team | Execute OT; delete traces to “clean” an incident |
| SOC | Confirm tables still render; treat model prose as untrusted | Promote narrative to ACTION_TIERS |
| Process Engineer | Confirm process_context / safe_state still UNKNOWN or MIN_LOAD as evidenced | Isolate from a caption |
| Safety / SIS Owner | Confirm no SIS/interlock tool appeared in `tool_trace` | Bypass a barrier because the model asked |
| VP Operations | Accountable for re-enable decision after harness green | Sign a fake certificate |

## Ownership map (operational, not CMDB winner)

| Surface | Owner function | Evidence |
|---------|----------------|----------|
| Identity / aliases | FDE + SOC | `GET /assets/{id}/identity`, `GET /identity/conflicts` |
| Telemetry quality | FDE + Process | `GET /telemetry/quality` |
| Contextual risk | SOC + Process | `GET /risk/contextual` |
| Safety barriers | Safety owner | `GET /safety/conflicts` |
| RecoveryReady | Process + VP Ops | `GET /recovery/{plant}` |
| Policy / tiers | FDE (code) + VP Ops (authority) | `policy.py`; OPEN-001 |
| Moonshot / twin sketch | FDE + Full/SOC/FDE personas | `GET /forecasts`, `GET /twin/preview` — advisory only |

## Hard rules

- Software **never** takes R or A on execute.
- `POST /recommend` returns packets only (`execute=false`).
- AI-disabled path (`AI_ENABLED=0`) must remain operable (EVAL-016 / ADR-12).
- Executive persona: Moonshot off by default; view filter is not authority.
