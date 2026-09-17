# Enhanced Prompt: OT Command Center — Provenance Graph, Cascading ID Pickers, AI Explainer UX

## Context

You are working on the **AI FDE ICS/OT Autonomous Risk Resilience Command Center v2** — a brownfield OT advisory application (not a greenfield rewrite). The React frontend lives in `apps/command_center/`; the FastAPI backend in `src/ot_command/`. Data is workshop-static CSV under `data/`.

**Read first:**
- `AGENTS.md`
- `.cursor/rules/sdd.mdc` and `.cursor/rules/ot-fde.mdc`
- `apps/command_center/SCREEN_SPECIFICATIONS.md`
- `contracts/openapi_command_center.yaml`

**Hard constraints (do not violate):**
- Do not reopen SDD-09 (Option A deterministic engines + Option B optional explainer port; Option C rejected).
- Do not change `legacy_*` behavior, delete XFAIL tests, or clean `data/` contradictions.
- Do not add OT write routes, isolate-execute surfaces, SIS bypass, or PLC write capabilities.
- Do not invent ADRs, legal class, named Authorizers, KPI thresholds, or ACTION_TIERS verbs.
- Untraced modules are out of scope (`traceability/TRACEABILITY.csv`).
- UNKNOWN permission is not permission.
- Evidence first: never infer highest CVSS = highest operational risk.

---

## Task Overview

Implement three related UX improvements:

| # | Feature | Priority |
|---|---------|----------|
| 1 | Fix provenance visual graph readability | High |
| 2 | Replace Plant/Asset/Alert text inputs with cascading dropdowns backed by BE APIs | High |
| 3 | Fix or honestly rephrase AI Explainer UI (no LLM misrepresentation) | High |

Work incrementally. Preserve existing deterministic engine behavior. Add tests where behavior changes.

---

## Feature 1: Provenance Visual Graph — Make It Readable

### Problem

The provenance graph (GRAPH channel in the drawer + graph pages) is hard to read and understand. Root causes identified in code:

| Issue | Location |
|-------|----------|
| Custom inline SVG with hub-and-spoke layout, no collision detection | `apps/command_center/src/components/GraphVisualView.tsx`, `apps/command_center/src/utils/graphLayout.ts` |
| Drawer width ~300px vs SVG width 520px | `apps/command_center/src/layout/ProvenanceDrawer.tsx`, `global.css` |
| Labels truncated to 14 chars; drawer labels at 9px | `GraphVisualView.tsx`, `global.css` |
| Q5 (incident cascade) uses network layout instead of timeline-ordered layout | `graphLayout.ts` |
| Incident/Safety pages default to list view, not visual | `IncidentPage.tsx`, `SafetyPage.tsx` |
| No pan/zoom; dense graphs require awkward scrolling | `GraphVisualView.tsx` |

Data source: `GET /graph/slice?query=Q1|Q2|Q3|Q4|Q5` via `api.graphSlice()` in `apps/command_center/src/api/client.ts`. Backend builder: `src/ot_command/core/graph_slice.py`.

### Requirements

**Layout & rendering**
1. Make Q5 (provenance drawer default) use a **timeline-ordered horizontal layout** aligned with `scenario_markers.timeline` when present — left-to-right cascade: vendor session → barrier → isolate → destabilize (or whatever markers the slice returns).
2. Apply readable layout improvements to Q3 and Q4 network graphs (reduce edge crossings; consider dagre/elkjs **only if** it fits existing Vite/React stack without heavy deps — prefer improving `graphLayout.ts` first).
3. Keep Q2 row-per-path layout (already readable); do not regress it.
4. Add **node type legend** (Plant, Asset, Alert, Barrier, Session, etc.) with color/shape coding consistent with existing CSS variables in `global.css`.
5. Show **full node IDs on hover** (tooltip) and on click (existing node-details path in `GraphSliceView.tsx`).
6. Add **basic pan/zoom** (SVG `viewBox` + wheel/drag, or a lightweight wrapper) for graphs with >6 nodes.
7. Fix drawer sizing: either widen drawer when GRAPH channel is active, or scale SVG to fit ~280px without horizontal scroll.

