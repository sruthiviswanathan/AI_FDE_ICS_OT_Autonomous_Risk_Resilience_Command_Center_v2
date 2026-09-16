# Datasheet — Tag telemetry

**ID:** D-TEL · **Path:** `data/telemetry/tag_telemetry.jsonl` · **n=31224**  
**Context:** Telemetry · **Claim type:** observed  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** TEL-00000000 keys `event_id, tag_id, asset_id, event_time, ingest_time, value, unit, quality, source`; `contracts/telemetry_event_schema.json` required **without** ingest_time/source/asset_id; diagnostics 4094 / 120 / 47; ingest−event p50 **120s** max **240s** min **1s** (0 negative).  
**Assumption:** `source=HISTORIAN` on **all 31224** is a label, not a live PI/PHD.  
**Unknown:** OPEN-009 contract; cause of BAD vs sensor vs generator (L3 unknown unknown).  
**Did not conclude:** process healthy (OPEN-026). Quality GOOD ≠ ProcessHealthy.

## Motivation / intended use

EVAL-004 temporal order; quality-aware plots. Not control feedback. Not a digital twin.

## Composition

| Item | Value |
|---|---|
| Grain / PK | TelemetryEvent / `event_id` |
| Join | `tag_id` → `data/reference/tags.csv` (864; historian_enabled NO **51** still appear in feed) → `asset_id` / `unit_id` |
| TelemetryQuality | GOOD 27130, UNCERTAIN 2743, BAD 1351 |
| Dual clock | `event_time`, `ingest_time` (always ingest ≥ event in this seed) |
| Unit | record `unit`; tag `engineering_unit` — **47** `*_TEMP` with unit ≠ C (SDD-03: all F) |
| Duplicates | extra **120** on key (tag_id, event_time, value, unit) |
| Collection | synthetic JSONL |

## Lineage

File → `jsonl(...)` → quality/unit/duplicate counters → `/diagnostics`.  
Schema **does not validate** extra fields. Product does not join tags.csv.

## Quality

Intentional: BAD/UNCERTAIN volume, duplicates, unit mismatch, ingest lag.  
Accidental drift: schema thinner than records — **keep record fields**; widen contract (proposed DATA.md §9).

## Provenance requirement

Mandatory: `source_system` (today HISTORIAN), `source_path`, `event_time`, `ingest_time`, `quality_flag`, `extracted_at`. Do **not** sort on ingest_time alone.

## Access

Workshop FDE full read. HTTP: ints only. Production: need-to-know tags; never dump all plants’ values to vendors. No recipe/setpoint export (none here — keep).

## Representativeness / gaps

Lag is generated in 1–240s; **cannot** prove a real historian SLA. Tag coverage 182 assets only. G-01 schema gap. G-07 process join gap.

## Must not

Plot BAD as process truth. Infer ProcessHealthy from GOOD. Drop ingest_time to match the thin schema.
