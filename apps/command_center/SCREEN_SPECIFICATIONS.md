# SCREEN_SPECIFICATIONS — Command Center

**APP-00** · Maps PRD §12 (15 screens) · Acceptance: `specs/APP_ACCEPTANCE_TESTS.md`

Each screen specifies: purpose, personas, API, layout, card hierarchy, states, forbidden controls.

---

## S01 — Risk & Resilience Control Tower

| Field | Value |
|-------|-------|
| **ID** | `control-tower` |
| **Personas** | All (default landing) |
| **API** | `GET /health`, `GET /diagnostics`, `GET /ops/slo` |
| **Acceptance** | APP-AT-016, APP-AT-008 |

**Layout:** CTQ strip → diagnostics grid (14 counters) → plant heatmap → open decisions footer.

**Cards (priority):**
1. SLO-OT / harness badge
2. Identity & telemetry defect counts
3. Safety & session counts
4. Recovery stale counts
5. Quick-incident list (links to S09/S11)

**States:** Loading skeleton; stale `workshop-static` freshness label.

**Forbidden:** Any OT action buttons.

---

## S02 — Asset Identity Reconciliation

| Field | Value |
|-------|-------|
| **ID** | `identity-reconciliation` |
| **Personas** | Analyst, FDE |
| **API** | `GET /assets/{id}/identity`, `GET /identity/conflicts` |
| **Acceptance** | APP-AT-001, APP-AT-008 |

**Layout:** Conflict summary tiles → alias collision table → asset bundle detail → shadow overlay panel (low confidence).

**Cards:** RegisteredState vs ObservedState split; alias candidates; evidence table with source_path.

**States:** 404 asset; collision (confidence < 1); shadow overlay present.

**Forbidden:** Merge aliases; CMDB winner; promote shadow.

---

## S03 — Telemetry Quality & Timeline

| Field | Value |
|-------|-------|
| **ID** | `telemetry-quality` |
| **Personas** | Analyst, PE |
| **API** | `GET /telemetry/quality`, `GET /telemetry/timeline?order=event_time` |
| **Acceptance** | APP-AT-004, APP-AT-009 |

**Layout:** Quality summary cards → dual-clock timeline table → unit mismatch filter.

**Cards:** bad/uncertain count; duplicates; unit_mismatches; ingest lag p50/max.

**States:** Temporal anomaly badge; unit F vs C flag; ingest_time_missing uncertainty.

**Forbidden:** Impute BAD→GOOD; plot F as C; “process healthy” from GOOD quality.

---

## S04 — Process / Dependency Graph

| Field | Value |
|-------|-------|
| **ID** | `process-graph` |
| **Personas** | PE, Safety |
| **API** | `GET /graph/slice?query=Q2`, process_dependencies.csv |
| **Acceptance** | APP-AT-012 |

**Layout:** Hop-capped path viewer → unit dependency list → undocumented path count banner.

**Cards:** PATH edges (documented vs observed); unit production_criticality; downstream safety deps.

**States:** Blast radius unknown (779 paths); unit_join_missing.

**Forbidden:** Regional isolate action.

---

## S05 — Contextual Risk Workbench

| Field | Value |
|-------|-------|
| **ID** | `contextual-risk` |
| **Personas** | Analyst |
| **API** | `GET /risk/contextual?limit=N` |
| **Acceptance** | APP-AT-002, APP-AT-014 |

**Layout:** Rank table with factor columns → selected-row breakdown drawer.

**Cards:** Finding ID, asset, CVSS (input not sort key), reachability, criticality, safety, recovery, score.

**States:** Legacy rank contrast note (educational — not used for sort).

**Forbidden:** CVSS-only default sort.

---

## S06 — Safety vs Security Conflict Board

| Field | Value |
|-------|-------|
| **ID** | `safety-conflicts` |
| **Personas** | Safety, Analyst |
| **API** | `GET /safety/conflicts`, `GET /graph/slice?query=Q3` |
| **Acceptance** | APP-AT-003, APP-AT-011 |

**Layout:** Degraded barrier table → bypassed_unauthorized highlight → alert cross-ref (soc vs SIS).

**Cards:** barrier_id, unit, state, bypass_authorized, proof_test_status.

**States:** UNKNOWN bypass_authorized (not treated as YES).

**Forbidden:** bypass_interlock; hide bypass from view.

---

## S07 — Remote Access & Vendor Sessions

| Field | Value |
|-------|-------|
| **ID** | `vendor-sessions` |
| **Personas** | Analyst |
| **API** | `GET /diagnostics`, remote_access_sessions.csv (structured view) |
| **Acceptance** | APP-AT-010 |

**Layout:** Unapproved/MFA summary → session table (plant-scoped) → tier-3 notice for access changes.

**Cards:** session_id, approved_window, mfa, asset_id (minimized export).

**Forbidden:** Auto-disable VPN; dump all plants’ sessions; execute change_remote_access.

---

## S08 — Recovery / Restore-Test Graph

| Field | Value |
|-------|-------|
| **ID** | `recovery-graph` |
| **Personas** | PE, VP Ops |
| **API** | `GET /recovery/{plant}`, `GET /graph/slice?query=Q4` |
| **Acceptance** | APP-AT-005, APP-AT-013, APP-AT-015 |

**Layout:** Plant selector → component matrix → blockers list per component.

**Cards:** backup_status, restore_test_days, runbook_status, dependency_verified, manual_fallback, recovery_ready.

