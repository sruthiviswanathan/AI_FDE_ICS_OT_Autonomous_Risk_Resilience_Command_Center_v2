# SDD-09 — Options and selected solution (OM-8)

**Prompt:** SDD-09 | OM-8 Options and selected solution  
**Depends on:** SDD-03 forensics, SDD-04 SCQA, SDD-05 use case, SDD-08 TEVV  
**Date:** 2026-09-16  
**FDE capabilities evidenced:** C10, C12, C23, C29, C30, C33, C34, C36, C59, C75–C77  
**Not this prompt:** information architecture (SDD-10); app C4 (SDD-11); implement engines.

`docs/04_target_capabilities.md`: KG, digital twin, RAG, and agents are **intervention options, not defaults**. Used below only where SDD-03 shows a real problem.

**Ban:** decorative graph. **Ban:** chatty multi-agent without FinOps. **Ban:** autonomous isolation. **Ban:** an AI component with no SDD-08 eval.

---

## Evidence used / assumptions / unknowns / what this artifact did not conclude

### Evidence used

| Source | Problem that options must solve |
|---|---|
| SDD-03 | 5 alias collisions; 200 state conflicts; 99 RETIRED∩ONLINE; 830 CVSS-label mismatch; 860 safety-blind ISOLATE; 113/119 CURRENT-backup lies; 4094 dirty telemetry; 182/2016 tagged; 779 undocumented paths; PLT-03-SAFE-14; OT-01016; CASCADE 08:47 vs 08:50 |
| `legacy_rank` / `legacy_recovery_ready` / `legacy_isolation_recommendation` | Anti-oracles (XFAIL) |
| SDD-05 | B always-on; C AI-assist after rules; D/E no-go |
| SDD-08 | EVAL-001…031 fail-closed contract |
| SDD-07 | Shadow ≠ CMDB; email untrusted; dual clocks |
| `docs/04` | Do not assume KG/twin/RAG/agents |
| `requirements.txt` | No graph DB, no LLM SDK today — workshop extend-this-repo is feasible |

### Assumptions

1. Workshop delivery = extend **this repo** unless a buy/partner option actually closes identity/safety/recovery joins (none does — §6).
2. “Graph” means **typed relationship views** for named queries, not a new master CMDB and not RDF-by-fashion. Persistence choice is SDD-10.
3. TCO is **order-of-magnitude workshop units** (FDE-weeks, relative token-units). Not a procurement quote.
4. Optional LLM is **off by default** until EVAL-016/021/025/026 have a harness.

### Unknowns

Provider/model pick **OPEN-028**. Named Authorizer OPEN-001. Production topology OPEN-003. Token $/incident OPEN-006.

### What this artifact did not conclude

- Did not pick Neo4j vs JSON vs RDF (SDD-10).
- Did not pick an LLM vendor (OPEN-028).
- Did not implement engines.
- Did not approve digital twin or isolate tools.

---

## 1. Solution catalogue

Primary catalogue is the three options this prompt requires. Adjacent rejects (dashboard, twin, buy-GRC) are recorded so they are not re-litigated.

### 1.1 Option A — Non-AI rules workbench (always-on core)

| | |
|---|---|
| **Description** | Deterministic joins + RACI + war-room checklist. Replace *use* of `legacy_*` with modern predicates; keep `legacy_*` as comparison shim (`00_SHARED_CONSTRAINTS`). CLI/API remain read-only. |
| **Uses** | No LLM. No agents. No vector. Bounded **identity / process / safety / recovery relationship views** (not a decorative KG). No digital twin. |
| **Maps to SDD-03** | L1 RC-C (wrong flags); L4 identity; L3 clocks; L7 bypass; L10 CURRENT lie; L12 authority |
| **SDD-08** | Can pass 001–006, 015–019, 023 as **pure functions**. Weak on 007 narrative and 020 fluency-bias *if* the UI still shouts CRITICAL. |
| **Residual** | Shift-email language and 2800-alert narration stay human (SDD-05 §4). Automation bias still possible from a red banner. |
| **Build/buy/partner** | **Build** — extend `src/ot_command/` |
| **TCO sketch** | Lowest incremental software; highest ongoing analyst minutes if volume stays 2800 alerts with 1735 UNKNOWN context |

### 1.2 Option B — Constrained AI advisory (selected envelope)

