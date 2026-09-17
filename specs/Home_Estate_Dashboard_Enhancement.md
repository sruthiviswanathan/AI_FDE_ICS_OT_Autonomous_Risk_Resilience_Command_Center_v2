# Enhanced Prompt: Home Estate Dashboard — Consolidated Plant, Asset & Alert View

## Context

You are working on the **AI FDE ICS/OT Autonomous Risk Resilience Command Center v2** — a brownfield OT advisory application (not a greenfield rewrite). The React frontend lives in `apps/command_center/`; the FastAPI backend in `src/ot_command/`. Data is workshop-static CSV under `data/`.

**Read first:**

- `AGENTS.md`
- `.cursor/rules/sdd.mdc` and `.cursor/rules/ot-fde.mdc`
- `apps/command_center/SCREEN_SPECIFICATIONS.md` (S01 — Risk & Resilience Control Tower)
- `apps/command_center/UI_WIREFRAMES.md` (Screen 1 — plant heatmap intent)
- `apps/command_center/DATA_LAYER.md`
- `contracts/openapi_command_center.yaml`
- `specs/Feature_Enhancement.md` (Feature 2 — cascading Plant/Asset/Alert APIs, if not yet merged)

**Hard constraints (do not violate):**

- Do not reopen SDD-09 (Option A deterministic engines + Option B optional explainer port; Option C rejected).
- Do not change `legacy_*` behavior, delete XFAIL tests, or clean `data/` contradictions.
- Do not add OT write routes, isolate-execute surfaces, SIS bypass, or PLC write capabilities.
- Do not invent ADRs, legal class, named Authorizers, KPI thresholds, or ACTION_TIERS verbs.
- Untraced modules are out of scope (`traceability/TRACEABILITY.csv`).
- UNKNOWN permission is not permission.
- **Evidence first:** never infer highest CVSS = highest operational risk; never rank plants by raw alert count alone without contextual signals and provenance labels.
- **ADR-11 / ADR-12:** dashboard remains read-only; deterministic tables visible regardless of AI toggle.
- **NFR-CAP:** graph slices remain hop-capped ≤ 8; do not render whole-estate force-directed graphs.

---



## Task Overview

Split estate visualization across **two screens** to keep Control Tower scannable:


| Screen                      | Route     | Purpose                                                                                       |
| --------------------------- | --------- | --------------------------------------------------------------------------------------------- |
| **S01 — Control Tower**     | `/`       | Compact home: CTQ strip, diagnostics, quick incidents, **summary + link** to estate dashboard |
| **S01b — Estate Dashboard** | `/estate` | Full interactive view: dashboard graph, heatmap grid, drill-down tables, neighborhood slice   |



| #   | Feature                                              | Priority | Screen |
| --- | ---------------------------------------------------- | -------- | ------ |
| 1   | Plant-level estate summary API (aggregates by plant) | High     | BE     |
| 2   | **Estate dashboard subpage** (`/estate`)             | High     | S01b   |
| 3   | **Dashboard interactive graph** (regional plant map) | High     | S01b   |
| 4   | Plant heatmap / status grid (18 plants)              | High     | S01b   |
| 5   | Interactive drill-down: Plant → Assets → Alerts      | High     | S01b   |
| 6   | Hop-capped neighborhood graph (Q1/Q4/Q5)             | Medium   | S01b   |
| 7   | Context sync with global Plant/Asset/Alert pickers   | Medium   | S01b   |
| 8   | Compact estate summary + nav link on Control Tower   | High     | S01    |
| 9   | Quick-incident rail (data-driven)                    | Medium   | S01    |
| 10  | Preserve CTQ strip + diagnostics on Control Tower    | High     | S01    |


Work incrementally. Preserve existing deterministic engine behavior. Add tests where behavior changes.

---



## Problem

The Home screen (`ControlTower.tsx`) today shows only estate-wide diagnostics counters and a static quick-incident link. It **does not** deliver the consolidated plant/asset/alert view described in wireframes and screen spec:


| Gap                               | Spec / wireframe                                                   | Current code                                               |
| --------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------- |
| Plant heatmap (18 plants)         | `UI_WIREFRAMES.md` Screen 1, `SCREEN_SPECIFICATIONS.md` S01 layout | Missing in `ControlTower.tsx`                              |
| Per-plant asset & alert counts    | Implied by heatmap bars                                            | No plant-level aggregation API                             |
| Interactive drill-down            | User request                                                       | Only hard-coded link to ALT-002783                         |
| Graph view of estate neighborhood | User request                                                       | Graph components exist but not on Home                     |
| Alert severity ≠ operational risk | OT-FDE rule                                                        | Must not sort/color plants by CVSS or raw HIGH count alone |


**Existing building blocks (reuse, do not rewrite):**

- List APIs: `GET /plants`, `GET /plants/{plant_id}/assets`, `GET /assets/{asset_id}/alerts` (`api/client.ts`, `src/ot_command/api.py`)
- Estate summary: `GET /data/views/estate`, `GET /diagnostics`
- Graph slice: `GET /graph/slice?query=Q1|Q5&plant_id=&asset_id=&alert_id=` (`GraphVisualView.tsx`, `GraphSliceView.tsx`)
- Cascading pickers: `ContextIdPickers.tsx` + `AppContext`
- Persona default landing: `/` for SOC Analyst and FDE (`personas/registry.ts`)

---



## Data Model (CSV sources)


| Entity | File                        | PK         | Count | FK                     | Notes                                                            |
| ------ | --------------------------- | ---------- | ----- | ---------------------- | ---------------------------------------------------------------- |
| Plant  | `data/reference/plants.csv` | `plant_id` | 18    | —                      | `region`, `country`, `plant_type`, `criticality`                 |
| Asset  | `data/raw/assets.csv`       | `asset_id` | 2016  | `plant_id`             | `registered_state`, `observed_state`, `zone`, `criticality`      |
| Alert  | `data/raw/cyber_alerts.csv` | `alert_id` | 2800  | `asset_id`, `plant_id` | `severity`, `type`, `soc_status`, `process_context`, `timestamp` |


Relationship: **Plant → Asset → Alert**

**Index helpers already in** `data_layer.py`**:**

- `derived_plants_by_id()`, `derived_assets_by_plant()`, `derived_alerts_by_id()`, `derived_alerts_by_asset()`
- `derived_recovery_by_plant()`, `derived_degraded_barriers_by_unit()` (for contextual signals, not whole-graph rendering)

---



## Feature 1: Plant-Level Estate Summary API



### Problem

Front-end cannot efficiently build a 18-plant dashboard by chaining 18× asset list + N alert calls. Need a **single read-only aggregate** derived at runtime from canonical CSV (same pattern as `estate_derived_view()`).

### Backend requirements

Add to `src/ot_command/core/data_layer.py` and expose via `src/ot_command/api.py`. Document in `contracts/openapi_command_center.yaml`.

```
GET /data/views/estate-by-plant
  Query params (optional):
    severity_min  — filter alert counts (e.g. HIGH, CRITICAL); default: include all
    include_top_alerts — int, default 3, max 10 per plant (most recent HIGH/CRITICAL OPEN/TRIAGED)

  Response:
  {
    "provenance": "runtime-derived",
    "freshness": "workshop-static",
    "plant_count": 18,
    "plants": [
      {
        "plant_id": "PLT-10",
        "region": "NA",
        "country": "Country-2",
        "plant_type": "chemicals",
        "criticality": "HIGH",
        "counts": {
          "assets": 112,
          "alerts_total": 156,
          "alerts_high_critical": 23,
          "alerts_open_or_triaged": 45,
          "asset_state_conflicts": 8,
          "telemetry_bad_or_uncertain": 0,   // if derivable per plant; else omit with note
          "safety_degraded_units": 2,        // units in plant with degraded barrier
          "recovery_stale": 1
        },
        "signals": {
          "elevated": true,                  // deterministic rule — see below
          "elevation_reasons": ["asset_state_conflicts", "safety_degraded_units"]
        },
        "top_alerts": [
          { "alert_id", "asset_id", "severity", "type", "timestamp", "soc_status", "process_context" }
        ]
      }
    ],
    "methodology": {
      "elevated_rule": "…",
      "not_operational_risk_rank": "Alert counts are inventory signals, not contextual risk rank. Use /risk/contextual for findings."
    }
  }
```

