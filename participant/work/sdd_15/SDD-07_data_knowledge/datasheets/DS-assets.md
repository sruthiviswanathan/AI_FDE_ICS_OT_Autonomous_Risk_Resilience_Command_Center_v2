# Datasheet — Assets

**ID:** D-AST · **Path:** `data/raw/assets.csv` · **n=2016** (manifest)  
**Context:** Identity · **Claim type:** RegisteredState **and** ObservedState in the **same row**  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** header `asset_id,plant_id,asset_type,vendor,model,firmware,ip_address,zone,protocol,registered_state,observed_state,criticality,owner,backup_age_days`; diagnostics `asset_state_conflicts=200`; SDD-06 §1.1–1.2.  
**Assumption:** `asset_type` is a class label, not a live device census.  
**Unknown:** OPEN-025 (no `device` column); OPEN-020 (tag join coverage).  
**Did not conclude:** which state is “true”; CMDB vs field.

## Motivation / intended use

Workshop identity grain for disagreement visibility (EVAL-001). **Not** a CMDB of record. **Not** a control target list.

## Composition

| Item | Value |
|---|---|
| Grain / PK | Asset / `asset_id` (OT-00001 …) |
| Plants | 18 (`plant_id`) |
| `asset_type` | DCS_CONTROLLER 176, NETWORK_SWITCH 172, GATEWAY 167, ENG_WORKSTATION 164, SAFETY_PLC 162, PLC 153, IED 151, SENSOR 151, HISTORIAN 150, OPC_SERVER 149, HMI 149, RTU 142, VFD 130 |
| RegisteredState | ACTIVE 1776, UNKNOWN 122, RETIRED 118 |
| ObservedState | ONLINE 1656, INTERMITTENT 129, UNSEEN 128, OFFLINE 103 |
| AssetCriticality | HIGH 776, CRITICAL 618, MEDIUM 461, LOW 161 |
| owner | OT Security 349, Unknown 343, Maintenance 341, Vendor 333, Operations 331, Engineering 319 |
| zone | L3_SITE_OPS 426, L0_FIELD 420, L1_CONTROL 417, DMZ 377, L2_SUPERVISORY 376 — **labels, not enforced segmentation** |
| Freshness | `backup_age_days` only — **not** RecoveryReady (SDD-06 §1.5) |
| Collection | Synthetic seed `20260910` via `scripts/generate_data.py` |

No `source_system` on the row. Two truths share one file.

## Lineage

File → `rows('data/raw/assets.csv')` → `asset_state_conflicts` (ACTIVE ∧ {OFFLINE,UNSEEN} only) → `/diagnostics`.  
Twin in `data/ot_legacy.db` table `assets` (set-equal; unread by diagnostics).  
v1/v2 asset APIs **unimplemented**.

## Quality (intentional)

- 200 ACTIVE vs OFFLINE/UNSEEN (diagnostics). Example pattern: OT-01016 registered ACTIVE observed UNSEEN (SDD-03 trace).
- RETIRED ∩ ONLINE **99** (OT-00528) **not** in the diagnostic counter.
- owner Unknown 343 — not DecisionAuthority.

## Provenance requirement

Split on ingest: `{RegisteredState, provenance=INVENTORY_REGISTERED}` and `{ObservedState, provenance=OBSERVATION}` plus `source_path`, `extracted_at`, `confidence` when they disagree.

## Access

Workshop FDE: full read. HTTP: integer only. Production: plant-scoped; vendors **deny** all-plants. Operational-truth permission: UNKNOWN.

## Representativeness / gaps

Synthetic 18 plants, not a real fleet. 182/2016 assets have tags — process joins from this table alone are incomplete (G-07). Do not invent Device.

## Must not

Treat filename as master. Collapse into one `status`. Use `backup_age_days` as RecoveryReady. Use AssetCriticality as isolate permission.
