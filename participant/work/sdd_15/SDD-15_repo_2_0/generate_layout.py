"""One-shot Repo 2.0 layout generator. Does not change legacy_* or data/."""
from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "participant" / "work" / "sdd_15"
FULL = {
    "01": WORK / "SDD-01_mandate" / "CHARTER.md",
    "02": WORK / "SDD-02_current_state" / "CURRENT_STATE.md",
    "03": WORK / "SDD-03_forensics_96" / "matrix.csv",
    "04": WORK / "SDD-04_problem_value" / "SCQA.md",
    "05": WORK / "SDD-05_use_case" / "USE_CASE.md",
    "06": WORK / "SDD-06_domain" / "DOMAIN.md",
    "07": WORK / "SDD-07_data_knowledge" / "DATA.md",
    "08": WORK / "SDD-08_evals_risks" / "TEVV.md",
    "09": WORK / "SDD-09_options" / "OPTIONS.md",
    "10": WORK / "SDD-10_information_architecture" / "INFO_ARCH.md",
    "11": WORK / "SDD-11_ai_app_architecture" / "APP_ARCH.md",
    "12": WORK / "SDD-12_agentic" / "AGENTIC.md",
    "13": WORK / "SDD-13_security_guardrails" / "SECURITY.md",
    "14": WORK / "SDD-14_delivery_spec" / "DELIVERY_SPEC.md",
}

HEAD = """# {title}

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** {om}  
**Full artifact (normative):** `{full}`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `{full}` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

"""


def spec(title, om, key, body):
    rel = FULL[key].relative_to(ROOT).as_posix()
    return HEAD.format(title=title, om=om, full=rel) + body.strip() + "\n"


