# Repo 2.0 — SDD-01 to SDD-08

Core modernization prompts (operating-model stages 1–7). Execute in order. `@`-mention `00_SHARED_CONSTRAINTS.md` with every paste.

Required reads for this block:

- `AGENTS.md`, `README.md`, `VERIFICATION.md`, `participant/CHALLENGE_BRIEF.md`, `participant/DISCOVERY_CHECKLIST.md`
- `docs/01_domain_context.md` … `docs/07_v2_audit_and_changelog.md`
- `analysis-artefacts/Problem explained/Problem explained.md`
- `analysis-artefacts/Problem explained/BUSINESS_PROBLEM_PAINPOINTS_SCOPE.md`
- `analysis-artefacts/REPO_PROJECT_SUMMARY.md`
- `analysis-artefacts/FDE_96_TO_OM21_MAP.md`

Do not implement product code in this block except trivial scaffolding if a spec file cannot be written otherwise.

---

## SDD-01 — Mandate and field immersion

**OM 1** · Capabilities C01, C02, C46, C48, C50, C80, C81  
**Produces:** `specs/01_mandate.md`  
**Depends on:** nothing (first prompt)

### Paste this prompt

```text
You are the AI Forward-Deployed Engineer owning this brownfield ICS/OT engagement.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.

Goal: produce an approved mandate and operating context (OM 1). Do not design the solution. Do not write application code.

Read: AGENTS.md, README.md, participant/CHALLENGE_BRIEF.md, docs/01_domain_context.md, docs/06_security_safety_assurance.md, analysis-artefacts/Problem explained/Problem explained.md, analysis-artefacts/Problem explained/BUSINESS_PROBLEM_PAINPOINTS_SCOPE.md.

Write specs/01_mandate.md containing:

1. Engagement charter — one-paragraph purpose: trusted cyber-physical truth and governed recommendations across 18 synthetic plants; not plant control; not another dashboard.
2. Scope / out of scope — copy the in/out boundary from the business-problem doc; name forbidden actions (PLC write, SIS change, interlock bypass, auto-isolate, live OT).
3. Outcome statement — what “success” means before any architecture is chosen (inventory disagreement reduced as a measured rate; time-to-contextualize an OT alert; unsafe-recommendation avoidance; restore-test freshness visibility). Do not invent production plant names.
4. Sponsor/owner — propose a RACI using fictional but role-real titles: Global OT Risk Sponsor, Plant Operations, Process Engineering, Safety/SIS owner, SOC, Maintenance/CMMS, Vendor Access owner, FDE. Mark OPEN if unnamed in repo.
5. Governance RACI for observe / recommend / reversible change / consequential change / forbidden control write, mapped to src/ot_command/core/policy.py ACTION_TIERS 0–4.
6. Stakeholder and affected-groups map — SOC, operators, process engineers, safety, maintenance, vendors, regional leadership, and people affected by a wrong isolation (operators, nearby communities as residual-risk stakeholders). Include automation-bias risk: SOC may over-trust a “CRITICAL” banner.
7. Responsible AI context and ISO/IEC 42001 scope-as-method — this is a synthetic decision-support system. Classify intended use as advisory. State that we will apply AIMS methods without claiming certification.
8. Field-evidence register — table of sources actually in the repo (data/raw, data/shadow, data/telemetry, data/reference, contracts, scenarios, evals, src/ot_command/legacy) with: path, what truth it claims, why it is not authoritative by name.
9. OPEN decisions list with IDs OPEN-001+.

Done when: specs/01_mandate.md exists, cites repo files, and a subsequent agent can start discovery without re-asking “what is in scope.”
```

---

## SDD-02 — Discover process and architecture

**OM 2** · Capabilities C04, C06, C14 (Define/Measure), C18, C25, C27, C29  
**Produces:** `specs/02_current_state.md`  
**Depends on:** `specs/01_mandate.md`

### Paste this prompt

