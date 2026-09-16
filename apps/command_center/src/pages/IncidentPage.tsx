import { api } from "../api/client";
import { GraphSliceView } from "../components/GraphSliceView";
import { PageLookup } from "../components/PageLookup";
import { ErrorBlock, LoadingBlock, UntrustedBadge } from "../components/StateViews";
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
          <h3 className="section-title">Timeline</h3>
          <div className="timeline">
            {timeline.map((t) => (
              <div key={t.time} className="timeline-item">
                <span className="time">{t.time}</span>
                {t.event}
              </div>
            ))}
          </div>
          <div className="dual-column">
            <div className="col-soc">
              <h4>08:47 — SOC recommends immediate isolation</h4>
              <p>Security-driven containment request. execute=false always.</p>
            </div>
            <div className="col-pe">
              <h4>08:50 — Process engineer warning</h4>
              <p>Abrupt isolation may destabilize unit at MIN_LOAD.</p>
            </div>
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

      {graph.loading && <LoadingBlock />}
      {graph.error && <ErrorBlock message={graph.error} />}
      {graph.data && (
        <div style={{ marginTop: "0.75rem" }}>
          <h3 className="section-title">Task-scoped graph (Q5)</h3>
          <GraphSliceView data={graph.data} />
        </div>
      )}
    </div>
  );
}
