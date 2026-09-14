# 96 FDE capabilities → Operating Model 21 (exact PDF homes)

Two different “96s” exist in this capstone. Do not collapse them.

| 96 | What it is | Where it lives |
|---|---|---|
| **96 FDE End-to-End Capability Stack** | The consulting → defence skills you listed | Mapped below onto the 21-phase PDF |
| **96 forensic cells** | L1–L12 layers × 8 brownfield lenses | SDD-03 only — ICS/OT repo analysis, not the capability stack |

Rule used here: **Home** = the PDF row whose *Methods* or *Essential artifacts* first require it. **Recurs** = later rows that consume or extend it. **Capstone** = the prompt that must produce the evidence.

ISO/IEC 42001, 42005 and EU AI Act appear in the PDF. This estate is synthetic ICS/OT. Apply the method; do not invent a certification.

---

## PDF row → capabilities that live there

### OM 1 — Mandate and field immersion

**PDF methods:** FDE ownership · Stakeholder discovery · Responsible AI context · ISO/IEC 42001 scope  
**PDF artifacts:** Engagement charter · Scope · Outcome statement · Sponsor/owner · Governance RACI · Stakeholder and affected-groups maps · Field-evidence register  
**PDF output:** Approved mandate and operating context

| # | Capability | Exact PDF hook |
|---|---|---|
| 01 | Consulting judgement | FDE ownership (judgement starts the engagement) |
| 02 | Stakeholder discovery | Method named; artifact: stakeholder and affected-groups maps |
| 46 | Responsible AI | Responsible AI context; ISO/IEC 42001 scope |
| 48 | Governance | Governance RACI |
| 50 | Regulatory and standards applicability analysis | ISO/IEC 42001 scope |
| 80 | Operating-model design | Mandate, owner, RACI as the seed operating model |
| 81 | Roles, RACI and decision-rights design | Governance RACI; Sponsor/owner |

**Capstone:** SDD-01 → `specs/01_mandate.md`

---

### OM 2 — Discover process and architecture

**PDF methods:** Process Discovery · Lean · Waste Elimination · DMAIC Define/Measure · Architecture Discovery · Brownfield repo assessment · C4  
**PDF artifacts:** SIPOC · Process/value-stream maps · Waste register · System landscape · Brownfield assessment · Current-state C4 views · Dependencies · Data flows · Trust boundaries  
**PDF output:** Current-state process and architecture baseline

| # | Capability | Exact PDF hook |
|---|---|---|
| 04 | Current-state / brownfield assessment | Brownfield repo assessment; Brownfield assessment; current-state C4 |
| 06 | Process discovery and process mining | Process Discovery; SIPOC; value-stream maps (mine `enterprise_events.jsonl`, alerts, work orders) |
| 14 | Process improvement / DMAIC | DMAIC **Define/Measure** |
| 18 | Constraint, assumption and dependency management | Dependencies; Trust boundaries |
| 25 | Enterprise integration | System landscape; Data flows |
| 27 | Brownfield modernization | Brownfield assessment (as-is; to-be is OM 14/17) |
| 29 | Architecture | Architecture Discovery; current-state C4 |

**Capstone:** SDD-02 → `specs/02_current_state.md` (process mining added)

---

### OM 3 — Frame problem, root cause and value

**PDF methods:** SCQA · DMAIC Analyse · Root-cause analysis · Baseline KPIs · Data-driven framing  
**PDF artifacts:** SCQA problem frame · Root-cause analysis · Baseline dataset · KPI tree · CTQs · Value hypothesis · Counter-metrics · Success/failure criteria  
**PDF output:** Evidence-backed problem and baseline

| # | Capability | Exact PDF hook |
|---|---|---|
| 03 | Problem framing and problem qualification | SCQA problem frame (qualification completes in OM 4) |
| 05 | Baseline KPI definition — Before AI FDE intervention | Baseline KPIs; Baseline dataset; KPI tree |
| 07 | Root-cause analysis | Root-cause analysis; DMAIC Analyse |
| 12 | Business-value engineering | Value hypothesis; CTQs; Success/failure criteria |
| 13 | Benefits hypothesis and value-tree design | KPI tree; Value hypothesis; Counter-metrics |
| 14 | Process improvement / DMAIC | DMAIC **Analyse** |
| 55 | Business-outcome evaluation | Success/failure criteria (design); measured in OM 19 |

**Capstone:** SDD-03 (96 forensic cells feed RCA) + SDD-04 → `specs/04_problem_value.md`

---

### OM 4 — Triage regulation and qualify use case

**PDF methods:** Responsible AI · ISO/IEC 42001 · EU AI Act classification · AI suitability · Solution Decoding  
**PDF artifacts:** Impact/regulatory screen · Prohibited-use check · AI suitability assessment · Non-AI alternative · Use-case card · Value-risk-feasibility matrix · Go/no-go and kill criteria  
**PDF output:** Approved and justified use case

