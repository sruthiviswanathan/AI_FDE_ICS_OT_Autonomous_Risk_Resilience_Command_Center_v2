# App changes so the demo can show AI ON and Moonshot

**Live today:** [https://ics-ot-command-center.onrender.com/estate?persona=full](https://ics-ot-command-center.onrender.com/estate?persona=full)

**Verdict:** the Render app does **not** have AI OFF / ON / MOONSHOT. Confirmed on `prd-v2`:

| Surface | What exists | What is missing |
|---|---|---|
| Header (`apps/command_center/src/layout/Shell.tsx`) | Persona, scenario rail, synthetic-read-only, SLO-OT | No AI three-state toggle |
| App state (`src/context/AppContext.tsx`) | plant / asset / alert / scenario / persona | No `aiMode` |
| API (`/openapi.json` v3.0.0) | estate, risk, recommend, scenarios, `/agent/workflow/demo` | No `/forecasts`, no AI mode |
| `/simulation` | Load injects + run EVAL harness | Not a twin what-if lab |
| `/recommend` | Draft packet, `execute=false` | No Moonshot panel, no advisory caption |

`/agent/workflow/demo` is a **deterministic workflow envelope** for EVAL-016. It is not Moonshot.

Do **not** add Execute Isolation, PLC/SIS writes, or an LLM that can change the packet. Engines stay authoritative.

---

## What the demo must be able to click

After deploy, these URLs should work:

| Mode | URL |
|---|---|
| AI OFF (default) | `https://ics-ot-command-center.onrender.com/estate?persona=full&ai=off` |
| AI ON | `…/estate?persona=full&scenario=cascade_001&ai=on` |
| Moonshot | `…/estate?persona=full&scenario=cascade_001&ai=moonshot` |
| Twin lab | `…/simulation?persona=full&scenario=cascade_001&ai=moonshot` |

Header control: **AI OFF | ON | MOONSHOT** (segmented). Persist in the query string `ai=`. `ai_outage` scenario **forces OFF** and disables the control.

| Mode | Visible | Hidden |
|---|---|---|
| **OFF** | Estate, engines, tables, packet | Narrative, forecast list |
| **ON** | Short cited caption of the **current** plant/alert slice | Forecast list |
| **MOONSHOT** | Caption **plus** ranked forecast list + banner `ADVISORY FORECAST — NOT A CONTROL ACTION` | Any execute / authorize |

Auditor / executive: Moonshot **off** by default; Full / FDE / SOC can turn it on.

---

## Minimum build (demo-blocking)

Do this first. Deterministic. No model required for Moonshot numbers.

### 1. API — `GET /forecasts`

Query: `plant_id` (required), `asset_id?`, `alert_id?`, `as_of=workshop-static`

Return:

```json
{
  "mode": "moonshot",
  "banner": "ADVISORY FORECAST — NOT A CONTROL ACTION",
  "execute": false,
  "plant_id": "PLT-10",
  "forecasts": [
    {
      "forecast_id": "FC-PLT10-01",
      "plant_id": "PLT-10",
      "asset_id": "OT-01016",
      "category": "VENDOR_SESSION_PLUS_WRITE_ALERT",
      "layer": "CYBER",
      "horizon_days": 7,
      "confidence": "MEDIUM",
      "recommended_action": "ABSTAIN",
      "required_role": "PROCESS_ENGINEER",
      "action_tier": 1,
      "twin_scenario_id": "cascade_001",
      "evidence_ids": ["ALT-002783", "RA-00025", "PLT-10-SAFE-07"],
      "missing_evidence": ["process_context"],
      "abstain_reason": "process_context=UNKNOWN; barrier BYPASSED unauthorized; safe_state=MIN_LOAD"
    }
  ]
}
```

**Engine (no LLM):** join the same CSVs already used by diagnostics / safety / recovery / sessions.

| category | Red if | Demo seed example |
|---|---|---|
| `VENDOR_SESSION_PLUS_WRITE_ALERT` | HIGH write-like alert + unapproved session on plant | CASCADE PLT-10 |
| `SAFETY_BYPASS_AGING` | SIS_TRIP/PERMISSIVE `state≠ACTIVE` | `PLT-10-SAFE-07` |
| `RESTORE_TEST_ROT` | backup CURRENT and restore-test >90d | PLT-01 IDENTITY 360d |
| `IDENTITY_CONFLICT_REACHABLE` | ACTIVE/OFFLINE or RETIRED/ONLINE + OPEN reachable vuln | OT-00528 |
| `UNDOCUMENTED_PATH_ON_CRITICAL_UNIT` | live undocumented edge on HIGH plant | estate undoc paths |
| `UNKNOWN_PROCESS_CONTEXT` | HIGH/CRITICAL alert, context UNKNOWN | ALT-002783 → **ABSTAIN only** |

**Hard rules**

- UNKNOWN process_context → `ABSTAIN` or `MONITOR`, never isolate.
- Unreachable CVSS ≥9.0 must not rank above reachable OPEN on CRITICAL/HIGH (same anti-CVSS as `/risk/contextual`).
- `recommended_action` ∈ `MONITOR | RECOMMEND_CONTAINMENT_REVIEW | ABSTAIN`.
- `execute` always `false`. No `isolate_endpoint` as an executable.

Also add `GET /explain?plant_id=&asset_id=&alert_id=` for **AI ON**: 4–8 sentence caption, citations (`evidence_ids`, source files). **v1 may be a template** filled from the same joins. LLM optional later; if it disagrees with engines, show both and keep the engine packet.

### 2. Frontend — toggle + panels

| File | Change |
|---|---|
| `src/context/AppContext.tsx` | `aiMode: "off" \| "on" \| "moonshot"`. Sync `?ai=`. If `scenario === "ai_outage"` → force `"off"`. |
| `src/layout/Shell.tsx` | Header control next to Persona. Badge `AI-DISABLED` / `AI-ON` / `MOONSHOT`. |
| `src/api/client.ts` | `forecasts()`, `explain()`. |
| new `src/components/AiCaption.tsx` | Shown when `aiMode !== "off"`. |
| new `src/components/MoonshotPanel.tsx` | Banner + table of forecasts. Button **Load in twin** → `/simulation?scenario={twin_scenario_id}&ai=moonshot`. **No Execute.** |
| `src/pages/EstateDashboardPage.tsx` | Caption + Moonshot for selected plant. |
| `src/pages/RecommendPage.tsx` | Same panel **below** the packet. Packet remains the engine. |
| `src/personas/registry.ts` | Hide Moonshot for `executive` default; allow on `full` / `fde` / `soc_analyst`. |

**AI outage:** tables, estate pills, and draft packet still render. Only caption + forecast list hide.

### 3. Twin slice (so “rehearse” is clickable)

Extend `/simulation` (or `GET /twin/preview`):

- Input: `scenario_id` or `forecast_id`, `proposed_action`: `do_nothing | isolate_preview | increase_logging | open_ticket`
- Output: `lab_result`: `CONSEQUENCE_SKETCHED | UNSAFE_ISOLATION | INSUFFICIENT_EVIDENCE | NO_MATERIAL_CHANGE`
- CASCADE isolate_preview → `UNSAFE_ISOLATION` (08:50 MIN_LOAD + bypass)
- Button: **Create approval packet** → existing `POST /recommend` (still `execute=false`)
- Never: write PLC, modify SIS, setpoint, interlock, “apply to plant”

---

## Demo click path once shipped

1. Open [estate Full, AI off](https://ics-ot-command-center.onrender.com/estate?persona=full&ai=off) — 18/18, engines only.  
2. Header → **AI ON** — caption appears; pills unchanged.  
3. Load **CASCADE-001** → header **MOONSHOT** — banner + hypotheses; ALT-002783 UNKNOWN abstains.  
4. **Load in twin** → Simulation isolate preview = unsafe.  
5. Recommendation Gate still **DO_NOT_ISOLATE**.  
6. Scenario **AI outage** — caption gone, map and packet remain.

---

## Out of scope for this demo patch

- Calling a foundation model as the ranker  
- Auto-promote after a green lab run  
- Physics / SIS-certified twin  
- Closed-loop OT  

Template captions + deterministic forecasts are enough to click AI ON and Moonshot on stage.
