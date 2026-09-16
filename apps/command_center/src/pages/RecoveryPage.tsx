import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";

export function RecoveryPage() {
  const { plantId } = useApp();
  const recovery = useFetch(() => api.recovery(plantId), [plantId]);
  const graph = useFetch(() => api.graphSlice({ query: "Q4", plant_id: plantId }), [plantId]);

  if (recovery.loading) return <LoadingBlock />;
  if (recovery.error) return <ErrorBlock message={recovery.error} />;

  const components = (recovery.data?.components as Record<string, unknown>[]) || [];

  return (
    <div>
      <h2 className="page-title">Recovery / Restore-Test Graph</h2>
      <p>
        Plant {plantId} · ready {String(recovery.data?.recovery_ready_count)} / {String(recovery.data?.component_count)}
      </p>
      <DataTable
        rows={components}
        rowKey={(r) => `${r.plant_id}-${r.component}`}
        highlight={(r) => r.backup_status === "CURRENT" && !r.recovery_ready}
        cols={[
          { key: "comp", header: "Component", render: (r) => String(r.component) },
          { key: "backup", header: "backup", render: (r) => String(r.backup_status) },
          { key: "restore", header: "restore_test_days", render: (r) => String(r.last_restore_test_days) },
          { key: "runbook", header: "runbook", render: (r) => String(r.runbook_status) },
          { key: "deps", header: "deps verified", render: (r) => String(r.dependency_verified) },
          { key: "manual", header: "manual_fallback", render: (r) => String(r.manual_fallback) },
          {
            key: "ready",
            header: "RecoveryReady",
            render: (r) => (r.recovery_ready ? "YES" : "NO"),
          },
          {
            key: "blockers",
            header: "blockers",
            render: (r) => ((r.blockers as string[]) || []).join("; "),
          },
        ]}
      />
      {graph.data && (
        <div className="card" style={{ marginTop: "0.75rem" }}>
          <h3>Graph Q4</h3>
          <pre className="mono">{JSON.stringify(graph.data, null, 2).slice(0, 1500)}…</pre>
        </div>
      )}
      <p className="ai-off-note">CURRENT backup alone ≠ RecoveryReady · no live restore UI</p>
    </div>
  );
}
