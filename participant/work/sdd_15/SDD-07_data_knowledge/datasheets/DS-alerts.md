# Datasheet — Cyber alerts

**ID:** D-ALT · **Path:** `data/raw/cyber_alerts.csv` · **n=2800**  
**Context:** Cyber · **Claim type:** SOC registered + OperationalInterpretation (`process_context`)  
**Date profiled:** 2026-09-16

## Evidence / assumptions / unknowns / did not conclude

**Evidence:** header `alert_id,asset_id,plant_id,timestamp,type,severity,soc_status,process_context`; SocSeverity CRITICAL 199 HIGH 661; process_context UNKNOWN 1735; `legacy_isolation_recommendation` HIGH/CRITICAL → `"ISOLATE"`; 860 HIGH+CRIT (SDD-03).  
**Assumption:** SIEM-like file, not a live SIEM.  
**Unknown:** OPEN-017 SOC SUPPRESSED ≠ SIS trip suppression.  
**Did not conclude:** isolation execute. SocSeverity ≠ IsolationRecommendation.

## Motivation / intended use

War-room queue **with** ProcessContext and Safety join. Not an autonomous isolate trigger.

## Composition

| Item | Value |
|---|---|
| Grain / PK | alert / `alert_id` (ALT-000001 …) |
| Clock | `timestamp` only — **no ingest/received** (gap vs EVAL-004 naming) |
| `type` | AUTH_ANOMALY 429, MALWARE_SIGNAL 418, UNEXPECTED_WRITE 404, POLICY_VIOLATION 400, NEW_DEVICE 399, CONFIG_DRIFT 388, PROTOCOL_ANOMALY 362 |
| SocSeverity | MEDIUM 1131, LOW 809, HIGH 661, CRITICAL 199 |
| SocStatus | TRIAGED 724, CLOSED 700, OPEN 693, SUPPRESSED 683 |
| ProcessContext | UNKNOWN 1735, MAINTENANCE_WINDOW 357, NORMAL 354, DEGRADED 354 |
| Collection | synthetic CSV; **not** in sqlite |

## Lineage

**Unread by diagnostics and API.** Humans / future risk engine only. Isolation string today comes from `legacy_isolation_recommendation(severity)`, not from this file’s other columns.

## Quality (intentional)

525/860 HIGH+CRIT with UNKNOWN process_context (SDD-03). SUPPRESSED is a SOC ticket state. NEW_DEVICE type is not AssetIdentity.

## Provenance requirement

`source_system=SIEM_SYNTHETIC`, `source_path`, `event_time=timestamp`, ingest **missing** (G-02 class), `confidence` low when ProcessContext UNKNOWN.

## Access

Workshop FDE full. HTTP unread. Future SOC plant-scoped. Vendors deny. Do not ship all-estate alert dumps.

## Representativeness / gaps

No correlation to `enterprise_events.correlation_id`. No IsolationRecommendation column (correct — must be **derived** with BR-10). G-11 unread by product.

## Must not

Map HIGH/CRITICAL → isolate execute or even an un-packeted ISOLATE string. Treat SocStatus CLOSED as process restored (use FieldStatus / ObservedState).
