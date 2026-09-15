# SDD-03 — 96 forensic cells (readable matrix)

**Prompt:** SDD-03 | L1–L12 × 8 lenses  
**Date:** 2026-09-15  
**Canonical 96 rows:** `matrix.csv` (header + 96 data rows; 0 empty)  
**Scripts:** `scripts/mine_forensics.py` (telemetry 31224 + joins), `scripts/generate_matrix.py`  
**Not:** solution code, CVSS ranking, identity winner, isolation execute.

This is the **forensic grid**, not the 96 FDE capability stack. SDD-03 seeds **C07** (root-cause input to SDD-04).

---

## Evidence used / assumptions / unknowns / what this artifact did not conclude

### Evidence used (file / field / count / id)

| Item | Evidence |
|---|---|
| Diagnostics | VERIFICATION.md 200, 5, 779, 120, 4094, 47, 61, 73, 244, 137, 128, 25, 29, 35 |
| Identity | assets 2016; aliases 6048 (CMDB/PASSIVE/CMMS 2016 each); collisions 5 e.g. `PLT-01-DCS_CONTROLLER-105` → OT-00012 and OT-00033; RETIRED∩ONLINE 99 e.g. OT-00528 |
| Topology | edges 3780; undocumented∩observed 779; 53 assets on no edge; 10 protocols |
| Telemetry | 31224; GOOD 27130 UNCERTAIN 2743 BAD 1351; F-on-TEMP 47 e.g. TEL-00000288; ingest−event p50 120s max 240s neg 0 |
| Process | units 216; MIN_LOAD 54; deps 198; critical∩undocumented 33; assets with tags **182/2016** |
| Cyber | vulns 1100; severity≠CVSS-band **830/1100**; cvss≥9 reachable NO 53 e.g. VUL-00706; alerts 2800; HIGH+CRIT 860 with process_context UNKNOWN 525 |
| Safety | 450; 61 not ACTIVE; 10 SIS_TRIP not ACTIVE; PLT-03-SAFE-14 BYPASSED + authorized NO |
| Ops | WO 1250; 244 CLOSED≠RTS e.g. WO-000009; handover Unit 04 |
| Enterprise | events 6500; empty correlation_id 3251; received before event 407 e.g. EVT-0000001 |
| Recovery | 144; CURRENT but weak **113/119**; PLT-01 IDENTITY restore 360d runbook STALE |
| Traces | OT-00211, OT-01016, OT-00528 |
| Authority | policy.py ACTION_TIERS; CASCADE-001 08:47 vs 08:50; EVAL-001..006 stubs |

### Assumptions

SDD-01/02 still bind. Workshop mining allowed. Operational truth UNKNOWN. Discovery order: inventory → topology → identity → telemetry → process → cyber/safety → recovery → authority.

### Unknowns

OPEN-018 Unit 04 plant; OPEN-019 CASCADE 37/6 firmware set; OPEN-020 tag coverage 182/2016; OPEN-012 case key; OPEN-001 named humans.

### Did not conclude

No solution. No CVSS operational rank. No isolate. No CMDB-as-winner. No recovery-ready. No architecture.

---

## How to read

Every cell in `matrix.csv` has: finding, evidence (file/field/count/id), consequence_class, naive_ai_failure, residual_unknown, confidence (HIGH/MED/LOW), blocks_autonomy (YES/PARTIAL/NO).

Consequence: **cyber / process / safety / resilience / authority**.

Weak cells are labeled known-unknown or unknown-unknown in residual_unknown. None are blank.

Index:

