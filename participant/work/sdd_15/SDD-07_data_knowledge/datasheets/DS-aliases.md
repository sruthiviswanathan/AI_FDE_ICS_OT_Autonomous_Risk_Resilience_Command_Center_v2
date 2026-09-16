# Datasheet — Asset aliases

**ID:** D-ALS · **Path:** `data/raw/asset_aliases.csv` · **n=6048**  
**Context:** Identity · **Claim type:** registered (CMDB, CMMS) + observed-like (PASSIVE)  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** header `asset_id,source,alias`; sources CMDB 2016, PASSIVE 2016, CMMS 2016; `alias_collisions=5`; EVAL-001.  
**Assumption:** 3× coverage is **source coverage**, not reconciliation.  
**Unknown:** OPEN-015 (shadow vs these aliases).  
**Did not conclude:** CMDB wins.

## Motivation / intended use

Force multi-source identity. EVAL-001 must_include evidence, source, confidence; must_not assume CMDB always correct.

## Composition

| Item | Value |
|---|---|
| Grain | one alias row per (`asset_id`,`source`) — **alias string is not a key** |
| `source` | {CMDB, PASSIVE, CMMS} exactly once per asset |
| Colliding aliases | `PLT-01-DCS_CONTROLLER-105`, `PLT-01-ENG_WORKSTATION-244`, `PLT-13-PLC-850`, `PLT-14-GATEWAY-737`, `PLT-15-VFD-444` — all PASSIVE vs PASSIVE |
| Example | PASSIVE `PLT-01-DCS_CONTROLLER-105` → **OT-00012** and **OT-00033** |
| Freshness | **none** |
| Collection | synthetic generator |

## Lineage

File → `rows(...)` → `Counter(alias)` → `alias_collisions=5`. Not in sqlite. Not in HTTP except the integer.

## Quality (intentional)

Five collisions are **seeded evidence**, not merge candidates. Do not collapse OT-00012 and OT-00033.

## Provenance requirement

Each alias: `source_system` = `source` field, `source_path`, `confidence` < 1 if collision or Registered/Observed conflict on the same `asset_id`.

## Access

Workshop FDE full read. Production: plant-scoped. Vendors deny. Do not publish collision maps as a “golden CMDB.”

## Representativeness / gaps

Every asset has three aliases by construction — not representative of messy real naming **coverage**. Collisions **are** representative of the identity problem this repo exists to show.

## Must not

Use alias as Asset. Use CMDB source as master. Treat collision as a data-entry bug to silently delete.
