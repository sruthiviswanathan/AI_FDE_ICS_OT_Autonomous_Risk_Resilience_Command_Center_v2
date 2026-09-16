# Datasheet — Vulnerability findings

**ID:** D-VUL · **Path:** `data/raw/vulnerabilities.csv` · **n=1100**  
**Context:** Cyber · **Claim type:** registered finding  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** header `finding_id,asset_id,severity,cvss,exploitability,network_reachable,compensating_control,status`; SDD-03 830/1100 label≠CVSS-band; 53 cvss≥9 ∧ reachable NO; `legacy_rank` sorts cvss only.  
**Assumption:** scanner-like synthetic findings; not a live Qualys/Tenable feed.  
**Unknown:** no process-unit field on the finding (join only via asset→tag→unit, sparse).  
**Did not conclude:** patch priority. Highest Cvss ≠ ContextualOperationalRisk.

## Motivation / intended use

EVAL-002 contextual rank. **Anti-use:** CVSS-only queue.

## Composition

| Item | Value |
|---|---|
| Grain / PK | Finding / `finding_id` (VUL-00001 …) |
| FindingSeverityLabel `severity` | HIGH 302, LOW 288, MEDIUM 255, CRITICAL 255 |
| Cvss | numeric; do not band-trust against `severity` |
| Reachability | YES 373, NO 383, UNKNOWN 344 |
| CompensatingControl | ALLOWLIST / MONITORED / SEGMENTED / NONE / UNKNOWN (label, not proven) |
| **FindingDisposition** (`status` column) | OPEN 799, MITIGATED 166, ACCEPTED 135 — **not** SocStatus |
| Freshness | **none** |
| Collection | synthetic; copied in sqlite `vulnerabilities` |

## Lineage

File present. **`run_diagnostics()` does not read it.** sqlite twin set-equal. `legacy_rank` would consume dicts in tests only.

## Quality (intentional)

Label vs score mismatch (e.g. VUL-00008 CRITICAL / cvss 4.1 — SDD-03). Reachability UNKNOWN is not YES. ACCEPTED disposition is not named-human Authorize (OPEN-001).

## Provenance requirement

`source_system=SCANNER_SYNTHETIC` (or named if later split), `source_path`, `extracted_at`, `confidence` down when reachable UNKNOWN or no unit join.

## Access

Workshop FDE full. HTTP unread. Future SOC: plant-scoped. Safety: join only, not a CVSS wall. Vendors deny. Public deny.

## Representativeness / gaps

No KEV/EPSS. No first-found date. G-11 product unread. Column name `status` is G-14 — pipelines must emit FindingDisposition.

## Must not

Rank by Cvss alone. Treat CRITICAL label as isolate. Treat MITIGATED as RecoveryReady or SafetyBarrierState ACTIVE.
