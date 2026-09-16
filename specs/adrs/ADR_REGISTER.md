# ADR register — SDD-14 freeze

Engagement-accepted for ENH. Not a production CAB. SDD-09 solution choice is not reopened.

| ID | Title | Source | Status | Notes |
|---|---|---|---|---|
| ADR-KG | Bounded evidence-graph view; decorative KG rejected | SDD-09 | Accepted | Five queries only |
| ADR-01 | Identity bundle; no silent winner | SDD-09 | Accepted | EVAL-001 |
| ADR-02 | Dual-clock telemetry provenance | SDD-09 | Accepted | EVAL-004 |
| ADR-03 | Contextual risk engine; no LLM re-rank | SDD-09 | Accepted | EVAL-002/017 |
| ADR-04 | Safety policy; no isolate execute | SDD-09 | Accepted | CTQ-ISO/0 |
| ADR-05 | RecoveryReady ≠ BackupCurrent | SDD-09 | Accepted | EVAL-005/018 |
| ADR-06 | Retrieval mix; vector untrusted only | SDD-09 | Accepted | Never policy |
| ADR-07 | One optional advisory agent | SDD-09 | Accepted | Functions first |
| ADR-08 | Evidence packet; no CoT authority | SDD-09 | Accepted | docs/06 |
| ADR-09 | Typed JSON persistence | SDD-10 | Accepted | Not RDF/Neo4j-now |
| ADR-10 | v1 operationalState is not ObservedState | SDD-10 | Accepted | OPEN-009 mapping |
| ADR-11 | Read-only API | SDD-11 | Accepted | No OT POST |
| ADR-12 | AI-disabled is core | SDD-11 | Accepted | EVAL-016 |
| ADR-13 | Model substitution port | SDD-11 | Accepted | OPEN-028 |
| ADR-14 | Autonomy = ACTION_TIERS; no ExecuteControl | SDD-12 | Accepted | EVAL-006 |
| ADR-15 | Guardrails after model | SDD-13 | Accepted | Prompt cannot raise tier |
| ADR-16 | SBOM/AIBOM; LLM-exit | SDD-13 | Accepted | Engines remain |

## Rejected directions (do not implement)

Unsafe autonomous OT agent · multi-agent · digital twin · isolate/PLC/SIS/firewall execute tools · RDF enterprise ontology · graph-as-CMDB · vector-as-policy.
