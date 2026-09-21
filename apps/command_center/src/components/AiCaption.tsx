import { api } from "../api/client";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { ErrorBlock, LoadingBlock } from "./StateViews";

export function AiCaption() {
  const { plantId, assetId, alertId, aiMode, lookupKey } = useApp();
  const query = useFetch(
    () =>
      aiMode === "off" || !plantId
        ? Promise.resolve(null)
        : api.explain({ plantId, assetId: assetId || undefined, alertId: alertId || undefined }),
    [aiMode, plantId, assetId, alertId, lookupKey],
  );

  if (aiMode === "off") return null;
  if (!plantId) return <p className="ai-off-note">Select a plant to load the advisory caption.</p>;
  if (query.loading) return <LoadingBlock variant="compact" label="Loading advisory caption…" />;
  if (query.error) return <ErrorBlock message={query.error} />;
  if (!query.data) return null;

  return (
    <div className="card ai-caption">
      <h3>Advisory caption</h3>
      <p className="ai-caption-body">{query.data.caption}</p>
      <p className="ai-off-note">
        Template {query.data.explainer} · engines authoritative · citations {query.data.evidence_ids.join(", ") || "—"}
      </p>
      <p className="ai-off-note mono">{query.data.source_files.join(" · ")}</p>
    </div>
  );
}
