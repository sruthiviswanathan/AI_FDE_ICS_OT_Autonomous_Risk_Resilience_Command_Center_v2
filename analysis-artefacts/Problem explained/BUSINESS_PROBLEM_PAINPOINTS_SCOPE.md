# Business Problem, Pain Points, and Scope

**Engagement:** AI FDE ICS/OT Autonomous Risk & Resilience Command Center (v2)  
**Document type:** Business problem, pain-point, and scope statement  
**Date:** 11 September 2026  
**Basis:** Repository challenge brief, domain docs, safety/assurance constraints, discovery checklist, seeded diagnostics, and engagement rules. All names and records in the estate are synthetic.

---

## 1. The business problem

Leadership wants a **global autonomous risk and resilience command center** for a multinational ICS/OT program: **18 plants** across five regions, mixed-generation PLC/DCS/SCADA/HMI/historians, SIS, CMMS/EAM, SOC/SIEM, IAM/PAM, and vendor remote access.

The business problem is not “we lack another dashboard.” The estate already produces many dashboards. The problem is that **no system holds a trusted cyber-physical truth**.

Current systems **disagree** about:

1. **What assets exist** — official inventories, aliases, shadow spreadsheets, and field discovery do not reconcile.
2. **What state those assets are in** — registered/CMDB state, observed/telemetry state, CMMS/work-order state, and operator interpretation diverge.
3. **How cyber findings map to physical consequence** — vulnerability severity is not reliably tied to reachability, process criticality, safety barriers, or recovery capability.
4. **Which safety barriers are actually active** — SIS, alarms, trips, and interlocks may be bypassed, degraded, or overdue for proof test while security still treats them as healthy.
5. **Whether recovery plans are executable** — a backup flag of CURRENT is treated as readiness even when restore tests, runbooks, or dependencies are stale or missing.

The core forensic tension the business cannot currently resolve is:

> **Cyber state ≠ Operational state ≠ Safety state ≠ Resilience state**

That gap has a direct business cost. The company cannot reliably answer, at global command-center speed:

- Which finding actually threatens production, safety, or continuity — versus which finding is a high CVSS on a low-criticality, unreachable asset?
- Which response is **safe** — versus which SOC-recommended isolation would destabilize a unit?
- Who has **authority** to act — versus who can only observe, ticket, or recommend?
- Can we recover this site if containment or outage happens — or is that an untested assumption?

**The goal of the engagement is not to automate plant control.** The goal is to establish:

- trustworthy cyber-physical situational awareness
- contextual risk (not CVSS-only)
- resilience decisions grounded in restore/runbook/dependency evidence
- governed action recommendations bounded by policy, safety, and human authority

Until that exists, “autonomy” would only accelerate the wrong recommendation.

---

## 2. Pain points overall

Pain is not concentrated in one tool. It is structural: **imperfection, inconsistency, friction, complexity, volatility, uncertainty, hidden dependency, and unknown unknowns** across twelve layers (L1–L12). The points below are the ones the business feels.

### 2.1 No single source of operational truth

- CMDB, passive discovery, historian, SCADA, CMMS, SIEM, and operator notes are each treated as authoritative by name, but they conflict.
- **200** assets are registered ACTIVE while observed as OFFLINE or UNSEEN.
- **5** alias collisions mean the same name can point to more than one asset.
- A shadow spreadsheet (`ot_asset_inventory_FINAL_v8.csv`) can be newer than the official inventory; shift handover notes already say the spreadsheet is newer than CMDB for a new gateway.
- v1 and v2 asset APIs use different field names (`assetId` / `fwVersion` / `operationalState` vs `asset_id` / `firmware` / `observed_state`), so even “the asset API” is not one contract.

**Business effect:** leadership cannot trust the command-center picture of what is on the plant floor.

### 2.2 Telemetry cannot be taken at face value

- **4,094** telemetry records are BAD or UNCERTAIN.
- **120** duplicate packets and **47** temperature unit mismatches exist in the seeded historian-style feed.
- Event time and ingest/received time can diverge; sorting only on received time reconstructs the wrong order.
- Shadow handover evidence: historian pressure looked flat for ~20 minutes while the HMI moved.