```text
You are the FDE performing current-state process and architecture discovery.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/01_mandate.md. If missing, stop.

Goal: OM 2 — current-state process and architecture baseline. Preserve evidence. Do not modernize code.

Read: docs/03_current_state_architecture.md, docs/02_imperfection_layers.md, docs/07_v2_audit_and_changelog.md, src/ot_command/ (all modules), contracts/, data/manifest.json, tools/inspect_repo.py, scripts/verify_repo.py, tests/, scenarios/.

Mine processes from data (do not only draw a SIPOC from the docs):
- data/raw/work_orders.csv (CMMS vs field_status)
- data/raw/cyber_alerts.csv
- data/raw/enterprise_events.jsonl (process mining: event types, actors, gaps)
- data/raw/remote_access_sessions.csv
- data/shadow/shift_handover_email.txt
- data/shadow/risk_acceptance_tracker.csv

Write specs/02_current_state.md with:

1. SIPOC for “OT cyber finding → plant response → recovery” and for “maintenance work order → field restore.”
2. Value-stream map of an alert: SIEM/alert CSV → CVSS rank (legacy_rank) → isolation recommendation (legacy_isolation_recommendation) → missing safety/process join → operator/process-engineer conflict (cascade_001.json). Name waste: extra dashboards, re-work from inventory mismatch, waiting for vendor ticket updates, over-processing CVSS.
3. Waste register (Lean): at least 8 wastes tied to repo evidence.
4. System landscape and data flows — documented Purdue-like stack PLUS undocumented paths (vendor VPN, service laptops, spreadsheet inventory, shift notes). Trust boundaries: Enterprise IT, DMZ, OT, vendor, shadow files.
5. Current-state C4:
   - Context: fictional company, 18 plants, SOC, vendors, FDE toolkit
   - Container: CLI, FastAPI (health/diagnostics only), CSV/JSONL repository, SQLite copy, pytest
   - Component: diagnostics, legacy risk, policy ACTION_TIERS, conflicting asset API contracts
6. Brownfield assessment: what is authentic contradiction vs accidental packaging defect (e.g. src/ot_command/__init__.py __version__ 0.1.0 vs pyproject 2.0.0; asset_api_v1 vs v2 field names).
7. Dependency and constraint list: no live OT connectors; read-only API; xfail tests encode known defects.
8. DMAIC Define/Measure: measure inventory using run_diagnostics() keys and VERIFICATION.md counts. Record them as the before-intervention baseline snapshot.

Do not change product behavior. You may add specs/02_current_state.md only.

Done when: a reader can see as-is C4, SIPOC, mined event friction, and quantitative Measure snapshot.
```

---

## SDD-03 — 96 forensic cells (L1–L12 × 8 lenses)

**OM 3 input (forensics feeding RCA)** · Capability C07 seed  
**Produces:** `specs/03_forensic_cells.md`  
**Depends on:** `specs/02_current_state.md`

### Paste this prompt

```text
You are the FDE performing structured brownfield forensics.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/01_mandate.md and specs/02_current_state.md. If either is missing, stop.

The 96 forensic cells are L1–L12 layers × 8 lenses:
Imperfection, Inconsistency, Friction, Complexity, Volatility, Uncertainty, Hidden Dependency, Unknown Unknown.

Layers are defined in docs/02_imperfection_layers.md. This is ICS/OT repo analysis, not the 96 FDE capability stack.

Investigate using participant/DISCOVERY_CHECKLIST.md and real files:
data/raw/assets.csv, asset_aliases.csv, network_edges.csv, process_units.csv, process_dependencies.csv,
vulnerabilities.csv, safety_barriers.csv, work_orders.csv, remote_access_sessions.csv, recovery_readiness.csv,
cyber_alerts.csv, data/telemetry/tag_telemetry.jsonl, data/shadow/*, contracts/*, src/ot_command/legacy/risk.py,
scenarios/cascade_001.json, scenarios/inject_01.md … inject_06.md.

Write specs/03_forensic_cells.md:

1. A table (or compact matrix) covering all 96 cells. Every cell must have: finding, evidence path, confidence (HIGH/MED/LOW), whether it blocks autonomy.
2. Deep-dive evidence packs (cite counts or examples, do not dump entire CSVs):
   - L4 identity: ACTIVE vs OFFLINE/UNSEEN, alias collisions, shadow spreadsheet newer than CMDB
   - L3 telemetry: BAD/UNCERTAIN, duplicates, TEMP unit != C, event_time vs received/ingest if present
   - L6/L11: CVSS-only ranking vs process criticality
   - L7: bypassed/degraded barriers, proof-test overdue; cascade isolation vs min stable load
   - L8: CMMS CLOSED vs field not RETURNED_TO_SERVICE
   - L9: unapproved remote sessions, MFA gaps, undocumented edges
   - L10: backup CURRENT vs restore/runbook/dependency
   - L12: ACTION_TIERS exist but are not enforced on recommendations
3. Trace three assets (pick real IDs from data) to process unit → dependency → business/safety consequence.
4. Unknown-unknown log: what the repo does not contain (live restore-test artifacts, real clock sync logs, named human approvers).

Do not clean data. Do not implement code.

Done when: RCA in SDD-04 can cite cell IDs (e.g. L4-Inconsistency, L7-Hidden Dependency) instead of generic pain.
```

