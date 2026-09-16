# UI_WIREFRAMES — Command Center (ASCII)

**APP-00** · Control-room density · Provenance always reachable (right drawer)  
**Layout system:** 12-col grid · Left nav 56px · Context bar 48px · Main + provenance drawer 320px

---

## Global chrome

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [≡] ICS/OT Command Center    PLT-10 · OT-01016 · ALT-002783 · CASCADE-001  │
│                                      AI: [OFF|ON]   Mode: synthetic-read-only │
├────┬─────────────────────────────────────────────────────────────┬───────────┤
│Nav │ MAIN WORKSPACE                                              │ PROVENANCE│
│    │                                                             │ drawer    │
│ ●  │                                                             │ source:   │
│ ○  │                                                             │ path · id │
│ ○  │                                                             │ confidence│
│ ○  │                                                             │ freshness │
│    │                                                             │ [pin]     │
└────┴─────────────────────────────────────────────────────────────┴───────────┘
```

**Card hierarchy (global):**
1. **CTQ status strip** — SLO-OT · harness · AI mode (Control Tower + Executive)
2. **Context bar** — plant / asset / alert / scenario (incident screens)
3. **Primary evidence table or graph** — largest visual weight
4. **Secondary factors / timeline** — supporting joins
5. **Advisory packet footer** — recommendation + roles — never execute CTA
6. **Explainer** (optional, AI on) — narrow column or drawer — lowest authority

---

## Screen 1 — Risk & Resilience Control Tower (home)

```
┌─ CTQ STRIP ────────────────────────────────────────────────────────────────┐
│ SLO-OT: OK (0 execute) │ Eval: 31/31 │ AI: OFF │ Legacy xfail: 3 (contrast) │
└────────────────────────────────────────────────────────────────────────────┘

┌─ ESTATE DIAGNOSTICS (14) ─────────────┐ ┌─ QUICK INCIDENTS ────────────────┐
│ state conflicts      200              │ │ ALT-002783 HIGH  PLT-10  [open] │
│ alias collisions       5              │ │ ...                             │
│ undocumented paths   779              │ └─────────────────────────────────┘
│ telemetry bad/uncert 4094             │
│ unapproved sessions  137              │ ┌─ PLANT HEATMAP (18) ────────────┐
│ ...                                   │ │ PLT-01 ██ PLT-10 ███ ...        │
└───────────────────────────────────────┘ └─────────────────────────────────┘

┌─ OPEN DECISIONS (read-only count) ─────────────────────────────────────────┐
│ OPEN-001 Authorizer · OPEN-006 KPI · OPEN-028 model · OPEN-029 auth       │
└────────────────────────────────────────────────────────────────────────────┘
```

API: `GET /diagnostics`, `GET /ops/slo`

---

## Screen 5 — Contextual Risk Workbench

```
┌─ RANK MODE: [Contextual ●] [CVSS-only (warn)] ─────────────────────────────┐
│ # │ Finding    │ Asset     │ CVSS │ Reach │ Crit │ Safety │ Recovery │ Score│
│ 1 │ VUL-00098  │ OT-01016  │ 8.7  │ YES   │ HIGH │ bypass │ weak     │ ▲    │
│ 2 │ VUL-00706  │ OT-00654  │ 9.8  │ NO    │ LOW  │ —      │ —        │      │
└────────────────────────────────────────────────────────────────────────────┘
┌─ FACTOR BREAKDOWN (selected row) ──────────────────────────────────────────┐
│ reachability +35 │ criticality +40 │ safety +8 │ recovery +8 │ cvss×2     │
└────────────────────────────────────────────────────────────────────────────┘
```

Anti-pattern blocked: default sort by CVSS descending (APP-AT-002).

---

## Screen 9 — Incident Context Graph (CASCADE)

```
┌─ TIMELINE ─────────────────────────────────────────────────────────────────┐
│ 08:01 advisory │ 08:24 vendor session │ 08:38 bypass │ 08:47 SOC │ 08:50 PE│
└────────────────────────────────────────────────────────────────────────────┘