| Layer | Imp | Inc | Fri | Cpx | Vol | Unc | Hid | UU |
|---|---|---|---|---|---|---|---|---|
| L1 | L1-Imperfection | L1-Inconsistency | L1-Friction | L1-Complexity | L1-Volatility | L1-Uncertainty | L1-Hidden Dependency | L1-Unknown Unknown |
| L2 | L2-Imperfection | L2-Inconsistency | L2-Friction | L2-Complexity | L2-Volatility | L2-Uncertainty | L2-Hidden Dependency | L2-Unknown Unknown |
| L3 | L3-Imperfection | L3-Inconsistency | L3-Friction | L3-Complexity | L3-Volatility | L3-Uncertainty | L3-Hidden Dependency | L3-Unknown Unknown |
| L4 | L4-Imperfection | L4-Inconsistency | L4-Friction | L4-Complexity | L4-Volatility | L4-Uncertainty | L4-Hidden Dependency | L4-Unknown Unknown |
| L5 | L5-Imperfection | L5-Inconsistency | L5-Friction | L5-Complexity | L5-Volatility | L5-Uncertainty | L5-Hidden Dependency | L5-Unknown Unknown |
| L6 | L6-Imperfection | L6-Inconsistency | L6-Friction | L6-Complexity | L6-Volatility | L6-Uncertainty | L6-Hidden Dependency | L6-Unknown Unknown |
| L7 | L7-Imperfection | L7-Inconsistency | L7-Friction | L7-Complexity | L7-Volatility | L7-Uncertainty | L7-Hidden Dependency | L7-Unknown Unknown |
| L8 | L8-Imperfection | L8-Inconsistency | L8-Friction | L8-Complexity | L8-Volatility | L8-Uncertainty | L8-Hidden Dependency | L8-Unknown Unknown |
| L9 | L9-Imperfection | L9-Inconsistency | L9-Friction | L9-Complexity | L9-Volatility | L9-Uncertainty | L9-Hidden Dependency | L9-Unknown Unknown |
| L10 | L10-Imperfection | L10-Inconsistency | L10-Friction | L10-Complexity | L10-Volatility | L10-Uncertainty | L10-Hidden Dependency | L10-Unknown Unknown |
| L11 | L11-Imperfection | L11-Inconsistency | L11-Friction | L11-Complexity | L11-Volatility | L11-Uncertainty | L11-Hidden Dependency | L11-Unknown Unknown |
| L12 | L12-Imperfection | L12-Inconsistency | L12-Friction | L12-Complexity | L12-Volatility | L12-Uncertainty | L12-Hidden Dependency | L12-Unknown Unknown |

Layer narrative (each lens named). Full naive-AI / residual text is in `matrix.csv`.

### L1 Software/logic — `risk.py`, `diagnostics.py`, `policy.py`, tests

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | Hard-coded wrong policy | `legacy_rank`/`legacy_recovery_ready`/`legacy_isolation_recommendation`; 3 XFAIL | authority | Trust ISOLATE/CURRENT/CVSS because functions return them | Plant copy of rules? | HIGH | YES |
| Inconsistency | Score uses criticality; rank does not | multipliers vs cvss sort; `__version__` 0.1.0 vs 2.0.0 | authority | Merge score and rank | OPEN-010 | HIGH | PARTIAL |
| Friction | Policy not on API | `/health` `/diagnostics` only; risk.py unused by API | authority | Invent orchestration because files exist | Wiring known-unknown | HIGH | PARTIAL |
| Complexity | 14 integers; UNKNOWN=fail | diagnostics.py heuristics | cyber | Auto-ticket from counts | No uncertainty object | HIGH | PARTIAL |
| Volatility | No rule version registry | literals in risk.py | authority | Prompt-edit multipliers | Who may change rules | MED | YES |
| Uncertainty | Silent defaults | `.get(criticality,1.0)`; `.get(action,4)` | authority | Treat default as measured | OPEN-004 | HIGH | YES |
| Hidden Dependency | Isolate skips policy; diagnostics skip process/vuln | no import; last_restore_test_days unused | safety | Assume policy.py protects isolate | Join list for SDD-08 | HIGH | YES |
| Unknown Unknown | No PLC/SIS logic in repo | 7 src files | safety | Hallucinate ladder logic | unknown-unknown plant logic | HIGH | YES |