**Elevated plant rule (deterministic, document in response):**
A plant is `elevated: true` when **any** of:

- `asset_state_conflicts > 0` (registered ACTIVE + observed OFFLINE/UNSEEN)
- `safety_degraded_units > 0` (barrier state ≠ ACTIVE or unauthorized bypass)
- `recovery_stale > 0` (backup_status ≠ CURRENT for plant)
- `alerts_high_critical_open > 0` where `soc_status` ∈ {OPEN, TRIAGED} **and** `process_context` ≠ UNKNOWN (avoid treating UNKNOWN process context as confirmed operational impact)

Do **not** use CVSS, legacy isolation strings, or raw alert volume as the sole elevation signal.

**Implementation guidance:**

- Add `derived_alerts_by_plant()` index in `data_layer.py` (mirror `derived_alerts_by_asset()`).
- Reuse asset conflict logic from `diagnostics.py` / `identity.py`, scoped per `plant_id`.
- Map safety barriers to plant via asset `unit_id` prefix or existing unit→plant join in assets.csv.
- Cache at module level (`lru_cache` or existing clear_cache pattern).
- Do not modify CSV files.

Add client method: `api.estateByPlant(params?)` in `apps/command_center/src/api/client.ts`.

### Acceptance criteria (Feature 1)

- [ ] Single request returns all 18 plants with counts and elevation flags.
- [ ] PLT-10 (CASCADE workshop plant) shows `elevated: true` with documented reasons.
- [ ] Response includes methodology disclaimer (alert count ≠ contextual risk rank).
- [ ] OpenAPI updated; pytest covers plant count, PLT-10 elevation, unknown plant N/A.

---



## Feature 2: Control Tower — Compact Summary (S01)



### Requirements

Keep **Control Tower** (`ControlTower.tsx`, `/`) **above the fold** — no drill-down tables or full heatmap on this page.

**Layout:**

1. CTQ strip (unchanged).
2. Estate diagnostics card (14 counters) + Quick incidents card (side-by-side).
3. **Estate summary card** (compact):
  - Elevated plant count / total plants (from `GET /data/views/estate-by-plant`).
  - Inline chips for elevated plants (max 6) linking to `/estate?plant=PLT-XX`.
  - Primary CTA: **Open Estate Dashboard →** (`/estate`).
4. Open decisions footer (unchanged).

**Forbidden on Control Tower:** full 18-tile heatmap, asset/alert drill-down tables, neighborhood graph embed.

### Acceptance criteria (Feature 2 — S01)

- [ ] Control Tower fits primary posture view without scrolling on typical laptop viewport (~900px height).
- [ ] Link to `/estate` visible from summary card.
- [ ] Quick incidents remain data-driven.

---



## Feature 3: Estate Dashboard Subpage (S01b)



### Requirements

New page `EstateDashboardPage.tsx` at route `/estate`. Nav label: **Estate Dashboard** under Home group.

**Page sections (top → bottom):**

1. Page title + methodology disclaimer + StaleBadge.
2. **Dashboard graph** (default primary view — see Feature 4).
3. View toggle: `[Dashboard ●] [Grid] [Drill-down]` — or combined layout with graph hero + collapsible drill-down.
4. Plant heatmap grid (when Grid selected or alongside graph in split layout).
5. Drill-down panel (assets + alerts + hop-capped neighborhood graph) when plant selected.

