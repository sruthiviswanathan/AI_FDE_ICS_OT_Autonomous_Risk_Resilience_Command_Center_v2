import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useFetch } from "../hooks/useFetch";

const KPI_ROWS = [
  { kpi: "CTQ-ID alias collisions", before: "5", after: "5 visible", note: "conflicts remain queryable" },
  { kpi: "CTQ-CVSS anti-pattern", before: "CVSS-only legacy", after: "contextual rank default", note: "" },
  { kpi: "CTQ-ISO execute attempts", before: "legacy safety-blind", after: "0 execute routes", note: "" },
  { kpi: "CTQ-REC CURRENT=ready", before: "legacy trusts backup", after: "blockers enforced", note: "" },
  { kpi: "Telemetry not-GOOD rate", before: "13.11%", after: "13.11% flagged", note: "not cleaned" },
  { kpi: "SLO-LAT p95", before: "—", after: "BASELINE_PENDING", note: "OPEN-006" },
];

export function KPIPage() {
  const diag = useFetch(() => api.diagnostics(), []);

  if (diag.loading) return <LoadingBlock />;
  if (diag.error) return <ErrorBlock message={diag.error} />;

  return (
    <div>
      <h2 className="page-title">KPI Before/After</h2>
      <DataTable
        rows={KPI_ROWS}
        rowKey={(r) => r.kpi}
        cols={[
          { key: "kpi", header: "KPI", render: (r) => r.kpi },
          { key: "before", header: "Before (legacy/estate)", render: (r) => r.before },
          { key: "after", header: "After (modern)", render: (r) => r.after },
          {
            key: "note",
            header: "Note",
            render: (r) => (r.note.includes("PENDING") ? <UncertaintyBadge text={r.note} /> : r.note),
          },
        ]}
      />
      <div className="card" style={{ marginTop: "0.75rem" }}>
        <h3>Live diagnostics (after)</h3>
        <pre className="mono">{JSON.stringify(diag.data, null, 2)}</pre>
      </div>
    </div>
  );
}