### L2 OT systems/protocols — assets protocol/zone/firmware, edges, contracts

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | 10 protocols incl. VendorSerial/OPC_DA | counts 223..181 | cyber | One adapter | No PCAP | HIGH | PARTIAL |
| Inconsistency | API v1 vs v2 vs CSV | assetId vs asset_id; unimplemented | cyber | Collapse operationalState=observed_state | OPEN-009 | HIGH | YES |
| Friction | Undocumented observed paths | 779 | cyber | Trust documented topology | Why 779 UU | HIGH | YES |
| Complexity | 13 types × 5 zones | DCS 176; L3 426 … | process | Flatten to “OT device” | OPEN-016 | HIGH | PARTIAL |
| Volatility | Firmware diversity; old backup_age | 815 firmware; p50 age 211d | resilience | Treat firmware as current | OPEN-019 | MED | PARTIAL |
| Uncertainty | approved_path UNKNOWN | 240; unapproved∩observed 168 | cyber | Coerce UNKNOWN | Approver unnamed | HIGH | YES |
| Hidden Dependency | 53 assets on no edge; 167 gateways | 1963/2016 on edges | resilience | Assume full graph | Air-gap vs missing join | HIGH | PARTIAL |
| Unknown Unknown | No capture | VendorSerial 182/344 | cyber | Claim segmentation | unknown-unknown buses | HIGH | YES |

### L3 Data/telemetry — `tag_telemetry.jsonl`, `tags.csv`, schema

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | BAD/UNCERTAIN volume | 4094/31224 (BAD 1351 UNCERTAIN 2743) | process | Plot as truth | Cause unknown | HIGH | YES |
| Inconsistency | F on TEMP; schema gap | 47 e.g. TEL-00000288; schema misses ingest_time/source/asset_id | process | Mix F and C | Plant unit standard | HIGH | YES |
| Friction | Duplicates | 120 extra packets | cyber | Double-count | Retransmit vs clone | HIGH | PARTIAL |
| Complexity | historian_enabled=NO still in feed | 51 NO tags; all 864 in telemetry | process | Skip NO tags | Flag vs source=HISTORIAN | HIGH | PARTIAL |
| Volatility | Ingest delay | p50 120s max 240s; >60s 23414; **neg 0** | process | Sort on ingest (EVAL-004) | Clock domain | HIGH | YES |
| Uncertainty | UNCERTAIN is a state | 2743; folded into diagnostics | process | Impute to GOOD | Plant meaning | HIGH | YES |
| Hidden Dependency | Only 182 assets tagged | 1834 untagged | process | Join all 2016 | OPEN-020 | HIGH | YES |
| Unknown Unknown | Handover 20-min HMI vs historian; enterprise 407 inversions vs telemetry 0 | email; EVT-0000001 | process | One global clock | UU which clock | MED | YES |

### L4 Asset/configuration — assets, aliases, shadow

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | UNKNOWN/unowned | registered UNKNOWN 122; owner Unknown 343 | cyber | Fill from CMDB name | Meaning of UNKNOWN | HIGH | YES |
| Inconsistency | Five-state clashes + collisions | 200 ACTIVE vs OFFLINE/UNSEEN; 99 RETIRED ONLINE; 5 alias collisions | cyber | CMDB always wins (EVAL-001) | Per-row winner | HIGH | YES |
| Friction | 3 alias sources + non-newer spreadsheet | 6048 aliases; shadow 220 firmware_diff=0 vs email | authority | Merge “newer” sheet | OPEN-015 | HIGH | YES |
| Complexity | 18 plants, colliding names | 5 collision aliases | cyber | Key on alias string | Full alias graph | HIGH | PARTIAL |
| Volatility | Stale config proxy | backup_age >90d 1581 | resilience | Equate to restore-test | vs last_restore_test_days | MED | PARTIAL |
| Uncertainty | INTERMITTENT/UNSEEN | 129 / 128 | process | Coerce to ONLINE | Scan-gap vs down | HIGH | YES |
| Hidden Dependency | Process join sparse | 182 tagged assets | process | Estate-wide mapping | OPEN-020 | HIGH | YES |
| Unknown Unknown | CASCADE 37/6 not in CSV | cascade_001 08:07 | cyber | Invent 37 IDs | OPEN-019 | MED | YES |