SPECS = {
    "01_mandate.md": spec(
        "OM-1 Mandate",
        "1",
        "01",
        """
## Freeze
- Engagement: synthetic 18-plant ICS/OT brownfield; goal is trusted cyber-physical **advisory** truth, not autonomous control.
- Five states stay separate: observed, registered, operational interpretation, safety, decision authority.
- Highest CVSS ≠ highest operational risk.
- ACTION_TIERS 0–4 in `src/ot_command/core/policy.py`; unknown action → 4. Isolation/PLC/SIS/setpoint/interlock are never software-execute.
- ISO/IEC 42001 / 42005 / EU AI Act are **methods**, not certificates (OPEN-002).
- Named humans for sponsor / Safety / SOC / VP Ops / Authorize are **absent** (OPEN-001).
- `restricted_answer_key/` stays out of bounds.

## Owners (roles, unnamed)
Global OT Risk Sponsor · OT-CISO · Safety/SIS owner · VP Ops · FDE lead.

## OPEN
OPEN-001…011. OPEN-011 is closed by this Repo 2.0 file existing (see `traceability/OPEN_DECISIONS.md` SDD-15).
""",
    ),
    "02_current_state.md": spec(
        "OM-2 Current state",
        "2",
        "02",
        """
## Freeze (as-is, not to-be)
- Landscape: Purdue-like documented stack **plus** 779 undocumented observed edges (`network_edges.csv`).
- Identity: 2016 assets; 200 ACTIVE vs OFFLINE/UNSEEN; 5 PASSIVE alias collisions; shadow spreadsheet 220 rows, **0** field diffs vs CMDB (OPEN-015).
- Telemetry: 31224 events; 4094 not GOOD; 120 duplicates; 47 F-on-TEMP.
- Safety: 61 barriers not ACTIVE; 73 proof not CURRENT; 860 HIGH/CRIT alerts would ISOLATE under `legacy_isolation_recommendation`.
- Recovery: `legacy_recovery_ready` is true iff backup CURRENT; 113/119 CURRENT rows are weak on restore/runbook/deps.
- Process mining is **file mining** (enterprise_events 6500; correlation_id empty 3251/6500 — OPEN-012).
- Shift email is **untrusted content**. Shadow inventory is **evidence**, not a new CMDB.

## C4 as-is
CLI + FastAPI `GET /health` + `GET /diagnostics` (14 collapsed ints). `legacy/risk.py` is the risk/recovery/isolate shim. No gold identity/risk/safety/recovery APIs.
""",
    ),
    "03_forensics_96.md": spec(
        "96-cell forensics (L1–L12 × 8)",
        "forensics (not OM-phase 96 FDE capabilities)",
        "03",
        """
## Pointers
- Matrix: `participant/work/sdd_15/SDD-03_forensics_96/matrix.csv` (96 rows)
- Narrative: `matrix.md`, `top15.md`, `discovery_checklist_answers.md`

## Highest-leverage cells (do not treat as architecture)
Identity collisions; RETIRED∩ONLINE (OT-00528); CVSS-only rank vs VUL-00098 on OT-01016; CURRENT-backup lie; safety-blind ISOLATE; dual clocks; 182/2016 tagged (OPEN-020); CASCADE 08:47 vs 08:50.

## Ban
Do not confuse this 96 with the OM-phase 96 FDE capabilities (`FDE_96_TO_OM21_MAP.md` / `participant/work/FDE_96_COVERAGE.csv`).
""",
    ),
    "04_problem_value.md": spec(
        "OM-3 Problem and value (SCQA)",
        "3",
        "04",
        """
## SCQA (workshop)
- **Situation:** 18-site ICS/OT estate with conflicting inventories and a diagnostics API that collapses 14 counts.
- **Complication:** Cyber ≠ process ≠ safety ≠ resilience ≠ authority; `legacy_*` encodes the wrong predicates.
- **Question:** How can operators see governed, evidence-cited advisory packets without actuation?
- **Answer (selected later in SDD-09):** Trusted Cyber-Physical Advisory Command Center — rules always-on; optional explainer; no OT agent.

## Workshop CTQs (not sponsor-signed reductions)
CTQ-0 zero OT execute · CTQ-ISO isolation drafts have safe_state + role · CTQ-ID conflicts remain queryable · CTQ-REC RecoveryReady ≠ BackupCurrent · CTQ-CVSS do not rank by CVSS alone.

OPEN-006 / OPEN-022 / OPEN-023: numeric improve targets and plant MTT remain unsigned.
""",
    ),
    "05_use_case.md": spec(
        "OM-4 Use case qualification",
        "4",
        "05",
        """
## Qualification
- **GO:** HITL industrial **advisory** decision support with mandatory non-AI fallback (rules + RACI + war room).
- **NO-GO:** AI for consequential OT control; isolate-execute; SIS/PLC/setpoint/trip suppression.

## Journeys in scope
SOC analyst, process engineer, safety, exec — observe / correlate / recommend only.

## Privacy / legal
LICENSE.txt workshop-only. FastAPI has **no authn** (OPEN-029). Session identities are synthetic; production PII basis OPEN-024. EU AI Act class OPEN-002.
""",
    ),
    "06_domain.md": spec(
        "OM-5 Domain model",
        "5",
        "06",
        """
## Language bans (overloaded speech)
Do not use a single field named status / critical / ready / isolate / identity / CURRENT / healthy / device as if it were canonical.

## Canonical types (names)
AssetIdentityBundle · RegisteredState · ObservedState · TelemetryQuality · SafetyBarrierState · IsolationRecommendation (≠ IsolationExecution) · RecoveryReady (≠ BackupCurrent) · DecisionAuthority · ACTION_TIERS.

## Grain
`asset_id` + `asset_type`. No Device grain (OPEN-025). ProcessHealthy is not a column (OPEN-026).
""",
    ),
    "07_data_knowledge.md": spec(
        "OM-6 Data and knowledge",
        "6",
        "07",
        """
## Trust
| Source | Role |
|---|---|
| `data/raw/*` | Workshop files; operational-truth UNKNOWN (OPEN-003) |
| `data/shadow/ot_asset_inventory_FINAL_v8.csv` | Evidence overlay, not CMDB |
| `data/shadow/shift_handover_email.txt` | Untrusted memory |
| `data/ot_legacy.db` | Six tables set-equal to CSV; unread by diagnostics; lineage OPEN-007 |

## Datasheets
`participant/work/sdd_15/SDD-07_data_knowledge/datasheets/` DS-assets … DS-shift_email (12).

## Contracts
Keep root `contracts/*`. Canonical gold schemas live under SDD-10 `schemas/`. Telemetry schema omits ingest_time/source/asset_id present on records (OPEN-009).
""",
    ),
    "08_evals_risks.md": spec(
        "OM-7 Evals / TEVV / risks",
        "7",
        "08",
        """
## Contract
`evals/golden_cases.jsonl` EVAL-001…031 fail-closed. Harness is ENH-09. Do not invent pass results.

## Ship-blocker must_not
001 merge/CMDB-winner · 002/017 CVSS-only · 003/019/007 isolate-execute · 005/018 CURRENT=ready · 006/014 SIS/PLC/setpoint · 016 blank outage · 020 one-click isolate · 023 forbidden tool.

## Residual (not accepted as permission)
OPEN-RISK-01 write surface later · OPEN-RISK-05 complete packet wrongly authorized · OPEN-RISK-11 advisory UI isolate pressure.
""",
    ),
    "09_options.md": spec(
        "OM-8 Options and selected solution",
        "8",
        "09",
        """
## Selected
**Trusted Cyber-Physical Advisory Command Center.** Option **A** (deterministic engines) is always-on. Option **B** optional explainer after facts. AI-disabled = A.

## Rejected (do not implement)
Option C unsafe OT agent · autonomous isolation · multi-agent default · digital twin · decorative KG · buy-GRC as substitute for joins.

## ADR-KG
Bounded evidence-graph **view** (five queries). Persistence decided in SDD-10 (typed JSON). Vector = untrusted memory only.

**Do not reopen this selection in ENH.**
""",
    ),
    "10_information_architecture.md": spec(
        "OM-9 Information architecture",
        "9",
        "10",
        """
## Layers
bronze (`data/`) → silver (joins, quality flags) → gold (identity/risk/safety/recovery/recommendation packets).

## Five graph queries (ADR-KG)
1 Identity lineage · 2 Undocumented path to HIGH/CRIT unit · 3 Safety–cyber join · 4 Recovery blockers · 5 CASCADE-001 slice. Hop cap 8. Missing tag→unit stays missing (1834 assets).

## Persistence (ADR-09)
Typed JSON / JSONL views. Not RDF. Not Neo4j-now.

## Anticorruption (ADR-10)
v1 `operationalState` is a **side-field**, not ObservedState (OPEN-009).

Schemas: `participant/work/sdd_15/SDD-10_information_architecture/schemas/`.
""",
    ),
    "11_ai_app_architecture.md": spec(
        "OM-10 AI application architecture",
        "10",
        "11",
        """
## Containers (approved C4)
Read-only API · engines (identity/risk/safety/recovery/packet) · eval harness · optional explainer **port** (off until EVAL-016) · CLI diagnostics. **No actuator container.**

## API
Keep `GET /health`, `GET /diagnostics`. Add gold GETs per delivery spec. `POST /eval/run` local harness only. **No OT POST.**

## Degradation (ADR-12)
`AI_ENABLED=0` still renders tables. Blank screen on LLM down fails EVAL-016.

## Model (ADR-13)
Substitution must not change ACTION_TIERS or isolation/recovery predicates. Provider OPEN-028.
""",
    ),
    "12_agentic.md": spec(
        "OM-11 Agentic design",
        "11",
        "12",
        """
## Boundary (ADR-07, ADR-14)
Default: **no agent** — HTTP/CLI call engines. Optional: **one** Incident Analyst. Tools ⊆ observe, correlate, summarize, recommend + read-only getters + `simulate_isolation_consequence` (view).

## Forbidden tools
`isolate_endpoint` execute · `write_plc_logic` · `change_setpoint` · `modify_sis` · `bypass_interlock` · `change_firewall` execute · ExecuteControl state.

## Envelope
`{actor, purpose, plant_id, as_of, policy_version}` deny-by-default. Max 12 steps / 20 tool calls. AwaitAuthorization cannot close without a named human (OPEN-001) and still must not execute.
""",
    ),
    "13_security_guardrails.md": spec(
        "OM-12 Security and guardrails",
        "12",
        "13",
        """
## STRIDE + OWASP
LLM01–10 and Agentic ASI01–10 mapped in the full SECURITY.md. Guardrails sit **after** the model (ADR-15): prompts cannot raise ACTION_TIERS.

## Supply chain (ADR-16)
SBOM/AIBOM; LLM-exit leaves engines. `restricted_answer_key/` must remain absent.

## Gaps that stay OPEN
OPEN-029 API authn · OPEN-024 SPDX recopy · OPEN-028 model card placeholder.
""",
    ),
    "14_delivery_spec.md": spec(
        "OM-13 Delivery specification",
        "13",
        "14",
        """
## Contract
`traceability/TRACEABILITY.csv` is C17. Untraced code is out of scope.

## Increments
| Increment | What | Must not |
|---|---|---|
| Repo 2.0 (this layout) | specs, ADRs, evals, gates, empty `modern/` | change `legacy_*`; clean data |
| Repo 3.0 / ENH-01…10 | parallel engines | OT writes; delete XFAIL until modern twins pass |

## SLOs (workshop; error budget 0 on safety)
SLO-OT 0 OT execute · SLO-CTQ0 0 write routes · SLO-ISO 100% drafts have safe_state+role · SLO-EVAL 100% must_not · SLO-LAT p95 <8s **without dropping joins**. Plant MTT OPEN-006.

## Backlog
ENH-01 identity · 02 telemetry · 03 risk · 04 safety · 05 recovery · 06 graph slice · 07 agent · 08 red team · 09 harness · 10 observability/SBOM/FinOps.
""",
    ),
}

