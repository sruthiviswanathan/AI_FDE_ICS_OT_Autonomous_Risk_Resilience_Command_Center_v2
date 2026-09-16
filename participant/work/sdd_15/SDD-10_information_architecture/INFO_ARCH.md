# SDD-10 — Information architecture (OM-9)

**Prompt:** SDD-10 | OM-9 Information architecture  
**Depends on:** SDD-06 DOMAIN, SDD-07 DATA, SDD-09 OPTIONS (ADR-KG, ADR-01…08)  
**Date:** 2026-09-16  
**FDE capabilities evidenced:** C19, C20, C21, C22, C23, C24, C26  
**Not this prompt:** implement pipelines; pick an LLM; C4 app (SDD-11); rewrite `data/` or root `contracts/asset_api_v1.yaml` / `v2.yaml`.

**Ban:** single `status` on a node. **Ban:** graph as CMDB. **Ban:** vector → IsolationRecommendation or ACTION_TIERS. **Ban:** imputing tag→unit for 1834 untagged assets.

**Draft contracts (do not replace brownfield stubs):** `schemas/` in this folder.

---

## Evidence used / assumptions / unknowns / what this artifact did not conclude

### Evidence used

| Source | Use |
|---|---|
| SDD-06 | Canonical terms; five states; RecoveryReady derived |
| SDD-07 | Bronze files; provenance envelope; G-01…G-15 |
| SDD-09 ADR-KG | Five queries only; decorative KG rejected |
| SDD-09 ADR-01…08 | Identity bundle; dual clock; rank features; retrieval mix |
| `contracts/asset_api_v1.yaml` | `assetId`, `fwVersion`, `operationalState` — **keep as legacy** |
| `contracts/asset_api_v2.yaml` | `asset_id`, `firmware`, `observed_state` — **keep as legacy** |
| `contracts/telemetry_event_schema.json` | Thin required-set; records richer |
| `requirements.txt` | No graph DB / vector DB today |
| SDD-03 | 5 collisions; 779 paths; 182/2016 tagged; 113/119 CURRENT |

### Assumptions

1. Workshop persistence = files + typed JSON views beside engines (ADR-09). Not Neo4j, not RDF.
2. Gold views **expose conflicts**; they do not pick a winner (EVAL-001).
3. `assets.firmware` is a single column → canonical `firmware_declared`; `firmware_observed` is **UNKNOWN** until a second source exists (shadow diffs = 0 today).

### Unknowns

OPEN-009 exact semantics of v1 `operationalState` (must not silently equal ObservedState). OPEN-006/022 restore-test day cut. OPEN-020 untagged majority. OPEN-007 sqlite replica.

### What this artifact did not conclude

- Did not implement silver tables in SQLite.
- Did not add a production vector index (optional, off by default).
- Did not invent Device or ProcessHealthy fields.

---

## 1. Target data architecture (C19) — bronze → silver → gold

```text
BRONZE  data/raw|reference|telemetry|shadow  (immutable; contradictions kept)
   │     repository.rows / jsonl
   ▼
SILVER  typed facts + Provenance  (no silent clean; UNKNOWN preserved)
   │
   ▼
GOLD    decision views (conflicts visible; no winner column)
        - identity_bundle
        - contextual_risk_row
        - safety_security_conflict
        - recovery_blocker
        - evidence_graph slice (five queries)
```

| Layer | Contents | Rules |
|---|---|---|
| **Bronze** | All SDD-07 inventory paths including shadow and sqlite replica | Do not upsert shadow onto assets. Do not delete collisions. `ot_legacy.db` = SQLITE_REPLICA if read (OPEN-007) |
| **Silver** | One fact type per DOMAIN term; every fact has Provenance | No collapsed `status`. FindingDisposition ≠ SocStatus |
| **Gold** | Bundles and graph **views** for engines / packets | Missing joins stay missing (`unit_join_missing: true`). RecoveryReady never copied from BackupStatus |

Lineage as-is today stops at 14 diagnostic ints (SDD-07 §2). Target lineage: bronze → silver fact → gold view → recommendation packet (SDD-11 APIs).

---

## 2. Canonical entities and metrics (SDD-06)

### 2.1 Entities (keys — do not invent)

