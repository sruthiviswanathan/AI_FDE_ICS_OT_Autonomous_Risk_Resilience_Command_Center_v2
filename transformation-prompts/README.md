# FDE transformation prompt pack

Executable Cursor/FDE prompts that move this brownfield repo along the **AI FDE Modernization Journey** (specs-driven development):

```text
Repo 1.0  --15 SDD prompts-->  Repo 2.0  --10 ENH prompts-->  Repo 3.0  -->  PRD + APP
Brownfield                    Structured SDD                Production-oriented     Product-ready
baseline                      repo                          repo                   artifacts
```

Source of truth for the 21-stage operating model: `1789394514979_FDE operating model.xlsx` Sheet2. Capability homes: `analysis-artefacts/FDE_96_TO_OM21_MAP.md`. Problem: `analysis-artefacts/Problem explained/`.

## How to execute

1. Open this repo in Cursor. Work on a feature branch.
2. `@`-mention `00_SHARED_CONSTRAINTS.md` and the prompt file section you are running.
3. Run prompts **in order**. Do not skip gates.
4. After each prompt, commit only if the user asks. Leave artifacts on disk either way.
5. At SDD-15, the repo is **Repo 2.0** (specs, ADRs, layout, coverage CSV).
6. At ENH-10, the repo is **Repo 3.0** (code remediations, evals, assurance, ops telemetry).
7. Then run the product-ready pack (PRD, APP, REL) to close OM 16–21.

If an upstream artifact is missing, stop. Re-run that prompt.

---

## Operating model (Excel Sheet2)