| # | Capability | Exact PDF hook |
|---|---|---|
| 08 | No-AI / conventional-automation alternative assessment | Non-AI alternative |
| 09 | AI intervention justification | AI suitability; Value-risk-feasibility; Go/no-go |
| 10 | Product judgement | Use-case card; Solution Decoding |
| 11 | User journey and service-design thinking | Use-case card (journeys must be explicit in the capstone) |
| 45 | Privacy-by-Design | Impact/regulatory screen |
| 46 | Responsible AI | Method named |
| 47 | Human-factors and automation-bias assessment | AI suitability + impact screen (bias named in capstone) |
| 50 | Regulatory and standards applicability analysis | ISO/IEC 42001; EU AI Act classification |
| 51 | Legal, contractual, licensing and IP assessment | Impact/regulatory screen (legal/IP named in capstone; no invented counsel opinion) |

**Capstone:** SDD-05 → `specs/05_use_case.md`

---

### OM 5 — Model the domain

**PDF methods:** Domain-Driven Design · Ubiquitous Language · Bounded Contexts · Domain Events  
**PDF artifacts:** Glossary · Domain capability map · Business rules · Decision model · Domain events · Ownership map · DDD Context Map · Bounded Contexts  
**PDF output:** Domain and decision model

| # | Capability | Exact PDF hook |
|---|---|---|
| 15 | Domain modelling / DDD | Entire OM 5 |
| 21 | Knowledge engineering | Ubiquitous language; glossary (semantic seed) |
| 22 | Taxonomy, ontology and semantic modelling | Glossary; Bounded Contexts (ontology engineered in OM 9) |
| 82 | Operational ownership | Ownership map |

**Capstone:** SDD-06 → `specs/06_domain.md`

---

### OM 6 — Qualify data and knowledge

**PDF methods:** Data Discovery · Quality · Lineage · Provenance · Permissible use · Knowledge discovery  
**PDF artifacts:** Data/knowledge inventories · Lineage · Quality profile · Provenance · Access matrix · Representativeness assessment · Data-gap register · Dataset datasheets  
**PDF output:** Data and knowledge readiness assessment

| # | Capability | Exact PDF hook |
|---|---|---|
| 19 | Data engineering | Data Discovery; inventories; datasheets |
| 20 | Data quality, contracts, lineage and provenance | Quality; Lineage; Provenance (contracts finalized OM 9) |
| 21 | Knowledge engineering | Knowledge discovery; Data/knowledge inventories |
| 45 | Privacy-by-Design | Permissible use; Access matrix |

**Capstone:** SDD-07 → `specs/07_data_knowledge.md`

---

### OM 7 — Define evaluations, impacts and risks

**PDF methods:** Evals · Responsible AI · ISO/IEC 42005 · ISO/IEC 42001 risk planning · EU AI Act requirements  
**PDF artifacts:** Evaluation strategy · Golden-set specification · Scenarios · Acceptance thresholds · AI impact assessment · Risk/harms registers · Risk treatment · Oversight and transparency requirements  
**PDF output:** Evaluation, impact and risk requirements

| # | Capability | Exact PDF hook |
|---|---|---|
| 46 | Responsible AI | Method named; AI impact assessment |
| 47 | Human-factors and automation-bias assessment | AI impact assessment; Oversight |
| 48 | Governance | Oversight and transparency requirements |
| 49 | AI assurance case | Evaluation strategy + impact + residual risk (completed OM 15) |
| 50 | Regulatory and standards applicability analysis | ISO/IEC 42005; 42001 risk planning; EU AI Act requirements |
| 52 | Evaluation and TEVV | Evals; Evaluation strategy |
| 53 | Golden, edge, adversarial and failure datasets | Golden-set specification; Scenarios |
| 55 | Business-outcome evaluation | Acceptance thresholds |

**Capstone:** SDD-08 → `specs/08_evals_risks.md`

---

### OM 8 — Generate, test and select options

**PDF methods:** Solution Decoding · Reference Architectures · GenAI patterns · PoCs · Trade-off Matrices  
**PDF artifacts:** Solution catalogue · Reference-architecture comparison · PoC/model/RAG results · Weighted trade-off matrix · Build/buy assessment · Provider comparison · Preliminary ADRs · Selected solution  
**PDF output:** Approved solution and trade-offs

| # | Capability | Exact PDF hook |
|---|---|---|
| 10 | Product judgement | Selected solution |
| 12 | Business-value engineering | Weighted trade-off matrix |
| 23 | Knowledge graph justification and engineering | Trade-off / PoC — **justify before OM 9 engineering** |
| 29 | Architecture | Reference Architectures; comparison |
| 30 | Architecture Decision Records — ADRs | Preliminary ADRs |
| 33 | AI-system design | GenAI patterns; PoC/model/RAG results |
| 34 | Model-selection and model-substitution engineering | Provider comparison; PoC/model results |
| 36 | RAG / grounding engineering | PoC/model/RAG results (architecture in OM 9–10) |
| 59 | Total Cost of Ownership — TCO | Build/buy assessment (name TCO in capstone) |
| 75 | Commercial judgement | Build/buy; Provider comparison |
| 76 | Build-vs-buy-vs-partner analysis | Build/buy assessment (partner named in capstone) |
| 77 | Vendor management | Provider comparison |

**Capstone:** SDD-09 → `specs/09_options.md`