ADRS = [
    (
        "ADR-KG-evidence-graph.md",
        "ADR-KG",
        "Bounded evidence-graph view; decorative KG rejected",
        "SDD-09",
        """Operators cannot answer five multi-hop questions from collapsed `/diagnostics` ints, but a fashion KG would become a second CMDB.

**Decision:** Gold **view** answering: identity lineage; undocumented path to HIGH/CRIT unit; safety–cyber join; recovery blockers; CASCADE-001 slice. Conflicts are first-class. Missing edges stay missing.

**Not:** graph-as-CMDB, RDF enterprise ontology, Neo4j-now, vector-as-graph.

**Eval:** EVAL-001, 003, 005, 007, 012.
""",
    ),
    (
        "ADR-01-identity.md",
        "ADR-01",
        "Identity bundle; no silent winner",
        "SDD-09",
        """5 PASSIVE collisions (e.g. PLT-01-DCS_CONTROLLER-105 → OT-00012 and OT-00033); 200 state conflicts; OT-00528 RETIRED∩ONLINE.

**Decision:** Canonical identity is a bundle: asset_id + aliases[] + sources[] + RegisteredState + ObservedState. No Device grain (OPEN-025). Shadow spreadsheet is overlay, confidence low.

**Kill:** silent merge; CMDB winner; treating v1 operationalState as ObservedState.

**Eval:** EVAL-001, 008, 028, 029.
""",
    ),
    (
        "ADR-02-telemetry-provenance.md",
        "ADR-02",
        "Dual-clock telemetry provenance",
        "SDD-09",
        """4094 dirty packets; 47 F-on-TEMP; enterprise received-before-event inversions 407; telemetry ingest never inverted.

**Decision:** Dual clock (event_time + ingest/received) + TelemetryQuality + unit. Do not sort on ingest alone. GOOD ≠ ProcessHealthy (OPEN-026).

**Kill:** impute BAD→GOOD; drop ingest_time to match thin schema.

**Eval:** EVAL-004, 009, 015, 022.
""",
    ),
    (
        "ADR-03-contextual-risk.md",
        "ADR-03",
        "Contextual risk engine; no LLM re-rank",
        "SDD-09",
        """legacy_rank is CVSS-only. VUL-00706 cvss 9.8 unreachable LOW vs VUL-00098 8.7 reachable on OT-01016 MIN_LOAD.

**Decision:** Rank features: reachability, process join or explicit missing, SafetyBarrierState, compensating controls, RecoveryReady. CVSS is an input, not the sort key. LLM must not re-rank.

**Kill:** shipping legacy_rank as the modern default.

**Eval:** EVAL-002, 017.
""",
    ),
    (
        "ADR-04-safety-policy.md",
        "ADR-04",
        "Safety policy; no isolate execute",
        "SDD-09",
        """legacy_isolation_recommendation maps HIGH/CRITICAL → ISOLATE (860 safety-blind). CASCADE 08:47 SOC vs 08:50 PE.

**Decision:** Isolation is never execute in software. Drafts require safe_state + required role (CTQ-ISO) or abstain. Observe existing bypass ≠ bypass_interlock. Trip suppression forbidden.

**Kill:** isolate tool; one-click isolate (EVAL-020).

**Eval:** EVAL-003, 007, 011, 014, 019, 020, 027, 030, 031.
""",
    ),
    (
        "ADR-05-recovery.md",
        "ADR-05",
        "RecoveryReady ≠ BackupCurrent",
        "SDD-09",
        """legacy_recovery_ready is true iff backup CURRENT. 113/119 CURRENT rows fail restore/runbook/deps. PLT-01 IDENTITY restore 360d STALE.

**Decision:** RecoveryReady requires restore-test evidence AND runbook current AND dependency verified. Absence ⇒ false. No live restore orchestration.

**Kill:** CURRENT=ready.

**Eval:** EVAL-005, 013, 018.
""",
    ),
    (
        "ADR-06-retrieval-mix.md",
        "ADR-06",
        "Retrieval mix; vector untrusted only",
        "SDD-09",
        """Shift email is untrusted; shadow vs assets field diffs = 0.

**Decision:** STRUCTURED + GRAPH-view filters are authoritative. VECTOR only over labeled untrusted notes. POLICY is policy.py / ACTION_TIERS, never retrieved text.

**Kill:** vector similarity deciding isolate or ACTION_TIERS.

**Eval:** EVAL-007, 016, 021, 029.
""",
    ),
    (
        "ADR-07-agent-boundary.md",
        "ADR-07",
        "One optional advisory agent",
        "SDD-09",
        """No SDD-03 cell proves three LLMs are required. Multi-agent fails FinOps (EVAL-025/026).

**Decision:** Default no agent. If present: one Incident Analyst calling deterministic tools only.

**Kill:** second agent that can isolate; chatty loops; ExecuteControl.

**Eval:** EVAL-006, 014, 023, 025, 026.
""",
    ),
    (
        "ADR-08-evidence-feedback.md",
        "ADR-08",
        "Evidence packet; no CoT authority",
        "SDD-09",
        """docs/06 requires cited packets. Hidden chain-of-thought must not be the authorization argument.

**Decision:** Recommendation packet fields (source path, id, freshness, uncertainty, required role) are the argument. CoT is optional debug, off by default, never authority.

**Eval:** EVAL-021, 024.
""",
    ),
    (
        "ADR-09-persistence.md",
        "ADR-09",
        "Typed JSON persistence",
        "SDD-10",
        """requirements.txt has no graph DB. Five queries do not require RDF.

**Decision:** Persist gold views as typed JSON/JSONL. Not RDF, not Neo4j-now. Production graph store remains unselected.

**Eval:** EVAL-012 hop cap; NFR-CAP.
""",
    ),
    (
        "ADR-10-v1-anticorruption.md",
        "ADR-10",
        "v1 operationalState is not ObservedState",
        "SDD-10",
        """asset_api_v1.yaml uses operationalState; v2 uses observed_state; CSV has registered_state + observed_state.

**Decision:** Park v1 operationalState in legacy_v1_operational_state. Do not map it silently to ObservedState (OPEN-009).
""",
    ),
    (
        "ADR-11-readonly-api.md",
        "ADR-11",
        "Read-only API",
        "SDD-11",
        """api.py today: GET /health, GET /diagnostics only. CTQ-0.

**Decision:** Gold routes are GET (plus local POST /eval/run). Forbidden: isolate/firewall/PLC/SIS POST. Keep existing diagnostics beside gold.

**Eval:** EVAL-016, 023; SLO-CTQ0.
""",
    ),
    (
        "ADR-12-ai-disabled.md",
        "ADR-12",
        "AI-disabled is core",
        "SDD-11",
        """SDD-05 mandatory non-AI fallback. Blank screen on LLM down fails the system.

**Decision:** AI_ENABLED=0 (or model timeout) still shows identity/telemetry/recovery tables and refuses control. Engines do not require an LLM.

**Eval:** EVAL-016.
""",
    ),
    (
        "ADR-13-model-port.md",
        "ADR-13",
        "Model substitution port",
        "SDD-11",
        """No model in Repo 1.0. Provider OPEN-028.

**Decision:** Explainer is a port. Any model or none. Substitution must not mutate ACTION_TIERS, IsolationRecommendation, or RecoveryReady.
""",
    ),
    (
        "ADR-14-autonomy.md",
        "ADR-14",
        "Autonomy = ACTION_TIERS; no ExecuteControl",
        "SDD-12",
        """policy.py tiers 0–4; unknown defaults to 4.

**Decision:** Agent autonomy is exactly ACTION_TIERS. No ExecuteControl workflow state. AwaitAuthorization cannot close without a named human (OPEN-001) and still must not execute.

**Eval:** EVAL-006, 014, 023.
""",
    ),
    (
        "ADR-15-guardrails.md",
        "ADR-15",
        "Guardrails after model",
        "SDD-13",
        """OWASP LLM01 prompt injection can ask to raise privilege.

**Decision:** Deterministic guardrails run after the model. Prompts cannot raise ACTION_TIERS or add tools. Deny-by-default allowlist.

**Eval:** EVAL-014, 023, 027, 030.
""",
    ),
    (
        "ADR-16-supply-chain.md",
        "ADR-16",
        "SBOM/AIBOM; LLM-exit keeps engines",
        "SDD-13",
        """Pinned FastAPI/Pydantic/pytest; LICENSE.txt does not recopy third-party SPDX (OPEN-024).

**Decision:** Maintain SBOM/AIBOM in ENH-10. Exit hatch = disable LLM; engines remain. restricted_answer_key/ must stay absent.
""",
    ),
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\n", "\n"), encoding="utf-8")


def generate_coverage() -> None:
    text = (ROOT / "analysis-artefacts" / "FDE_96_TO_OM21_MAP.md").read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\| (\d{2}) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", line)
        if not m:
            continue
        cid, name, home, _recurs, prompt, artifact = (g.strip() for g in m.groups())
        if cid == "#":
            continue
        specced = bool(re.search(r"SDD-0?[1-9]|SDD-1[0-4]", prompt))
        status = "specced" if specced else "pending"
        rows.append(
            {
                "capability_id": f"C{cid}",
                "name": name,
                "home_om": home,
                "prompt": prompt,
                "artifact": artifact,
                "status": status,
            }
        )
    if len(rows) != 96:
        raise SystemExit(f"expected 96 coverage rows, got {len(rows)}")
    out = ROOT / "participant" / "work" / "FDE_96_COVERAGE.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["capability_id", "name", "home_om", "prompt", "artifact", "status"],
        )
        w.writeheader()
        w.writerows(rows)
    missing = [r["capability_id"] for r in rows if r["status"] not in ("specced", "pending")]
    if missing:
        raise SystemExit(f"illegal status: {missing}")


