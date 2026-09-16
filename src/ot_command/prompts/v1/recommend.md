# prompt-v1 recommend

Draft a recommendation packet. Enum: MONITOR | DO_NOT_ISOLATE | ABSTAIN | ISOLATE_DRAFT (or RECOMMEND_CONTAINMENT_REVIEW synonym).
Recommend is ACTION_TIERS 1. executed remains false. AwaitAuthorization cannot close (OPEN-001).
Do not flip engine rank, RecoveryReady, or isolation enum. Explainer model substitution must not change those outputs.