---

### OM 9 — Design information architecture

**PDF methods:** Semantic Layers · Ontology · Knowledge Graphs · Graph/Vector Databases · Data Architecture Decisions  
**PDF artifacts:** Target data architecture · Data contracts · Semantic model · Metadata/provenance design · Retrieval architecture · Data ADRs · Conditional ontology and graph/vector schemas  
**PDF output:** Approved information architecture

| # | Capability | Exact PDF hook |
|---|---|---|
| 19 | Data engineering | Target data architecture; Data contracts |
| 20 | Data quality, contracts, lineage and provenance | Data contracts; Metadata/provenance design |
| 21 | Knowledge engineering | Semantic Layers; Ontology |
| 22 | Taxonomy, ontology and semantic modelling | Semantic model; Conditional ontology |
| 23 | Knowledge graph justification and engineering | Knowledge Graphs; **conditional** graph/vector schemas (only if OM 8 justified) |
| 24 | Context engineering | Retrieval architecture |
| 26 | API, event and data-contract engineering | Data contracts |

**Capstone:** SDD-10 → `specs/10_information_architecture.md`

---

### OM 10 — Design AI and application architecture

**PDF methods:** C4 · GenAI patterns · RAG · Model routing · Prompt/context design · Integration/deployment patterns  
**PDF artifacts:** Target C4 Context/Container/Component · AI/RAG architecture · Model-routing design · API contracts · Prompt/context design · Deployment topology · Failure-mode design · Architecture ADRs  
**PDF output:** Complete base AI/application architecture

| # | Capability | Exact PDF hook |
|---|---|---|
| 24 | Context engineering | Prompt/context design |
| 25 | Enterprise integration | Integration/deployment patterns |
| 26 | API, event and data-contract engineering | API contracts |
| 28 | Migration, coexistence, cutover and rollback strategy | Deployment topology (rollback signed in OM 13/17) |
| 29 | Architecture | Target C4; Architecture ADRs |
| 33 | AI-system design | Entire OM 10 |
| 34 | Model-selection and model-substitution engineering | Model-routing design |
| 35 | Prompt engineering and prompt lifecycle management | Prompt/context design (lifecycle registry in OM 14) |
| 36 | RAG / grounding engineering | RAG method; AI/RAG architecture |
| 40 | Deterministic control boundaries | Failure-mode design (tools locked in OM 11) |
| 61 | Performance and latency engineering | Deployment topology / later NFRs in OM 13 |
| 63 | Reliability and resilience | Failure-mode design |
| 64 | Graceful degradation and AI-disabled operation | Failure-mode design |

**Capstone:** SDD-11 → `specs/11_ai_app_architecture.md`

---

### OM 11 — Design agentic and multi-agent orchestration

**PDF methods:** Agentic AI · Single-agent versus multi-agent decision · Multi-Agent Orchestration · Human-in-the-loop · Agent communication and control  
**PDF artifacts:** Agent-suitability assessment · Autonomy-level ADR · Agent responsibility map · Orchestration topology · Agent interaction/sequence diagram · State-machine model · Tool/action catalogue · Identity/permission matrix · Shared-memory design · Handoff protocol · Termination/loop controls · Human approval/override/escalation matrix  
**PDF output:** Approved, bounded and testable agentic architecture

| # | Capability | Exact PDF hook |
|---|---|---|
| 37 | Agentic-system engineering | Entire OM 11 |
| 38 | Tool-contract and bounded-agency engineering | Tool/action catalogue; Autonomy-level ADR |
| 39 | Human-in-the-loop / Human-on-the-loop design | HITL method; Human approval/override/escalation matrix |
| 40 | Deterministic control boundaries | Termination/loop controls; tool catalogue vs forbidden actions |
| 43 | Zero Trust authorization | Identity/permission matrix |
| 47 | Human-factors and automation-bias assessment | HITL + handoff protocol (bias controls in capstone) |

**Capstone:** SDD-12 → `specs/12_agentic.md`

---

### OM 12 — Design security, guardrails and supplier controls

**PDF methods:** AI Security · Threat Modelling · OWASP GenAI LLM Top 10 2026 · OWASP Agentic Top 10 2026 · Guardrails · Supply-chain assurance  
**PDF artifacts:** Threat model · Agentic attack-surface map · Trust boundaries · Abuse cases · OWASP mapping · Guardrail architecture · Control matrix · Supplier/model assessment · Model/system cards · Component register · SBOM/AIBOM · Exit plan  
**PDF output:** Controlled architecture and approved components

| # | Capability | Exact PDF hook |
|---|---|---|
| 41 | Security-by-Design | Threat model; Trust boundaries; Control matrix |
| 42 | AI / agentic security | AI Security; OWASP LLM + Agentic Top 10; Guardrails; attack-surface |
| 43 | Zero Trust authorization | Trust boundaries; Control matrix |
| 44 | Software and AI supply-chain security | Supply-chain assurance; SBOM/AIBOM; Component register |
| 45 | Privacy-by-Design | Trust boundaries; Control matrix; abuse cases |
| 51 | Legal, contractual, licensing and IP assessment | Supplier/model assessment; Model/system cards |
| 77 | Vendor management | Supplier/model assessment |
| 78 | Third-party risk management | Supply-chain assurance; Supplier/model assessment |
| 79 | Vendor concentration and exit strategy | Exit plan |

