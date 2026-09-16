# Datasheet — Safety barriers

**ID:** D-SAF · **Path:** `data/raw/safety_barriers.csv` · **n=450**  
**Context:** Safety · **Claim type:** recorded SafetyBarrierState (not live SIS)  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** header `barrier_id,plant_id,unit_id,barrier_type,state,proof_test_status,bypass_authorized`; state ACTIVE 389, DEGRADED 35, BYPASSED 26; proof CURRENT 377, DUE 29, OVERDUE 44; bypass NO 157, UNKNOWN 157, YES 136; diagnostics lump ≠ACTIVE → 61 and ≠CURRENT → 73; PLT-03-SAFE-14 BYPASSED authorized NO on MIN_LOAD (SDD-03).  
**Assumption:** rows are **records**, not a connected safety PLC.  
**Unknown:** bypass age clock (OPEN-006 aging KPI).  
**Did not conclude:** permission to bypass. UNKNOWN ≠ permission. Tier 4 `bypass_interlock` remains forbidden in software.

## Motivation / intended use

Constrain IsolationRecommendation (CTQ-ISO / EVAL-003). Never an actuation interface.

## Composition

| Item | Value |
|---|---|
| Grain / PK | Barrier / `barrier_id` (e.g. PLT-01-SAFE-01) |
| Join | `unit_id` → ProcessUnit SafeState |
| barrier_type | INTERLOCK 101, PERMISSIVE 100, RELIEF 91, ALARM 85, SIS_TRIP 73 |
| Freshness | ProofTestStatus **label only** — no proof-test date |
| Collection | synthetic; sqlite `safety_barriers` set-equal |

## Lineage

File → diagnostics **collapsed** counters (BYPASSED+DEGRADED; DUE+OVERDUE) → `/diagnostics`. No row-level safety API. Isolate legacy path **does not read this file**.

## Quality (intentional)

61 non-ACTIVE; 73 proof not CURRENT; 157 bypass UNKNOWN. Diagnostics hide the BYPASSED vs DEGRADED split.

## Provenance requirement

`source_system=SAFETY_REGISTER`, `source_path`, `extracted_at`, quality/confidence down if bypass_authorized=UNKNOWN or proof OVERDUE. Keep state, proof, and bypass as **three fields**.

## Access

Workshop FDE full. HTTP ints only. Future Safety read; **no write**. SOC read. Vendors deny. Public deny.

## Representativeness / gaps

Not live restore of SIS logic. No trip logs. G-04 class: no proof-test certificates on disk.

## Must not

Implement bypass_interlock. Treat ALARM type as SIS_TRIP. Treat ACTIVE as ProcessHealthy. Collapse with SocStatus or ObservedState.
