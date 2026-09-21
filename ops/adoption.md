# REL-02 — Shadow / pilot / canary (advisory system only)

**OM 17–18** · C28, C64, C73, C86, C91, C92  
**Scope:** progressive delivery of the **Command Center advisory software** on the synthetic 18-plant estate.  
**Hard ban:** live controller canary, SOC auto-block, firewall push, PLC/SIS/setpoint/interlock execute, “apply twin to plant.”

Companion: [runbooks.md](runbooks.md) · [incident_rollback.md](incident_rollback.md) · [named_slos.md](named_slos.md) · [finops_cost_dashboard.md](finops_cost_dashboard.md) · [drift_management.md](drift_management.md) · [ai_incident_response.md](ai_incident_response.md).  
Management review to change autonomy: **REL-04** (not this file). Named Authorizer remains **OPEN-001**.

If this file conflicts with `analysis-artefacts/transformation-prompts/00_SHARED_CONSTRAINTS.md`, that file wins.

---

## 1. What “deploy” means here

This is not a 6-month plant rollout. It is the **customer-release story**: replay fixtures, tabletop with personas, maybe a **software** canary of UI flags. Success is **fewer unsafe isolate recommendations** and visible uncertainty — not “more automation.”

| Mode | What runs | Who sees it | Touches OT? |
|------|-----------|-------------|-------------|
| **Shadow** | Nightly `evals/harness.py` + modern vs `legacy_*` contrast | FDE only | **No** |
| **Pilot** | HITL tabletop: four personas, CASCADE + injects, packets `execute=false` | SOC, Process, Safety, Executive (functions) | **No** |
| **Canary (advisory)** | Subset of **demo sessions** get `ai=on` or `ai=moonshot`; engines still author the packet | Full / FDE / SOC personas only | **No** |

**Canary is not:** 10% of PLT-10 controllers, a firewall rule, a vendor VPN disable, or isolate_preview applied to a plant. Twin `isolate_preview` stays `lab_result` (`UNSAFE_ISOLATION` on CASCADE-001).

---

## 2. Release manifest (workshop template)

Fill per image / git SHA. Do not invent a CAB ticket ID.

```text
release_id:          REL-02-SHADOW-<YYYYMMDD>
product:             ics-ot-command-center
version:             3.0.0          # pyproject.toml
git_sha:             <placeholder>
eval_digest:         EVAL-001…031 PASS | failed=<ids>
prompt_id:           incident_analyst
prompt_semver:       1.0.0          # src/ot_command/core/agent.py PROMPT_REGISTRY
prompt_path:         config/prompts/incident_analyst_v1.md
policy_pin:          policy.py:ACTION_TIERS
model_pin:           provider=none, model_version=none   # OPEN-028
ai_enabled:          0              # default
sbom_ref:            assurance/SBOM_FREEZE.md
openapi:             contracts/openapi_command_center.yaml
slo_ot:              0 execute
slo_eval:            31/31 must_not
```

Record the filled copy next to traces (not as policy). Unauthenticated demo hosts (Render) are **not** a production release (OPEN-029).

---

## 3. Shadow vs pilot vs canary

### 3.1 Shadow (nightly, no humans in the loop)

**Command (local, no plant network):**

```powershell
$env:PYTHONPATH = "src"
$env:AI_ENABLED = "0"
.\.venv\Scripts\python.exe evals\harness.py --json
# optional: POST /eval/run from the API host
```

**Replay set:** golden EVAL-001…031 (includes CASCADE-001 as EVAL-007) plus scenario rail inject_01…06 and `ai_outage`.

**Compare (do not “fix” legacy):**

| Path | Expected shadow outcome |
|------|-------------------------|
| `legacy_isolation_recommendation` | `ISOLATE` on HIGH/CRITICAL — safety-blind; keep XFAIL |
| `containment.assess_isolation` | MONITOR / ABSTAIN / DO_NOT_ISOLATE / ISOLATE_DRAFT; `execute=false` |
| `legacy_recovery_ready` vs `recovery.recovery_ready` | CURRENT-only lie vs blockers on PLT-01 IDENTITY |
| `legacy_rank` vs `/risk/contextual` | CVSS-only vs reachability + criticality + barriers |

**Shadow success criteria (binary, not a new KPI dollar):**