| | |
|---|---|
| **Description** | **Option A is the control plane.** Optional LLM **explains already-computed facts** and drafts `docs/06` packets. Single bounded agent **if and only if** a thin tool loop is needed to call **deterministic** tools (observe/correlate/summarize/recommend). HITL for Authorize. AI-disabled = Option A. |
| **Uses** | LLM: optional, provider-abstracted. RAG/vector: **only** untrusted memory over shift notes / inject narratives (EVAL-029/007). Agents: default **none**; max **one** advisory agent + deterministic tools. KG: **bounded evidence graph views** (Forced ADR-KG). Twin: **no**. Isolate tools: **no**. |
| **Maps to SDD-03** | Same as A **plus** L11 explanation of SOC vs PE (CASCADE); L3 handover historian-vs-HMI as untrusted text |
| **SDD-08** | Must pass **all** EVAL-001…031 including 014/016/020/026/027 |
| **Residual** | OPEN-RISK-05/11 automation bias; token cost if misused for rank |
| **Build/buy/partner** | **Build** on this repo; **partner** only as optional LLM port (not selected now) |
| **TCO sketch** | A’s engine cost + small explanation layer; tokens bounded by “facts first, then N sentences” (EVAL-026) |

### 1.3 Option C — Unsafe autonomous OT agent (**reject**)

| | |
|---|---|
| **Description** | Multi-agent copilot with `isolate_endpoint` / firewall / PLC/SIS tools; closed-loop optimization; “command center” as actuator. |
| **Uses** | Agents yes; tools that fail EVAL-023; likely decorative KG; twin optional |
| **Maps to SDD-03** | **Scales RC-C** (L12): 860 ISOLATE, safety-blind, CURRENT=ready |
| **SDD-08** | **Fails** 003, 006, 007, 014, 019, 023, 027, 030, CTQ-0 |
| **Residual** | Intolerable people/process/safety (SDD-05 impact screen) |
| **Build/buy/partner** | Must not |
| **TCO sketch** | Token-cheap, harm-infinite. FinOps **cannot** select this. |

### 1.4 Adjacent options (evaluated, not selected)

| Option | Why not |
|---|---|
| **A0 Status-quo war room + prettier `/diagnostics`** | 14 collapsed ints; does not fix RC-C; SDD-05 rejected “another dashboard” |
| **Digital twin + closed-loop** | SDD-07: not a real fleet; 1834/2016 untagged; no restore blobs (OPEN-027); closed-loop = actuation |
| **Buy GRC / OT cyber platform, wrap CSVs** | Would still CVSS-rank unless **our** joins exist; vendor concentration; does not own SafetyBarrierState vs isolate |
| **Multi-agent** (SOC agent, safety agent, recovery agent chatting) | No SDD-03 proof a **single** bounded caller of deterministic tools is insufficient. Token multiplier fails FinOps (EVAL-025/026). Default **rejected**. Re-open only with a measured cost+eval case |

---

## 2. Component justification (from SDD-03, not fashion)

| Component | Verdict | SDD-03 evidence | If built, must pass |
|---|---|---|---|
| **Identity graph** (alias–asset–state, **no winner**) | **YES** | 5 collisions e.g. `PLT-01-DCS_CONTROLLER-105` → OT-00012 **and** OT-00033; 200 conflicts; OT-00528 RETIRED∩ONLINE | EVAL-001, 008, 028, 029; CTQ-ID |
| **Contextual risk engine** | **YES** | `legacy_rank` CVSS-only; VUL-00706 9.8 unreachable LOW vs VUL-00098 8.7 reachable on OT-01016 MIN_LOAD; 53 cvss≥9 reachable NO | EVAL-002, 017; CTQ-CVSS |
| **Safety policy** | **YES** | 860 HIGH/CRIT → ISOLATE; 32 MIN_LOAD/non-ACTIVE joins; PLT-03-SAFE-14 BYPASSED authorized NO | EVAL-003, 011, 014, 019, 020, 027, 030; CTQ-ISO |
| **Recovery graph** (plant×component + process deps as **blockers**, not a ready badge) | **YES** | 113/119 CURRENT weak; PLT-01 IDENTITY 360d STALE; diagnostics ignore restore-test days | EVAL-005, 013, 018; CTQ-REC |
| **Vector over shift notes** | **ONLY untrusted memory** | `shift_handover_email.txt` is untrusted (SDD-07); useful for CASCADE language, **never** policy | EVAL-007, 016, 021, 029; vector **must not** set IsolationRecommendation or ACTION_TIERS |
| **Autonomous isolation** | **NO** | 08:47 vs 08:50; handover “do not isolate without PE”; CTQ-0 | EVAL-003, 007, 019, 023 — fail if tool exists |
| **Multi-agent** | **NO unless proven insufficient** | No cell shows three LLMs needed; FinOps | Default: **single agent + deterministic tools** or **no agent** (rules only). EVAL-023, 025, 026 |
| **Digital twin** | **NO** | No live process envelope; tag coverage 9%; no restore proof | Would fake ProcessHealthy (OPEN-026) |
| **Enterprise / decorative KG** | **NO** | Diagnostics already collapse facts; a pretty graph of 14 ints solves nothing | Forced ADR-KG |