### L5 Process/control — units, deps, safe_state

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | Safe-state unused by software | MIN_LOAD 54; manual NO 19 | process | Isolate anyway | vs handover min load | HIGH | YES |
| Inconsistency | Critical undocumented deps | 33 | process | Use documented graph only | Real existence | HIGH | YES |
| Friction | Cyber rarely joins unit | many vulns units=[] e.g. VUL-00706 | process | Fake process-impact prose | No other join key | HIGH | YES |
| Complexity | 9 unit types, 5 dep types | safety deps 49 | process | All deps = IT depends_on | Trip semantics | HIGH | PARTIAL |
| Volatility | Static snapshot | no timestamp on process_units | process | Freeze safe_state | Live operating point | HIGH | YES |
| Uncertainty | ISOLATED vs ISOLATE | 43 units safe_state=ISOLATED vs string ISOLATE | safety | Equate them | Electrical vs process | HIGH | YES |
| Hidden Dependency | Safety-critical downstream | PLT-10-U06→U07 safety critical YES | safety | Isolate U06 alone | Unlisted utilities | HIGH | YES |
| Unknown Unknown | No envelope/trip matrix | 6 columns only | safety | Twin narrative | UU causality | HIGH | YES |

### L6 Cyber — vulns, alerts, remote sessions

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | OPEN + no control | OPEN 799; control NONE 222 UNKNOWN 235 | cyber | MITIGATED=safe | Control test | HIGH | PARTIAL |
| Inconsistency | severity≠CVSS; high CVSS unreachable | 830 mismatch; VUL-00008 CRITICAL/4.1; VUL-00706 9.8 reachable NO LOW switch | cyber | Rank by CVSS or label (EVAL-002) | Scanner intent | HIGH | YES |
| Friction | Missing process context | 525/860 HIGH+CRIT UNKNOWN | process | Isolate on HIGH | Why UNKNOWN | HIGH | YES |
| Complexity | 7 alert types; 4 access methods | laptop 170 vpn 169 | cyber | One malware playbook | TPR unmeasured | MED | PARTIAL |
| Volatility | 2800 alerts ~35 days | 404 UNEXPECTED_WRITE | authority | Calm if OPEN drops | Synthetic vs campaign | HIGH | PARTIAL |
| Uncertainty | Reachability/MFA UNKNOWN | reachable UNKNOWN 344; mfa UNKNOWN 72; identity unknown 140 | cyber | Coerce YES or NO | UNKNOWN≠permission | HIGH | YES |
| Hidden Dependency | Service laptop / ENG_WS vendor | 10 vendor.engineer on ENG_WORKSTATION | cyber | Model jump_host only | No NAC | HIGH | YES |
| Unknown Unknown | No exploit evidence | no evidence_url | cyber | Generate exploit/patch-now | UU real exposure | HIGH | YES |

### L7 Safety — `safety_barriers.csv`

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | 61 not ACTIVE; 10 SIS_TRIP unhealthy | PLT-04-SAFE-19 … PLT-16-SAFE-19 | safety | SIS up because SAFETY_PLC exists | Demand-mode diagnostics | HIGH | YES |
| Inconsistency | Unauthorized bypass | PLT-03-SAFE-14 BYPASSED authorized NO; 157 UNKNOWN | safety | authorized YES = safe | Who authorized 8 YES | HIGH | YES |
| Friction | Barriers unused by isolate | risk.py severity only | safety | Isolate while BYPASSED | OPEN-008 | HIGH | YES |
| Complexity | 5 barrier types | INTERLOCK 101 … SIS_TRIP 73 | safety | ALARM=SIS | SIL absent | HIGH | PARTIAL |
| Volatility | Proof-test debt | 73 not CURRENT | safety | Ignore OVERDUE if ACTIVE | Aging OPEN-006 | HIGH | YES |
| Uncertainty | bypass_authorized UNKNOWN | 157/450 | authority | Fill UNKNOWN | UNKNOWN≠permission | HIGH | YES |
| Hidden Dependency | SAFETY_PLC on MIN_LOAD + unauthorized bypass | OT-00211 / PLT-03-U05 / PLT-03-SAFE-14 | safety | Isolate “just a PLC” | Food-plant detail | HIGH | YES |
| Unknown Unknown | No C&E / SIS program | 7 columns; inject_04 title only | safety | Generate trip matrix | UU protection layers | HIGH | YES |

