# Datasheet — Enterprise events

**ID:** D-ENT · **Path:** `data/raw/enterprise_events.jsonl` · **n=6500**  
**Context:** Enterprise adjacent · **Claim type:** mixed observed/registered enterprise signals  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** keys `event_id, asset_id, plant_id, source, event_type, event_time, received_time, correlation_id, payload_state`; sources IAM 749, MES 747, HISTORIAN 741, EAM 724, SCADA 717, PASSIVE_DISCOVERY 712, CMMS 704, VENDOR_PORTAL 704, SIEM 702; types RISK_CHANGE 969, SESSION 959, HEARTBEAT 938, CONFIG_CHANGE 935, ALARM 906, WORK_ORDER 901, STATE_CHANGE 892; empty `correlation_id` **3251**; received_time **before** event_time **407** (EVT-0000001 SIEM CONFIG_CHANGE); payload_state NORMAL 1111, HOLD 1108, OFFLINE 1107, UNKNOWN 1081, MAINTENANCE 1058, DEGRADED 1035.  
**Assumption:** nine `source` strings are labels, not live connectors.  
**Unknown:** OPEN-012 incident case key; payload_state vs ObservedState / ProcessContext (not the same field).  
**Did not conclude:** an end-to-end case from correlation_id (majority empty).

## Motivation / intended use

Process mining (SDD-02): queues, lag, missing case keys. EVAL-004 dual clock (received vs event). Not a SOAR execute bus.

## Composition

| Item | Value |
|---|---|
| Grain / PK | event / `event_id` (EVT-0000001 …) |
| Dual clock | `event_time`, `received_time` (inversions **seeded**) |
| `correlation_id` | present or **empty** — empty ≠ “no incident,” it is missing join |
| Collection | synthetic JSONL; **not** in sqlite; **unread** by diagnostics |

## Lineage

File on disk only. SDD-02 mined it; product Measure does not. No enterprise API.

## Quality (intentional)

3251 missing case keys. 407 clock inversions. `payload_state` is **another** overloaded state-like field — must not replace ObservedState, SafetyBarrierState, or SocStatus. SIEM source ≠ cyber_alerts row.

## Provenance requirement

`source_system` = `source` field, `source_path`, `event_time`, `received_time`, `extracted_at`, `confidence` down if correlation empty or clocks invert. Do not sort on received_time alone.

## Access

Workshop FDE full. HTTP unread. Future: source-scoped (SOC sees SIEM/IAM; maintainers CMMS/EAM). VENDOR_PORTAL rows: that vendor only. Public deny. Minimize any future real identity in SESSION payloads (today `payload_state` only).

## Representativeness / gaps

Not a real IT-OT bus. G-08 / OPEN-012. No schema file for this JSONL (G-02). Cannot mine MTT contextualize (OPEN-006).

## Must not

Invent correlation ids to “complete” cases. Treat `source=SCADA` as live controller I/O. Treat `payload_state=OFFLINE` as ObservedState. Drive isolate from RISK_CHANGE events.