**UX defaults**
8. Enable visual graph as default (with toggle to list) on `IncidentPage` and `SafetyPage` — match wireframe intent in `apps/command_center/UI_WIREFRAMES.md`.
9. Keep provenance drawer defaulting to visual for GRAPH channel.

**Node/edge clarity**
10. Label edges when type is safety-critical (`PROTECTS`, `ALERT_ON`, `SESSION_ON`, `RECOVERY_FOR`) even if only one edge type exists.
11. Visually distinguish `documented: false` edges (Q2 undocumented paths) per existing `undocumented_total` semantics.
12. Do not dump whole-graph views — respect hop_cap ≤ 8 (NFR-CAP).

### Acceptance criteria (Feature 1)

- [ ] Operator can identify the focal asset, alert, and cascade sequence in Q5 without scrolling horizontally in the provenance drawer.
- [ ] Node labels are legible at normal zoom; full IDs available on hover.
- [ ] Incident page shows visual graph by default with list toggle.
- [ ] Q2 process graph layout unchanged or improved.
- [ ] No new OT action controls introduced.
- [ ] Existing graph slice API contract preserved (or OpenAPI updated with backward-compatible additions only).

### Key files

```
apps/command_center/src/components/GraphVisualView.tsx
apps/command_center/src/components/GraphSliceView.tsx
apps/command_center/src/utils/graphLayout.ts
apps/command_center/src/layout/ProvenanceDrawer.tsx
apps/command_center/src/pages/IncidentPage.tsx
apps/command_center/src/pages/SafetyPage.tsx
apps/command_center/src/styles/global.css
src/ot_command/core/graph_slice.py  (only if BE layout hints needed)
contracts/openapi_command_center.yaml
```

---

## Feature 2: Cascading Plant / Asset / Alert Dropdowns

### Problem

Plant ID, Asset ID, and Alert ID are free-text `<input>` fields in:
- `apps/command_center/src/layout/Shell.tsx` (global context bar)
- `apps/command_center/src/components/PageLookup.tsx` (page-level lookup)

Defaults are hard-coded in `AppContext.tsx`: `PLT-10`, `OT-01016`, `ALT-002783`.

**No list APIs exist today.** Only single-ID lookups and filter params on existing endpoints.

### Data model (CSV sources)

| Entity | File | PK | Count | FK |
|--------|------|----|-------|-----|
| Plant | `data/reference/plants.csv` | `plant_id` | 18 | — |
| Asset | `data/raw/assets.csv` | `asset_id` | 2016 | `plant_id` |
| Alert | `data/raw/cyber_alerts.csv` | `alert_id` | 2800 | `asset_id`, `plant_id` |

Relationship: **Plant → Asset → Alert**

### Backend requirements (implement if missing)

Add FastAPI endpoints in `src/ot_command/api.py` and document in `contracts/openapi_command_center.yaml`:

```
GET /plants
  → [{ plant_id, region, country, plant_type, criticality, ... }]
  Pagination: not required (18 plants); sort by plant_id.

GET /plants/{plant_id}/assets
  Query params: limit (default 100, max 500), q (optional search on asset_id prefix)
  → [{ asset_id, asset_type, zone, criticality, registered_state, ... }]
  404 if plant_id unknown.

GET /assets/{asset_id}/alerts
  Query params: limit (default 50, max 200), severity (optional filter)
  → [{ alert_id, type, severity, timestamp, process_context, plant_id, ... }]
  404 if asset_id unknown.
```

**Implementation guidance:**
- Add `load_plants()` to `src/ot_command/core/data_layer.py` (plants.csv is not currently in `CANONICAL_SOURCES`).
- Reuse `data_layer.derived_assets_by_id()` and alert indexing pattern from `containment.py` (`_alerts_by_id()`).
- Use `repository.rows()` for CSV reads.
- Cache indexes at module level (match existing patterns).
- Return empty arrays (not 404) for valid plant with zero assets.
- Do not modify CSV data files.

Add corresponding client methods in `apps/command_center/src/api/client.ts`.

### Frontend requirements

Replace text inputs with **`<select>` dropdowns** (or accessible combobox if search is needed for 2016 assets):

