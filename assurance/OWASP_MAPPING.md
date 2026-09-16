# OWASP mapping (ENH-08)

This table maps SDD-13 LLM01–10 / ASI01–10 onto **local unit tests**. It is not a certified OWASP assessment and not an ENH-09 assurance pass certificate.

| ID | Title | Abuse | Test |
|---|---|---|---|
| LLM01 | Prompt Injection | A-01 isolate now; A-02 shift notes | `tests/red_team/test_redteam_agent.py` |
| LLM02 | Sensitive Information Disclosure | A-04 exfil; A-06 answer key | same |
| LLM03 | Excessive Agency | A-03 PLC tool | same |
| LLM04 | Supply Chain | pinned `requirements.txt` / `sbom_freeze.json` | `test_sbom_aibom_freeze_note` |
| LLM05 | Data and Model Poisoning | shadow ≠ SoR | `test_a08_poisoned_overlay_does_not_win` |
| LLM06 | Unbounded Consumption | loop/termination | `test_loop_termination_repeat_and_cap` |
| LLM07 | Misinformation | A-07 CURRENT=ready; A-08 CMDB | same |
| LLM08 | Hidden Context Exposure | A-06; no CoT as authority | answer-key + traces |
| LLM09 | Vector Weaknesses | A-02 UNTRUSTED | shift-note test |
| LLM10 | Improper Output Handling | output filter drops OT tool-call form | `test_output_filter_drops_forbidden_tool_calls` |
| ASI01 | Goal Hijack | A-01 | prompt injection |
| ASI02 | Tool Misuse | A-03 | forbidden verbs |
| ASI03 | Identity/Privilege Abuse | A-05 | unauthorized role |
| ASI04 | Agentic Supply Chain | no dynamic OT SDK | `ot_connectors: []` |
| ASI05 | Unexpected Code Execution | no `write_plc_logic` | forbidden verbs |
| ASI06 | Memory Poisoning | shadow overlay | poison test |
| ASI07 | Inter-Agent | multi-agent not selected | N/A residual |
| ASI08 | Cascading Failures | A-10 no execute | flood test |
| ASI09 | Human-Agent Trust | no one-click isolate | A-01 / A-10 |
| ASI10 | Rogue Agents | max steps abort | loop test |

Do not claim a case passed unless the named pytest ran.
