import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { GraphSliceView } from "../components/GraphSliceView";
import { PageLookup } from "../components/PageLookup";
import { ErrorBlock, GraphAsyncContent, LoadingBlock, SafetyBadge, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function SafetyPage() {
  const { plantId, lookupKey } = useApp();
  const conflicts = useFetch(() => api.safetyConflicts(plantId), [plantId, lookupKey]);
  const graph = useFetch(() => api.graphSlice({ query: "Q3", plant_id: plantId }), [plantId, lookupKey]);

  return (
    <div>
      <h2 className="page-title">Safety vs Security Conflict Board</h2>
      <PageLookup fields={{ asset: false, alert: false }} />
      {conflicts.loading && <LoadingBlock />}
      {conflicts.error && <ErrorBlock message={conflicts.error} />}
      {conflicts.data && (
        <>
          <div className="card-grid">
            <div className="card">
              <h3>Degraded barriers</h3>
              <div className="metric">{fmt(conflicts.data.degraded_barrier_count)}</div>
            </div>
            <div className="card">
              <h3>Bypassed unauthorized</h3>
              <div className="metric">{fmt(conflicts.data.bypassed_unauthorized_count)}</div>
            </div>
            <div className="card">
              <h3>High/Critical unknown context</h3>
              <div className="metric">{fmt(conflicts.data.high_critical_unknown_process_context)}</div>
            </div>
          </div>
          <DataTable
            rows={(conflicts.data.sample_bypassed_unauthorized as Record<string, unknown>[]) || []}
            rowKey={(r) => String(r.barrier_id)}
            highlight={() => true}
            cols={[
              { key: "id", header: "Barrier", render: (r) => fmt(r.barrier_id) },
              { key: "unit", header: "Unit", render: (r) => fmt(r.unit_id) },
              { key: "state", header: "State", render: (r) => fmt(r.state) },
              {
                key: "bypass",
                header: "Bypass authorized",
                render: (r) =>
                  r.bypass_authorized === "UNKNOWN" ? (
                    <UncertaintyBadge text="UNKNOWN" />
                  ) : (
                    fmt(r.bypass_authorized)
                  ),
              },
              { key: "flags", header: "", render: () => <SafetyBadge /> },
            ]}
          />
        </>
      )}
      <div style={{ marginTop: "0.75rem" }}>
        <h3 className="section-title">Safety context (Q3)</h3>
        <GraphAsyncContent
          loading={graph.loading}
          error={graph.error}
          label="Loading safety context graph (Q3)…"
        >
          {graph.data && <GraphSliceView data={graph.data} showVisualToggle defaultView="visual" />}
        </GraphAsyncContent>
      </div>
    </div>
  );
}