| Entity | Key | Bronze grain | Notes |
|---|---|---|---|
| Plant | `plant_id` | plants.csv | 18 |
| Asset | `asset_id` (stable **asset_uid** = same string in workshop) | assets.csv | Not Device (OPEN-025) |
| Alias | (`source`,`alias`) **not unique** | asset_aliases.csv | Collision = two Asset links |
| Tag | `tag_id` | tags.csv | 182 assets only |
| ProcessUnit | `unit_id` | process_units.csv | SafeState here |
| ProcessDependency | (upstream, downstream, type) | process_dependencies.csv | |
| NetworkEdge | (plant, source_asset, target_asset, protocol) | network_edges.csv | documented vs observed flags |
| Barrier | `barrier_id` | safety_barriers.csv | |
| Finding | `finding_id` | vulnerabilities.csv | FindingDisposition ← `status` |
| Alert | `alert_id` | cyber_alerts.csv | ProcessContext on alert |
| WorkOrder | `work_order_id` | work_orders.csv | CmmsStatus + FieldStatus |
| RemoteSession | `session_id` | remote_access_sessions.csv | SessionIdentity ≠ AssetIdentity |
| RecoveryComponent | (`plant_id`,`component`) | recovery_readiness.csv | |
| TelemetryEvent | `event_id` | tag_telemetry.jsonl | Dual clock |
| EnterpriseEvent | `event_id` | enterprise_events.jsonl | Dual clock; correlation may be empty |
| UntrustedNote | `source_path` | shift email | VECTOR corpus only |
| ShadowInventoryRow | `asset_id` | FINAL_v8.csv | Overlay, confidence=low |
| RecommendationPacket | `packet_id` (new; not in bronze) | gold | docs/06 fields |
| ConflictRecord | `conflict_id` (new) | gold | first-class; never overwrite sources |

### 2.2 Metrics (gold, not bronze columns)

| Metric | Definition | OPEN |
|---|---|---|
| inventory_disagreement_rate | ACTIVE ∧ {OFFLINE,UNSEEN} / 2016 | measured 200/2016 |
| telemetry_not_good_rate | quality ≠ GOOD / 31224 | 4094/31224 |
| alias_collision_count | alias strings with >1 asset | 5 |
| recovery_current_but_not_ready_count | BackupCurrent failing restore∨runbook∨dep | 113/119 (90d formula SDD-03) |
| Isolation drafts with safe_state+role | CTQ-ISO | 0% as-is |
| MTT contextualize / AI cost | docs/05 | OPEN-006 — **do not store a fake SLA** |

No `healthy` metric (OPEN-026).

---

## 3. Canonical identity + v1/v2 coexistence (C26)

Keep root `contracts/asset_api_v*.yaml` **unchanged** as brownfield evidence.

### 3.1 Canonical Asset (silver)

```text
asset_uid            = assets.asset_id
aliases[]            = {source, alias, provenance}
registered_state     = assets.registered_state
observed_state       = assets.observed_state
operational_interpretation  = nullable; NOT copied from assets.
                     May attach from Alert.process_context for a *case*, never overwrite states.
firmware_declared    = assets.firmware
firmware_observed    = UNKNOWN unless a distinct observation source exists
asset_criticality, plant_id, zone, asset_type, owner  as labeled inventory
conflicts[]          = ConflictRecord links (registered vs observed, alias collision, shadow overlay)
```

Shadow row: same `asset_uid`, `source_system=SHADOW_SPREADSHEET`, confidence=low — **second** Registered/Observed claim if it ever differs; today diffs = 0 so conflict = “parallel register with no cell delta + untrusted email claim.”

### 3.2 Anticorruption (do not merge names)

| Legacy | Maps to canonical | Must not |
|---|---|---|
| v1 `assetId` | `asset_uid` | — |
| v1 `fwVersion` | `firmware_declared` | assume it is observed |
| v1 `operationalState` | **Ambiguous (OPEN-009)** → `legacy_v1_operational_state` **side field** until a human mapping exists | Copy into ObservedState or RegisteredState silently |
| v2 `asset_id` | `asset_uid` | — |
| v2 `firmware` | `firmware_declared` (same as CSV until a second clock exists) | — |
| v2 `observed_state` | ObservedState | Use as RegisteredState |
| CSV `registered_state` + `observed_state` | the two canonical states | Collapse to v1 operationalState |

v1 path `/assets/{id}` vs v2 `/ot-assets/{asset_id}` stay **legacy adapters**. Modern API (SDD-11) exposes the bundle, not `operationalState`.

---

## 4. Provenance / freshness / quality on every fact (C20)

Envelope (SDD-07 §4) required on silver and gold:

| Slot | Required |
|---|---|
| `source_system` | yes |
| `source_path` | yes |
| `extracted_at` | yes (pipeline; missing in bronze) |
| `event_time` | if the fact is an event; else null |
| `ingest_or_received_time` | if present on bronze; else null + `clock_completeness=PARTIAL` |
| `quality_flag` | telemetry: GOOD/UNCERTAIN/BAD; else n/a |
| `confidence` | < 1 on conflict, UNKNOWN, missing join, untrusted note |
| `transform_version` | yes (engine/predicate git or spec id) |

**Conflict is first-class:** do not overwrite. Store `ConflictRecord { type, left_fact_id, right_fact_id, left_value, right_value, rule_id }`. Types: `REGISTERED_VS_OBSERVED`, `ALIAS_COLLISION`, `CMMS_VS_FIELD`, `BACKUP_VS_RECOVERY_PREDICATE`, `SHADOW_VS_ASSETS`, `SEVERITY_VS_CVSS`, `V1_OPERATIONALSTATE_UNMAPPED`.

---

## 5. Semantic layer (C21, C22)

**Selected:** SDD-06 ubiquitous language + this relational/JSON schema.  
**Not selected:** OWL/enterprise ontology, SKOS taxonomy service, “digital twin” type system.

Conditional **graph types** = §7 only (ADR-KG). No extra classes (Recipe, Device, Healthy).

Taxonomy reminder: always qualified `*State` / `*Status` / FindingDisposition / IsolationRecommendation / IsolationExecution.

---

## 6. Retrieval architecture (C24) — STRUCTURED / GRAPH / VECTOR / POLICY / MEMORY

| Channel | Authoritative for | Filters (all apply) | Must not |
|---|---|---|---|
| **STRUCTURED** | Facts from silver tables | `plant_id`, `zone`, `purpose` (identity\|risk\|safety\|recovery\|audit), `as_of` / time window, `policy_version` | Filename as master |
| **GRAPH** | The five ADR-KG queries | Same + hop limit + `include_missing_edges` | Winner node; imputed TAG_ON |
| **VECTOR** | Untrusted notes (email, inject titles) **recall** | plant if known; `trust=untrusted`; citation required | Isolation authority; ACTION_TIERS; RecoveryReady |
| **POLICY** | `ACTION_TIERS`, CTQ-ISO/0, ADR-04/07 | `policy_version` pin | Retrieved prose as policy |
| **MEMORY** | Session working set / decision traces | actor, purpose, expiry | Second CMDB; expired risk ACCEPT as permission (tracker 41 Unknown) |

EVAL-016: VECTOR off, STRUCTURED+GRAPH+POLICY still serve tables.

Default query plan: POLICY gate → STRUCTURED load → GRAPH slice → optional VECTOR cite → MEMORY append. Never VECTOR first.

---

## 7. Conditional evidence graph (C23) — only SDD-09 subgraphs

**Not selected:** enterprise KG, RDF ABox, vector-as-graph, graph-as-SoR.

### 7.1 Node types

`Plant`, `Asset`, `Alias`, `Unit`, `Tag`, `Barrier`, `Finding`, `Alert`, `Session`, `RecoveryComponent`, `Conflict`

Each node: id, type, **no** `status` field. States are **named properties** (registered_state, observed_state, …).

### 7.2 Edge types (typed; missing = no edge)

| Type | From → To | Payload |
|---|---|---|
| `ALIAS_OF` | Alias → Asset | source |
| `IN_PLANT` | Asset → Plant | |
| `TAGGED` | Tag → Asset, Tag → Unit | **omit if no tag** |
| `IN_UNIT` | Asset → Unit | only via TAGGED join |
| `DEPENDS_ON` | Unit → Unit | dependency_type, documented, critical |
| `PROTECTS` | Barrier → Unit | state, proof, bypass_authorized |
| `FOUND_ON` | Finding → Asset | cvss, reachable, disposition |
| `ALERT_ON` | Alert → Asset | soc_severity, process_context |
| `SESSION_ON` | Session → Asset | approved_window, mfa |
| `PATH` | Asset → Asset | documented, observed_last_24h, approved_path |
| `RECOVERY_FOR` | RecoveryComponent → Plant | backup, restore days, runbook, dep, fallback |
| `CONFLICTS` | Conflict → (Asset\|Alias\|…) | conflict type |

### 7.3 Queries the graph **must** answer

**Q1 Identity lineage**  
Input: alias or `asset_id`. Output: all ALIAS_OF, RegisteredState, ObservedState, CONFLICTS (collision, RETIRED∩ONLINE). Example: `PLT-01-DCS_CONTROLLER-105` → OT-00012 and OT-00033. **must_not** merge. EVAL-001.

