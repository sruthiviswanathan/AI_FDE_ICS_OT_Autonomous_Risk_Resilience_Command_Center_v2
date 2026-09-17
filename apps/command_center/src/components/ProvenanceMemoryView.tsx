import { useMemo } from "react";
import { api } from "../api/client";
import { useFetch } from "../hooks/useFetch";
import { traceMatchesContext } from "../utils/provenanceContext";
import { ErrorBlock, LoadingBlock } from "./StateViews";
import { fmt } from "../utils/format";

export function ProvenanceMemoryView({
  plantId,
  assetId,
  alertId,
  lookupKey,
}: {
  plantId: string;
  assetId: string;
  alertId: string;
  lookupKey: number;
}) {
  const traces = useFetch(() => api.traces(40), [lookupKey]);

  const filtered = useMemo(() => {
    const rows = traces.data?.traces ?? [];
    if (!plantId && !assetId && !alertId) return rows.slice(-15).reverse();
    const matched = rows.filter((t) =>
      traceMatchesContext(t as Record<string, unknown>, plantId, assetId, alertId),
    );
    return (matched.length ? matched : rows).slice(-15).reverse();
  }, [traces.data, plantId, assetId, alertId]);

  if (traces.loading) return <LoadingBlock label="Loading decision traces…" />;
  if (traces.error) return <ErrorBlock message={traces.error} />;

  if (!filtered.length) {
    return (
      <p className="ai-off-note">
        No decision traces persisted yet for this context. Traces append on recommendation / audit flows.
      </p>
    );
  }

  return (
    <ul className="provenance-evidence-list mono">
      {filtered.map((t) => {
        const row = t as Record<string, unknown>;
        return (
          <li key={String(row.decision_id || row.persisted_at)}>
            {fmt(row.persisted_at || row.timestamp)} · {fmt(row.action || row.purpose || row.decision_id)}
            {row.execute !== undefined && ` · execute=${fmt(row.execute)}`}
          </li>
        );
      })}
    </ul>
  );
}
