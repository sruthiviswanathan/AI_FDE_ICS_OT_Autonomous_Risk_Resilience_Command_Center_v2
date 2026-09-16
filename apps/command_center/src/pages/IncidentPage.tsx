import { api } from "../api/client";
import { ErrorBlock, LoadingBlock, UntrustedBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";

export function IncidentPage() {
  const { plantId, assetId, alertId, scenario, setScenario } = useApp();
  const graph = useFetch(
    () => api.graphSlice({ query: "Q5", plant_id: plantId, asset_id: assetId, alert_id: alertId }),
    [plantId, assetId, alertId],
  );
  const scenarioData = useFetch(
    () => (scenario === "cascade_001" ? api.scenario("cascade_001") : Promise.resolve(null)),
    [scenario],
  );
  const timelineFixture = scenarioData.data?.timeline_fixture as { timeline?: { time: string; event: string }[] } | undefined;
  const shift = useFetch(() => api.shiftNotes(), []);

  if (graph.loading) return <LoadingBlock />;

  const timeline = timelineFixture?.timeline || [];

  return (
    <div>
      <h2 className="page-title">Incident Context Graph</h2>
      <div className="btn-row">
        <button type="button" className="primary" onClick={() => setScenario("cascade_001")}>
          Load CASCADE-001
        </button>
        <span className="badge amber">{scenario}</span>
      </div>

      {scenario === "cascade_001" && timeline.length > 0 && (
        <>
          <h3>Timeline</h3>
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
        <div>
          <h3>
            Shift handover <UntrustedBadge />
          </h3>
          <div className="untrusted-panel">{shift.data.content}</div>
        </div>
      )}

      {graph.error ? <ErrorBlock message={graph.error} /> : null}
      {graph.data && (
        <div className="card" style={{ marginTop: "0.75rem" }}>
          <h3>Task-scoped graph slice (Q5)</h3>
          <pre className="mono">{JSON.stringify(graph.data, null, 2).slice(0, 3000)}</pre>
        </div>
      )}
      <p className="ai-off-note">Forbidden: execute at 08:47 SOC step · ignore PE warning</p>
    </div>
  );
}
