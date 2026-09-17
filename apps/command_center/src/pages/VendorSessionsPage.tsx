import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { PageLookup } from "../components/PageLookup";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function VendorSessionsPage() {
  const { plantId, lookupKey, pinProvenance } = useApp();
  const diag = useFetch(() => api.diagnostics(), [lookupKey]);
  const sessions = useFetch(() => api.vendorSessions(100), [lookupKey]);

  return (
    <div>
      <h2 className="page-title">Remote Access &amp; Vendor Sessions</h2>
      <PageLookup fields={{ asset: false, alert: false }} />
      {(sessions.loading || diag.loading) && <LoadingBlock />}
      {sessions.error && <ErrorBlock message={sessions.error} />}
      {diag.data && (
        <div className="card-grid">
          <div className="card">
            <h3>Unapproved sessions (estate)</h3>
            <div className="metric">{fmt(diag.data.unapproved_remote_sessions)}</div>
          </div>
          <div className="card">
            <h3>MFA not confirmed</h3>
            <div className="metric">{fmt(diag.data.remote_sessions_without_confirmed_mfa)}</div>
          </div>
        </div>
      )}
      {sessions.data && (
        <>
          <p>Filtered to plant <strong>{plantId}</strong></p>
          <DataTable
            rows={((sessions.data.sessions as Record<string, unknown>[]) || []).filter(
              (s) => !plantId || s.plant_id === plantId,
            )}
            rowKey={(r) => String(r.session_id)}
            highlight={(r) => ((r.anomaly_flags as string[]) || []).length > 0}
            cols={[
              { key: "id", header: "Session", render: (r) => fmt(r.session_id) },
              { key: "asset", header: "Asset", render: (r) => fmt(r.asset_id) },
              { key: "plant", header: "Plant", render: (r) => fmt(r.plant_id) },
              { key: "approved", header: "Approved window", render: (r) => fmt(r.approved_window) },
              { key: "mfa", header: "MFA", render: (r) => fmt(r.mfa) },
              {
                key: "identity",
                header: "Identity",
                render: (r) =>
                  r.identity === "unknown" ? <UncertaintyBadge text="unknown" /> : fmt(r.identity),
              },
              { key: "flags", header: "Anomalies", render: (r) => ((r.anomaly_flags as string[]) || []).join(", ") || "—" },
              {
                key: "src",
                header: "Source",
                render: () => (
                  <button
                    type="button"
                    className="linkish"
                    onClick={() =>
                      pinProvenance({
                        source_path: String(sessions.data?.source_path),
                        label: "vendor_sessions",
                      })
                    }
                  >
                    Pin
                  </button>
                ),
              },
            ]}
          />
        </>
      )}
    </div>
  );
}