**Business effect:** alerts and trends can be late, duplicated, unit-wrong, or contradicted by the operator screen. Decisions made on raw tags will be wrong.

### 2.3 Cyber risk is scored without operational context

- Legacy ranking sorts findings by **CVSS alone**.
- A 9.8 on a low-criticality, unreachable asset outranks a 6.5 on a critical, reachable asset.
- **1,100** vulnerability findings and **2,800** cyber alerts exist without a proven map to process unit, safety consequence, compensating control, or recovery capability.
- Risk-acceptance trackers show DEFER/ACCEPT decisions with thin rationale (“vendor patch pending,” “shutdown unavailable,” “compensating controls assumed”).

**Business effect:** the SOC and the plant argue past each other. Patch and escalation queues are driven by score, not by what can actually hurt production or people.

### 2.4 Safety and security can recommend opposite actions

- **61** safety barriers are bypassed or degraded; **73** are overdue for proof test.
- Legacy logic recommends **ISOLATE** on HIGH/CRITICAL alerts with no safe-state check.
- The cascade scenario is the pain in narrative form: SOC wants immediate isolation; process engineering warns the unit is near minimum stable load and isolation may destabilize it; a related safety barrier is already recorded as bypassed.
- Shift notes repeat the same warning: do not isolate the controller without process engineering review.

**Business effect:** a “fast” security response can become a process or safety incident. The command center has no agreed way to hold both truths at once.

### 2.5 Operations and maintenance truth is split from the field

- **244** work orders are CLOSED in CMMS while field status is not RETURNED_TO_SERVICE.
- Temporary bypasses, contractor activity, and vendor firmware work appear in handover notes before tickets are updated.
- Night-shift reality (vendor says work is done; safety bypass still visible; ticket not updated) is not visible on the enterprise dashboard.

**Business effect:** planners close risk on paper while the plant is still in a temporary or degraded condition.

### 2.6 Remote access and undocumented paths expand the attack and error surface

- **779** network paths were observed in the last 24 hours but are not documented.
- **137** remote sessions are outside an approved window; **128** lack confirmed MFA.
- Vendor VPNs, service laptops, jump hosts, and informal access sit beside the documented Purdue-like architecture.

**Business effect:** the company cannot say who is on the network, whether that session is approved, or which path an incident would actually travel.

### 2.7 Resilience is assumed, not proven

- Legacy recovery logic treats `backup_status == CURRENT` as “ready.”
- Seeded gaps: **25** stale/unknown backups, **29** unverified recovery dependencies, **35** stale or missing runbooks.
- Inject 06 is a restore failure during a recovery drill — the exact failure mode the flag-based check cannot see.

**Business effect:** continuity and DR statements overstate readiness. A regional SCADA outage or containment action may have no tested path back.

### 2.8 Decision overload with weak authority

- Alert volume is high relative to actionable, evidence-backed incidents.
- There is no enforced separation of **observe / recommend / reversible change / consequential change / forbidden control write**.
- Authority is fragmented across SOC, operations, process engineering, safety, vendors, and business units.
- There are no eval gates (identity, temporal correctness, safety policy, authority) required before autonomy is switched on.

**Business effect:** more automation would scale noise and unsafe recommendations. Humans still do not know which decisions they must own.

### 2.9 Pain-point summary by layer

| Layer | What hurts the business |
|---|---|
| L1 Software / logic | Hard-coded risk rules and weak tests encode the wrong decision policy. |
| L2 OT systems / protocols | Mixed generations and interface drift make one estate view unreliable. |
| L3 Data / telemetry | Bad, stale, duplicate, and unit-wrong tags undermine every downstream decision. |
| L4 Asset / configuration | Competing identities and undocumented devices hide real exposure. |
| L5 Process / control | Cyber findings are not traced to unit dependencies or safe-state constraints. |
| L6 Cyber risk | Severity is disconnected from reachability, criticality, safety, and recovery. |
| L7 Safety | Bypasses and overdue proof tests collide with security isolation pressure. |
| L8 Operations / maintenance | CMMS “closed” does not mean the field is restored. |
| L9 Enterprise / IT-OT | SOC, CMMS, IAM, vendors, and ERP each hold only partial truth. |
| L10 Resilience | Backups, runbooks, and restore tests are not a verified recovery graph. |
| L11 Decision intelligence | Alert overload and CVSS ranking hide the few incidents that matter. |
| L12 Autonomy / assurance | No bounded authority, TEVV, or audit model exists for consequential AI. |