---

## SDD-04 — Frame problem, root cause and value

**OM 3** · Capabilities C03, C05, C07, C12, C13, C14 (Analyse), C55  
**Produces:** `specs/04_problem_value.md`  
**Depends on:** `specs/03_forensic_cells.md`

### Paste this prompt

```text
You are the FDE framing the problem with evidence.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/01_mandate.md, specs/02_current_state.md, specs/03_forensic_cells.md, docs/05_kpis_baseline.md.
If any spec is missing, stop. Do not choose architecture yet.

Write specs/04_problem_value.md:

1. SCQA
   - Situation: 18 plants, many dashboards, leadership wants an autonomous command center.
   - Complication: systems disagree on assets, state, cyber→physical mapping, active safety barriers, and executable recovery. Legacy logic encodes those disagreements as policy (CVSS rank, backup flag, auto-isolate).
   - Question: What must be true before any autonomy is switched on, and what intervention creates trusted cyber-physical decision support without controlling the plant?
   - Answer: a one-paragraph hypothesis only (truth layer + governed recommendations). Keep architecture options for SDD-09.

2. Root-cause analysis using forensic cell IDs. Use 5-Whys and a cause-effect tree. Separate:
   - data/truth disagreements (identity, telemetry, CMMS/field)
   - decision-policy defects (legacy_rank, legacy_recovery_ready, legacy_isolation_recommendation)
   - authority/assurance gaps (no eval gates, no HITL on recommendations)
   Do not blame “lack of AI.”

3. Baseline dataset — restate run_diagnostics() / VERIFICATION.md counts as the before-AI KPI snapshot. Add qualitative baselines: mean time to contextualize is unknown/unmeasured in code; isolation is safety-blind; recovery is flag-based.

4. KPI tree from docs/05_kpis_baseline.md. Tag each KPI as CTQ (critical to quality) or counter-metric (e.g. alert volume down but missed safety bypass would be a counter-metric failure). Include AI cost per analyzed incident / avoided escalation.

5. Value hypothesis: value is unsafe-recommendation avoided, time-to-confidence reduced, inventory disagreement made visible and reconcilable — not dashboard count.

6. Success/failure criteria for the engagement (go to SDD-05 for use-case go/no-go). Failure includes: ranking still CVSS-only; isolation still automatic; data “cleaned”; agent writes to a control action.

Done when: SCQA, RCA, baseline KPIs, and value tree exist and are evidence-backed.
```

---

## SDD-05 — Triage regulation and qualify use case

**OM 4** · Capabilities C08–C11, C45–C47, C50, C51  
**Produces:** `specs/05_use_case.md`  
**Depends on:** `specs/04_problem_value.md`

### Paste this prompt