**Reference shapes (C29) — not code**

```text
Option A:  Files → deterministic engines → packet JSON → human war room
Option B:  Option A → optional explainer LLM (facts in, prose out) → same packet → HITL
Option C:  LLM → tools(isolate/PLC) → plant     REJECT
```

Option B C4-level containers (detail in SDD-11): read-only API, engines (identity/risk/safety/recovery), eval harness, optional explainer port, CLI. No OT actuator container.

---

## 3. Forced ADR-KG — knowledge graph (C23) **before SDD-10**

**Status:** Proposed  
**Decision:** **CONDITIONAL YES — bounded evidence graph as a gold *view*, not a system of record. Decorative / enterprise KG: REJECTED.**

### 3.1 Why not “relational only, no graph language”

CSV **already** stores the edges. SDD-03 still fails operators because **multi-hop questions are not in the product**:

| Query the view must answer (feeds SDD-10) | Evidence it is a real query |
|---|---|
| Identity lineage (aliases × sources × registered vs observed) | 5 collisions; 6048 aliases; EVAL-001 |
| Undocumented path to a CRITICAL / HIGH unit | 779 undocumented observed edges; OT-01016 |
| Safety–cyber join | 32 HIGH/CRIT on MIN_LOAD or non-ACTIVE barrier; traces A–C |
| Recovery blockers | CURRENT ∧ stale restore/runbook/dep; process_dependencies 198 |
| CASCADE-001 slice | 08:24 session, 08:38 bypass, 08:47/08:50 conflict |

A **graph-shaped view** (nodes = Asset, Alias, Unit, Barrier, Finding, Alert, Session, RecoveryComponent; edges typed; **conflicts as first-class nodes/edges, never overwritten**) is justified so SDD-10 can schema those queries.

### 3.2 Why not a knowledge-graph platform as architecture answer

| Reject | Reason |
|---|---|
| Graph as CMDB / winner | EVAL-001 must_not; CTQ-ID |
| Graph that imputes missing tag→unit for 1834 assets | OPEN-020; missing edge must stay missing |
| RDF/property-graph fashion without those five queries | Decorative — **gate fail** |
| Vector store as the graph | Retrieval mix ADR-06; not identity truth |

**Relational / typed JSON adjacency can implement the view.** Store engine = SDD-10 (queries, not fashion). This ADR does **not** select Neo4j.

**Kill for SDD-10:** a schema with nodes that have a single `status`, or a graph used as DecisionAuthority.

---

## 4. RAG / retrieval thought-experiment (C36) — not a production index

| Corpus | Trust | Retrieval |
|---|---|---|
| Structured CSV/JSONL | Workshop files; operational-truth UNKNOWN | **STRUCTURED + GRAPH view** filters (plant, zone, time, policy version) |
| `shift_handover_email.txt`, inject titles | **Untrusted content** | Optional **VECTOR** for recall of phrasing (“min stable load”, “temporary bypass”) **with citation** |
| CASCADE JSON | Eval narrative | Structured scenario id, not RAG-as-history |
| Shadow spreadsheet | Evidence of disagreement | Structured overlay; **no** embedding-as-master |

**Thought-experiment PoC (not built):** embed the six email bullets; query “should we isolate?”; **correct** result is a **cited quote** plus engine output `safe_state=MIN_LOAD` / DO_NOT_ISOLATE. **Incorrect** result is vector similarity deciding isolate. EVAL-007/027/029.

No production vector index in Repo 2.0 unless SDD-10/11 keep the untrusted label and EVAL-016 still works with vector **off**.

