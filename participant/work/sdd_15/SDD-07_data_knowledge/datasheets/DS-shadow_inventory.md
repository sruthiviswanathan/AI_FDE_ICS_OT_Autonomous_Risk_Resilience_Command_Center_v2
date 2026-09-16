# Datasheet — Shadow spreadsheet inventory

**ID:** D-SHI · **Path:** `data/shadow/ot_asset_inventory_FINAL_v8.csv` · **n=220**  
**Context:** Identity (shadow) · **Claim type:** shadow evidence  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** same columns as `assets.csv`; 220 rows; **all** `asset_id` ⊆ `assets.csv`; firmware_diff **0**, observed_diff **0**, registered_diff **0**, ip_diff **0**, type_diff **0** (profile 2026-09-16). Shift email: “Asset list in spreadsheet is newer than CMDB for the new gateway.”  
**Assumption:** filename `FINAL_v8` is theatre, not authority.  
**Unknown:** OPEN-015 which inventory wins; which “new gateway” the email means (no unique unmatched row in this file).  
**Did not conclude:** spreadsheet is newer. **Did not conclude:** CMDB is newer.

## Motivation / intended use

Keep disagreement **visible** (CTQ-ID / EVAL-001). Poisoning/surface for SDD-08: a model that silently prefers this file would invent a CMDB.

## Composition

Subset overlay of Identity fields. No extra columns. No `source_system` column. No gateway-only delta.

## Lineage

**Unread by `run_diagnostics()`, API, sqlite.** Human war-room only (SDD-02 TB-5). Must not be an ETL master.

## Quality

**Intentional friction:** email vs file. **Observed:** no cell-level delta vs assets on the compared fields — so the spreadsheet is **not** a demonstrated newer CMDB; it is still evidence that a shadow path exists.

This is **intentional evidence of a parallel register**, not a defect to “fix” by deleting the file.

## Provenance requirement

`source_system=SHADOW_SPREADSHEET`, `source_path`, `confidence=low`, never overwrite RegisteredState/ObservedState without a human OPEN-015 decision.

## Access

Workshop FDE evidence read. HTTP unread. Future SOC **must not** load as CMDB. Vendors deny. Public deny.

## Representativeness / gaps

220/2016 overlay only. Cannot represent a real plant’s Excel estate. G-12: no measurable “newer gateway” in cells.

## Must not

**Promote this file to the new CMDB.** Silent upsert onto `assets.csv`. Drop it as “dirt.”