---

## 3. In scope

In-scope work is **brownfield discovery and modernization design** against the synthetic estate, then **bounded** recommendation capability. It is evidence-first. It is not a greenfield rewrite and not live plant control.

### 3.1 Discovery and current-state forensics

- Treat this as a production brownfield engagement: preserve evidence before changing behavior.
- Map current-state architecture, including documented and undocumented paths.
- Reconcile asset identity across CMDB-like, passive, CMMS, alias, and shadow sources.
- Separate **observed state**, **registered state**, **operational interpretation**, **safety state**, and **decision authority**.
- Quantify telemetry quality: duplicates, unit mismatches, stale/uncertain data, temporal anomalies.
- Build a process/asset dependency view and trace assets to process units and downstream business consequence.
- Compare cyber severity with process criticality, reachability, compensating controls, safety, and recovery.
- Find safety barriers that are bypassed, degraded, or overdue for proof test.
- Compare CMMS status with field/observed status.
- Identify unapproved remote access and weak MFA evidence.
- Quantify backup, runbook, and restore-test weakness.
- Find cases where isolation would be operationally unsafe.

### 3.2 Decision and target-state design (still bounded)

- Contextual risk model that can outrank a high CVSS when process/safety/recovery context says so.
- Safety/security conflict handling (SOC isolation vs process-safe operation).
- Resilience/recovery graph (backup ≠ restore-tested ≠ runbook-complete ≠ dependency-verified).
- Target architecture options only where evidence shows they fix a real gap.
- Bounded-autonomy model with human authority for consequential actions.
- Evaluation / TEVV strategy and eval gates **before** agentic automation.
- KPI before/after model (inventory disagreement, telemetry quality, time to contextualize an OT alert, safety-bypass aging, restore-test freshness, false-positive escalation, evidence completeness, approval latency, AI cost per incident).
- 90-day roadmap and executive defense.

### 3.3 Allowed system behavior (this repository and any proposed design)

| Tier | Examples | In scope? |
|---|---|---|
| Autonomous / always allowed | Collect, correlate, enrich, summarize, rank evidence, read-only simulation | Yes |
| Policy-controlled, reversible (real-world option) | Request fresh telemetry, open a ticket, increase logging, capture evidence | Design in scope; not live OT |
| Human-authorized consequential | Network isolation, remote-access change, firewall change, maintenance-mode transition | Recommendation + authority model in scope; execution is human |

### 3.4 Participant / program deliverables that are in scope

Current-state map; top L1–L12 imperfections; asset identity reconciliation; telemetry quality findings; process/asset dependency model; contextual risk model; safety/security conflict handling; resilience/recovery graph; target architecture; bounded-autonomy model; TEVV strategy; KPI before/after; 90-day roadmap; executive defense.

### 3.5 Suggested investigation path (in scope order)

inventory → topology → asset identity → telemetry quality → process dependencies → cyber/safety context → recovery dependencies → decision/authority model → evals → intervention

---

## 4. Out of scope

Out-of-scope items are either **unsafe**, **unauthorized**, **explicitly forbidden by the engagement**, or **not justified until evidence exists**.

### 4.1 Control, safety, and live OT — do not do these

- Connect to real OT systems or real industrial equipment.
- PLC logic writes, setpoint changes, or any live controller write.
- SIS modifications, interlock bypass, trip suppression.
- Unsafe restart or unsafe isolation as an automated or unreviewed action.
- Automatic isolation solely because an alert is HIGH or CRITICAL.
- Code or agents that perform network blocking or real control actions.

These are out of scope for this repository and are generally highly restricted in any real implementation.

### 4.2 Engagement and method — do not do these