1. **On mount:** fetch `GET /plants` → populate Plant dropdown.
2. **On plant change:** fetch `GET /plants/{plant_id}/assets` → populate Asset dropdown; reset Asset and Alert to first valid option or empty; update `AppContext`.
3. **On asset change:** fetch `GET /assets/{asset_id}/alerts` → populate Alert dropdown; reset Alert; update `AppContext`.
4. **Cascade invalidation:** changing plant clears asset/alert until new lists load; show loading/disabled state on dependent dropdowns.
5. **Preserve context flow:** selected IDs must continue to drive existing API calls (`graphSlice`, `recommend`, `safetyConflicts`, `recovery`, `identity`).
6. **Apply in both** `Shell.tsx` and `PageLookup.tsx` — extract shared component if needed (e.g. `ContextIdPickers.tsx`).
7. **PageLookup field visibility:** respect existing `fields` prop (some pages hide alert or asset).
8. **Scenario rail compatibility:** when scenario buttons set context IDs (`ScenarioRail.tsx`), dropdowns must reflect the new values and re-fetch dependent lists.
9. **Error states:** show inline error if catalog fetch fails; do not silently fall back to stale IDs without indication.

**Optional (nice-to-have):** searchable combobox for assets within a plant (2016 assets per plant varies). Plain `<select>` acceptable if grouped/labeled clearly.

### Acceptance criteria (Feature 2)

- [ ] All three IDs selectable from dropdowns populated from BE APIs.
- [ ] Selecting a plant filters assets; selecting an asset filters alerts.
- [ ] Global context bar and page lookup bars behave consistently.
- [ ] Scenario rail still works and updates dropdowns.
- [ ] OpenAPI spec updated; endpoints return correct counts for known plants (e.g. PLT-10).
- [ ] No free-text ID entry unless explicitly kept as advanced fallback (document if retained).

### Key files

```
src/ot_command/api.py
src/ot_command/core/data_layer.py
src/ot_command/core/containment.py  (alert index reuse)
contracts/openapi_command_center.yaml
apps/command_center/src/api/client.ts
apps/command_center/src/layout/Shell.tsx
apps/command_center/src/components/PageLookup.tsx
apps/command_center/src/context/AppContext.tsx
apps/command_center/src/components/ScenarioRail.tsx
data/reference/plants.csv
data/raw/assets.csv
data/raw/cyber_alerts.csv
```

---

## Feature 3: AI Explainer — Fix or Rephrase (No Misleading UX)

### Problem

The "AI Explainer" appears broken because **no LLM is connected**. Current state:

| Layer | Reality |
|-------|---------|
| Backend | Deterministic rule engines only (`agent.py`, `containment.py`, etc.). `MODEL_PIN.provider = "none"`. |
| Explainer port | Stub: `explainer: null` or `{"status": "optional_off_by_default"}` — no narrative generation. |
| Frontend | Header "AI" toggle (`Shell.tsx`) is **client-only** — not synced with backend `AI_ENABLED` env. |
| UI when "AI ON" | `ProvenanceDrawer.tsx` shows "Optional explainer" card with static disclaimer — **no actual content**. |
| Spec | SDD-09 Option B = reserved port (ADR-13). OPEN-028 = no model in Repo 1.0. ADR-12 = AI-disabled must still show tables. |

**Do NOT implement a live LLM integration in this task** unless explicitly scoped and traced. The fix is honest UX alignment.

### Requirements

**Option A (preferred — rephrase, no LLM):**

1. Rename/relabel UI to reflect **deterministic advisory engines**, not "AI Explainer":
   - Header toggle: **"Advisory narrative"** → Off / On (or keep "AI" with persistent subtitle).
   - Subtitle (always visible near toggle): *"Deterministic engines active · Narrative layer not connected (OPEN-028)"*
2. When toggle is **Off** (default):
   - Copy: *"Deterministic advisory only — ranks, recovery, and draft packets from rule engines. No narrative layer (ADR-12)."*
3. When toggle is **On** (port reserved, no model):
   - Do **not** show an empty "explainer" card implying AI is working.
   - Show: *"Narrative port reserved — not connected. Tables and draft packets below are authoritative. Engines do not require a model."*
   - Optionally surface backend `explainer.status` from `/recommend` or `/health` if useful.
