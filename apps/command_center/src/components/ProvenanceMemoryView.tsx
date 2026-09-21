import { useMemo } from "react";
import { api } from "../api/client";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";
import type { PageProvenance } from "../utils/pageProvenance";
import { traceMatchesContext } from "../utils/provenanceContext";
import { ErrorBlock, LoadingBlock } from "./StateViews";

export function ProvenanceMemoryView({
  plantId,
  assetId,
  alertId,
  lookupKey,
  page,
}: {
  plantId: string;
  assetId: string;
  alertId: string;
  lookupKey: number;
  page: PageProvenance;
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

  return (
    <div>
      <p className="ai-off-note">{page.memoryNote}</p>
      <p className="mono provenance-policy-meta">source_path data/local/decision_traces.jsonl</p>
      {!filtered.length ? (
        <p className="ai-off-note">
          No decision traces persisted yet for this context. Traces append on recommendation / audit flows.
        </p>
      ) : (
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
      )}
    </div>
  );
}
