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

---

## SDD-02 | OM-2 | 2026-09-15

**Evidence used:** `data/raw/enterprise_events.jsonl` (6500); `data/raw/cyber_alerts.csv` (2800); `data/raw/work_orders.csv` (1250); `data/shadow/shift_handover_email.txt`; `data/shadow/ot_asset_inventory_FINAL_v8.csv` (220); `src/ot_command/legacy/risk.py`; `src/ot_command/api.py`; `docs/03_current_state_architecture.md`.  
**Assumptions:** SDD-01 OPEN items remain open; process mining describes files, not live shifts.  
**Unknowns:** listed per new ID.  
**Did not conclude:** system of record; future architecture; isolation authority.

| ID | Decision needed | Why it is open (evidence) | Blocked work | Owner (role, unnamed) |
|---|---|---|---|---|
| OPEN-012 | Durable case / correlation key for alert → WO → session → barrier → recovery | `correlation_id` empty on **3251 / 6500** enterprise events; max non-empty reuse is 6; no foreign key from `cyber_alerts` to `work_orders` | End-to-end process cycle time; agent “incident object” | FDE + SOC mgr |
| OPEN-013 | Semantic contract for `enterprise_events.event_type` vs `source` | HISTORIAN emits SESSION 122 and WORK_ORDER 88; IAM emits ALARM 109; CMMS is only 118/901 WORK_ORDER events | Enterprise integration design (SDD-10) | FDE |
| OPEN-014 | Work-order clock vs status semantics | 133 CLOSED with empty `closed_at`; 489 not-CLOSED with `closed_at` set; `WO-000018` CLOSED + field ACTIVE + bypass YES + notes awaiting vendor | Maintenance value-stream Measure | Maint/CMMS owner |
| OPEN-015 | Whether shadow spreadsheet is actually newer than CMDB | Handover email claims newer gateway inventory; `ot_asset_inventory_FINAL_v8.csv` vs `assets.csv`: **0** firmware diffs and **0** state-pair diffs on 220 overlapping IDs | Identity reconciliation (SDD-03 L4) | FDE; do not pick a winner |
| OPEN-016 | `docs/03` Purdue-like boxes vs enforceable zones | `zone` is a CSV label (DMZ 377); 779 undocumented observed edges; no firewall policy table | Trust-boundary engineering | OT-CISO |
| OPEN-017 | Meaning of SOC SUPPRESSED on HIGH/CRITICAL | 211 HIGH/CRIT `soc_status=SUPPRESSED` (e.g. `ALT-000040`); not an ACTION_TIERS action; not trip suppression in SIS | Alert-queue vs safety policy | SOC mgr + Safety/SIS |

SDD-01 IDs OPEN-001…011 are **not** closed by SDD-02. Isolation execute remains forbidden. No KG/ADR invented.