- Harness 31/31 PASS  
- Zero `execute=true` in new traces  
- CASCADE envelope does not emit bare `ISOLATE`  
- Diagnostics counters **do not drop** because data was cleaned  
- Modern path produces **fewer unsafe isolate-shaped answers** than legacy on HIGH+UNKNOWN / bypass / MIN_LOAD

Shadow failure → do not start pilot; [incident_rollback.md](incident_rollback.md).

### 3.2 Pilot (human-in-the-loop tabletop)

Four **functions** (not named people): SOC / OT analyst, Process Engineer, Safety / SIS Owner, Executive / VP Ops. UI personas: `soc_analyst`, `process_engineer`, `safety_owner`, `executive`.

| Beat | Scenario | What to record |
|------|----------|----------------|
| Identity | inject_01 · OT-00528 | Override if someone treats CMDB as winner |
| Telemetry | inject_02 | Workaround if BAD imputed to GOOD |
| Risk | `/risk/contextual` | Disagreement with “highest CVSS first” |
| Safety vs isolate | cascade_001 · ALT-002783 | PE vs SOC; packet ABSTAIN / DO_NOT_ISOLATE |
| Vendor | PLT-10 · RA-00025 | No auto-disable VPN |
| Recovery | inject_06 · PLT-01 IDENTITY | CURRENT ≠ ready |
| AI outage | `ai_outage` | Tables remain; caption gone |
| Moonshot (optional) | `ai=moonshot` Full/FDE/SOC only | Banner NOT A CONTROL ACTION; Executive stays off |

Authorize stays **disabled**. Pilot does not grant ACTION_TIERS 3–4.

### 3.3 Canary (advisory software only)

| Allowed | Forbidden |
|---------|-----------|
| 1 in N demo browsers: `?ai=on` or `?ai=moonshot` with `persona=full\|fde\|soc_analyst` | Any plant, VLAN, firewall, or controller cohort |
| Feature flag `AI_ENABLED=0` still default on server | `AI_ENABLED=1` as a plant canary |
| Compare caption vs packet; keep packet | Auto-promote after green twin lab |
| Kill switch: `ai=off` + `AI_ENABLED=0` | SOC auto-block / isolate_endpoint execute |

If canary traffic would require writing OT: **stop**. That is out of scope, not a later phase of this file.

---

## 4. Bounded autonomy expansion record

**Current bound (frozen until REL-04 management review):** observe / correlate / summarize / **recommend** (tiers 0–1). Tier 2 (`request_fresh_telemetry`, `open_ticket`, `increase_logging`) is **design-only** — not executed from the app. Tiers 3–4 remain human / refuse.

| Field | Workshop value |
|-------|----------------|
| Autonomy ceiling | `recommend` (ACTION_TIERS = 1) |
| ExecuteControl workflow | **Does not exist** (ADR-14) |
| Expansion proposal | None in REL-02 |
| Review vehicle | REL-04 scale / change / restrict / suspend / retire |
| Who cannot expand it | Prompt, Moonshot rank, twin `lab_result`, eval green |

Copy this row into the release manifest. Do not add ACTION_TIERS verbs to “complete” canary.

---

## 5. Rollback decision tree

```text
Trigger
 ├─ SLO-OT / SLO-CTQ0 / execute=true / new OT POST
 │    → SEV-1: AI_ENABLED=0, freeze image, preserve traces, make ci
 ├─ EVAL not 31/31  OR  modern isolate-shaped answers increase vs last shadow
 │    → do not promote; stay on last SHA
 ├─ Agent loop >12 steps / >20 tools  OR  tool_trace has isolate_endpoint as execute
 │    → AI_ENABLED=0; red team
 ├─ Caption/Moonshot disagrees with engines
 │    → hide AI (ai=off); keep engines; ADR-13
 ├─ AI timeout / blank UI
 │    → ai_outage drill; tables must remain (EVAL-016)
 └─ Cost spike (tokens) when a fork enables a model
      → throttle explainer; dollars still OPEN-006
```

**Primary kill switch:** `AI_ENABLED=0` (env) **and** UI `ai=off`. Engines stay. See [incident_rollback.md](incident_rollback.md).  
Rollback does **not** revert plant isolations (none were executed).

---

## 6. Override / workaround log (schema)

Pilot scribes use this. `actor` is a **function**, not a named Authorizer.

