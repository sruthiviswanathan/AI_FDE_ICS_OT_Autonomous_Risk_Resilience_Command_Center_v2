# AI FDE Brownfield Repo 3.0 — ICS/OT Autonomous Risk & Resilience Command Center

**Repo 3.0:** mature / **production-oriented** (still synthetic), **refined specs**, **stronger governance**, **readiness-focused validation**, **PRD + App ready**. This tree is not the customer application; PRD-01 / APP-01 follow. No live plant deploy.

A **fictional, deterministic, locally runnable multinational ICS/OT brownfield simulation** for AI Forward-Deployed Engineering. It models plants where PLC/DCS/SCADA/HMI/historians, SIS, CMMS/EAM, SOC/SIEM, IAM/PAM, vendor remote access, engineering workstations and production systems have evolved independently.

## Core forensic tension

**Cyber state ≠ Operational state ≠ Safety state ≠ Resilience state**

The baseline works well enough to operate, but it contains conflicting inventories, stale configurations, telemetry quality issues, weak contextual risk logic, safety/security conflicts, undocumented bypasses, recovery gaps, shadow processes and fragmented authority.

## L1–L12 imperfection model

1. **L1 — Software / Engineering Logic** — legacy code, PLC logic mirrors, scripts, hard-coded rules, configuration debt and weak tests.
2. **L2 — OT Systems / Protocols** — PLC/DCS/SCADA/HMI/historian/RTU/IED/gateway integration and protocol/version drift.
3. **L3 — Data / Telemetry** — tags, signals, timestamps, units, quality flags, historian gaps and provenance inconsistencies.
4. **L4 — Asset / Configuration** — asset identity, firmware, topology, inventory, baselines and undocumented devices.
5. **L5 — Physical Process / Control** — process dependencies, operating envelopes, abnormal states and cyber-physical causality.
6. **L6 — Cyber Risk / Exposure** — vulnerabilities, access paths, segmentation, identity, remote access and contextual-risk gaps.
7. **L7 — Safety / Protection** — SIS, alarms, trips, interlocks, hazards, bypasses and fail-safe behavior.
8. **L8 — Operations / Maintenance** — work orders, operators, shifts, overrides, contractors, temporary changes and workarounds.
9. **L9 — Enterprise / IT-OT Ecosystem** — SOC/SIEM, CMMS/EAM, ERP/MES, IAM/PAM, vendors and enterprise dependencies.
10. **L10 — Resilience / Recovery** — containment, degraded operation, continuity, backups, restoration, DR and safe restart.
11. **L11 — Decision Intelligence Gaps** — alert overload, weak contextual risk, poor causal reasoning, limited prediction and uncertainty handling.
12. **L12 — Autonomy / Safety / Assurance** — authority boundaries, bounded autonomy, HITL, safety validation, TEVV, governance and auditability.

Every layer should be investigated through **Imperfection, Inconsistency, Friction, Complexity, Volatility, Uncertainty, Hidden Dependency and Unknown Unknown**.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_data.py --check-only
python -m ot_command.cli diagnostics
pytest -q
```

Optional read-only API and command-room UI (full Windows/macOS/Docker steps: `apps/command_center/README.md`):

```powershell
$env:PYTHONPATH = "src"
$env:AI_ENABLED = "0"
python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

UI: http://127.0.0.1:8000/ui (`AI_ENABLED=0` by default). `GET /` is 404; the product surface is `/ui`.

## Repo 3.0 status

This tree is **production-oriented synthetic advisory software**. Structured specs live in `specs/` (OM 1–13 freeze, refined with as-built C4). Accepted ADRs live in `adrs/`. Traceability and open decisions live in `traceability/`. ENH-01…10 engines live in `src/ot_command/core/` (not a rewrite of `legacy_*`). Ops pack, FinOps design, and readiness checklist live in `ops/`. Decision traces append to `data/local/decision_traces.jsonl` (gitignored).

**Legacy behavior is preserved:** `legacy_rank` / `legacy_recovery_ready` / `legacy_isolation_recommendation` and the three strict XFAIL tests are unchanged. Seeded `data/` contradictions were not cleaned. The API is GET-only for OT plus `POST /recommend` (recommendation packet, not an OT action). Gold GETs include `/graph/slice`. Ops views: `GET /ops/slo`, `GET /ops/cost-per-incident`.

| Dimension | Repo 1.0 | Repo 2.0 | Repo 3.0 |
|---|---|---|---|
| Stage | Baseline | Modernized (structure) | Modernized (engines + ops) |
| Nature | Brownfield sim | SDD-aligned | Production-oriented synthetic |
| Specs | `docs/` scattered | structured `specs/` | refined + as-built C4 |
| Controls | weak | traceability + gates | + guardrails + traces + SBOM freeze |
| Validation | 3 pass / 3 xfail | spec-aligned | readiness-focused (harness + assurance) |
| Outcome | messy repo | improved repo | **PRD + App ready** |

Gates: `python scripts/check_sdd_gates.py` (`make sdd-gates`); `specs/REPO_3_0_GATE.md`; `participant/work/enh_10/REPO_3_0_GATE.md`. Coverage: `participant/work/FDE_96_COVERAGE.csv`. Default: `AI_ENABLED=0`.

## Participant path

Read `AGENTS.md` → `specs/README.md` → `participant/CHALLENGE_BRIEF.md` → `docs/02_imperfection_layers.md` → `data/manifest.json` → `src/ot_command/legacy/`. ENH starts at FR-001 (`specs/14_delivery_spec.md`).


## Safety

This repository is synthetic and **does not connect to real industrial equipment**. No code performs PLC writes, safety changes, network blocking or real control actions. IsolationRecommendation is not IsolationExecution. CURRENT backup is not RecoveryReady. Highest CVSS is not highest operational risk.

## V2 reliability profile

This repository intentionally preserves domain-realistic brownfield contradictions and expected-failure tests while accidental packaging, import, stale-metadata and distributable-content defects are treated as release blockers. All external integrations are synthetic or read-only simulation surfaces; no real clinical, military, robotic, or OT control endpoint is configured. See `VERIFICATION.md` and `docs/07_v2_audit_and_changelog.md`.