---

## 5. Weighted trade-off (C12)

Weights sum to 100. **AI sophistication is not a criterion.** FinOps/tokens included.

| Criterion | W | A Rules | B Constrained advisory | C Unsafe agent | Notes |
|---|---:|---:|---:|---:|---|
| Safety (no actuate, CTQ-ISO) | 18 | 5 | 5 | 1 | C fails by design |
| Authority enforcement | 14 | 5 | 5 | 1 | EVAL-006/014 |
| Identity truth | 12 | 5 | 5 | 2 | C will merge to act |
| Telemetry provenance | 8 | 5 | 5 | 2 | |
| Recovery honesty | 10 | 5 | 5 | 1 | C likely CURRENT=ready |
| Explainability | 8 | 3 | 5 | 2 | B’s only extra value |
| Eval-ability (SDD-08) | 10 | 4 | 5 | 1 | B must map every AI piece |
| TCO / FinOps (tokens) | 10 | 5 | 4 | 1 | C “cheap tokens, infinite harm”; B capped |
| Time-to-90-days (workshop) | 6 | 5 | 4 | 2 | Extend repo |
| Vendor concentration | 4 | 5 | 4 | 1 | B optional port; C vendor lock + tools |
| **Weighted /5** | | **4.72** | **4.78** | **1.30** | B wins on explainability at small FinOps cost; **A is mandatory subset** |

**Read:** select **B as envelope**, **A as non-optional core**. C eliminated. If LLM never turns on, the selected solution **degrades to A** and still beats C.

---

## 6. Build / buy / partner (C75–C77) + TCO (C59)

**Workshop default: build = extend this repository.** No evidence that a purchased OT-cyber/GRC tool already performs EVAL-002/003/005 joins on **these** files.

| Approach | Verdict |
|---|---|
| **Build** modern engines beside `legacy/` | **Selected** |
| **Buy** platform | **Reject for workshop** — would wrap CVSS dashboards unless we still build the engines |
| **Partner** LLM provider | **Optional later**; not required to pass A-path evals. Comparison **OPEN-028** |
| **Partner** SIEM/SOAR isolate | **Reject** — isolate execute |

### TCO sketch (synthetic, named assumptions)

Assumptions: one FDE; local venv; no production IAM; LLM off or local/small; 90-day workshop horizon; harm cost of unsafe isolate **not monetized** (intolerable, not a line item).

| Cost element | Status-quo war room | Advisory CC (A+B) | Unsafe autonomous agent |
|---|---|---|---|
| Software 90d | ~0 (already `/diagnostics`) | **M**: engines + evals + optional explainer (order: several FDE-weeks, same repo) | **L** code, **unbounded** review/legal/safety |
| Human time | **H** (identity rework, PE unused, 860 false isolate strings) | **M** — joins cut rework; HITL remains | **Fake L** then incident **H** |
| Tokens / FinOps | 0 | **L** if explain-after-facts; **H** if multi-agent debate (rejected) | **H** tool loops + still wrong |
| Eval/TEVV | 3 XFAIL only | **M** harness for EVAL-001…031 | Fail-closed; cannot ship |
| Residual harm | Medium (wrong advice, no write path) | Medium-low (OPEN-RISK-11) | **Intolerable** |
| **Select?** | Baseline, not the modernization | **Yes** | **No** |

FinOps selection rule: a design whose token path can answer EVAL-002 by **omitting** safety/recovery joins is **disqualified** even if cheaper (EVAL-026). Multi-agent chatter is **disqualified** without a measured insufficiency of a single tool-caller.

---

## 7. Model / provider (C34) — OPEN

| Requirement | Decision now |
|---|---|
| Deterministic engines | **Required**; no vendor |
| LLM | Optional explainer behind a **port**; substitution: any model **or none** (EVAL-016) |
| Hosted vs local | **OPEN-028** — not required for selected A-core |
| AI-disabled | **Mandatory** equal to Option A |

Do not pick a provider in this ADR set.

---

## 8. Preliminary ADRs ADR-01…ADR-08 (C30)

All status **Proposed**. They constrain SDD-10/11. They do not implement code.

### ADR-01 — Identity

**Decision:** Canonical identity is a **bundle**: `asset_id` + aliases[] + sources[] + RegisteredState + ObservedState. Conflicts remain queryable. No Device grain (OPEN-025). Shadow spreadsheet is an overlay with `confidence=low`, not CMDB.