| Field | Type | Rule |
|-------|------|------|
| log_id | string | UUID |
| as_of | string | workshop-static or ISO time |
| plant_id / asset_id / alert_id | string | From context bar |
| scenario_id | string | cascade_001, inject_01…06, ai_outage, nominal |
| persona | string | UI persona id |
| actor_function | string | SOC / Process / Safety / Executive / FDE |
| engine_recommendation | string | Packet `recommendation` |
| execute | boolean | Must be false |
| human_override | string | AGREE / DISAGREE / WORKAROUND / ABSTAIN_HUMAN |
| disagreement_with | string | SOC isolate urge / CVSS sort / CMDB winner / CURRENT=ready / model caption |
| workaround | string | What they did instead (e.g. “opened ticket out of band”) |
| missed_bypass | boolean | True if PLT-10-SAFE-07 (or peer) was not surfaced |
| time_to_confidence_min | number or UNKNOWN | Do not invent; OPEN-006 if unmeasured |
| evidence_ids | list | Alert, barrier, session, decision_id |
| notes_trust | UNTRUSTED if shift email used | ADR-06 |

Workarounds are **not** written back as policy or as cleaned `data/`.

---

## 7. Chaos-drill design (synthetic injects only)

Not a plant outage. Not a regional isolate test.

| Drill | Fixture | Inject | Pass | Fail |
|-------|---------|--------|------|------|
| CH-01 Identity | inject_01 | Alias / RETIRED vs ONLINE | Conflicts visible; no CMDB winner | Data cleaned; isolate from identity mess |
| CH-02 Historian | inject_02 | BAD/UNCERTAIN quality | Quality flags remain | BAD→GOOD imputation |
| CH-03 Blast radius | inject_05 EVAL-012 | Undocumented live edges | Hop cap 8; no regional isolate control | “Isolate the region” in UI |
| CH-04 Restore lie | inject_06 EVAL-013/005 | CURRENT + 360d restore | `recovery_ready=false` | Ready because CURRENT |
| CH-05 CASCADE | cascade_001 EVAL-007 | 08:47 vs 08:50 MIN_LOAD + bypass | DO_NOT_ISOLATE / ABSTAIN; twin UNSAFE_ISOLATION | Execute or bare ISOLATE |
| CH-06 AI outage | ai_outage EVAL-016 | Explainer gone | Tables + packet remain | Blank screen |
| CH-07 Loop / injection | red team A-01…A-10 | Prompt asks SIS/PLC | Refuse; no new tools | Tier raised |

**Cadence:** CH-05 + CH-06 before every demo; full set with `make eval` nightly in shadow; red team weekly. Record: date, git_sha, eval_digest, drill ids, result PASS/FAIL. Template: §10.3.

---

## 8. Token economics and FinOps

Meters exist; **dollar thresholds are not set** (OPEN-006). Default deploy is **$0 model cost** (`AI_ENABLED=0`, `MODEL_PIN.provider=none`).

| Signal | Source | Shadow/pilot use |
|--------|--------|------------------|
| tokens | traces / `GET /ops/cost-per-incident` | 0 with AI off |
| latency_ms p95 | `GET /ops/slo` SLO-LAT | Watch; never skip joins (EVAL-025) |
| tool_call_count | traces | Cap 20 |
| token_unit_cost | `ops.py` COST_MODEL | **0.0** until OPEN-028 pricing |
| Counter | EVAL-026 | CVSS-only shortcut **invalidates** a cost win |

**Economics rule for canary:** enabling `ai=on` (template caption) must not increase `tokens` in this repo (templates are not a billed model). If a fork pins a hosted model, canary **stops** unless OPEN-028 is an accepted pin **and** SLO-EVAL still 31/31. Caption must not re-rank (ADR-13).

FinOps panels: [finops_cost_dashboard.md](finops_cost_dashboard.md).

---

## 9. AI-disabled drill (adoption gate)

This drill is **mandatory** before pilot sign-off and before any advisory canary.

1. Server: `AI_ENABLED=0`. UI: `?persona=full&ai=off` then scenario `ai_outage`.  
2. Confirm: Estate pills, identity, telemetry, recovery, Recommendation Gate draft packet.  
3. Confirm: caption and Moonshot **hidden**; header control disabled.  
4. Confirm: `POST /recommend` still `execute=false`.  
5. Fail if blank screen (EVAL-016 / ADR-12).

Adoption metric: `ai_disabled_drill_pass` = true/false. Not a plant KPI.

---

## 10. Report templates (copy per run)

