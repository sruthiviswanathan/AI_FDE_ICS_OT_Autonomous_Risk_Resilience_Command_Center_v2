# Estate Graphical Interactive View — Implementation Prompt

## Context

Brownfield ICS/OT advisory Command Center (`apps/command_center/`, `src/ot_command/`). Workshop-static CSV under `data/`. Read `AGENTS.md`, `.cursor/rules/sdd.mdc`, `.cursor/rules/ot-fde.mdc` before coding.

**Parent spec:** `specs/Home_Estate_Dashboard_Enhancement.md` (S01b `/estate`).

**Motivation:** Executive and SOC users need an **interactive graphical estate view** as the primary `/estate` experience — not a flat grid alone. Eighteen plant nodes only; **never** 2,016 asset sprites.

---

## Goal

Build an **interactive regional estate map** on `/estate` that:

1. Renders **18 plant nodes** grouped by region (NA · EU · APAC · LATAM · MEA).
2. **Sizes** nodes by switchable metric: **criticality** (default) or **asset count**.
3. **Colors** nodes by switchable posture layer; **worst layer wins** for Composite:
   - **Cyber** → `posture_layers.cyber_exposure`
   - **Safety** → `posture_layers.safety_posture`
   - **Recovery** → `posture_layers.recovery_credibility`
   - **Identity disagreement** → `posture_layers.evidence_quality` (registered vs observed conflicts)
   - **Composite** → `signals.posture_composite` (any red blocks green)
4. **Click plant** → set global context (`plantId`), scroll to **asset table drill-down** (existing panel), not inline 2,016 nodes.
5. **Drill further** via existing screens: Incident, Risk, Safety, Identity, Recovery, Telemetry.
6. Surfaces **estate diagnostics** from `GET /diagnostics` (200 state conflicts, 61 degraded barriers, 779 live undocumented paths, restore-test / recovery gaps).

---

## Hard constraints

- Read-only advisory — no OT write / isolate-execute surfaces.
- **NFR-CAP:** no whole-estate force-directed graph; no 2,016 asset nodes; hop-capped graph slices unchanged (≤ 8).
- Do not reopen SDD-09; do not change `legacy_*`; do not clean `data/` contradictions.
- **cyber ≠ operational ≠ safety ≠ recovery** — color is layered posture, not CVSS-only rank.
- Alert counts are **inventory signals**, not contextual risk rank.
- Reuse existing APIs and components where possible.

---

## Data sources (already implemented)

| Need | API / field |
|------|-------------|
| 18 plants + counts | `GET /data/views/estate-by-plant` → `plants[]` |
| Five posture layers | `plants[].posture_layers`, `signals.posture_composite` |
| Plant metadata | `region`, `criticality`, `counts.assets`, `counts.asset_state_conflicts`, … |
| Estate diagnostics | `GET /diagnostics` |
| Asset drill-down | `GET /plants/{plant_id}/assets` |
| Alert drill-down | `GET /assets/{asset_id}/alerts` |
| Neighborhood slice | `GET /graph/slice?query=Q1\|Q4\|Q5&plant_id=&asset_id=` |

**Do not** add Neo4j or new write paths. Optional BE enrichment (per-plant undocumented path counts) is out of scope unless trivially derived from existing `network_edges.csv` joins in `data_layer.py`.

---

## UI specification

### Route & persona

- **Route:** `/estate` (S01b Estate Dashboard)
- **Personas:** executive (primary audience), SOC, FDE, full
- **Default view:** `[Graph ●] [Grid]` toggle — Graph is default on load

### Layout (top → bottom)

1. **Page header** + link back to Control Tower
2. **Estate diagnostics strip** — highlight workshop anchors from `/diagnostics`:
   - `asset_state_conflicts` (~200)
   - `safety_bypassed_or_degraded` (~61)
   - `undocumented_network_paths` (~779 live undocumented)
   - `recovery_stale_or_unknown_backup` / restore-test age signals
   - Tooltip: estate-wide inventory signals, not operational risk rank
3. **Graph controls**
   - **Color by:** Composite | Cyber | Safety | Recovery | Identity
   - **Size by:** Criticality | Asset count
   - **Region filter** (optional): All · NA · EU · APAC · LATAM · MEA