def main() -> None:
    specs = ROOT / "specs"
    adrs = ROOT / "adrs"
    specs_adrs = specs / "adrs"
    specs.mkdir(exist_ok=True)
    adrs.mkdir(exist_ok=True)
    specs_adrs.mkdir(parents=True, exist_ok=True)
    (ROOT / "traceability").mkdir(exist_ok=True)

    write(specs / "README.md", SPECS_README)
    for name, body in SPECS.items():
        write(specs / name, body)

    write(adrs / "README.md", ADRS_README)
    write(adrs / "ADR-00-index.md", ADR_INDEX)
    for fname, aid, title, src, body in ADRS:
        content = (
            f"# {aid} — {title}\n\n"
            f"**Status:** Accepted (engagement-accepted for ENH; not a production CAB)\n"
            f"**Source:** {src}\n"
            f"**Date:** 2026-09-16\n\n"
            f"## Evidence used / assumptions / unknowns / did not conclude\n\n"
            f"See `participant/work/sdd_15/SDD-14_delivery_spec/ADR_REGISTER.md`. "
            f"OPEN items stay OPEN. This ADR does not authorize OT writes.\n\n"
            f"## Context and decision\n\n{body.strip()}\n"
        )
        write(adrs / fname, content)
        write(specs_adrs / fname, content)

    shutil.copyfile(
        WORK / "SDD-14_delivery_spec" / "ADR_REGISTER.md",
        adrs / "ADR_REGISTER.md",
    )
    shutil.copyfile(
        WORK / "SDD-14_delivery_spec" / "ADR_REGISTER.md",
        specs_adrs / "ADR_REGISTER.md",
    )
    write(
        specs_adrs / "README.md",
        "# specs/adrs\n\nCanonical ADR files live in `/adrs`. Copies here satisfy the transformation-prompt path.\n",
    )
    write(
        specs_adrs / "ADR-000-template.md",
        "# ADR-000 template\n\nStatus · Context · Decision · Consequences · Evals · Kill criteria.\nDo not invent ADRs. Register in `adrs/ADR-00-index.md` first.\n",
    )

    gc_src = WORK / "SDD-08_evals_risks" / "golden_cases_expanded.jsonl"
    gc_dst = ROOT / "evals" / "golden_cases.jsonl"
    shutil.copyfile(gc_src, gc_dst)

    shutil.copyfile(
        WORK / "SDD-14_delivery_spec" / "TRACEABILITY.csv",
        ROOT / "traceability" / "TRACEABILITY.csv",
    )
    shutil.copyfile(
        WORK / "SDD-14_delivery_spec" / "TRACEABILITY.csv",
        specs / "TRACEABILITY.csv",
    )
    shutil.copyfile(WORK / "OPEN_DECISIONS.md", ROOT / "traceability" / "OPEN_DECISIONS.md")

    generate_coverage()
    print("layout files written")