┌─ GRAPH (Q5 slice) ────────────────────────┐ ┌─ DISSENT PANEL ────────────────┐
│  [Session]─── OT-01016 ─── [Unit MIN_LOAD]│ │ SOC 08:47: isolate request   │
│       │              │                    │ │ PE  08:50: destabilize risk  │
│       └── [Barrier BYPASSED]               │ │ Handover: UNTRUSTED (email)  │
│  hop cap: 8 / 8                            │ └──────────────────────────────┘
└───────────────────────────────────────────┘
```

Scenario counts (37 controllers) shown with badge **SCENARIO — not census**.

---

## Screen 11 — Authority Gate / Recommendation (critical)

```
┌─ RECOMMENDATION PACKET ────────────────────────────────────────────────────┐
│ Status: DO_NOT_ISOLATE          execute: false          authorizable: false  │
├────────────────────────────────────────────────────────────────────────────┤
│ safe_state: MIN_LOAD          process_context: UNKNOWN                       │
│ required roles: Process Engineer · Safety/SIS Owner · VP Operations        │
│ missing_fields: [process_context]                                            │
├────────────────────────────────────────────────────────────────────────────┤
│ EVIDENCE TABLE                                                             │
│ source_path                          │ record_id   │ field           │ value │
│ data/raw/safety_barriers.csv         │ PLT-10-...  │ state           │ BYP.. │
├────────────────────────────────────────────────────────────────────────────┤
│ [ Export packet ]  [ View trace ]     NO [ Execute isolation ]  NO [ Authorize in app ] │
└────────────────────────────────────────────────────────────────────────────┘
```

**Primary actions:** Export · View trace · Copy war-room summary  
**Absent by design:** Execute Isolation · Write PLC · Modify SIS · One-click Authorize

---

## Screen 2 — Identity Reconciliation

```
┌─ ALIAS COLLISION: PLT-01-DCS_CONTROLLER-105 ──────────────────────────────┐
│ confidence: 0.4   merged: false   cmdb_winner: false                       │
├──────────────────┬──────────────────┬──────────────────────────────────────┤
│ OT-00012         │ OT-00033         │ sources: PASSIVE                     │
│ reg: ACTIVE      │ reg: ACTIVE      │ evidence → asset_aliases.csv         │
│ obs: OFFLINE     │ obs: UNSEEN      │                                      │
└──────────────────┴──────────────────┴──────────────────────────────────────┘
```

No “Merge” or “Pick CMDB winner” button.

---

## Screen 10 — Hybrid Retrieval Evidence (drawer / panel)

```
┌─ RETRIEVAL CHANNELS ───────────────────────────────────────────────────────┐
│ [STRUCTURED ●] [GRAPH] [VECTOR off] [POLICY] [MEMORY]                       │
├────────────────────────────────────────────────────────────────────────────┤
│ STRUCTURED: assets.csv row OT-01016                                        │
│ GRAPH: Q3 safety-cyber join                                                │
│ POLICY: ACTION_TIERS recommend=tier1                                       │
│ VECTOR: (disabled) — untrusted notes only when enabled                     │
│ MEMORY: decision trace dec-abc123                                          │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Screen 15 — Executive Brief

```
┌─ POSTURE SUMMARY ──────────────────────────────────────────────────────────┐
│ Plants: 18 │ Assets: 2016 │ Harness: PASS │ Assurance: ENH-09 complete    │
├────────────────────────────────────────────────────────────────────────────┤
│ CTQ-0  zero execute  │ CTQ-ISO drafts gated │ CTQ-REC ≠ backup flag      │
├────────────────────────────────────────────────────────────────────────────┤
│ RESIDUAL RISK (workshop)                                                   │
│ OPEN-RISK-05 human wrong authorize │ OPEN-RISK-11 UI isolate pressure     │
└────────────────────────────────────────────────────────────────────────────┘
                    [ Drill to KPI ]  [ Drill to Control Tower ]
```

No execute controls. Read-only drill-down links only.

---

## Dashboard layout — analyst default (multi-panel)

```
┌────────────┬────────────────────────────┬──────────────┐
│ Nav        │ Control Tower / Incident   │ Provenance   │
│            ├────────────────────────────┤              │
│            │ Risk strip (top 5)         │ Evidence pin │
│            ├─────────────┬──────────────┤              │
│            │ Safety      │ Recovery     │              │
│            │ mini-board  │ mini-graph   │              │
│            └─────────────┴──────────────┘              │
│            │ Recommendation footer (advisory)         │
└────────────┴────────────────────────────┴──────────────┘
```

Density over whitespace. Tables over prose. Side panel over modal chat.

---

## AI-disabled wireframe note

When AI toggle OFF, remove explainer column entirely — main workspace expands. Same tables/graphs remain. Banner: “Deterministic engines — explainer unavailable (ADR-12).”