**Capstone:** SDD-13 → `specs/13_security_guardrails.md`

---

### OM 13 — Approve ADRs and delivery specification

**PDF methods:** ADRs · Spec-Driven Development · Telemetry/Observability design · Traceability  
**PDF artifacts:** Final ADR register · Approved C4 baseline · Delivery specification · NFRs · API/data contracts · Agent specifications · Evaluation cases · Telemetry/logging specification · Rollback requirements · Traceability matrix · Backlog  
**PDF output:** Build-ready specification

| # | Capability | Exact PDF hook |
|---|---|---|
| 16 | Requirements engineering | Delivery specification; NFRs; Backlog |
| 17 | Requirements-to-evidence traceability | Traceability; Traceability matrix |
| 18 | Constraint, assumption and dependency management | Rollback requirements; OPEN items in delivery spec |
| 26 | API, event and data-contract engineering | API/data contracts |
| 28 | Migration, coexistence, cutover and rollback strategy | Rollback requirements |
| 30 | Architecture Decision Records — ADRs | Final ADR register; Approved C4 baseline |
| 32 | AI-assisted engineering / Cursor-style engineering discipline | Spec-Driven Development |
| 61 | Performance and latency engineering | NFRs |
| 62 | Scalability and capacity engineering | NFRs |
| 65 | Observability | Telemetry/Observability design; Telemetry/logging specification |
| 66 | AI / agent observability and traceability | Telemetry/logging specification; Traceability matrix |
| 68 | SLO / SLA / error-budget engineering | NFRs (name SLO/SLA/error budget in capstone) |
| 94 | 90-day / medium-term transformation roadmap | Backlog (roadmap published OM 19) |

**Capstone:** SDD-14 + SDD-15 → `specs/14_delivery_spec.md` + Repo 2.0 layout

---

### OM 14 — Engineer

**PDF methods:** AI-Assisted Engineering · Spec-Driven Development using Cursor · Brownfield integration · Agent/workflow implementation  
**PDF artifacts:** Source/IaC · Prompt/configuration registry · Model/tool versions · Data pipelines · Agent definitions · Orchestration workflows · Unit/integration tests · CI/CD evidence · As-built C4 views  
**PDF output:** Versioned deployable increments

| # | Capability | Exact PDF hook |
|---|---|---|
| 27 | Brownfield modernization | Brownfield integration |
| 31 | Software engineering | Source/IaC; tests; CI/CD; as-built C4 |
| 32 | AI-assisted engineering / Cursor-style engineering discipline | Named methods |
| 35 | Prompt engineering and prompt lifecycle management | Prompt/configuration registry; Model/tool versions |
| 37 | Agentic-system engineering | Agent definitions; Orchestration workflows |

**Capstone:** ENH-01 … ENH-07

---

### OM 15 — Evaluate, attack and independently assure

**PDF methods:** Model/RAG/agent/multi-agent Evals · Responsible AI testing · OWASP testing · Red teaming · Guardrail validation  
**PDF artifacts:** Evaluation harness · Golden datasets · Model/RAG results · Agent task-completion results · Inter-agent handoff tests · Coordination/conflict tests · Loop/termination tests · Prompt-injection/tool-misuse tests · Assurance report · Residual-risk acceptance  
**PDF output:** Independently assured release candidate

| # | Capability | Exact PDF hook |
|---|---|---|
| 49 | AI assurance case | Assurance report; Residual-risk acceptance |
| 52 | Evaluation and TEVV | Entire OM 15 |
| 53 | Golden, edge, adversarial and failure datasets | Golden datasets; injection/misuse tests |
| 54 | AI red teaming | Red teaming; OWASP testing; prompt-injection/tool-misuse |
| 56 | Token efficiency | Not named in PDF; **measure here** with eval harness (capstone addition, still OM 15 output) |

**Capstone:** ENH-08 … ENH-09 → `assurance/ASSURANCE_REPORT.md`

---

### OM 16 — Prepare operations, recovery and regulatory evidence

**PDF methods:** Telemetry · Observability · Change management · Pre-production Chaos Drill · ISO/IEC 42001/42005 · EU AI Act  
**PDF artifacts:** Operational RACI · Agent/LLM telemetry · Dashboards/alerts · Runbooks · Incident/rollback plans · SOPs/training · Recovery evidence · AI-system record · Technical documentation · Transparency and oversight records  
**PDF output:** Operationally and legally ready release