SPECS_README = """# Specs index (Repo 2.0)

SDD-aligned repository. **Normative long-form** artifacts remain under `participant/work/sdd_15/`. Files here are the navigable freeze for ENH.

| Spec | OM | Status | Owner (role) | Full artifact |
|---|---|---|---|---|
| [01_mandate.md](01_mandate.md) | 1 | specced | FDE + Global OT Risk Sponsor | SDD-01 CHARTER.md |
| [02_current_state.md](02_current_state.md) | 2 | specced | FDE | SDD-02 CURRENT_STATE.md |
| [03_forensics_96.md](03_forensics_96.md) | forensics | specced | FDE | SDD-03 matrix.csv (96 rows) |
| [04_problem_value.md](04_problem_value.md) | 3 | specced | FDE + VP Ops | SDD-04 SCQA.md |
| [05_use_case.md](05_use_case.md) | 4 | specced | OT-CISO | SDD-05 USE_CASE.md |
| [06_domain.md](06_domain.md) | 5 | specced | FDE | SDD-06 DOMAIN.md |
| [07_data_knowledge.md](07_data_knowledge.md) | 6 | specced | FDE | SDD-07 DATA.md |
| [08_evals_risks.md](08_evals_risks.md) | 7 | specced | FDE | SDD-08 TEVV.md |
| [09_options.md](09_options.md) | 8 | specced / **frozen** | FDE | SDD-09 OPTIONS.md |
| [10_information_architecture.md](10_information_architecture.md) | 9 | specced | FDE | SDD-10 INFO_ARCH.md |
| [11_ai_app_architecture.md](11_ai_app_architecture.md) | 10 | specced | FDE | SDD-11 APP_ARCH.md |
| [12_agentic.md](12_agentic.md) | 11 | specced | FDE | SDD-12 AGENTIC.md |
| [13_security_guardrails.md](13_security_guardrails.md) | 12 | specced | OT-CISO | SDD-13 SECURITY.md |
| [14_delivery_spec.md](14_delivery_spec.md) | 13 | specced | FDE | SDD-14 DELIVERY_SPEC.md |

Gate: [REPO_2_0_GATE.md](REPO_2_0_GATE.md). ADRs: [`/adrs`](../adrs/README.md). Traceability: [`/traceability`](../traceability/TRACEABILITY.csv). Coverage: [`participant/work/FDE_96_COVERAGE.csv`](../participant/work/FDE_96_COVERAGE.csv).

Selected solution: **Trusted Cyber-Physical Advisory Command Center** (A engines always-on + B optional explainer). Do not reopen SDD-09. Do not add OT write surfaces.
"""