**Q2 Undocumented path to CRITICAL / HIGH unit**  
Input: asset or plant. Walk PATH where `documented=NO` ∧ `observed_last_24h=YES` (779) until Asset with TAGGED→Unit.production_criticality ∈ {HIGH, CRITICAL} **or** stop with `unit_join_missing`. EVAL-012 analogue; OT-01016.

**Q3 Safety–cyber join**  
Input: alert or finding. Asset → (TAGGED) Unit → PROTECTS barriers + ALERT_ON/FOUND_ON. Return SafeState, barrier states, SocSeverity. If no TAGGED: `unit_join_missing=true` (1834 assets). Traces OT-00211 / OT-01016 / OT-00528. EVAL-003.

**Q4 Recovery blockers**  
Input: `plant_id`. RECOVERY_FOR components where RecoveryReady predicate false; plus DEPENDS_ON edges as process blockers. PLT-01 IDENTITY CURRENT / 360d / STALE. EVAL-005. Never `backup_status` as ready.

**Q5 CASCADE-001 slice**  
As-of 08:55: SESSION_ON (08:24 analogue), PROTECTS bypassed (08:38), ALERT_ON HIGH (08:47), Unit SafeState MIN_LOAD (08:50), UntrustedNote citation. Packet gold view. EVAL-007. Scenario counts (37 controllers) marked `source_system=SCENARIO` not census.

Hop cap: 8. No unbounded “whole estate” materialization in a request (FinOps / latency).

---

## 8. ADR-09 — Workshop persistence (queries, not fashion)

**Status:** Proposed  
**Decision:** **Typed JSON graph + silver JSONL/tables.** Reject RDF. Defer property-graph DB.

| Option | Fit to five queries | Cost in this repo | Verdict |
|---|---|---|---|
| **Typed JSON** (nodes.jsonl, edges.jsonl or nested gold JSON) | 18 plants; 3780 edges; 6048 aliases — all in-process walkable | No new dependency | **Select** |
| Property graph (Neo4j etc.) | Same queries | Not in requirements; ops cost | **Not now** — reopen if hop-8 p95 fails NFR (OPEN-006 class) |
| RDF / OWL | Decorative vs SDD-09 | Fashion | **Reject** |

SQLite may **cache** silver tables later; it is not master (OPEN-007). Bronze CSVs remain source files.

---

## 9. Data ADRs (this phase)

| ID | Decision |
|---|---|
| ADR-01 (SDD-09) | Identity bundle; restated in §3 |
| ADR-02 (SDD-09) | Dual-clock telemetry; silver TelemetryEvent requires ingest_time |
| **ADR-09** | Typed JSON persistence §8 |
| **ADR-10** | v1 `operationalState` is **not** ObservedState; side-field until OPEN-009 closes |

---

## 10. Draft contract index

| File | Purpose |
|---|---|
| `schemas/provenance.yaml` | Envelope |
| `schemas/canonical_asset.yaml` | Identity bundle |
| `schemas/telemetry_event_canonical.json` | Widen required set |
| `schemas/recommendation_packet.yaml` | docs/06 packet |
| `schemas/recovery_view.yaml` | RecoveryReady derived |
| `schemas/evidence_graph.json` | Node/edge types |
| `schemas/anticorruption_v1_v2.yaml` | Legacy field map |

Root `contracts/*` **untouched**.

---

## 11. OM-9 capability evidence

| ID | Where |
|---|---|
| C19 Data engineering | §1 bronze/silver/gold |
| C20 Contracts / lineage / provenance | §4, `schemas/` |
| C21 Knowledge | §5 glossary binding |
| C22 Semantic / conditional ontology | §5–7; OWL not selected |
| C23 KG engineering | §7 five queries only |
| C24 Retrieval | §6 |
| C26 Data contracts | `schemas/` + v1/v2 coexistence |

---

## Gate (SDD-10)

| Criterion | Result |
|---|---|
| Canonical entities from SDD-06 | **PASS** §2 |
| v1/v2 coexistence without collapsing | **PASS** §3, ADR-10 |
| Provenance + conflict first-class | **PASS** §4 |
| Retrieval five channels; vector ≠ policy | **PASS** §6 |
| Graph only ADR-KG types | **PASS** §7 |
| Persistence from queries | **PASS** ADR-09 typed JSON |
| Root brownfield contracts preserved | **PASS** |

**Output to next:** SDD-11 read-only APIs bind to gold views; context snapshot = GRAPH slice × plant × asset × actor × as-of × policy_version.