**States:** CURRENT but not ready; drill failure narrative (inject_06).

**Forbidden:** “Recoverable because backup CURRENT” badge; live restore sequence UI.

---

## S09 — Incident Context Graph

| Field | Value |
|-------|-------|
| **ID** | `incident-context` |
| **Personas** | All (incident mode) |
| **API** | `GET /graph/slice?query=Q5`, cascade_001.json timeline |
| **Acceptance** | APP-AT-007 |

**Layout:** Timeline bar → graph canvas → dissent dual column (SOC vs PE).

**Cards:** Session, Asset, Unit safe_state, Barrier, UntrustedNote nodes.

**States:** Scenario badge on narrative counts; execute=false on all paths.

**Forbidden:** Execute at 08:47 SOC step; ignore 08:50 PE warning.

---

## S10 — Hybrid Retrieval Evidence panel

| Field | Value |
|-------|-------|
| **ID** | `retrieval-evidence` |
| **Personas** | Analyst |
| **API** | Packet `evidence[]`, policy catalog, traces |
| **Acceptance** | APP-AT-003, APP-AT-006 |

**Layout:** Channel tabs → cited rows → POLICY pin footer.

**Channels:** STRUCTURED · GRAPH · VECTOR (off) · POLICY · MEMORY.

**Forbidden:** VECTOR setting isolation or ACTION_TIERS.

---

## S11 — Authority Gate / Recommendation

| Field | Value |
|-------|-------|
| **ID** | `recommendation-gate` |
| **Personas** | Analyst, Safety, VP Ops |
| **API** | `POST /recommend`, `GET /authority/actions` |
| **Acceptance** | APP-AT-003, 007, 017–022 |

**Layout:** Workflow progress (8 states) → packet body → evidence table → advisory footer.

**Cards:** recommendation enum; safe_state; process_impact; safety_impact; required_authority; missing_fields; authorizable flag.

**Primary actions:** Export packet · View trace · Copy summary.

**Forbidden:** Execute Isolation · Write PLC · Modify SIS · One-click Authorize · Trip suppress.

**Automation bias (EVAL-020):** Authorize disabled when CTQ-ISO incomplete even if CRITICAL banner shown.

---

## S12 — Decision Trace / Audit

| Field | Value |
|-------|-------|
| **ID** | `decision-trace` |
| **Personas** | FDE, audit |
| **API** | traces JSONL (via API wrapper future), `GET /ops/slo`, `GET /ops/cost-per-incident` |
| **Acceptance** | APP-AT-023 |

**Layout:** Trace list → trace detail (tool_trace, tokens, latency_ms, policy_gate).

**Cards:** decision_id, actor, purpose, recommendation, execute (always false).

---

## S13 — Inject / Failure Simulation

| Field | Value |
|-------|-------|
| **ID** | `inject-simulator` |
| **Personas** | FDE, QA |
| **API** | `POST /eval/run`, scenario fixtures |
| **Acceptance** | APP-AT-023, APP-AT-024 |

**Layout:** Scenario picker (inject_01…06, cascade_001, nominal) → expected badges → run harness → results table.

**Cards:** Per-case PASS/FAIL; must_not violations highlighted.

**Forbidden:** Hide conflicts to beautify demo.

---

## S14 — KPI Before/After

| Field | Value |
|-------|-------|
| **ID** | `kpi-before-after` |
| **Personas** | Executive, FDE |
| **API** | diagnostics vs `docs/05_kpis_baseline.md` |
| **Acceptance** | PRD §17 |

**Layout:** KPI table with before (legacy/estate) vs after (modern) columns → counter-metrics row.

**Note:** Numeric pass thresholds OPEN-006 — show BASELINE_PENDING where unset.

---

## S15 — Executive Brief

| Field | Value |
|-------|-------|
| **ID** | `executive-brief` |
| **Personas** | Executive |
| **API** | Aggregated diagnostics, ops/slo, assurance summary |
| **Acceptance** | Journey D |

**Layout:** One-page posture → CTQ checklist → residual risk → drill links (read-only).

**Forbidden:** Execute controls; deep operational mutate actions.

---

## Cross-screen screen map

| PRD # | Screen ID | Route (APP-02) |
|-------|-----------|----------------|
| 1 | control-tower | `/` |
| 2 | identity-reconciliation | `/identity` |
| 3 | telemetry-quality | `/telemetry` |
| 4 | process-graph | `/process` |
| 5 | contextual-risk | `/risk` |
| 6 | safety-conflicts | `/safety` |
| 7 | vendor-sessions | `/sessions` |
| 8 | recovery-graph | `/recovery` |
| 9 | incident-context | `/incident` |
| 10 | retrieval-evidence | drawer (global) |
| 11 | recommendation-gate | `/recommend` |
| 12 | decision-trace | `/audit` |
| 13 | inject-simulator | `/simulation` |
| 14 | kpi-before-after | `/kpi` |
| 15 | executive-brief | `/executive` |

---

## Visual language

| Element | Treatment |
|---------|-----------|
| Uncertainty | Amber badge, confidence decimal, UNKNOWN literal |
| Untrusted | Red border (shift email, inject narrative) |
| Safety degraded | Orange row highlight — not alarm red execute |
| Execute forbidden | Controls absent — not disabled-with-tooltip only |
| Provenance | Monospace source_path; click to pin in drawer |
| AI | Toggle in header; off = default |

**Aesthetic:** Industrial control room — dark-neutral chrome, high information density, no marketing hero blocks.
