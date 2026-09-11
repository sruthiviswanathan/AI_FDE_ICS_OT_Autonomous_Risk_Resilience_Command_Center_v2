# L1–L12 Brownfield Imperfection Architecture

## L1 — Software / Engineering Logic
Duplicated rules, hard-coded risk thresholds, weak tests, stale configuration and scripts.

## L2 — OT Systems / Protocols
Mixed PLC/DCS/SCADA/HMI/historian/gateways; proprietary/legacy protocol behavior; interface drift.

## L3 — Data / Telemetry
Missing/duplicate/stale tags, unit mismatches, quality flags, clock drift, ingestion delay and weak provenance.

## L4 — Asset / Configuration
Competing inventories, aliases, firmware mismatches, undocumented devices and stale topology.

## L5 — Physical Process / Control
Control-loop and unit dependencies, abnormal states, safe-state constraints and cyber-physical causality.

## L6 — Cyber Risk / Exposure
Vulnerability severity disconnected from reachability, process criticality, safety consequence and recovery capability.

## L7 — Safety / Protection
SIS/interlocks/alarms/bypasses/proof-test state; security response can conflict with process safety.

## L8 — Operations / Maintenance
Work orders, field reality, shift handovers, temporary bypasses, contractor activity and workarounds.

## L9 — Enterprise / IT-OT Ecosystem
SOC/SIEM, CMMS/EAM, ERP/MES, IAM/PAM, vendors and external support all hold partial truth.

## L10 — Resilience / Recovery
Backups that may be stale, untested restore paths, missing runbooks, manual fallback and recovery dependency uncertainty.

## L11 — Decision Intelligence Gaps
Alert overload, weak contextual ranking, poor causal reasoning, limited prediction and uncertainty handling.

## L12 — Autonomy / Safety / Assurance
Human authority, bounded agency, safe action tiers, evidence, explainability, TEVV, auditability and governance.

Across every layer inspect: **Imperfection, Inconsistency, Friction, Complexity, Volatility, Uncertainty, Hidden Dependency, Unknown Unknown**.
