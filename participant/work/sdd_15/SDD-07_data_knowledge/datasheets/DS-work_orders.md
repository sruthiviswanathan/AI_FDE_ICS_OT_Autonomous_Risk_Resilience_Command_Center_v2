# Datasheet — Work orders

**ID:** D-WO · **Path:** `data/raw/work_orders.csv` · **n=1250**  
**Context:** MaintenanceWork (adjacent) · **Claim type:** CmmsStatus (registered) + FieldStatus (operational)  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** header `work_order_id,asset_id,plant_id,type,cmms_status,field_status,opened_at,closed_at,temporary_bypass,notes`; Cmms CLOSED 328, IN_PROGRESS 332, OPEN 303, DEFERRED 287; Field RTS 326, ACTIVE 314, DEGRADED 313, OUT_OF_SERVICE 297; `maintenance_state_conflicts=244`; WO-000009 pattern.  
**Assumption:** CMMS-like file, not Maximo/SAP live.  
**Unknown:** OPEN-017 notes vs SIS; vendor “awaiting vendor” 224 (SDD-02) is a string, not an SLA clock.  
**Did not conclude:** paper closed ⇒ restored.

## Motivation / intended use

Show maintenance dual-state. Feed Isolation/recovery **context**, not auto-close of cyber alerts.

## Composition

| Item | Value |
|---|---|
| Grain / PK | work order / `work_order_id` |
| type | INSPECTION 268, CALIBRATION 260, EMERGENCY 259, CM 236, PM 227 |
| Clocks | `opened_at`, `closed_at` (nullable when not closed) |
| `temporary_bypass` | flag on the WO — **not** SafetyBarrierState |
| Collection | synthetic; sqlite `work_orders` set-equal |

## Lineage

File → CLOSED ∧ field ≠ RTS → 244 → `/diagnostics`. No WO API. Shadow email claims vendor complete vs ticket — **do not overwrite** this file with email.

## Quality (intentional)

244 paper/field disagreements. Notes are canned (e.g. awaiting vendor, standard work). Dual timestamps exist; product does not compute cycle time (OPEN-006).

## Provenance requirement

Two facts per row: CmmsStatus (`source_system=CMMS`) and FieldStatus (`source_system=FIELD_REPORT` — **inferred grain**, not a separate file). Never one `status`.

## Access

Workshop FDE full. HTTP ints. Future: planners + ops; vendor sees **own** notes only if a later policy says so (OPEN). No public export.

## Representativeness / gaps

Not a real CMMS backlog. No technician identity table. `temporary_bypass=YES` is not Authorize for interlock bypass.

## Must not

Map CLOSED → ObservedState ONLINE. Map EMERGENCY → isolate. Use notes as trusted authority.
