import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";

export function VendorSessionsPage() {
  const { plantId, pinProvenance } = useApp();
  const diag = useFetch(() => api.diagnostics(), []);
  const sessions = useFetch(() => api.vendorSessions(100), []);

  if (sessions.loading || diag.loading) return <LoadingBlock />;
  if (sessions.error) return <ErrorBlock message={sessions.error} />;

  const all = (sessions.data?.sessions as Record<string, unknown>[]) || [];
  const scoped = all.filter((s) => !plantId || s.plant_id === plantId);

  return (
    <div>
      <h2 className="page-title">Remote Access &amp; Vendor Sessions</h2>
      <div className="card-grid">
        <div className="card">
          <h3>Unapproved sessions (estate)</h3>
          <div className="metric">{diag.data?.unapproved_remote_sessions}</div>
        </div>
        <div className="card">
          <h3>MFA not confirmed</h3>
          <div className="metric">{diag.data?.remote_sessions_without_confirmed_mfa}</div>
        </div>
      </div>
      <p>Showing plant {plantId} — tier-3 access changes require human Authorize (OPEN-001).</p>
      <DataTable
        rows={scoped}
        rowKey={(r) => String(r.session_id)}
        highlight={(r) => (r.anomaly_flags as string[])?.length > 0}
        cols={[
          { key: "id", header: "Session", render: (r) => String(r.session_id) },
          { key: "asset", header: "Asset", render: (r) => String(r.asset_id) },
          { key: "approved", header: "approved_window", render: (r) => String(r.approved_window) },
          { key: "mfa", header: "mfa", render: (r) => String(r.mfa) },
          {
            key: "identity",
            header: "identity",
            render: (r) =>
              r.identity === "unknown" ? <UncertaintyBadge text="unknown" /> : String(r.identity),
          },
          {
            key: "flags",
            header: "anomalies",
            render: (r) => ((r.anomaly_flags as string[]) || []).join(", "),
          },
          {
            key: "src",
            header: "source",
            render: () => (
              <button
                type="button"
                className="mono"
                onClick={() =>
                  pinProvenance({
                    source_path: String(sessions.data?.source_path),
                    freshness: "workshop-static",
                  })
                }
              >
                pin
              </button>
            ),
          },
        ]}
      />
      <p className="ai-off-note">Forbidden: auto-disable VPN · dump all plants · execute change_remote_access</p>
    </div>
  );
}
