# As-built C4 (Repo 3.0, synthetic)

**No actuator container.** Option A engines + Option B optional explainer. Option C rejected.

```text
[Person: SOC / PE / Safety / VP Ops]
        | HTTP (workshop; OPEN-029 no authn)
        v
[Container: Read-only API]
  GET /health /diagnostics
  gold GETs: identity, telemetry, risk, safety, recovery, recommendations,
             /authority/actions, /graph/slice
  GET /ops/slo /ops/cost-per-incident
  POST /recommend  (packet only — not OT)
        |
        v
[Container: Deterministic engines]
  identity · telemetry · risk · containment · recovery · graph_slice
  authority · guardrails · agent workflow · traces
        |
        +--> [Container: Eval harness] evals/harness.py
        +--> [Container: CLI diagnostics]
        +--> [Container: Optional explainer port] AI_ENABLED=0 default; OPEN-028
        x    [FORBIDDEN] actuator / PLC / SIS / isolate-execute / firewall execute
```

Bronze `data/` is untrusted as authority. Shadow + shift email = UNTRUSTED overlay. Decision traces append to `data/local/` (gitignored).

Normative architecture: `specs/11_ai_app_architecture.md`.