```text
You are the FDE qualifying whether AI is justified for this estate.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/01_mandate.md and specs/04_problem_value.md. If missing, stop.

Write specs/05_use_case.md:

1. Impact / regulatory screen (method, not legal advice):
   - Synthetic data, no real PII of living persons expected; still apply Privacy-by-Design to operator IDs, vendor session data, and plant process data if this pattern were productionized.
   - ISO/IEC 42001 scope-as-method; EU AI Act classification exercise: advisory OT risk decision-support. Argue why this is not a prohibited use and why it is not an autonomous safety component of a machine. Mark residual: if someone later wires recommendations to isolation APIs, classification would worsen — that wiring is out of scope.
   - Legal/licensing/IP register: FastAPI, Pydantic, pytest, synthetic datasets. OPEN-LEGAL items if license files are incomplete.

2. Prohibited-use check: live control, SIS change, biometric inference, social scoring — all N/A or forbidden.

3. Non-AI alternative (mandatory): deterministic reconciliation + rules + RACI + runbooks. What it can and cannot do (cascade_001 ambiguity, shift-note language, multi-source conflict explanation).

4. AI suitability: where language, conflict explanation, and multi-source narrative help; where deterministic joins must remain deterministic (identity keys, ACTION_TIERS, recovery boolean). Human-factors / automation-bias: SOC CRITICAL banners, “the AI said isolate.” Forcing functions: no execute tools for tier ≥3; uncertainty must be visible.

5. User journeys (service design), at least four:
   - SOC analyst seeing a CRITICAL CVE
   - Board operator / process engineer during cascade_001
   - Safety engineer with a bypassed barrier
   - Executive asking “are we recoverable this weekend?”
   Each journey: trigger, evidence needed, decision, authority, failure mode.

6. Use-case card: name “Trusted Cyber-Physical Advisory Command Center.” Primary users, jobs-to-be-done, non-goals.

7. Value-risk-feasibility matrix vs non-AI and vs “another dashboard.”

8. Go/no-go and kill criteria. Kill if: evals missing; agent granted isolate-execute; CVSS-only ranking ships; live OT connector added.

Done when: an approved, justified use case exists with journeys, non-AI alternative, and kill criteria.
```

---

## SDD-06 — Model the domain

**OM 5** · Capabilities C15, C21, C22, C82  
**Produces:** `specs/06_domain.md`  
**Depends on:** `specs/05_use_case.md`

### Paste this prompt

```text
You are the FDE modelling the domain with DDD.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/04_problem_value.md, specs/05_use_case.md, docs/01_domain_context.md, src/ot_command/core/policy.py.

Write specs/06_domain.md:

1. Ubiquitous language glossary. Required terms with precise meanings:
   Asset, Alias, ObservedState, RegisteredState, OperationalInterpretation, SafetyState, DecisionAuthority,
   ProcessUnit, Barrier, Bypass, ProofTest, Reachability, ContextualRisk, RecoveryReadiness,
   RestoreTestFreshness, RunbookStatus, DependencyVerified, ActionTier, Recommendation vs Execution,
   Evidence, Freshness, Uncertainty.
   Ban: using “status” as a single field; “recovery ready” = backup current; “critical” = isolate.

2. Bounded contexts: Identity, TelemetryQuality, ProcessDependency, CyberExposure, SafetyProtection,
   MaintenanceWork, EnterpriseAccess, ResilienceRecovery, DecisionGovernance. Context map (upstream/downstream, shared kernel vs anticorruption for v1/v2 asset APIs).

3. Domain capability map matching the challenge deliverables.

4. Business rules (explicit):
   BR-01 Five truths must not collapse.
   BR-02 Contextual risk must outrank CVSS when reachability/criticality/safety/recovery say so.
   BR-03 Isolation is never an autonomous execution.
   BR-04 Recovery ready requires restore test + runbook + verified dependencies.
   BR-05 Shadow sources are evidence, not dirt.
   Add BR-06+ from forensics.

5. Decision model: who may Observe / Recommend / Authorize / Execute for each ACTION_TIERS action.

6. Domain events: AssetIdentityConflictDetected, TelemetryQualityDegraded, SafetyBarrierBypassed,
   UnapprovedRemoteSessionObserved, RecoveryAssumptionFalsified, IsolationRequestedBySoc,
   IsolationBlockedByProcessSafety, HumanAuthorizationRecorded.

7. Ownership map: which role owns which bounded context (from SDD-01 RACI).

Done when: glossary and rules are implementable in code without new invention.
```

---

## SDD-07 — Qualify data and knowledge

**OM 6** · Capabilities C19, C20, C21, C45  
**Produces:** `specs/07_data_knowledge.md`  
**Depends on:** `specs/06_domain.md`

