import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useFetch } from "../hooks/useFetch";

export function AuditPage() {
  const traces = useFetch(() => api.traces(30), []);
  const slo = useFetch(() => api.opsSlo(), []);
  const cost = useFetch(() => api.opsCost(), []);

  if (traces.loading) return <LoadingBlock />;

  const rows = traces.data?.traces || [];

  return (
    <div>
      <h2 className="page-title">Decision Trace / Audit</h2>
      {traces.error && <ErrorBlock message={traces.error} />}
      <div className="card-grid">
        <div className="card">
          <h3>SLO snapshot</h3>
          <pre className="mono">{JSON.stringify(slo.data?.checks || {}, null, 2).slice(0, 800)}</pre>
        </div>
        <div className="card">
          <h3>Cost per incident</h3>
          <pre className="mono">{JSON.stringify(cost.data || {}, null, 2)}</pre>
        </div>
      </div>
      <DataTable
        rows={rows as Record<string, unknown>[]}
        rowKey={(r) => String(r.decision_id)}
        cols={[
          { key: "id", header: "decision_id", render: (r) => String(r.decision_id).slice(0, 8) },
          { key: "actor", header: "actor", render: (r) => String(r.actor) },
          { key: "rec", header: "recommendation", render: (r) => String(r.recommendation) },
          { key: "exec", header: "execute", render: (r) => String(r.execute) },
          { key: "lat", header: "latency_ms", render: (r) => String(r.latency_ms ?? "—") },
          { key: "ai", header: "ai_enabled", render: (r) => String(r.ai_enabled) },
        ]}
      />
      <p className="ai-off-note">execute is always false in traces — packet is the argument.</p>
    </div>
  );
}