Add route in `App.tsx`, nav in `personas/registry.ts` (`ALL_ROUTES`, SOC/FDE/Full/Executive personas).

---



## Feature 4: Dashboard Interactive Graph



### Requirements

New component `EstateOverviewGraph.tsx` — a **dashboard-style** SVG (not a raw graph slice dump):

**Visual design:**

- **Regional columns:** NA · EU · APAC · LATAM — plants grouped under region headers.
- **Plant nodes:** rounded cards showing `plant_id`, asset count, conflict count, HC alert count (inventory).
- **Elevation encoding:** border/ glow from deterministic `signals.elevated` — **not** CVSS color scale.
- **Node size:** proportional to asset count (min/max clamped) — inventory scale, not risk rank.
- **KPI strip** above graph: total plants · elevated · total assets · open HC alerts (with disclaimer tooltip).
- **Interactivity:** click plant node → select in AppContext + scroll/focus drill-down; hover tooltip with `elevation_reasons`.
- **Pan/zoom:** reuse `PanZoomSvg.tsx`.
- **Selected plant:** highlight ring + optional dashed edges to top-alert asset nodes (max 3 per plant from API).

**Do not:** render all 2016 assets or 2800 alerts. Max ~18 plant nodes + 4 region headers + optional ≤3 alert satellites for selected plant only.

### Acceptance criteria (Feature 4)

- [ ] All 18 plants visible in dashboard graph without scrolling the graph panel.
- [ ] Regional grouping readable; pan/zoom works.
- [ ] Click PLT-10 selects plant and loads drill-down.
- [ ] KPI strip shows methodology disclaimer.

---



## Feature 5: Plant Heatmap / Status Grid



### Requirements

On `/estate` (not Control Tower):

**Layout:**

- **View toggle:** `[Grid ●] [Graph]` (grid default).
- **Region filter** (optional chips): All · NA · EU · APAC · LATAM — client-side filter on `region`.
- **Sort:** Plant ID (default) · Elevated first · Alert HC (with disclaimer tooltip) · Asset conflicts.
- **Plant tiles** (18): each shows `plant_id`, region, asset count, HC alert badge, elevation pill.
- **Visual encoding:** bar or heat intensity from `signals.elevated` + conflict count — **not** CVSS-colored.
- **Click plant tile:** sets global `plantId` in `AppContext`, loads Feature 3 drill-down panel, scrolls/focuses asset table.
- **Keyboard:** tiles focusable; Enter selects plant.

**States:**

- Loading skeleton while `estateByPlant` fetches.
- Error inline with retry (match `ErrorBlock` pattern).
- Stale `workshop-static` freshness label (reuse `StaleBadge` semantics).

**Forbidden:**

- Red "critical" styling based only on alert severity counts without elevation rule.
- Execute / isolate / acknowledge buttons on tiles.



### Acceptance criteria (Feature 5)

- [ ] All 18 plants visible in grid without pagination.
- [ ] Elevated plants visually distinct; tooltip shows `elevation_reasons`.
- [ ] Clicking PLT-10 updates global context pickers and drill-down panel.
- [ ] Region filter and sort work client-side without extra API calls.

---



## Feature 6: Interactive Drill-Down Panel



### Requirements

When a plant is selected (from heatmap, picker, or URL `?plant=PLT-10`):

**Three-column or stacked panel below heatmap:**


| Column       | Content                                                                            | API                                                                                                               |
| ------------ | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Assets       | Searchable table: asset_id, type, zone, registered/observed state, conflict flag   | `GET /plants/{plant_id}/assets?limit=500&q=`                                                                      |
| Alerts       | Filterable table: alert_id, severity, type, soc_status, process_context, timestamp | `GET /assets/{asset_id}/alerts` per selected asset; or plant-level top_alerts from Feature 1 until asset selected |
| Detail strip | Selected row summary + deep links                                                  | —                                                                                                                 |


