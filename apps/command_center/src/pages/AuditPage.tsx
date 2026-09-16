import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { DetailGrid } from "../components/DetailGrid";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function AuditPage() {
  const traces = useFetch(() => api.traces(30), []);
  const slo = useFetch(() => api.opsSlo(), []);
  const cost = useFetch(() => api.opsCost(), []);

  if (traces.loading) return <LoadingBlock />;

  const rows = traces.data?.traces || [];
  const checks =
    ((slo.data?.slos ?? slo.data?.checks) as Record<string, Record<string, unknown>>) || {};

  return (
    <div>
      <h2 className="page-title">Decision Trace / Audit</h2>
      {traces.error && <ErrorBlock message={traces.error} />}
      <div className="card-grid">
        {Object.entries(checks).map(([name, check]) => (
          <div key={name} className="card">
            <h3>{name}</h3>
            <DetailGrid
              items={[
                { label: "Status", value: check.status },
                { label: "Observed", value: check.observed ?? check.observed_p95_ms },
                { label: "Target", value: check.target ?? check.target_ms },
                { label: "Description", value: check.description },
              ]}
            />
          </div>
        ))}
        <div className="card">
          <h3>Cost model</h3>
          <DetailGrid
            items={[
              { label: "Currency", value: cost.data?.currency },
              { label: "Baseline / incident", value: cost.data?.baseline_cost_per_incident },
              { label: "Note", value: cost.data?.note },
            ]}
          />
        </div>
      </div>
      <DataTable
        rows={rows as Record<string, unknown>[]}
        rowKey={(r) => String(r.decision_id)}
        cols={[
          { key: "id", header: "Decision", render: (r) => String(r.decision_id).slice(0, 12) },
          { key: "actor", header: "Actor", render: (r) => fmt(r.actor) },
          { key: "purpose", header: "Purpose", render: (r) => fmt(r.purpose) },
          { key: "rec", header: "Recommendation", render: (r) => fmt(r.recommendation) },
          { key: "exec", header: "Execute", render: (r) => fmt(r.execute) },
          { key: "lat", header: "Latency (ms)", render: (r) => fmt(r.latency_ms) },
          { key: "ai", header: "AI", render: (r) => fmt(r.ai_enabled) },
        ]}
      />
    </div>
  );
}