- Greenfield rewrite of the estate “to clean it up.”
- Silently cleaning intentional data inconsistencies (they are evidence, not dirt).
- Treating CMDB, passive discovery, historian, SCADA, CMMS, SIEM, or operator notes as authoritative by name alone.
- Ranking risk by CVSS alone.
- Declaring recovery ready because a backup flag is CURRENT.
- Using `restricted_answer_key/` unless explicitly authorized.
- Introducing agentic automation before tests/evals exist.
- Consequential target-state action that is not bounded by policy, safety constraints, and human authority.

### 4.3 Technology assumptions that are out of scope unless evidence justifies them

Knowledge graph, digital twin, RAG, and agents are **intervention options, not mandatory technologies**. They are out of scope as default architecture. Use them only when evidence shows they solve a real identity, temporal, safety, recovery, or authority problem.

### 4.4 Recommendation quality bars that put a design out of scope

A recommendation is out of scope if it does not expose:

- evidence and source
- freshness
- uncertainty
- process impact
- safety impact
- rollback considerations
- required authority

---

## 5. Scope boundary in one view

| Question | In scope | Out of scope |
|---|---|---|
| What is broken in the inherited estate? | Forensics across L1–L12 using synthetic data and conflicting sources | Assuming one system is the truth |
| What should the command center do first? | Situational awareness, contextual risk, governed recommendations | Automating plant control |
| How should risk be ranked? | Reachability + criticality + safety + controls + recovery | CVSS-only |
| How should containment be handled? | Safety-aware recommendation with human authority | Auto-isolate / PLC isolation |
| How should recovery be judged? | Restore test, runbook, dependencies, manual fallback | “Backup exists therefore recoverable” |
| What may software do alone? | Collect, correlate, summarize, rank, read-only simulate | Writes, SIS changes, bypasses, live isolation |
| What AI is allowed? | Bounded, evaluated, auditable decision support | Unbounded agents or control-loop AI |
| What architecture is required? | Whatever evidence justifies | KG / twin / RAG / agents by default |
| What environment is this? | Local synthetic simulation | Real plants, real credentials, real controllers |

---

## 6. What we need to consider when working the problem

1. **Highest CVSS is not highest operational risk.** Always ask reachability, process criticality, safety barrier state, compensating controls, and recovery capability.
2. **Do not collapse five truths into one status field.** Observed, registered, operational, safety, and authority states must stay distinct.
3. **Security response can create a safety or production incident.** Isolation is a consequential act, not a default playbook.
4. **Preserve contradictions.** Cleaning the dataset removes the problem the engagement is meant to solve.
5. **Prove recovery; do not infer it.** Backup, restore-test freshness, runbook, and dependency verification are separate facts.
6. **Authority before autonomy.** Eval gates (identity, evidence grounding, temporal correctness, safety policy, authority, side effects, uncertainty) come before agents.
7. **Every recommendation needs an owner.** If the action is isolation, remote-access change, firewall change, or maintenance-mode, a human must authorize it.
8. **Measure before modernizing.** Baseline the KPI catalogue so the 90-day roadmap is judged on disagreement rate, quality, time-to-confidence, and unsafe-recommendation avoidance — not on dashboard count.

---

## 7. Bottom line

**Business problem:** the company wants a global risk and resilience command center, but it cannot trust what it sees, cannot map cyber to process and safety consequence, and cannot prove it can recover — so it cannot safely automate decisions.

**Pain:** conflicting inventories, dirty telemetry, CVSS-blind risk, safety/security collision, CMMS/field split, undocumented access, untested recovery, and fragmented authority.

**In scope:** brownfield forensics, contextual risk, safety-aware and recovery-aware decision design, bounded recommendations, TEVV, KPIs, and a 90-day governed roadmap.

**Out of scope:** live OT connection, controller/SIS/interlock writes, automatic isolation, CVSS-only ranking, backup-as-recovery, silent data cleanup, unrestricted answer keys, and AI architecture chosen without evidence.

---

*This statement does not recommend live controller writes, SIS changes, interlock bypasses, or unsafe isolation. All counts cited are from the synthetic v2 verification/diagnostics evidence in the repository.*
