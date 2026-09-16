import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock, SafetyBadge, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";

export function SafetyPage() {
  const { plantId } = useApp();
  const conflicts = useFetch(() => api.safetyConflicts(plantId), [plantId]);
  const graph = useFetch(() => api.graphSlice({ query: "Q3", plant_id: plantId }), [plantId]);

  if (conflicts.loading) return <LoadingBlock />;
  if (conflicts.error) return <ErrorBlock message={conflicts.error} />;

  const rows = (conflicts.data?.sample_bypassed_unauthorized as Record<string, unknown>[]) || [];

  return (
    <div>
      <h2 className="page-title">Safety vs Security Conflict Board</h2>
      <p>
        Plant: {plantId} · degraded: {String(conflicts.data?.degraded_barrier_count)} · bypassed
        unauthorized: {String(conflicts.data?.bypassed_unauthorized_count)}
      </p>
      <DataTable
        rows={rows}
        rowKey={(r) => String(r.barrier_id)}
        highlight={(r) => r.state !== "ACTIVE" || r.bypass_authorized === "NO"}
        cols={[
          { key: "id", header: "Barrier", render: (r) => String(r.barrier_id) },
          { key: "unit", header: "Unit", render: (r) => String(r.unit_id) },
          { key: "state", header: "State", render: (r) => String(r.state) },
          {
            key: "bypass",
            header: "bypass_authorized",
            render: (r) =>
              r.bypass_authorized === "UNKNOWN" ? (
                <UncertaintyBadge text="UNKNOWN" />
              ) : (
                String(r.bypass_authorized)
              ),
          },
          { key: "proof", header: "proof_test", render: (r) => String(r.proof_test_status) },
          {
            key: "flags",
            header: "",
            render: (r) => (r.state !== "ACTIVE" ? <SafetyBadge /> : null),
          },
        ]}
      />
      {graph.data && (
        <div className="card" style={{ marginTop: "0.75rem" }}>
          <h3>Graph slice Q3</h3>
          <pre className="mono">{JSON.stringify(graph.data, null, 2).slice(0, 2000)}…</pre>
        </div>
      )}
      <p className="ai-off-note">Forbidden: bypass_interlock · hide bypass from view</p>
    </div>
  );
}