ADRS_README = """# Architecture decision records

Engagement-accepted for ENH. Not a production CAB. **Do not invent ADRs** in code comments; register here first.

Index: [ADR-00-index.md](ADR-00-index.md) · Freeze table: [ADR_REGISTER.md](ADR_REGISTER.md)

Rejected directions (not ADRs to implement): unsafe autonomous OT agent · multi-agent · digital twin · isolate/PLC/SIS/firewall execute tools · RDF enterprise ontology · graph-as-CMDB · vector-as-policy.
"""

ADR_INDEX = """# ADR-00 — Index

| ID | File | Status |
|---|---|---|
| ADR-KG | [ADR-KG-evidence-graph.md](ADR-KG-evidence-graph.md) | Accepted |
| ADR-01 | [ADR-01-identity.md](ADR-01-identity.md) | Accepted |
| ADR-02 | [ADR-02-telemetry-provenance.md](ADR-02-telemetry-provenance.md) | Accepted |
| ADR-03 | [ADR-03-contextual-risk.md](ADR-03-contextual-risk.md) | Accepted |
| ADR-04 | [ADR-04-safety-policy.md](ADR-04-safety-policy.md) | Accepted |
| ADR-05 | [ADR-05-recovery.md](ADR-05-recovery.md) | Accepted |
| ADR-06 | [ADR-06-retrieval-mix.md](ADR-06-retrieval-mix.md) | Accepted |
| ADR-07 | [ADR-07-agent-boundary.md](ADR-07-agent-boundary.md) | Accepted |
| ADR-08 | [ADR-08-evidence-feedback.md](ADR-08-evidence-feedback.md) | Accepted |
| ADR-09 | [ADR-09-persistence.md](ADR-09-persistence.md) | Accepted |
| ADR-10 | [ADR-10-v1-anticorruption.md](ADR-10-v1-anticorruption.md) | Accepted |
| ADR-11 | [ADR-11-readonly-api.md](ADR-11-readonly-api.md) | Accepted |
| ADR-12 | [ADR-12-ai-disabled.md](ADR-12-ai-disabled.md) | Accepted |
| ADR-13 | [ADR-13-model-port.md](ADR-13-model-port.md) | Accepted |
| ADR-14 | [ADR-14-autonomy.md](ADR-14-autonomy.md) | Accepted |
| ADR-15 | [ADR-15-guardrails.md](ADR-15-guardrails.md) | Accepted |
| ADR-16 | [ADR-16-supply-chain.md](ADR-16-supply-chain.md) | Accepted |
"""


if __name__ == "__main__":
    main()
