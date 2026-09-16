import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { GraphSliceView } from "../components/GraphSliceView";
import { PageLookup } from "../components/PageLookup";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function RecoveryPage() {
  const { plantId, lookupKey } = useApp();
  const recovery = useFetch(() => (plantId ? api.recovery(plantId) : Promise.reject(new Error("Enter a plant ID"))), [
    plantId,
    lookupKey,
  ]);
  const graph = useFetch(() => api.graphSlice({ query: "Q4", plant_id: plantId }), [plantId, lookupKey]);

  return (
    <div>
      <h2 className="page-title">Recovery / Restore-Test Graph</h2>
      <PageLookup fields={{ asset: false, alert: false }} />

      {!plantId && <p className="ai-off-note">Enter a Plant ID and click Search.</p>}
      {recovery.loading && plantId && <LoadingBlock />}
      {recovery.error && <ErrorBlock message={recovery.error} />}
      {recovery.data && (
        <>
          <div className="card-grid">
            <div className="card">
              <h3>Plant</h3>
              <div className="metric">{fmt(recovery.data.plant_id)}</div>
            </div>
            <div className="card">
              <h3>Recovery ready</h3>
              <div className="metric">
                {fmt(recovery.data.recovery_ready_count)} / {fmt(recovery.data.component_count)}
              </div>
            </div>
          </div>
          <DataTable
            rows={(recovery.data.components as Record<string, unknown>[]) || []}
            rowKey={(r) => `${r.plant_id}-${r.component}`}
            highlight={(r) => r.backup_status === "CURRENT" && !r.recovery_ready}
            cols={[
              { key: "comp", header: "Component", render: (r) => fmt(r.component) },
              { key: "backup", header: "Backup", render: (r) => fmt(r.backup_status) },
              { key: "restore", header: "Restore test (days)", render: (r) => fmt(r.last_restore_test_days) },
              { key: "runbook", header: "Runbook", render: (r) => fmt(r.runbook_status) },
              { key: "deps", header: "Deps verified", render: (r) => fmt(r.dependency_verified) },
              { key: "manual", header: "Manual fallback", render: (r) => fmt(r.manual_fallback) },
              { key: "ready", header: "RecoveryReady", render: (r) => (r.recovery_ready ? "YES" : "NO") },
              { key: "blockers", header: "Blockers", render: (r) => ((r.blockers as string[]) || []).join("; ") || "—" },
            ]}
          />
        </>
      )}
      {graph.data && (
        <div style={{ marginTop: "0.75rem" }}>
          <h3 className="section-title">Recovery dependencies (Q4)</h3>
          <GraphSliceView data={graph.data} showVisualToggle defaultView="visual" />
        </div>
      )}
    </div>
  );
}