**SDD-03:** 5 collisions; 200 conflicts; OT-00528.  
**Eval:** EVAL-001, 008, 028, 029.  
**Kill:** silent merge; v1 `operationalState` used as ObservedState without anticorruption (OPEN-009).

### ADR-02 — Telemetry provenance

**Decision:** Dual clock (`event_time`, `ingest_time`/`received_time`) + TelemetryQuality + unit on every assembled telemetry fact. Schema must not drop record fields. No sort on ingest alone. GOOD ≠ ProcessHealthy (OPEN-026).

**SDD-03:** 4094 dirty; 47 F-on-TEMP; EVT-0000001 inversion.  
**Eval:** EVAL-004, 009, 015, 022.  
**Kill:** impute BAD→GOOD; drop ingest_time to match thin schema.

### ADR-03 — Contextual risk

**Decision:** Deterministic rank features: reachability, unit production criticality / process join (or **explicit missing**), SafetyBarrierState, CompensatingControl, RecoveryReady. Cvss is an input **not** the sort key. LLM **must not** re-rank.

**SDD-03:** XFAIL rank; VUL-00706 vs VUL-00098.  
**Eval:** EVAL-002, 017.  
**Kill:** `legacy_rank` as the modern path.

### ADR-04 — Safety policy

**Decision:** Isolation is never execute in software. Drafts require `safe_state` + required role (CTQ-ISO) or **abstain**. Observe existing bypass ≠ `bypass_interlock`. Trip suppression forbidden. UNKNOWN ≠ authorized.

**SDD-03:** 860 ISOLATE; PLT-03-SAFE-14; CASCADE 08:50.  
**Eval:** EVAL-003, 007, 011, 014, 019, 020, 027, 030, 031.  
**Kill:** isolate tool; one-click isolate (EVAL-020).

### ADR-05 — Recovery

**Decision:** RecoveryReady := restore-test evidence **and** RunbookCurrent **and** DependencyVerified=YES. BackupCurrent insufficient. Day threshold OPEN-006/022 — **absence ⇒ false**. No live restore orchestration. Bounded **recovery blocker graph** (ADR-KG).

**SDD-03:** 113/119; PLT-01 IDENTITY.  
**Eval:** EVAL-005, 013, 018.  
**Kill:** `legacy_recovery_ready`.

### ADR-06 — Retrieval mix

**Decision:** STRUCTURED + GRAPH-view filters are authoritative for facts. VECTOR only over **labeled untrusted** notes. POLICY is `policy.py` / ACTION_TIERS, never retrieved text. MEMORY = session working set, not a second CMDB.

**SDD-03/07:** email vs CSV; shadow vs assets diffs 0.  
**Eval:** EVAL-007, 016, 021, 029.  
**Kill:** vector similarity → isolate or ACTION_TIERS.

### ADR-07 — Agent boundary

**Decision:** Default **no agent**: HTTP/CLI calls engines. If an agent exists: **one** advisory agent, tools ⊆ {observe, correlate, summarize, recommend}. No multi-agent unless a later measured case shows the single caller fails EVAL-025/026 **and** still passes 014/023. Unknown tool → refuse (tier 4).

**SDD-03:** ACTION_TIERS unused at recommend time.  
**Eval:** EVAL-006, 014, 023, 025, 026.  
**Kill:** second agent “for safety” that can still isolate; chatty loops.

### ADR-08 — Evidence / feedback

**Decision:** Every recommendation packet: evidence, source, freshness, uncertainty, process impact, safety impact, rollback, required authority (`docs/06`). Feedback = eval harness + preserved contradictions (do not clean). HumanAuthorizationRecorded does not exist yet (G-03) — do not fake it. Hidden CoT is not authority.

**Eval:** EVAL-021, 024, 016; C49 skeleton.  
**Kill:** unsourced prose as DecisionAuthority; deleting collisions to raise CTQ-ID.

---

## 9. AI component → SDD-08 eval map (gate)

