# SBOM / requirements freeze — workshop (ADR-16)

**Evidence used:** `requirements.txt` pins; `pyproject.toml`; OPEN-024 SPDX recopy pending.  
**Assumptions:** Local workshop supply-chain note — not production SBOM attestation.  
**Unknowns:** OPEN-024 full SPDX recopy; OPEN-028 model card.  
**Did not conclude:** signed SBOM; counsel approval.

## Pinned runtime (2026-09-16)

| Package | Version | Role |
|---|---|---|
| fastapi | 0.115.0 | Read-only API |
| uvicorn | 0.30.6 | Workshop server |
| pydantic | 2.9.2 | Request models |
| pytest | 8.3.3 | TEVV / red team |

## AIBOM placeholder

| Component | Version | Notes |
|---|---|---|
| Explainer LLM | **none** (AI_ENABLED=0) | OPEN-028 |
| Embeddings / vector | **off** | ADR-06 |

## Exit strategy

`AI_ENABLED=0` → deterministic engines + tables remain (ADR-12). No OT connectors added in ENH-08.