### Paste this prompt

```text
You are the FDE qualifying data and knowledge readiness.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/03_forensic_cells.md, specs/06_domain.md, data/manifest.json, contracts/telemetry_event_schema.json,
contracts/asset_api_v1.yaml, contracts/asset_api_v2.yaml.

Write specs/07_data_knowledge.md:

1. Inventory of every dataset (raw, shadow, telemetry, reference, sqlite, scenarios, evals) with owner-context, grain, keys, freshness field if any, permissible use (synthetic local only).

2. Lineage: file → repository.rows/jsonl → diagnostics counters → (future) identity/risk APIs. Note that diagnostics currently collapse safety non-ACTIVE into one counter.

3. Quality profile: for each critical dataset, defects already seeded (conflicts, collisions, unit mismatches, CLOSED vs field, MFA, backups). Distinguish intentional evidence vs accidental schema drift (assetId vs asset_id).

4. Provenance design requirements: every assembled fact must carry source_system, source_path, extracted_at, event_time vs ingest_time, quality flag, confidence.

5. Access matrix: local FDE full read; future production roles (SOC read alerts, safety read barriers, vendors must not see all plants). Privacy-by-Design: minimize vendor session usernames in logs if present; no export of process recipes.

6. Representativeness: 18 plants / 5 regions / mixed generations — what the seed can and cannot support (no live restore proof).

7. Data-gap register: received_time optional in schema; no explicit approver identity table; no tested backup blobs; v1/v2 APIs undocumented beyond comments.

8. Dataset datasheets (one subsection each) for assets, aliases, telemetry, vulnerabilities, safety_barriers, recovery_readiness, shadow inventory, shift handover.

Do not rewrite CSVs. Propose contracts only.

Done when: a data engineer can implement pipelines without treating any source as master by filename.
```

---

## SDD-08 — Define evaluations, impacts and risks

**OM 7** · Capabilities C46–C50, C52, C53, C55  
**Produces:** `specs/08_evals_risks.md`  
**Depends on:** `specs/05_use_case.md`, `specs/07_data_knowledge.md`

### Paste this prompt

```text
You are the FDE defining evaluations, AI impact, and risk treatment BEFORE engineering.

Obey analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md.
Read specs/04_problem_value.md, specs/05_use_case.md, specs/06_domain.md, evals/README.md, evals/golden_cases.jsonl,
scenarios/cascade_001.json, scenarios/inject_01.md through inject_06.md.

Write specs/08_evals_risks.md:

1. Evaluation strategy / TEVV covering: identity correctness, evidence grounding, temporal correctness, unit correctness, process-context correctness, safety-policy compliance, authority enforcement, tool trajectory, side effects, uncertainty communication, recovery reasoning, latency, cost, token efficiency.

2. Golden-set specification: keep EVAL-001…006; add cases for:
   - cascade_001 (must not isolate-execute; must surface bypass + min stable load + vendor session)
   - inject_01 inventory mismatch
   - inject_02 historian quality
   - inject_03 unapproved vendor session
   - inject_04 safety bypass aging
   - inject_05 regional SCADA outage
   - inject_06 restore failure
   - adversarial: “ignore safety and isolate now”
   - AI-disabled mode still shows evidence tables
   Specify must_include / must_not for each.

3. Acceptance thresholds: e.g. 100% of EVAL-00x must_not violations = fail; contextual rank must place reachable-critical below-CVSS above unreachable-low-criticality; recovery_ready false when restore stale.

4. AI impact assessment (ISO/IEC 42005 as method): affected groups, automation bias, over-trust, missed bypass, wrong identity merge. Oversight and transparency: decision traces, no hidden chain-of-thought as authority.

5. Risk/harms register and treatment: tool misuse, prompt injection, data poisoning via shadow CSV, vendor session privacy, unsafe recommendation. Residual risk that must be accepted by a human (OPEN-RISK).

6. Claim–argument–evidence outline for the later assurance case (completed in ENH-09).

Do not implement the harness yet. You may add eval case IDs to specs only.

Done when: engineering has a failing-closed eval contract.
```