| # | Capability | Exact PDF hook |
|---|---|---|
| 48 | Governance | Transparency and oversight records; AI-system record |
| 63 | Reliability and resilience | Recovery evidence; Chaos Drill |
| 65 | Observability | Telemetry; Observability; Dashboards/alerts |
| 66 | AI / agent observability and traceability | Agent/LLM telemetry |
| 67 | Service management | Runbooks; SOPs; Dashboards |
| 69 | Incident response | Incident/rollback plans |
| 70 | AI-specific incident response | Agent/LLM telemetry + incident plans (AI IR named in capstone) |
| 71 | Business continuity and disaster recovery | Recovery evidence; Chaos Drill; runbooks |
| 72 | Change management | Method named |
| 74 | Training and enablement | SOPs/training |
| 80 | Operating-model design | Operational RACI |
| 81 | Roles, RACI and decision-rights design | Operational RACI |
| 82 | Operational ownership | Operational RACI |
| 83 | Operational handover | Technical documentation; SOPs/training |
| 84 | Knowledge transfer | SOPs/training; Technical documentation |
| 85 | Production-readiness assessment | Output: Operationally and legally ready release |

**Capstone:** ENH-10 + REL-01 → `ops/`

---

### OM 17 — Deploy progressively and integrate adoption

**PDF methods:** Shadow/pilot/canary · Bounded agent autonomy · Human–AI workflow integration  
**PDF artifacts:** Release manifest · Deployment record · Pilot/canary results · Autonomy-expansion record · Rollback decision · Adoption dashboard · Override/workaround logs · Updated SOPs  
**PDF output:** Controlled live service and adoption evidence

| # | Capability | Exact PDF hook |
|---|---|---|
| 28 | Migration, coexistence, cutover and rollback strategy | Shadow/pilot/canary; Rollback decision |
| 72 | Change management | Updated SOPs; Human–AI workflow integration |
| 73 | User adoption and behavioural change | Adoption dashboard; Override/workaround logs |
| 85 | Production-readiness assessment | Release manifest; Deployment record |
| 86 | Deployment and release governance | Entire OM 17 |

**Capstone:** REL-02 — **advisory/shadow only; no live OT canary**

---

### OM 18 — Monitor and validate operational resilience

**PDF methods:** Telemetry · Observability · Continuous Evals · Agent monitoring · Drift · Controlled Chaos Drills  
**PDF artifacts:** Operational dashboards · Model/tool/agent traces · Inter-agent interaction logs · Drift reports · Cost/availability reports · Incident records · Agent-loop alerts · Chaos/recovery results · Updated runbooks  
**PDF output:** Operational performance, risk and resilience evidence

| # | Capability | Exact PDF hook |
|---|---|---|
| 57 | Token economics | Cost/availability reports |
| 58 | AI FinOps | Cost/availability reports |
| 63 | Reliability and resilience | Chaos/recovery results; Agent-loop alerts |
| 64 | Graceful degradation and AI-disabled operation | Chaos drills; Updated runbooks |
| 65 | Observability | Operational dashboards; traces |
| 66 | AI / agent observability and traceability | Model/tool/agent traces; Inter-agent logs |
| 67 | Service management | Dashboards; Updated runbooks |
| 70 | AI-specific incident response | Agent-loop alerts; Incident records |
| 91 | Continuous improvement | Continuous Evals |
| 92 | Model / system drift management | Drift; Drift reports |

**Capstone:** REL-02 (templates) + ENH-10 (telemetry implemented)

---

### OM 19 — Prove value and tell the decision story

**PDF methods:** KPIs before/after · DMAIC Improve · Lean · SCQA · Data-Driven Storytelling  
**PDF artifacts:** Benefits-realisation report · Before/after KPIs · Cost-to-value analysis · Counter-metrics · Waste reduction · Unintended effects · Executive SCQA paper · C4 executive view · Decision recommendation  
**PDF output:** Evidence-backed scale/change/stop package

| # | Capability | Exact PDF hook |
|---|---|---|
| 12 | Business-value engineering | Cost-to-value; Benefits-realisation |
| 14 | Process improvement / DMAIC | DMAIC **Improve** |
| 55 | Business-outcome evaluation | Benefits-realisation report |
| 59 | Total Cost of Ownership — TCO | Cost-to-value analysis |
| 60 | Cost-per-successful-business-outcome measurement | Cost-to-value; maps to repo KPI “AI cost per analyzed incident / avoided escalation” |
| 87 | Benefits-realisation measurement | Benefits-realisation report |
| 88 | Post-intervention KPI measurement — After AI FDE intervention | Before/after KPIs |
| 89 | Before-vs-after KPI variance analysis | Before/after KPIs |
| 90 | Value leakage analysis | Unintended effects; Counter-metrics (name leakage in capstone) |
| 94 | 90-day / medium-term transformation roadmap | Decision recommendation |
| 95 | Executive communication | Executive SCQA paper; C4 executive view |
| 96 | Elevator pitch and final defence | Data-Driven Storytelling; Decision recommendation (pitch named in capstone) |

**Capstone:** REL-03 → `participant/work/release/EXECUTIVE_DEFENSE.md`

---

### OM 20 — Evaluate AIMS and decide lifecycle state

**PDF methods:** ISO/IEC 42001 Check/Act · Internal audit · Management review · DMAIC Control · Change reassessment  
**PDF artifacts:** AIMS performance report · Audit findings · CAPA register · Management-review decision · Control plan · Updated impact/risk/C4/ADRs/evaluations · Scale/change/restrict/suspend/retire decision  
**PDF output:** Authorised lifecycle state or return to an earlier phase

