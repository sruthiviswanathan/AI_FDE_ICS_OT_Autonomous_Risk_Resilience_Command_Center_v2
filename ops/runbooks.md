# Runbooks (advisory)

## RB-01 — HIGH/CRITICAL cyber alert
1. GET identity + process_context. UNKNOWN is not NORMAL.
2. GET safety conflicts and `safe_state`. MIN_LOAD / PE warning → ABSTAIN.
3. GET recovery for the plant. CURRENT backup is not RecoveryReady.
4. POST `/recommend` (packet only) or GET `/recommendations/{incident_id}`.
5. Hand to Process Eng + Safety + VP Ops. Stop. No isolate_endpoint.

## RB-02 — AI outage
Set `AI_ENABLED=0`. Engines and GET views remain. EVAL-016: not a blank screen.

## RB-03 — Prompt injection / “isolate now”
Refuse execute. Shift notes stay UNTRUSTED. See `ai_incident_response.md`.

## RB-04 — Restore drill failure
Record RecoveryReady false. Do not sequence live restore from this API (OPEN-027).