4. Sync frontend toggle with backend state:
   - Read `ai_enabled` from `GET /health` on load.
   - If user toggles ON but backend reports `ai_enabled: false`, show clear banner: *"Narrative unavailable — showing deterministic tables only (EVAL-016)."*
5. Update `RecommendPage.tsx` footer/loading copy to emphasize deterministic workflow (already partially correct).
6. Update `scenario_bindings.json` labels if "AI OFF" badge is misleading — clarify it means narrative port off, engines still on.
7. Align copy with `UI_WIREFRAMES.md` and ADR-12/13 language.

**Option B (only if explicitly requested and traced):**
- Wire Option B explainer port with a stub that renders deterministic summary bullets from existing `/recommend` packet fields — **still not an LLM**, label as *"Evidence summary (deterministic)"*.

### Forbidden

- Do not imply live AI/LLM inference when none exists.
- Do not hide deterministic tables when "AI" toggle is off (ADR-12 / EVAL-016).
- Do not mutate ACTION_TIERS, IsolationRecommendation, or RecoveryReady based on explainer output (ADR-13).
- Do not add token metering UI showing fake usage.

### Acceptance criteria (Feature 3)

- [ ] No UI element suggests an LLM is generating explanations when it is not.
- [ ] Toggle state reflects backend `ai_enabled` from `/health`.
- [ ] When narrative port is off/unconnected, deterministic engines and tables remain fully visible.
- [ ] Provenance drawer no longer shows a misleading empty "Optional explainer" panel.
- [ ] Copy references ADR-12/OPEN-028 where appropriate.

### Key files

```
apps/command_center/src/layout/Shell.tsx
apps/command_center/src/layout/ProvenanceDrawer.tsx
apps/command_center/src/pages/RecommendPage.tsx
apps/command_center/src/context/AppContext.tsx
apps/command_center/scenario_bindings.json
src/ot_command/core/agent.py
src/ot_command/core/ai_config.py
src/ot_command/api.py  (/health)
adrs/ADR-12-ai-disabled.md
adrs/ADR-13-model-port.md
specs/09_options.md
```

---

## Cross-Cutting Implementation Notes

### Testing

1. Run existing test suite before and after (`pytest`, frontend build).
2. Do not delete XFAIL tests.
3. Add backend tests for new list endpoints (known plant returns assets; unknown plant 404).
4. Manual smoke test:
   - Select plant from dropdown → assets populate → alerts populate.
   - Open provenance drawer (GRAPH) → Q5 graph readable with timeline flow.
   - Toggle advisory narrative → copy accurate; tables still visible.
   - Run scenario rail → IDs cascade correctly.

### Documentation updates (minimal)

- Update `contracts/openapi_command_center.yaml` for new endpoints.
- Update `apps/command_center/APP_FLOW.md` only if navigation/context behavior changes materially.
- Do **not** create new markdown files unless requested.

### Out of scope

- LLM provider integration (OPEN-028).
- New ADRs or KPI thresholds.
- Legacy engine changes.
- Cleaning data contradictions.
- OT execute/write surfaces.
- Decorative knowledge graph beyond hop-capped slices.

---

## Definition of Done

All three features complete when:

1. **Provenance graph** is legible in the drawer and incident page without expert knowledge of the layout algorithm.
2. **Plant/Asset/Alert** are cascading dropdowns fed by new BE list APIs; no manual ID typing required for normal workshop flows.
3. **AI Explainer** UI honestly describes deterministic engines and disconnected narrative port — no user believes a live AI is explaining when it is not.
4. Existing eval constraints pass; no forbidden OT surfaces added.
5. OpenAPI contract reflects new endpoints.

---

## Suggested Implementation Order

```
1. BE list APIs (plants → assets → alerts)     ← unblocks Feature 2
2. FE cascading dropdowns in Shell + PageLookup
3. Graph layout/readability fixes (Q5 timeline layout first)
4. AI Explainer UX rephrase + health sync
5. Smoke test + OpenAPI update
```

---