| # | Workflow | Methods | Essential artifacts | Output to next phase |
|---|---|---|---|---|
| 1 | Mandate and field immersion | FDE ownership · Stakeholder discovery · Responsible AI context · ISO/IEC 42001 scope | Engagement charter · Scope · Outcome statement · Sponsor/owner · Governance RACI · Stakeholder and affected-groups maps · Field-evidence register | Approved mandate and operating context |
| 2 | Discover process and architecture | Process Discovery · Lean · Waste Elimination · DMAIC Define/Measure · Architecture Discovery · Brownfield repo assessment · C4 | SIPOC · Process/value-stream maps · Waste register · System landscape · Brownfield assessment · Current-state C4 views · Dependencies · Data flows · Trust boundaries | Current-state process and architecture baseline |
| 3 | Frame problem, root cause and value | SCQA · DMAIC Analyse · Root-cause analysis · Baseline KPIs · Data-driven framing | SCQA problem frame · Root-cause analysis · Baseline dataset · KPI tree · CTQs · Value hypothesis · Counter-metrics · Success/failure criteria | Evidence-backed problem and baseline |
| 4 | Triage regulation and qualify use case | Responsible AI · ISO/IEC 42001 · EU AI Act classification · AI suitability · Solution Decoding | Impact/regulatory screen · Prohibited-use check · AI suitability assessment · Non-AI alternative · Use-case card · Value-risk-feasibility matrix · Go/no-go and kill criteria | Approved and justified use case |
| 5 | Model the domain | DDD · Ubiquitous Language · Bounded Contexts · Domain Events | Glossary · Domain capability map · Business rules · Decision model · Domain events · Ownership map · DDD Context Map · Bounded Contexts | Domain and decision model |
| 6 | Qualify data and knowledge | Data Discovery · Quality · Lineage · Provenance · Permissible use · Knowledge discovery | Data/knowledge inventories · Lineage · Quality profile · Provenance · Access matrix · Representativeness assessment · Data-gap register · Dataset datasheets | Data and knowledge readiness assessment |
| 7 | Define evaluations, impacts and risks | Evals · Responsible AI · ISO/IEC 42005 · ISO/IEC 42001 risk planning · EU AI Act requirements | Evaluation strategy · Golden-set specification · Scenarios · Acceptance thresholds · AI impact assessment · Risk/harms registers · Risk treatment · Oversight and transparency requirements | Evaluation, impact and risk requirements |
| 8 | Generate, test and select options | Solution Decoding · Reference Architectures · GenAI patterns · PoCs · Trade-off Matrices | Solution catalogue · Reference-architecture comparison · PoC/model/RAG results · Weighted trade-off matrix · Build/buy assessment · Provider comparison · Preliminary ADRs · Selected solution | Approved solution and trade-offs |
| 9 | Design information architecture | Semantic Layers · Ontology · Knowledge Graphs · Graph/Vector Databases · Data Architecture Decisions | Target data architecture · Data contracts · Semantic model · Metadata/provenance design · Retrieval architecture · Data ADRs · Conditional ontology and graph/vector schemas | Approved information architecture |
| 10 | Design AI and application architecture | C4 · GenAI patterns · RAG · Model routing · Prompt/context design · Integration/deployment patterns | Target C4 · AI/RAG architecture · Model-routing design · API contracts · Prompt/context design · Deployment topology · Failure-mode design · Architecture ADRs | Complete base AI/application architecture |
| 11 | Design agentic and multi-agent orchestration | Agentic AI · Single- vs multi-agent · Orchestration · HITL · Agent communication and control | Agent-suitability · Autonomy-level ADR · Responsibility map · Orchestration · Sequence diagram · State machine · Tool catalogue · Identity/permission matrix · Shared memory · Handoff · Termination/loop · Human approval/override/escalation | Approved, bounded and testable agentic architecture |
| 12 | Design security, guardrails and supplier controls | AI Security · Threat Modelling · OWASP GenAI LLM Top 10 2026 · OWASP Agentic Top 10 2026 · Guardrails · Supply-chain assurance | Threat model · Attack-surface · Trust boundaries · Abuse cases · OWASP mapping · Guardrail architecture · Control matrix · Supplier/model assessment · Model/system cards · Component register · SBOM/AIBOM · Exit plan | Controlled architecture and approved components |
| 13 | Approve ADRs and delivery specification | ADRs · Spec-Driven Development · Telemetry/Observability design · Traceability | Final ADR register · Approved C4 · Delivery specification · NFRs · API/data contracts · Agent specifications · Evaluation cases · Telemetry/logging specification · Rollback · Traceability matrix · Backlog | Build-ready specification |
| 14 | Engineer | AI-Assisted Engineering · SDD using Cursor · Brownfield integration · Agent/workflow implementation | Source/IaC · Prompt/configuration registry · Model/tool versions · Data pipelines · Agent definitions · Orchestration workflows · Unit/integration tests · CI/CD evidence · As-built C4 | Versioned deployable increments |
| 15 | Evaluate, attack and independently assure | Model/RAG/agent evals · RAI testing · OWASP testing · Red teaming · Guardrail validation | Evaluation harness · Golden datasets · Model/RAG results · Agent task-completion · Handoff/coordination/conflict/loop tests · Prompt-injection/tool-misuse tests · Assurance report · Residual-risk acceptance | Independently assured release candidate |
| 16 | Prepare operations, recovery and regulatory evidence | Telemetry · Observability · Change management · Pre-production Chaos Drill · ISO/IEC 42001/42005 · EU AI Act | Operational RACI · Agent/LLM telemetry · Dashboards/alerts · Runbooks · Incident/rollback plans · SOPs/training · Recovery evidence · AI-system record · Technical documentation · Transparency records | Operationally and legally ready release |
| 17 | Deploy progressively and integrate adoption | Shadow/pilot/canary · Bounded agent autonomy · Human–AI workflow integration | Release manifest · Deployment record · Pilot/canary results · Autonomy-expansion record · Rollback decision · Adoption dashboard · Override/workaround logs · Updated SOPs | Controlled live service and adoption evidence |
| 18 | Monitor and validate operational resilience | Telemetry · Observability · Continuous Evals · Agent monitoring · Drift · Controlled Chaos Drills | Operational dashboards · Traces · Inter-agent logs · Drift reports · Cost/availability · Incident records · Agent-loop alerts · Chaos/recovery results · Updated runbooks | Operational performance, risk and resilience evidence |
| 19 | Prove value and tell the decision story | KPIs before/after · DMAIC Improve · Lean · SCQA · Data-Driven Storytelling | Benefits-realisation · Before/after KPIs · Cost-to-value · Counter-metrics · Waste reduction · Unintended effects · Executive SCQA · C4 executive view · Decision recommendation | Evidence-backed scale/change/stop package |
| 20 | Evaluate AIMS and decide lifecycle state | ISO/IEC 42001 Check/Act · Internal audit · Management review · DMAIC Control · Change reassessment | AIMS performance report · Audit findings · CAPA · Management-review decision · Control plan · Updated impact/risk/C4/ADRs/evaluations · Scale/change/restrict/suspend/retire | Authorised lifecycle state or return to an earlier phase |
| 21 | Retire and capture reusable IP | Safe retirement · Record control · Lessons learned · Reference Architecture improvement | Retirement plan · Notifications · Access revocation · Data/model/memory disposition · Agent/tool credential revocation · Supplier closure · Reusable ADRs/C4 · Updated reference architectures · Eval and guardrail templates | Formally closed system and reusable FDE IP |

---

## Prompt map