### L8 Operations — WOs, handover

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | Queue + workarounds | 922 not closed; bypass 94; workaround notes 252 | process | CLOSED=done | field vs observed | HIGH | PARTIAL |
| Inconsistency | Paper-closed | 244 e.g. WO-000009; WO-000018 CLOSED+bypass+awaiting vendor | process | Close risk from CMMS | OPEN-014 | HIGH | YES |
| Friction | Shift email as SOR | vendor done / ticket not / do not isolate | authority | Ignore non-CSV | OPEN-018 | HIGH | YES |
| Complexity | 16/16 status cells filled | CLOSED/ACTIVE 92 … | process | Legal state machine | Generator vs plant | HIGH | PARTIAL |
| Volatility | 259 EMERGENCY vs 2800 alerts | same dates | process | Correlate without keys | Coincidence | MED | PARTIAL |
| Uncertainty | Canned notes | 5 note values | process | parts substituted = MOC | MOC absent | HIGH | PARTIAL |
| Hidden Dependency | Vendor wait inside CLOSED | 64 awaiting vendor CLOSED | resilience | Start recovery | Ticket IDs absent | HIGH | PARTIAL |
| Unknown Unknown | Unit 04 plant unbound | email vs 18×U04 | process | Pick PLT-01-U04 | OPEN-018 | HIGH | YES |

### L9 Enterprise — events, vendors, tracker

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | 9 sources; no ERP file | ~700 each; docs/03 names ERP | cyber | Assume ERP feed | Missing vs OOS | HIGH | PARTIAL |
| Inconsistency | type≠source; empty corr | HISTORIAN SESSION 122; corr empty 3251 | authority | Fake incident timeline | OPEN-012/013 | HIGH | YES |
| Friction | Expired ACCEPT | 134/180 expiry before 2026-09-15; 19 ACCEPT Unknown | authority | ACCEPT=current | OPEN-005 | HIGH | YES |
| Complexity | 18 plants, 10 vendors | regions 5 | cyber | One vendor playbook | OPEN-003 | MED | PARTIAL |
| Volatility | payload_state ~even split | 6 states ~1035–1111 | process | Latest=plant state | vs observed_state | MED | PARTIAL |
| Uncertainty | received before event | 407; EVT-0000001 | cyber | Sort received only | Clock domain | HIGH | YES |
| Hidden Dependency | SLA not joined | RemoteAssist sla 4h vs 224 awaiting vendor | resilience | Promise 4h restore | Contract vs table | MED | PARTIAL |
| Unknown Unknown | No directory | identity unknown 140 | authority | Invent named approvers | OPEN-001 | HIGH | YES |