**Interactions:**

1. Select plant → load assets; auto-select first asset with HC alert if any, else first asset.
2. Select asset → load alerts; highlight OPEN/TRIAGED HIGH/CRITICAL.
3. Select alert → set `alertId` in context; enable links:
  - `/incident?…` (graph Q5)
  - `/risk` (contextual rank if asset has finding)
  - `/safety` (if barrier conflict on unit)
  - `/identity` (if asset has state conflict)
4. Row click updates provenance drawer focal context (existing drawer behavior).
5. Reuse `DataTable.tsx` where possible; add compact density variant if needed.

**Empty states:**

- Plant with zero assets: show "No assets in catalog" (unlikely for workshop data).
- Asset with zero alerts: "No alerts indexed for this asset" — not an error.

**Performance:**

- Debounce asset search (`q` param).
- Do not fetch all 2800 alerts client-side; scope to selected plant/asset.



### Acceptance criteria (Feature 6)

- [ ] Drill-down cascade Plant → Asset → Alert works without manual ID typing.
- [ ] Selecting ALT-002783 deep-links to Incident page with context preserved.
- [ ] Asset conflict rows link to Identity page.
- [ ] Loading/disabled states on dependent tables during fetch.

---



## Feature 7: Hop-Capped Neighborhood Graph (Estate Neighborhood)



### Requirements

When view toggle is **Graph**, show a hop-capped neighborhood graph for the selected context:


| Context                  | Graph query                                 | Purpose                                                                             |
| ------------------------ | ------------------------------------------- | ----------------------------------------------------------------------------------- |
| Plant selected, no asset | Custom slice or Q4 recovery slice           | Plant + top conflict assets + recovery components                                   |
| Asset selected           | Q1 identity lineage or Q5 if alert selected | Asset ↔ aliases ↔ tags ↔ alerts                                                     |
| Alert selected (CASCADE) | Q5                                          | Timeline cascade (reuse timeline layout from Feature 1 of `Feature_Enhancement.md`) |


**UI:**

- Reuse `GraphSliceView.tsx` / `GraphVisualView.tsx` / `PanZoomSvg.tsx`.
- Embed in card (~480px height), not full-page — with **Expand** → `GraphExpandModal`.
- Legend for node types (already in `GraphVisualView`).
- Label: *"Hop-capped slice — not full estate topology (NFR-CAP)"*.

**Do not:**

- Render all 2016 assets or 2800 alerts in one graph.
- Add new graph query types without updating `graph_slice.py` and OpenAPI; prefer existing Q1/Q4/Q5 with `plant_id`/`asset_id`/`alert_id` params.



### Acceptance criteria (Feature 7)

- [ ] Neighborhood slice renders readable Q5 for PLT-10 / OT-01016 / ALT-002783 in drill-down column.
- [ ] Pan/zoom works in embedded card and expand modal.
- [ ] Graph API contract unchanged or backward-compatible only.

---



## Feature 8: Context Sync & URL State



### Requirements

1. **Bidirectional sync** with `ContextIdPickers` in `Shell.tsx`:
  - Dashboard plant click → updates pickers and vice versa.
  - Scenario rail (`ScenarioRail.tsx`) still overrides all three IDs; dashboard reflects scenario context.
2. **Optional URL params** (read on mount, write on selection):
  - `?plant=PLT-10&asset=OT-01016&alert=ALT-002783`
  - Do not break persona routes or `?persona=` param from persona views spec.
3. **Persona behavior:**
  - Home (`/`) remains default landing for `soc_analyst` and `fde`.
  - `/estate` available to SOC, FDE, Full, Executive personas.
  - Executive persona may still use `/executive`; do not remove Control Tower from nav.



### Acceptance criteria (Feature 8)

- [ ] Changing plant in topbar updates dashboard selection.
- [ ] CASCADE scenario rail click selects PLT-10 / OT-01016 / ALT-002783 in dashboard.
- [ ] URL params restore selection on page reload.