| AI / optional component | Allowed? | Eval IDs that fail if it misbehaves |
|---|---|---|
| Explainer LLM | Optional, after engines | 016, 021, 024, 025, 026, 020 |
| Single advisory agent | Optional, ADR-07 | 006, 014, 023, 027 |
| Vector untrusted memory | Optional, off in outage | 007, 016, 021, 029 |
| Identity graph **view** | Required (deterministic) | 001, 008, 028, 029 |
| Contextual risk engine | Required (deterministic) | 002, 017 |
| Safety policy engine | Required (deterministic) | 003, 011, 014, 019, 020, 027, 030, 031 |
| Recovery graph **view** | Required (deterministic) | 005, 013, 018 |
| Dual-clock / units | Required (deterministic) | 004, 009, 015, 022 |
| Multi-agent | **Not selected** | 025, 026, 023 |
| Isolate / PLC / SIS tools | **Forbidden** | 003, 007, 014, 019, 023, 027, 030 |
| Decorative KG | **Forbidden** | (architecture gate; no eval can pass a winner-graph vs 001) |

Deterministic engines are not “AI” but are in the map so SDD-10 does not treat them as optional decoration.

---

## 10. Selected solution (C10)

**Name:** Trusted Cyber-Physical **Advisory** Command Center  
**Envelope:** **Option B**  
**Core (non-optional):** **Option A** rules workbench  
**Rejected:** Option C unsafe agent; digital twin; buy-GRC-as-truth; multi-agent; autonomous isolation; decorative KG

**Means:**

1. Keep `legacy_*` as shims; add modern identity bundle, contextual rank, safety policy, recovery predicate, provenance stamps.
2. Bounded evidence-graph **views** for the five queries in ADR-KG — persistence in SDD-10.
3. Optional explainer LLM behind a port, **off** until EVAL-016 works.
4. Vector only as untrusted memory, never policy.
5. Zero OT write routes (CTQ-0). Recommend ≠ Authorize ≠ Execute.

**Conditions (all required):**

- SDD-08 T-MUSTNOT / T-CTQ0 / T-ISO / T-ID / T-REC / T-CVSS / T-REFUSE / T-OUTAGE hold on the modern path before any LLM default-on.
- Five states never collapsed (SDD-06).
- Workshop = extend this repo (ADR build).
- Provider remains OPEN-028.

**Kill criteria (halt or return to Option A-only / earlier OM):**

| Kill | Evidence trigger |
|---|---|
| K1 | Any isolate/PLC/SIS/setpoint/trip-suppress route or tool (CTQ-0, SDD-04 stop) |
| K2 | Sponsor redefines moonshot as autonomous isolation (SDD-04) |
| K3 | Modern rank is still CVSS-only (EVAL-017 fail) |
| K4 | RecoveryReady true on CURRENT alone (EVAL-018 fail) |
| K5 | Decorative graph or graph-as-CMDB (ADR-KG) |
| K6 | Multi-agent or unmetered tokens without EVAL-026 (FinOps) |
| K7 | AI outage blank screen (EVAL-016) |
| K8 | Wiring recommendations to isolation/PLC APIs (SDD-05; worsens OPEN-002) |
| K9 | Vector or CoT used as authority (ADR-06/08) |

**90-day workshop outcome:** eval-gated advisory packets on synthetic data, not a live plant command center.

---

## 11. OM-8 capability evidence

| ID | Where |
|---|---|
| C10 Product judgement | §10 selected + kill |
| C12 Value engineering | §5 weighted matrix |
| C23 KG justification | Forced ADR-KG §3 |
| C29 Architecture | §2 reference shapes |
| C30 ADRs | ADR-01…08 + ADR-KG |
| C33 / C36 GenAI / RAG | §1.2, §4; optional only |
| C34 Model substitution | §7 OPEN-028 |
| C59 TCO | §6 |
| C75–C77 Build/buy/partner | §6 |

---

## Gate (SDD-09)

| Criterion | Result |
|---|---|
| Catalogue A / B / C-reject | **PASS** §1 |
| Components justified from SDD-03 | **PASS** §2 |
| KG forced ADR before SDD-10 | **PASS** §3 CONDITIONAL bounded view; decorative rejected |
| FinOps vs multi-agent | **PASS** multi-agent not selected |
| ADR-01…08 | **PASS** §8 |
| Every AI component → SDD-08 eval | **PASS** §9 |
| No decorative graph | **PASS** ADR-KG |
| Selected + conditions + kill | **PASS** §10 |

**Output to next:** SDD-10 may schema **only** the subgraph types in ADR-KG (identity lineage, path-to-unit, safety-cyber, recovery blockers, cascade slice). No enterprise ontology by default.
