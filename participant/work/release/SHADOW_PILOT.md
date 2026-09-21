# SHADOW_PILOT (pointer)

**Canonical REL-02 design:** [`ops/adoption.md`](../../../ops/adoption.md)

This path is the PRODUCT_READY expected filename. Content lives in the ops pack so runbooks, rollback, FinOps, and adoption stay one set.

| Asked | Where |
|-------|--------|
| Release manifest | `ops/adoption.md` §2 |
| Shadow vs `legacy_*` | §3.1 |
| Pilot + override log | §3.2, §6 |
| Advisory canary only | §3.3 — **never a live controller canary** |
| Autonomy still recommend-only | §4 until REL-04 |
| Rollback `AI_ENABLED=0` | §5 |
| Chaos drills on injects / CASCADE | §7 |
| Drift / cost / availability templates | §10 |
| Token economics / FinOps | §8 |
| AI-disabled drill | §9 |
| Change management + adoption metrics | §11–12 |
| Continuous evals | §13 |

`scripts/shadow_replay.py` is **not** added (untraced). Replay is `evals/harness.py` as documented in §3.1.
