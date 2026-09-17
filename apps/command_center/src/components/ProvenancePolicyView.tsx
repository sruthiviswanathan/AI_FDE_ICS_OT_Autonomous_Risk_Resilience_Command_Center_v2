import { api } from "../api/client";
import { useFetch } from "../hooks/useFetch";
import { ErrorBlock, LoadingBlock } from "./StateViews";
import { fmt } from "../utils/format";

export function ProvenancePolicyView({ lookupKey }: { lookupKey: number }) {
  const policy = useFetch(() => api.authority(), [lookupKey]);

  if (policy.loading) return <LoadingBlock label="Loading ACTION_TIERS…" />;
  if (policy.error) return <ErrorBlock message={policy.error} />;

  const data = policy.data || {};
  const actions = (data.actions as { action: string; tier: number; autonomous: boolean }[]) || [];
  const tier3 = (data.human_authorize_tier3 as string[]) || [];
  const tier4 = (data.refuse_tier4 as string[]) || [];

  return (
    <div className="provenance-policy">
      <p className="ai-off-note">{fmt(data.note)}</p>
      <p className="mono provenance-policy-meta">
        {fmt(data.policy_version)} · default unknown tier {fmt(data.unknown_action_default_tier)}
      </p>
      <h4 className="provenance-subheading">Tier 3 — human authorize</h4>
      <ul className="provenance-evidence-list mono">
        {tier3.map((a) => (
          <li key={a}>{a}</li>
        ))}
      </ul>
      <h4 className="provenance-subheading">Tier 4 — refuse / no execute</h4>
      <ul className="provenance-evidence-list mono">
        {tier4.slice(0, 12).map((a) => (
          <li key={a}>{a}</li>
        ))}
        {tier4.length > 12 && <li className="ai-off-note">+{tier4.length - 12} more</li>}
      </ul>
      <h4 className="provenance-subheading">Full catalog ({actions.length})</h4>
      <ul className="provenance-evidence-list mono">
        {actions.slice(0, 15).map((a) => (
          <li key={a.action}>
            tier {a.tier}: {a.action}
            {a.autonomous ? " · autonomous OK" : ""}
          </li>
        ))}
      </ul>
    </div>
  );
}