---



## Feature 9: Quick-Incidents Rail (Control Tower)



### Requirements

Enhance the existing **Quick incidents** card:

- Populate from `estateByPlant` aggregated `top_alerts` across elevated plants (max 8 rows).
- Columns: alert_id, severity, plant_id, asset_id, soc_status, process_context badge.
- UNKNOWN process_context shown with uncertainty styling (not hidden).
- Each row links to `/incident` with context applied.
- Fallback: if API empty, keep workshop default ALT-002783 link.

Retain **Open decisions** read-only footer unchanged.

### Acceptance criteria (Feature 9)

- [ ] Quick-incident list is data-driven, not hard-coded only.
- [ ] ALT-002783 appears for CASCADE estate state.
- [ ] SUPPRESSED alerts visible with SOC status label (do not hide — EVAL-007 class).

---



## Screen Layout (Target)



### S01 — Control Tower (`/`)

```
┌─ CTQ STRIP ────────────────────────────────────────────────────────────────┐
│ SLO-OT · Eval · Legacy xfail · StaleBadge                                   │
└────────────────────────────────────────────────────────────────────────────┘

┌─ ESTATE DIAGNOSTICS (14) ─────────────┐ ┌─ QUICK INCIDENTS (dynamic) ──────┐
│ (existing diag-grid)                  │ │ top alerts from elevated plants  │
└───────────────────────────────────────┘ └──────────────────────────────────┘

┌─ ESTATE SUMMARY (compact) ─────────────────────────────────────────────────┐
│ 4/18 elevated · [PLT-10] [PLT-03] …  →  Open Estate Dashboard               │
└────────────────────────────────────────────────────────────────────────────┘

┌─ OPEN DECISIONS (read-only) ──────────────────────────────────────────────┐
│ OPEN-001 · OPEN-006 · OPEN-028 · OPEN-029                                   │
└────────────────────────────────────────────────────────────────────────────┘
```



### S01b — Estate Dashboard (`/estate`)

```
┌─ KPI STRIP ────────────────────────────────────────────────────────────────┐
│ 18 plants · 4 elevated · 2016 assets · HC alerts (inventory, not risk rank)│
└────────────────────────────────────────────────────────────────────────────┘

┌─ DASHBOARD GRAPH (regional plant map) ── pan/zoom ─────────────────────────┐
│  NA          EU         APAC        LATAM                                    │
│ [PLT-01]    [PLT-02]   [PLT-03]    [PLT-04]  …                              │
└────────────────────────────────────────────────────────────────────────────┘

┌─ [Grid toggle] Plant heatmap · filters · sort ───────────────────────────────┐

┌─ DRILL-DOWN (selected plant) ───────────────────────────────────────────────┐
│ Assets │ Alerts │ Neighborhood graph (Q1/Q4/Q5)                              │
└────────────────────────────────────────────────────────────────────────────┘
```

---



## Cross-Cutting Implementation Notes



### Testing

1. Run existing suite before and after (`pytest`, `npm run build` in `apps/command_center`).
2. Do not delete XFAIL tests.
3. Add backend tests:
  - `GET /data/views/estate-by-plant` returns 18 plants.
  - PLT-10 has `elevated: true`.
  - Methodology field present.
4. Add frontend smoke tests if project has component tests; otherwise manual checklist below.



### Manual smoke test

- [ ] Open `/` → compact view; no long scroll; link to `/estate` works.
- [ ] Open `/estate` → dashboard graph shows 18 plants by region.
- [ ] Click PLT-10 on graph → drill-down loads assets/alerts.
- [ ] Neighborhood Q5 readable for CASCADE alert in drill-down.
- [ ] Quick incidents on `/` open Incident page with correct context.
- [ ] Nav shows Estate Dashboard under Home group.



### Documentation updates (minimal)

