# Shared constraints — every transformation prompt

Paste or `@`-mention this file at the start of every SDD, ENH, REL, PRD, and APP prompt. If a later instruction conflicts with this file, **this file wins**.

## Estate and engagement

This repository is a **synthetic, locally runnable multinational ICS/OT brownfield**. Leadership wants a global autonomous risk and resilience command center, but **no system holds a trusted cyber-physical truth**. The business problem is not “we lack another dashboard.”

Core forensic tension:

> Cyber state ≠ Operational state ≠ Safety state ≠ Resilience state

Five truths must stay distinct: **observed**, **registered**, **operational interpretation**, **safety**, **decision authority**.

## Hard safety bounds

- Do not connect to real OT systems or produce code that writes to controllers.
- Never recommend or implement live PLC/DCS writes, setpoint changes, SIS modifications, interlock bypasses, trip suppression, unsafe restart, or automatic isolation.
- Allowed autonomous behavior: collect, correlate, enrich, summarize, rank evidence, read-only simulation.
- Policy-controlled reversible (design only): request fresh telemetry, open a ticket, increase logging, capture evidence.
- Human-authorized only: network isolation, remote-access change, firewall change, maintenance-mode transition.
- Every recommendation must expose: evidence, source, freshness, uncertainty, process impact, safety impact, rollback, required authority.

## Evidence rules

- Preserve intentional brownfield contradictions. Do **not** silently clean `data/` inconsistencies.
- Do not treat CMDB, passive discovery, historian, SCADA, CMMS, SIEM, or operator notes as authoritative **by name**.
- Never rank operational risk by CVSS alone.
- Never declare recovery ready because `backup_status == CURRENT`.
- Do not use `restricted_answer_key/`.
- Highest CVSS is not highest operational risk. Always consider reachability, process criticality, safety barrier state, compensating controls, and recovery capability.
- ISO/IEC 42001, 42005, and EU AI Act are **methods** to apply. Do not invent a certification.

## Architecture judgement

Knowledge graph, digital twin, RAG, and agents are **intervention options, not defaults**. Use them only when prior-stage evidence shows they solve a real identity, temporal, safety, recovery, or authority problem.

Keep `src/ot_command/legacy/` as the as-is baseline. Add a parallel modern path. Do not “fix” `legacy_*` by deleting the defect until a new function is proven by tests and the ADR says the legacy path is a comparison shim.

## Spec-driven execution

- Read prior-stage artifacts before writing new ones.
- If a required upstream artifact is missing, **stop** and say which prompt must be re-run.
- Prefer tests/evals **before** agentic automation.
- Cite repository evidence (file path + finding) rather than inventing plant facts.
- Seeded diagnostic counts in `VERIFICATION.md` / `run_diagnostics()` are the quantitative baseline unless re-measured from data.

## Output quality

Write artifacts that a subsequent FDE agent can implement without re-discovering the estate. Use explicit IDs (`FR-###`, `ADR-###`, `EVAL-###`, `NFR-###`, `OPEN-###`). Mark uncertainty as uncertainty.