### L10 Resilience — `recovery_readiness.csv`

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | Flag failures | backup≠CURRENT 25; runbook 35; dep 29; fallback NO 42 | resilience | 119 CURRENT = ready | Image granularity | HIGH | YES |
| Inconsistency | CURRENT is a lie | **113/119** weak; PLT-01 IDENTITY 360d STALE; HISTORIAN 657d; PLC_DCS 510d rto=2 | resilience | backup exists ⇒ recoverable (EVAL-005) | success vs attempt | HIGH | YES |
| Friction | Diagnostics hide the lie | backup key ignores restore days | resilience | Trust /diagnostics | New Measure vs legacy | HIGH | YES |
| Complexity | 8 components × 18 | 144 rows | resilience | Restore “the plant” | Order unknown | HIGH | PARTIAL |
| Volatility | restore p50 376d | >180d 114/144 | resilience | Believe RTO hours | Drift | HIGH | YES |
| Uncertainty | UNKNOWN flags | backup 9; dep 13; LIMITED 47 | resilience | Coerce UNKNOWN | UNKNOWN≠ready | HIGH | YES |
| Hidden Dependency | MES CURRENT + dep NO | PLT-01 MES_INTERFACE 433d dep NO | resilience | Restore MES without identity | Runtime coupling | HIGH | YES |
| Unknown Unknown | No restore artifact | inject_06 title only | resilience | Claim DR tested | UU failure modes | HIGH | YES |

### L11 Decision intelligence

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | Rank/isolate ignore context | 860 ISOLATE candidates; 525 unknown ctx | authority | Contextual AI that still sorts cvss | No gold rank | HIGH | YES |
| Inconsistency | Four “criticality” languages | VUL-00706 vs VUL-00008 vs OT-01016 | cyber | Hide all but one number | Ontology winner | HIGH | YES |
| Friction | 08:47–08:55 war-room not in software | CASCADE-001 | authority | Auto-resolve for SOC | OPEN-001 | HIGH | YES |
| Complexity | Five states + 14 ints + shadow | CHARTER; diagnostics; 3 shadow files | authority | One RAG status | Presentation | HIGH | YES |
| Volatility | Volume vs joins | 2800 alerts; 703 WO overlap | cyber | Cluster by time | OPEN-006 rate | MED | PARTIAL |
| Uncertainty | No uncertainty object | /diagnostics ints; /health ok | authority | Fake confidence=0.9 | SDD-08 schema | HIGH | YES |
| Hidden Dependency | Dead multiplier | legacy_risk_score unused by rank | cyber | Cite unused formula | Confirmed only in risk.py | HIGH | PARTIAL |
| Unknown Unknown | No “actionable incident” label | docs/05 BASELINE_PENDING | process | Train on cvss | UU leadership accept | MED | YES |

### L12 Autonomy/assurance — ACTION_TIERS, evals, forbidden actions

| Lens | Finding | Evidence | Conseq | Naive-AI | Residual | Conf | Block |
|---|---|---|---|---|---|---|---|
| Imperfection | Stub evals; XFAIL not a gate | EVAL-001..006; 3 xfail | authority | Enable agent because jsonl exists | SDD-08 thresholds | HIGH | YES |
| Inconsistency | Tiers vs docs/06; ISOLATE ungoverned | isolate_endpoint tier 3 vs recommend string | authority | Execute isolate because recommend is tier 1 | OPEN-004 | HIGH | YES |
| Friction | HITL test is PLC/SIS only | test_safety_critical_actions_require_human_approval | authority | HITL exists | No audit log | HIGH | YES |
| Complexity | Tiers 0–4; tier 4 forbidden | write_plc_logic/setpoint/modify_sis/bypass_interlock | safety | Add tier 4 “with confirm” | trip suppression unnamed in dict | HIGH | YES |
| Volatility | No prompt/model registry | no src/prompts | authority | Swap models | SDD-09 | MED | YES |
| Uncertainty | Unnamed humans + default 4 | OPEN-001; CASCADE 08:55 | authority | Fill “SOC manager” | Named authority missing | HIGH | YES |
| Hidden Dependency | Must keep XFAIL + dirty data | docs/07; AGENTS.md | authority | Make tests pass by changing expect | Repo 3.0 path later | HIGH | YES |
| Unknown Unknown | Read-only today ≠ forever | api.py; Dockerfile :8000 | safety | Assume no write API later | SDD-13 guardrail | MED | YES |

**96/96 filled.** Deep-dive packs: `top15.md`.
