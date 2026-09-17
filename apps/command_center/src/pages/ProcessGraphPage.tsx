import { api } from "../api/client";
import { GraphSliceView } from "../components/GraphSliceView";
import { PageLookup } from "../components/PageLookup";
import { GraphAsyncContent } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";

export function ProcessGraphPage() {
  const { plantId, assetId, lookupKey } = useApp();
  const slice = useFetch(
    () => api.graphSlice({ query: "Q2", plant_id: plantId, asset_id: assetId || undefined }),
    [plantId, assetId, lookupKey],
  );

  return (
    <div>
      <h2 className="page-title">Process / Dependency Graph</h2>
      <PageLookup />
      <GraphAsyncContent
        loading={slice.loading}
        error={slice.error}
        label="Loading process dependency graph (Q2)…"
      >
        {slice.data && (
          <GraphSliceView
            data={slice.data}
            showVisualToggle
            defaultView="visual"
            focusAssetId={assetId || undefined}
            expandable
          />
        )}
      </GraphAsyncContent>
      <p className="ai-off-note">Hop cap 8 · Forbidden: regional isolate action</p>
    </div>
  );
}
