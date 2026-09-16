import { api } from "../api/client";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";

export function ProcessGraphPage() {
  const { plantId, assetId } = useApp();
  const slice = useFetch(() => api.graphSlice({ query: "Q2", plant_id: plantId, asset_id: assetId }), [plantId, assetId]);

  if (slice.loading) return <LoadingBlock />;
  if (slice.error) return <ErrorBlock message={slice.error} />;

  return (
    <div>
      <h2 className="page-title">Process / Dependency Graph</h2>
      <div className="advisory-footer">Undocumented network paths: 779 (estate) — blast radius may be UNKNOWN.</div>
      <pre className="mono">{JSON.stringify(slice.data, null, 2)}</pre>
      <p className="ai-off-note">Hop cap 8 · Forbidden: regional isolate action</p>
    </div>
  );
}
