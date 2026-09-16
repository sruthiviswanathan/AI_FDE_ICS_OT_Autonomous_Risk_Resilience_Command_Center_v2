# prompt-v1 gather

Call read-only getters only: identity, telemetry quality, contextual risk, safety conflicts, recovery, authority catalog, isolation-consequence simulation (view).
Envelope required: actor, purpose, plant_id, as_of, policy_version. Missing field → deny.
Cite file, field, record id, freshness. UNKNOWN is not permission.
Max 12 steps / 20 tool calls. Repeat tool+args → abort.
