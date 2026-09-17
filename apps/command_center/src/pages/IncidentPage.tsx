import { api } from "../api/client";
import { GraphSliceView } from "../components/GraphSliceView";
import { PageLookup } from "../components/PageLookup";
import { ErrorBlock, GraphAsyncContent, LoadingBlock, UntrustedBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";

export function IncidentPage() {
  const { plantId, assetId, alertId, scenario, setScenario, lookupKey } = useApp();
  const graph = useFetch(
    () => api.graphSlice({ query: "Q5", plant_id: plantId, asset_id: assetId, alert_id: alertId || undefined }),
    [plantId, assetId, alertId, lookupKey],
  );
  const scenarioData = useFetch(
    () => (scenario === "cascade_001" ? api.scenario("cascade_001") : Promise.resolve(null)),
    [scenario],
  );
  const timelineFixture = scenarioData.data?.timeline_fixture as { timeline?: { time: string; event: string }[] } | undefined;
  const shift = useFetch(() => api.shiftNotes(), [lookupKey]);

  const timeline = timelineFixture?.timeline || [];

  return (
    <div>
      <h2 className="page-title">Incident Context Graph</h2>
      <PageLookup />
      <div className="btn-row">
        <button type="button" className="primary" onClick={() => setScenario("cascade_001")}>
          Load CASCADE-001
        </button>
      </div>

      {scenario === "cascade_001" && timeline.length > 0 && (
        <>
          <h3 className="section-title">Timeline ({scenarioData.data?.binding?.title || "cascade_001"})</h3>
          <div className="timeline">
            {timeline.map((t) => (
              <div key={t.time} className="timeline-item">
                <span className="time">{t.time}</span>
                {t.event}
              </div>
            ))}
          </div>
        </>
      )}

      {shift.data && (
        <div className="card untrusted-border">
          <h3>
            Shift handover <UntrustedBadge />
          </h3>
          <div className="untrusted-panel">{shift.data.content}</div>
        </div>
      )}

      <div style={{ marginTop: "0.75rem" }}>
        <h3 className="section-title">Task-scoped graph (Q5)</h3>
        <GraphAsyncContent
          loading={graph.loading}
          error={graph.error}
          label="Loading incident cascade graph (Q5)…"
        >
          {graph.data && (
            <GraphSliceView
              data={graph.data}
              showVisualToggle
              defaultView="visual"
              focusAssetId={assetId || undefined}
            />
          )}
        </GraphAsyncContent>
      </div>
    </div>
  );
}
