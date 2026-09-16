# Datasheet — Remote access sessions

**ID:** D-RA · **Path:** `data/raw/remote_access_sessions.csv` · **n=700**  
**Context:** Cyber / Authority · **Claim type:** observed session + registered approval flags  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** header `session_id,asset_id,plant_id,identity,method,approved_window,start_time,end_time,mfa`; SessionIdentity site.engineer 158, shared_support 143, unknown 140, contractor 136, vendor.engineer 123; ApprovedWindow YES 563 NO 61 UNKNOWN 76 → diagnostics **137** ≠ YES; Mfa YES 572 NO 56 UNKNOWN 72 → **128** ≠ YES; methods jump_host 182, remote_desktop 179, local_service_laptop 170, vendor_vpn 169.  
**Assumption:** synthetic labels, not real usernames (still **PII-class** in production — OPEN-024).  
**Unknown:** OPEN-001 who approved the window.  
**Did not conclude:** UNKNOWN window or MFA = approved. SessionIdentity ≠ AssetIdentity.

## Motivation / intended use

Unapproved / un-MFA visibility (inject_03). Privacy-by-Design: minimize identity in logs.

## Composition

| Item | Value |
|---|---|
| Grain / PK | session / `session_id` (RA-00001 …) |
| Clocks | `start_time`, `end_time` |
| Collection | synthetic; sqlite table name `remote_access` set-equal |

## Lineage

File → `approved_window != YES` and `mfa != YES` (UNKNOWN lumped with NO) → `/diagnostics`. No session API. `change_remote_access` is ACTION_TIERS 3 — **not implemented**.

## Quality (intentional)

137 + 128 fail-visible counters. `shared_support` / `unknown` are weak identity. Diagnostics hide UNKNOWN vs NO.

## Provenance requirement

`source_system=PAM_SYNTHETIC`, `source_path`, `event_time=start_time`, `extracted_at`. SessionIdentity stored with purpose limitation.

## Access (C45)

| Actor | Rule |
|---|---|
| Workshop FDE | full read of synthetic labels |
| Workshop HTTP | ints only |
| Future SOC | plant-scoped |
| Future vendor | **must not** see other vendors’ sessions or all-plants dump |
| Public | deny |

Minimize SessionIdentity in traces. No export of process recipes (none in this file).

## Representativeness / gaps

Not a real PAM. No HumanAuthorizationRecorded (G-03). Vendors.csv `remote_access` is a **support path label**, not a join to these sessions.

## Must not

Treat `identity=unknown` as a person. Treat ApprovedWindow YES as IsolateExecution authority. Implement vendor_vpn blocking in this repo.
