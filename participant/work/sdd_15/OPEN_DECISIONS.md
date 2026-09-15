# OPEN_DECISIONS (append-only)

This file is **append-only**. Later prompts add dated sections. Do not rewrite or delete prior IDs.

UNKNOWN permission is not permission. Missing named authority, threshold, ADR, or legal class stays OPEN.

---

## SDD-01 | OM-1 | 2026-09-15

**Evidence used:** `src/ot_command/core/policy.py`; `docs/06_security_safety_assurance.md`; `docs/05_kpis_baseline.md`; `data/shadow/risk_acceptance_tracker.csv` (180 rows); `contracts/*`; `src/ot_command/__init__.py`; `pyproject.toml`; `data/ot_legacy.db`; `evals/golden_cases.jsonl`; `scenarios/cascade_001.json`.  
**Assumptions:** SDD-01 does not invent people, counsel opinions, or architecture.  
**Unknowns:** listed per ID.  
**Did not conclude:** any of the items below as closed.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-001 | Named human authorities for sponsor, Safety/SIS owner, SOC manager, VP Ops, FDE lead, and every ACTION_TIERS ≥ 3 action | No person names in `policy.py`, `docs/06`, or data. CASCADE-001 has SOC vs process engineer as **roles** only. | Cannot execute consequential recommendations; cannot close HITL RACI as people | Global OT Risk Sponsor (unnamed) |
| OPEN-002 | EU AI Act classification and ISO/IEC 42001 certification status | Methods apply; **no counsel sign-off** and no certificate in repo. Working assumption only: advisory HITL industrial decision support, prohibited from actuation. | Regulatory claims in exec materials | OT-CISO + counsel (not in repo) |
| OPEN-003 | Production (non-workshop) permissible use of each `data/` source | `README.md` permits synthetic local analysis. No plant-operator license for real OT reuse. Operational-truth permission = UNKNOWN for all tables in CHARTER §7. | Any live-plant deployment (out of this repo anyway) | OT-CISO |
| OPEN-004 | Complete ACTION_TIERS vs `docs/06` verb set | Code keys: observe/correlate/summarize/recommend/request_fresh_telemetry/open_ticket/increase_logging/isolate_endpoint/change_remote_access/change_firewall/write_plc_logic/change_setpoint/modify_sis/bypass_interlock. Docs also: enrich, rank evidence, read-only simulation, capture evidence, maintenance-mode. Unknown action defaults to tier 4. | Policy completeness; evals of “permissible autonomous action” (EVAL-006) | FDE + OT-CISO |
| OPEN-005 | Authority when `risk_acceptance_tracker.risk_owner = Unknown` | 41 / 180 rows; e.g. `PLT-15,OT-01094` is Engineering but `PLT-15,OT-00904,Unknown,ACCEPT`. UNKNOWN is not permission. | Risk-acceptance workflow | OT-CISO |
| OPEN-006 | KPI formulas and baselines for unmeasured `docs/05` clocks/cost | BASELINE_PENDING: MTT contextualize; alerts per actionable incident; safety-bypass **aging**; vuln-to-process coverage; restore-test freshness as a KPI; time-to-confidence; time-to-safe-containment; degraded-operation duration; false-positive escalation; decision-evidence completeness; approval latency; AI cost per incident. | SDD-04 baseline dataset completeness | FDE + VP Ops |
| OPEN-007 | Lineage of `data/ot_legacy.db` vs CSV | 6 tables; row counts match CSV; `run_diagnostics()` does not read DB; integrity ok. Independent vs derived = unknown. | SDD-07 lineage | FDE |
| OPEN-008 | Who may authorize isolation in CASCADE-001 / Unit 04 | Handover: “Do not isolate the controller without process engineering review.” SOC recommends isolation at 08:47. No named approver. Software must not execute isolate. | Isolation **execute** remains forbidden; even draft authority is unnamed | VP Ops + Process Eng + Safety (unnamed) |
| OPEN-009 | Canonical telemetry/asset contract | v1 vs v2 field/path split; telemetry schema omits `ingest_time`/`source`/`asset_id` present on `TEL-00000000`. FastAPI implements neither asset API. | SDD-10 contracts; identity API | FDE (no silent pick in SDD-01) |
| OPEN-010 | Canonical package `__version__` | `0.1.0` in `src/ot_command/__init__.py` vs `2.0.0` in `pyproject.toml` / API / manifest. `docs/07` says normalized. | Packaging identity | FDE (do not “clean” in SDD-01) |
| OPEN-011 | `specs/01_mandate.md` at repo root | OM map says SDD-01 produces `specs/01_mandate.md`; capstone SDD-15 **distills** it from this charter. Root spec deferred. | SDD-15 gate | FDE |

**SDD-01 closure rule:** none of OPEN-001…011 is treated as approved permission, threshold, ADR, or architecture.