| # | Capability | Exact PDF hook |
|---|---|---|
| 14 | Process improvement / DMAIC | DMAIC **Control** |
| 48 | Governance | Internal audit; Management review |
| 50 | Regulatory and standards applicability analysis | ISO/IEC 42001 Check/Act |
| 80 | Operating-model design | Control plan; management-review decision |
| 91 | Continuous improvement | CAPA register; updated evaluations |

**Capstone:** REL-04 → `participant/work/release/AIMS_LIFECYCLE.md`

---

### OM 21 — Retire and capture reusable IP

**PDF methods:** Safe retirement · Record control · Lessons learned · Reference Architecture improvement  
**PDF artifacts:** Retirement plan · Notifications · Access revocation · Data/model/memory disposition · Agent/tool credential revocation · Supplier/dependency closure · Reusable ADRs/C4 templates · Updated reference architectures · Eval and guardrail templates  
**PDF output:** Formally closed system and reusable FDE IP

| # | Capability | Exact PDF hook |
|---|---|---|
| 51 | Legal, contractual, licensing and IP assessment | Record control; reusable IP |
| 79 | Vendor concentration and exit strategy | Supplier/dependency closure |
| 84 | Knowledge transfer | Lessons learned; reusable templates |
| 93 | Retirement and decommissioning strategy | Entire OM 21 |

**Capstone:** REL-04 (workshop plan only)

---

## Master table (C01–C96)

