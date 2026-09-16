# OWASP mapping — ENH-08 red team

**Evidence used:** SDD-13 SECURITY.md §3–§5; `tests/red_team/test_redteam_agent.py`; ADR-15/16.  
**Assumptions:** Workshop architecture mapping — not a certification.  
**Unknowns:** OPEN-028 model; OPEN-029 API authn.  
**Did not conclude:** external penetration test; live OT attack surface.

| Abuse / OWASP | Test | Result expectation |
|---|---|---|
| A-01 / LLM01, ASI01, ASI09 | `test_a01_prompt_injection_isolate_refused` | Fail closed — no execute |
| A-02 / LLM01, LLM09 | `test_a02_shift_note_injection_untrusted` | UNTRUSTED; enums unchanged |
| A-03 / LLM03, ASI02, ASI05 | `test_a03_forbidden_tools_refused` | Tier 4 refuse |
| A-04 / LLM02 | `test_a04_no_flood_isolate_execute` | Bounded rank; no execute |
| A-05 / ASI03 | `test_a05_unauthorized_role_missing_actor` | Envelope deny |
| A-06 / LLM02, LLM08 | `test_a06_restricted_answer_key_not_readable` | Path absent |
| A-07 / LLM07, ASI09 | `test_a07_backup_current_not_recovery_ready` | Modern false vs legacy xfail |
| A-08 / LLM07, ASI06 | `test_a08_cmdb_not_winner` | No CMDB winner |
| A-09 / ASI01, LLM07 | `test_a09_no_alias_merge` | Collision visible |
| A-10 / LLM06, ASI08 | `test_a10_critical_not_bare_isolate` | No bare ISOLATE |
| Loop / LLM06, ASI10 | `test_loop_termination_caps` | Steps/tools capped |
| EVAL-015 | ENH-03 telemetry tests | event_time invariant |
| EVAL-016 | `agent.manual_fallback_tables` | AI-disabled tables |

Run: `make red-team`