- Update `contracts/openapi_command_center.yaml` for new endpoint.
- Update `apps/command_center/SCREEN_SPECIFICATIONS.md` S01 layout section to reflect implemented heatmap + drill-down (when done).
- Update `apps/command_center/DATA_LAYER.md` if new derived index documented.
- Do **not** create additional markdown files beyond this spec unless requested.



### Out of scope

- New map/geo visualization (no lat/long in plants.csv).
- Real-time WebSocket alert streaming.
- LLM-generated estate summaries (OPEN-028).
- CVSS-only plant ranking or "top vulnerable plants" widget.
- OT execute/write surfaces, acknowledge/close alert actions.
- Cleaning data contradictions in CSVs.
- Neo4j or full-estate force-directed graph.

---



## Definition of Done

1. **Control Tower** stays compact; full interactive view lives at `/estate`.
2. **Dashboard graph** shows regional plant map with elevation signals — not CVSS-only ranking.
3. **Drill-down** on `/estate` exposes assets and alerts with deep links to Incident, Identity, Risk, Safety.
4. **Context pickers, scenario rail, and URL params** stay in sync on estate dashboard.
5. CTQ strip, diagnostics, quick incidents, open-decisions preserved on Control Tower.
6. API documented in OpenAPI; tests pass; no forbidden OT surfaces added.

---



## Suggested Implementation Order

```
1. data_layer: derived_alerts_by_plant + estate_by_plant_view()
2. api.py: GET /data/views/estate-by-plant + pytest
3. client.ts: api.estateByPlant()
4. EstateOverviewGraph.tsx: regional dashboard SVG + pan/zoom
5. EstateDashboardPage.tsx: graph hero + grid + drill-down at /estate
6. ControlTower.tsx: compact summary + link to /estate (remove heavy sections)
7. App.tsx + registry nav: /estate route
8. Context sync: AppContext + URL params + ScenarioRail
9. Quick-incidents on Control Tower
10. Manual smoke + persona regression
```

---



## Key Files

```
src/ot_command/core/data_layer.py          # derived_alerts_by_plant, estate_by_plant_view
src/ot_command/diagnostics.py              # per-plant conflict helpers (if extracted)
src/ot_command/api.py                      # GET /data/views/estate-by-plant
src/ot_command/core/graph_slice.py         # only if plant-scoped slice hints needed
contracts/openapi_command_center.yaml
tests/test_api_product.py                  # estate-by-plant tests

apps/command_center/src/pages/ControlTower.tsx       # compact S01 home
apps/command_center/src/pages/EstateDashboardPage.tsx  # S01b full interactive view
apps/command_center/src/components/EstateOverviewGraph.tsx  # dashboard regional graph
apps/command_center/src/utils/estateDashboard.ts      # shared sort/filter helpers
apps/command_center/src/api/client.ts
apps/command_center/src/context/AppContext.tsx
apps/command_center/src/components/ContextIdPickers.tsx
apps/command_center/src/components/DataTable.tsx
apps/command_center/src/components/GraphSliceView.tsx
apps/command_center/src/components/GraphVisualView.tsx
apps/command_center/src/components/GraphExpandModal.tsx
apps/command_center/src/components/ScenarioRail.tsx
apps/command_center/src/styles/global.css    # heatmap tiles, elevation badges
apps/command_center/SCREEN_SPECIFICATIONS.md
apps/command_center/UI_WIREFRAMES.md

data/reference/plants.csv
data/raw/assets.csv
data/raw/cyber_alerts.csv
```

---



## Agent Handoff Prompt (copy-paste)

> Implement per `specs/Home_Estate_Dashboard_Enhancement.md`: keep **Control Tower** (`/`) compact; build **Estate Dashboard** subpage at `/estate` with `EstateOverviewGraph` (regional dashboard SVG), heatmap grid, and drill-down. Reuse `/data/views/estate-by-plant`, list APIs, and graph slice components. No OT write surfaces. Alert counts are inventory signals — deterministic elevation rules only.