| # | Capability | Home OM | Recurs | Prompt | Artifact (this capstone) |
|---|---|---|---|---|---|
| 01 | Consulting judgement | 1 | 3–4, 8, 19 | SDD-01 | Charter + every SCQA |
| 02 | Stakeholder discovery | 1 | 16 | SDD-01 | Stakeholder / affected-groups maps |
| 03 | Problem framing and qualification | 3 | 4 | SDD-04, SDD-05 | SCQA + use-case card |
| 04 | Current-state / brownfield assessment | 2 | 14 | SDD-02 | Brownfield assessment + C4 as-is |
| 05 | Baseline KPI definition (Before) | 3 | 19 | SDD-04 | Baseline dataset + KPI tree |
| 06 | Process discovery and process mining | 2 | 3 | SDD-02 | SIPOC, VSM, **event mining** |
| 07 | Root-cause analysis | 3 | — | SDD-03, SDD-04 | RCA from 96 forensic cells |
| 08 | No-AI / conventional-automation alternative | 4 | 8 | SDD-05 | Non-AI alternative |
| 09 | AI intervention justification | 4 | 8 | SDD-05 | Suitability + go/no-go |
| 10 | Product judgement | 4 | 8, 13 | SDD-05, SDD-09, PRD-01 | Use-case + selected solution + PRD |
| 11 | User journey and service-design thinking | 4 | 17 | SDD-05, PRD-01 | **Journeys** (SOC, process, safety, exec) |
| 12 | Business-value engineering | 3 | 8, 19 | SDD-04, SDD-09, REL-03 | Value hypothesis + trade-off + benefits |
| 13 | Benefits hypothesis and value-tree design | 3 | 19 | SDD-04 | KPI / value tree |
| 14 | Process improvement / DMAIC | 2 | 3, 19, 20 | SDD-02/04, REL-03/04 | Define-Measure-Analyse-Improve-Control |
| 15 | Domain modelling / DDD | 5 | 9 | SDD-06 | DOMAIN.md |
| 16 | Requirements engineering | 13 | PRD | SDD-14, PRD-01 | Delivery spec + FR-### |
| 17 | Requirements-to-evidence traceability | 13 | 14–15 | SDD-14 | TRACEABILITY.csv |
| 18 | Constraint, assumption and dependency management | 2 | 13 | SDD-02, SDD-14 | Dependencies + OPEN_DECISIONS |
| 19 | Data engineering | 6 | 9, 14 | SDD-07, SDD-10, ENH | Inventories + pipelines |
| 20 | Data quality, contracts, lineage, provenance | 6 | 9 | SDD-07, SDD-10 | Quality profile + data contracts |
| 21 | Knowledge engineering | 5–6 | 9 | SDD-06, SDD-07, SDD-10 | Glossary → knowledge inventory → semantic |
| 22 | Taxonomy, ontology and semantic modelling | 5 | 9 | SDD-06, SDD-10 | Glossary + ontology |
| 23 | Knowledge graph justification and engineering | 8 | 9 | SDD-09, SDD-10 | **Justify first**; conditional graph |
| 24 | Context engineering | 9 | 10–11 | SDD-10, SDD-11, SDD-12 | Retrieval + context snapshots |
| 25 | Enterprise integration | 2 | 10 | SDD-02, SDD-11 | Landscape + integration patterns |
| 26 | API, event and data-contract engineering | 9 | 10, 13 | SDD-10, SDD-11, SDD-14 | Contracts; read-only API |
| 27 | Brownfield modernization | 2 | 14, 17 | SDD-02, ENH, REL-02 | Preserve evidence; coexist with legacy_* |
| 28 | Migration, coexistence, cutover, rollback | 10 | 13, 17 | SDD-11, SDD-14, REL-02 | Rollback + shadow/pilot **advisory only** |
| 29 | Architecture | 2 | 8, 10, 13 | SDD-02, 09, 11, 14 | As-is C4 → to-be C4 → approved C4 |
| 30 | ADRs | 8 | 10–13 | SDD-09 … SDD-14 | Preliminary → final ADR register |
| 31 | Software engineering | 14 | — | ENH-01…07 | Tests, source, CI, as-built C4 |
| 32 | AI-assisted / Cursor engineering discipline | 13 | 14 | SDD-14, ENH | Specs constrain code |
| 33 | AI-system design | 10 | 8 | SDD-11 | C4 + model routing + failure modes |
| 34 | Model-selection and substitution | 8 | 10, 14 | SDD-09, SDD-11, ENH-07 | Provider + routing + version pin |
| 35 | Prompt engineering and lifecycle | 10 | 14 | SDD-11, ENH-07 | Prompt design + registry |
| 36 | RAG / grounding engineering | 8 | 9–10 | SDD-09, SDD-10, SDD-11 | Hybrid retrieval; vector never = policy |
| 37 | Agentic-system engineering | 11 | 14 | SDD-12, ENH-07 | Bounded single agent default |
| 38 | Tool-contract and bounded-agency | 11 | 14 | SDD-12, ENH-07 | Tool catalogue; no isolate-execute |
| 39 | HITL / HOTL design | 11 | 17 | SDD-12, REL-02 | Approval/override/escalation matrix |
| 40 | Deterministic control boundaries | 11 | 10 | SDD-12, ENH-05 | ACTION_TIERS enforced in code |
| 41 | Security-by-Design | 12 | — | SDD-13 | Threat model + control matrix |
| 42 | AI / agentic security | 12 | 15 | SDD-13, ENH-08 | OWASP LLM + Agentic Top 10 |
| 43 | Zero Trust authorization | 11 | 12 | SDD-12, SDD-13 | Permission matrix + trust boundaries |
| 44 | Software and AI supply-chain security | 12 | 21 | SDD-13 | SBOM/AIBOM + component register |
| 45 | Privacy-by-Design | 4 | 6, 12 | SDD-05, SDD-07, SDD-13 | Impact + access matrix + controls |
| 46 | Responsible AI | 1 | 4, 7, 15 | SDD-01, 05, 08, ENH-09 | Context → impact → RAI tests |
| 47 | Human-factors and automation-bias | 4 | 7, 11 | SDD-05, SDD-08, SDD-12 | Bias assessment + HITL forcing functions |
| 48 | Governance | 1 | 7, 16, 20 | SDD-01, 08, REL-01, REL-04 | RACI → oversight → AIMS |
| 49 | AI assurance case | 7 | 15 | SDD-08, ENH-09 | Claim–argument–evidence + report |
| 50 | Regulatory and standards applicability | 1 | 4, 7, 16, 20 | SDD-01, 05, 08, REL | 42001/42005/EU AI Act **as methods**, not certs |
| 51 | Legal, contractual, licensing and IP | 4 | 12, 21 | SDD-05, SDD-13, REL-04 | Register + OPEN_DECISION |
| 52 | Evaluation and TEVV | 7 | 15 | SDD-08, ENH-09 | Strategy then harness |
| 53 | Golden, edge, adversarial, failure datasets | 7 | 15 | SDD-08, ENH-09 | golden_cases + injects + cascade |
| 54 | AI red teaming | 15 | 12 | ENH-08, ENH-09 | Injection, tool-misuse, loop tests |
| 55 | Business-outcome evaluation | 3 | 7, 19 | SDD-04, SDD-08, REL-03 | Criteria → thresholds → realisation |
| 56 | Token efficiency | 15 | 18 | ENH-09, REL-02 | **Named eval metric** (not in PDF text) |
| 57 | Token economics | 18 | 19 | REL-02, REL-03 | Cost/availability reports |
| 58 | AI FinOps | 18 | 19 | ENH-10, REL-03 | Cost dashboards + cost-to-value |
| 59 | TCO | 8 | 19 | SDD-09, REL-03 | Build/buy + cost-to-value |
| 60 | Cost-per-successful-business-outcome | 19 | 3 | SDD-04, REL-03 | KPI from docs/05 + after measurement |
| 61 | Performance and latency engineering | 13 | 10 | SDD-11, SDD-14 | NFRs; evals README latency |
| 62 | Scalability and capacity engineering | 13 | 10 | SDD-11, SDD-14 | NFRs |
| 63 | Reliability and resilience | 10 | 16, 18 | SDD-11, REL-01, REL-02 | Failure-mode + chaos + recovery |
| 64 | Graceful degradation and AI-disabled operation | 10 | 18 | SDD-11, APP-02, REL-02 | Failure-mode + UI fallback |
| 65 | Observability | 13 | 16, 18 | SDD-14, ENH-10 | Telemetry spec + dashboards |
| 66 | AI / agent observability and traceability | 13 | 16, 18 | SDD-14, ENH-07, ENH-10 | Decision traces; no hidden CoT |
| 67 | Service management | 16 | 18 | REL-01 | Runbooks, SOPs, dashboards |
| 68 | SLO / SLA / error-budget engineering | 13 | 16 | SDD-14, REL-01 | **Named SLOs** in NFRs |
| 69 | Incident response | 16 | 18 | REL-01 | Incident/rollback plans |
| 70 | AI-specific incident response | 16 | 18 | REL-01, REL-02 | Agent-loop alerts + AI IR runbook |
| 71 | Business continuity and disaster recovery | 16 | 10 (L10) | SDD-03, ENH-06, REL-01 | Recovery graph + ops recovery evidence |
| 72 | Change management | 16 | 17 | REL-01, REL-02 | Change + updated SOPs |
| 73 | User adoption and behavioural change | 17 | — | REL-02 | Adoption dashboard; override logs |
| 74 | Training and enablement | 16 | 17 | REL-01 | SOP/training outline |
| 75 | Commercial judgement | 8 | 12 | SDD-09, SDD-13 | Trade-off + supplier |
| 76 | Build-vs-buy-vs-partner analysis | 8 | — | SDD-09 | Build/buy **+ partner** |
| 77 | Vendor management | 8 | 12 | SDD-09, SDD-13 | Provider + supplier assessment |
| 78 | Third-party risk management | 12 | — | SDD-13 | Supply-chain + supplier risk |
| 79 | Vendor concentration and exit strategy | 12 | 21 | SDD-13, REL-04 | Exit plan |
| 80 | Operating-model design | 1 | 16, 20 | SDD-01, REL-01, REL-04 | Mandate → ops RACI → AIMS |
| 81 | Roles, RACI and decision-rights design | 1 | 11, 16 | SDD-01, SDD-12, REL-01 | Governance + HITL + ops RACI |
| 82 | Operational ownership | 5 | 16 | SDD-06, REL-01 | Ownership map + ops RACI |
| 83 | Operational handover | 16 | 17 | REL-01 | Handover pack |
| 84 | Knowledge transfer | 16 | 21 | REL-01, REL-04 | SOPs + reusable IP |
| 85 | Production-readiness assessment | 16 | 17 | ENH-10, REL-01, REL-02 | Readiness checklist |
| 86 | Deployment and release governance | 17 | — | REL-02 | Release manifest (workshop) |
| 87 | Benefits-realisation measurement | 19 | — | REL-03 | Benefits report |
| 88 | Post-intervention KPI measurement (After) | 19 | — | REL-03 | After KPIs |
| 89 | Before-vs-after KPI variance analysis | 19 | — | REL-03 | Variance table |
| 90 | Value leakage analysis | 19 | — | REL-03 | Unintended effects **named leakage** |
| 91 | Continuous improvement | 18 | 20 | REL-02, REL-04 | Continuous evals + CAPA |
| 92 | Model / system drift management | 18 | 20 | REL-02, REL-04 | Drift reports |
| 93 | Retirement and decommissioning strategy | 21 | — | REL-04 | Retirement plan |
| 94 | 90-day / medium-term transformation roadmap | 13 | 19 | SDD-14, REL-03 | Backlog + 90-day roadmap |
| 95 | Executive communication | 19 | — | REL-03 | Executive SCQA + C4 exec view |
| 96 | Elevator pitch and final defence | 19 | — | REL-03 | **60–90s pitch** + 12-min defence |