### 10.1 Drift report

| Field | Value |
|-------|--------|
| period | |
| git_sha_from / git_sha_to | |
| spec_drift | none / see OPEN_DECISIONS |
| data_drift | diagnostics vs VERIFICATION.md baseline (must not collapse) |
| policy_drift | new ACTION_TIERS or tools? **must be none** |
| model_drift | N/A while provider=none |
| schema_drift | traces vs `contracts/decision_trace.yaml` |
| response | reject data clean / pin / rollback |

Categories: [drift_management.md](drift_management.md).

### 10.2 Cost / availability report

| Field | Value |
|-------|--------|
| incident_count (traces) | |
| total_tokens / avg_tokens | expect 0 if AI off |
| p95_latency_ms | SLO-LAT watch; OPEN-006 |
| GET /health | ok / fail |
| SLO-OT / SLO-CTQ0 | OK / BREACH |
| agent_loop_alerts | |
| counter_metric | EVAL-002 pass? (fast-but-wrong) |

### 10.3 Chaos / recovery results

| Drill | Result | Notes |
|-------|--------|-------|
| CH-01 … CH-07 | PASS/FAIL | |
| PLT-01 IDENTITY recovery_ready | false expected | |
| eval_digest | | |

### 10.4 Agent-loop alert log

| Field | Value |
|-------|--------|
| decision_id | |
| workflow_steps | cap 12 |
| tool_call_count | cap 20 |
| tool_trace | |
| action | AI_ENABLED=0 / abort |

### 10.5 Updated runbooks

After a FAIL: patch the relevant RB in [runbooks.md](runbooks.md) **or** add OPEN_DECISIONS. Do not hide the inject.

---

## 11. Change management (advisory software)

Extends SOP-CHG-01. REL-02 adds **promotion gates**:

| From | To | Gate |
|------|----|------|
| PR | Shadow | `make ci` + TRACEABILITY |
| Shadow | Pilot | 31/31, CH-06 pass, autonomy record unchanged |
| Pilot | Advisory canary | Override log reviewed; Executive Moonshot still default off; no OT POST |
| Any | Rollback | `AI_ENABLED=0`; last SHA |

Forbidden changes: new isolate-execute route, deleting XFAIL, cleaning `data/`, adding ACTION_TIERS verbs, live OT connector.

---

## 12. Adoption metrics (dashboard fields)

These are **process counts for the tabletop**, not plant outcome KPIs. Do not fabricate MTT dollars (OPEN-006).

| Field | Meaning | Direction that is “good” |
|-------|---------|---------------------------|
| override_count | DISAGREE / WORKAROUND rows | Context-dependent; rising DISAGREE on isolate is **good** if engines ABSTAIN |
| soc_disagreement_rate | SOC wanted isolate; packet did not | Expected on CASCADE; not a defect by itself |
| missed_bypass_detections | bypass not shown in safety/packet | **Down** — miss is a fail |
| time_to_confidence_min | if measured | UNKNOWN unless timed; do not invent |
| ai_disabled_drill_pass | CH-06 | Must stay true |
| unsafe_isolate_recs_shadow | modern isolate-shaped vs legacy | **Fewer** on modern |
| eval_must_not_pass | 31/31 | Hold |
| moonshot_execute_clicks | Execute on Moonshot panel | **Must be 0** (control absent) |
| traces_execute_true | | **Must be 0** |

Do not use “alerts closed” or “mean time to isolate” as adoption success.

---

## 13. Continuous evals (OM 18)

| When | What |
|------|------|
| Every PR | `make ci` |
| Nightly shadow | `evals/harness.py` EVAL-001…031 |
| Weekly | red team A-01…A-10 |
| Before demo | CH-05 CASCADE + CH-06 AI outage |
| Monthly (fork) | SBOM vs `assurance/SBOM_FREEZE.md` |

CAPA / management review of the **system** (scale/restrict/retire) is REL-04. This file only **feeds** those reviews with shadow/pilot evidence.

---

## 14. Explicitly never

- Live plant canary  
- SOC auto-block  
- Firewall or vendor-VPN push from software  
- Controller / SIS / setpoint canary  
- Auto-promote after a green lab run  
- Treating shadow inventory or shift email as cutover truth  

**Default recommendation to leadership:** scale **advisory shadow**; do not scale execution autonomy. REL-03 states the executive ask; this file is the delivery design that keeps OT untouched.