| Prompt | File | OM | Journey | Primary artifacts | Code / remediation |
|---|---|---|---|---|---|
| SDD-01 | `REPO_2.0_SDD_01_TO_08.md` | 1 | 1.0→2.0 | `specs/01_mandate.md` | None (charter only) |
| SDD-02 | same | 2 | 1.0→2.0 | `specs/02_current_state.md` | None (as-is; note packaging defects) |
| SDD-03 | same | 3 (forensics) | 1.0→2.0 | `specs/03_forensic_cells.md` | None |
| SDD-04 | same | 3 | 1.0→2.0 | `specs/04_problem_value.md` | None |
| SDD-05 | same | 4 | 1.0→2.0 | `specs/05_use_case.md` | None |
| SDD-06 | same | 5 | 1.0→2.0 | `specs/06_domain.md` | None |
| SDD-07 | same | 6 | 1.0→2.0 | `specs/07_data_knowledge.md` | None |
| SDD-08 | same | 7 | 1.0→2.0 | `specs/08_evals_risks.md` | Expand eval spec only |
| SDD-09 | `REPO_2.0_SDD_09_TO_15.md` | 8 | 1.0→2.0 | `specs/09_options.md` + preliminary ADRs | Optional read-only PoC notes, no product rewrite |
| SDD-10 | same | 9 | 1.0→2.0 | `specs/10_information_architecture.md` | Contract drafts |
| SDD-11 | same | 10 | 1.0→2.0 | `specs/11_ai_app_architecture.md` | API contract drafts |
| SDD-12 | same | 11 | 1.0→2.0 | `specs/12_agentic.md` | Tool-catalogue spec vs `ACTION_TIERS` |
| SDD-13 | same | 12 | 1.0→2.0 | `specs/13_security_guardrails.md` | Guardrail spec |
| SDD-14 | same | 13 | 1.0→2.0 | `specs/14_delivery_spec.md` + traceability | Backlog of remediations |
| SDD-15 | same | 13 gate | **Repo 2.0** | Layout, `FDE_96_COVERAGE.csv` | Scaffold dirs only |
| ENH-01 | `REPO_3.0_ENH_01_TO_10.md` | 14 | 2.0→3.0 | Identity reconciliation | `identity` module + API |
| ENH-02 | same | 14 | 2.0→3.0 | Telemetry quality | Provenance-aware telemetry |
| ENH-03 | same | 14 | 2.0→3.0 | Contextual risk | Parallel to `legacy_rank` |
| ENH-04 | same | 14 | 2.0→3.0 | Safety/security conflict | Isolation recommender (advisory) |
| ENH-05 | same | 14 | 2.0→3.0 | Recovery graph | Parallel to `legacy_recovery_ready` |
| ENH-06 | same | 14 | 2.0→3.0 | Process/consequence join | Dependency/impact API |
| ENH-07 | same | 14 | 2.0→3.0 | Bounded agent + prompt registry | Advisory agent, traces |
| ENH-08 | same | 15 | 2.0→3.0 | Red-team / OWASP tests | Injection, tool-misuse, loop tests |
| ENH-09 | same | 15 | 2.0→3.0 | Eval harness + assurance | Golden set runner, report |
| ENH-10 | same | 16 | **Repo 3.0** | Ops telemetry, FinOps, readiness | Decision telemetry, SLOs |
| PRD-01 | `PRODUCT_READY_PRD_APP_REL.md` | 4/13/19 | Product | PRD | Requirements freeze |
| APP-01 | same | 14/16 | Product | Read-only command-center API | Route expansion |
| APP-02 | same | 10/14 | Product | Operator UI with AI-disabled mode | Front-end |
| REL-01 | same | 16 | Product | `ops/` runbooks, RACI, IR | Docs + templates |
| REL-02 | same | 17–18 | Product | Shadow/pilot pack (advisory only) | No live OT canary |
| REL-03 | same | 19 | Product | Executive defense | KPI before/after |
| REL-04 | same | 20–21 | Product | AIMS lifecycle + retirement plan | Workshop only |

---

## Target solution the later prompts implement

SDD-01…08 **must not assume** the architecture. SDD-09 is required to select it from evidence. The intended winning option, unless SDD-09 produces a better evidenced alternative:

**Trusted Cyber-Physical Truth Layer + Bounded Advisory Command Center**

Not another dashboard. A reconciliation and decision-support system that:

1. Reconciles inventories without collapsing five state types into one field.
2. Treats telemetry as evidence with quality, event time, and provenance.
3. Ranks cyber findings by process/safety/recovery context, not CVSS alone.
4. Detects safety/security conflicts (SOC isolate vs process-safe operation).
5. Scores recovery as restore-tested + runbook-complete + dependency-verified.
6. Recommends only; humans authorize consequential actions.
7. Is eval-gated before any agent is enabled.

Conditional (only if SDD-09 justifies): hybrid retrieval over shift notes/runbooks; evidence graph for identity/dependency joins. Default agent posture: **single bounded advisory agent**, not a multi-agent control plane.

---

## Repo 1.0 defects the remediations must address (do not silently clean data)

From `src/ot_command/legacy/risk.py` and `tests/test_known_legacy_defects.py` (currently `xfail`):

- `legacy_rank` sorts by CVSS only.
- `legacy_recovery_ready` trusts `backup_status == CURRENT`.
- `legacy_isolation_recommendation` returns `ISOLATE` for HIGH/CRITICAL with no safe-state check.

From runtime: API is `/health` + `/diagnostics` only; asset API v1/v2 field names conflict; `__version__` is `0.1.0` while `pyproject.toml` is `2.0.0`. Seeded diagnostics (asset conflicts, alias collisions, undocumented paths, dirty telemetry, safety bypasses, CMMS/field split, unapproved remote access, recovery gaps) are **evidence**, not dirt.