---

## What changed in the path because of this list

The 15+10 SDD sequence does **not** change. The PDF order is still the spine.

These artifacts were under-specified before and are now **required** so all 96 are evidenced:

| Gap vs prior playbook | Where it now lives |
|---|---|
| Process **mining** (not only SIPOC) | SDD-02 |
| User **journeys** | SDD-05, PRD-01 |
| Human-factors / **automation bias** | SDD-05, SDD-08, SDD-12 |
| **Privacy-by-Design** named | SDD-05, SDD-07, SDD-13 |
| Legal / licensing / **IP** register | SDD-05, SDD-13, REL-04 |
| **KG justification before** KG engineering | SDD-09 then SDD-10 |
| Build-vs-buy-vs-**partner** + **TCO** | SDD-09 |
| Model **substitution** + prompt **lifecycle** | SDD-11, ENH-07 |
| **Zero Trust** authorization | SDD-12, SDD-13 |
| **SLO/SLA/error budget** | SDD-14, REL-01 |
| **AI assurance case** | SDD-08, ENH-09 |
| **Red team** + **token efficiency** | ENH-08, ENH-09 |
| **FinOps / token economics / cost-per-outcome** | ENH-10, REL-03 |
| **AI-disabled** UX | SDD-11, APP-02 |
| Production-readiness, handover, AI-specific IR, BC/DR, training | ENH-10, REL-01 |
| Adoption / override logs / release governance | REL-02 |
| **Value leakage**, elevator **pitch**, before/after variance | REL-03 |
| Drift, CAPA, retire, reusable IP | REL-04 |

Fill `participant/work/FDE_96_COVERAGE.csv` at Repo 2.0 gate (SDD-15) with status=`specced`, and again at defence (REL-03) with status=`evidenced`.
