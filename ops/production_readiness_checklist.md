# Production-readiness checklist (synthetic workshop)

Not a live-plant go-live. Tick only with executed evidence.

| Check | Evidence | OK |
|---|---|---|
| EVAL-001…031 harness | `evals/harness.py` | ENH-09 ran 31 PASS |
| No OT execute tools | `forbidden_execute_tools`; pytest denied-control | yes |
| AI-disabled still usable | EVAL-016; `AI_ENABLED=0` | yes |
| Rollback = flag off | `ops/incident_rollback.md` | yes |
| `data/` contradictions preserved | FR-014; no CSV cleanup | yes |
| Version pins | `requirements.txt` | yes |
| SBOM/AIBOM outline | `src/ot_command/sbom_freeze.json` unsigned OPEN-024 | outline only |
| Guardrails after model | ENH-08 red team | yes |
| Assurance case | `assurance/ASSURANCE_REPORT.md` | workshop |
| As-built C4 | `specs/as_built_c4.md` | yes |
| Gold GETs including `/graph/slice` | `tests/test_api_readonly.py` | this increment |
| No real OT connectors | `verify_repo.py` | yes |
| Named Authorizer | OPEN-001 | **no** |
| API authn | OPEN-029 | **no** — localhost workshop |
| Customer UI | PRD/APP next | **not this prompt** |

Gate: **PRD+App ready**, not production certified.
