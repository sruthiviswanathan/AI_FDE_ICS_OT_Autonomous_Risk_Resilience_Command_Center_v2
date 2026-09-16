# AI FDE Brownfield Repo v2 — ICS/OT Autonomous Risk & Resilience Command Center

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

Optional read-only API:

```bash
uvicorn ot_command.api:app --reload
```

Set `PYTHONPATH=src` if your IDE does not infer it.

## Repo 3.0 status

This tree is **production-oriented (synthetic)** and **PRD + App ready**. Structured specs live in `specs/`; ADRs in `adrs/`; traceability in `traceability/`. Modern engines live in `src/ot_command/core/` (ENH-01…10 complete). Ops pack in `ops/`. Assurance in `assurance/ASSURANCE_REPORT.md`.

| Property | Repo 3.0 |
|----------|----------|
| Maturity | Governed advisory increment with eval harness + ops telemetry |
| Specs | Refined freeze + as-built C4 (`specs/as_built_c4.md`) |
| Validation | 31/31 golden evals, red team, readiness checklist |
| API | Read-only gold GETs + local `POST /recommend`, `POST /eval/run` |
| AI | Disabled by default (`AI_ENABLED=0`) — deterministic core (ADR-12) |

**Legacy behavior preserved:** `legacy_*` and three strict XFAIL tests unchanged. Seeded `data/` contradictions not cleaned. No OT execute surfaces.

```bash
make ci          # sdd-gates + verify + test + eval + red-team
make eval        # EVAL-001…031 harness
uvicorn ot_command.api:app --reload   # PYTHONPATH=src
```

Gate: `specs/REPO_3_0_GATE.md` · Coverage: `participant/work/FDE_96_COVERAGE.csv`

## Participant path

Read `AGENTS.md` → `specs/PRD.md` → `specs/APP_ACCEPTANCE_TESTS.md` → `assurance/ASSURANCE_REPORT.md`. Next: **APP-01** / **APP-02**.


## Safety

This repository is synthetic and **does not connect to real industrial equipment**. The API is read-only. No code performs PLC writes, safety changes, network blocking or real control actions.

## V2 reliability profile

This repository intentionally preserves domain-realistic brownfield contradictions and expected-failure tests while accidental packaging, import, stale-metadata and distributable-content defects are treated as release blockers. All external integrations are synthetic or read-only simulation surfaces; no real clinical, military, robotic, or OT control endpoint is configured. See `VERIFICATION.md` and `docs/07_v2_audit_and_changelog.md`.