4. **Interactive graph panel** (`EstateOverviewGraph.tsx`)
   - SVG + `PanZoomSvg` (pan/zoom; `data-panzoom-interactive` on nodes)
   - Regional column headers
   - Plant nodes: circle or rounded card; label `plant_id`; sublabel asset count
   - Fill = layer status color (ok / amber / red)
   - Stroke ring on selected plant
   - Hover tooltip: layer reason, conflicts, HC alerts (inventory)
   - Click → `selectPlant()` → context sync + scroll to drill-down
5. **Inventory summary** (compact table — existing `EstateInventorySummary`)
6. **Grid view** (existing heatmap tiles — when Grid toggle selected)
7. **Drill-down panel** (existing: assets table, alerts, hop-capped graph slice)

### Color encoding

| Status | Color | Meaning |
|--------|-------|---------|
| `ok` | Green | Layer clear |
| `amber` | Amber | Caution / unresolved |
| `red` | Red | At risk; blocks composite OK |

Composite mode uses `signals.posture_composite`. Single-layer modes read `posture_layers[layerKey].status`.

### Size encoding

| Mode | Rule |
|------|------|
| Criticality | HIGH → largest radius; MEDIUM → mid; other → min |
| Asset count | Linear scale `counts.assets` with min/max clamp across 18 plants |

---

## Components to create / modify

| File | Action |
|------|--------|
| `apps/command_center/src/components/EstateOverviewGraph.tsx` | **New** — interactive SVG estate map |
| `apps/command_center/src/components/EstateDiagnosticsStrip.tsx` | **New** — diagnostics KPI strip |
| `apps/command_center/src/utils/estateGraphLayout.ts` | **New** — regional node positions |
| `apps/command_center/src/pages/EstateDashboardPage.tsx` | Graph hero, view toggle, diagnostics fetch |
| `apps/command_center/src/utils/estateDashboard.ts` | Add `MEA` to region list |
| `apps/command_center/src/styles/global.css` | Graph panel, nodes, controls |
| `apps/command_center/SCREEN_SPECIFICATIONS.md` | Document graph as primary view |

**Reuse:** `PanZoomSvg.tsx`, `PlantPostureBadges.tsx`, `PostureQuickLegend`, `EstateInventorySummary`, drill-down block, `api.estateByPlant()`, `api.diagnostics()`.

---

## Acceptance criteria

- [ ] `/estate` opens with **interactive graph** showing all **18 plants** in regional groups (including MEA).
- [ ] Color switch changes node fill across Cyber / Safety / Recovery / Identity / Composite.
- [ ] Size switch changes node radius (criticality vs asset count).
- [ ] Click PLT-10 selects plant, updates shell context, scrolls to asset table (not 2,016 sprites).
- [ ] Diagnostics strip shows estate anchors from `/diagnostics` (conflicts, barriers, undocumented paths, recovery).
- [ ] Pan/zoom works; plant clicks are not swallowed by pan handler.
- [ ] Grid view remains available via toggle.
- [ ] No new OT write routes; existing pytest passes.

---

## Implementation order

1. `estateGraphLayout.ts` — pure layout from `PlantEstateRow[]`
2. `EstateOverviewGraph.tsx` — SVG nodes + controls props
3. `EstateDiagnosticsStrip.tsx`
4. Wire into `EstateDashboardPage.tsx` with `[Graph | Grid]` toggle
5. CSS + SCREEN_SPECIFICATIONS update
6. Manual test: PLT-01 vs PLT-10 color change; click → drill-down

---

## Copy-paste agent prompt

> Implement the **Estate Graphical Interactive View** per `specs/Estate_Graphical_Interactive_View.md`. Add `EstateOverviewGraph.tsx` as the default primary view on `/estate`: 18 plant nodes in regional columns, pan/zoom via `PanZoomSvg`, color by switchable posture layer (Composite worst-layer-wins), size by criticality or asset count. Show `EstateDiagnosticsStrip` from `GET /diagnostics`. Click plant → existing asset drill-down (no asset sprites). Keep grid as toggle. Reuse `GET /data/views/estate-by-plant` posture layers. No OT writes; no whole-estate force graph.
