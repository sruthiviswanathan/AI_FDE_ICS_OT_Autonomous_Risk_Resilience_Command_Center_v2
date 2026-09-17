import { useMemo } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function KPIPage() {
  const diag = useFetch(() => api.diagnostics(), []);
  const slo = useFetch(() => api.opsSlo(), []);

  const rows = useMemo(() => {
    if (!diag.data) return [];
    const d = diag.data;
    const slos = (slo.data as { slos?: Record<string, { status?: string; baseline_status?: string }> })?.slos;
    return [
      { kpi: "Asset state conflicts", value: fmt(d.asset_state_conflicts), note: "registered vs observed" },
      { kpi: "Alias collisions", value: fmt(d.alias_collisions), note: "identity reconciliation" },
      { kpi: "Undocumented network paths", value: fmt(d.undocumented_network_paths), note: "observed, not documented" },
      { kpi: "Telemetry bad or uncertain", value: fmt(d.telemetry_bad_or_uncertain), note: "quality != GOOD" },
      { kpi: "Safety bypassed or degraded", value: fmt(d.safety_bypassed_or_degraded), note: "barrier state" },
      { kpi: "Recovery stale / unknown backup", value: fmt(d.recovery_stale_or_unknown_backup), note: "blockers enforced" },
      { kpi: "Unapproved remote sessions", value: fmt(d.unapproved_remote_sessions), note: "vendor access" },
      {
        kpi: "SLO-LAT p95",
        value: fmt(slos?.["SLO-LAT"]?.baseline_status || slos?.["SLO-LAT"]?.status),
        note: "OPEN-006 baseline",
      },
      {
        kpi: "SLO-OT execute violations",
        value: fmt(slos?.["SLO-OT"]?.status),
        note: "must remain OK",
      },
    ];
  }, [diag.data, slo.data]);

  if (diag.loading || slo.loading) return <LoadingBlock />;
  if (diag.error) return <ErrorBlock message={diag.error} />;

  return (
    <div>
      <h2 className="page-title">KPI Before/After</h2>
      <p className="ai-off-note">Live estate diagnostics and SLO synthesis — values refresh from API on load.</p>
      <DataTable
        rows={rows}
        rowKey={(r) => r.kpi}
        cols={[
          { key: "kpi", header: "Signal", render: (r) => r.kpi },
          { key: "value", header: "Observed", render: (r) => r.value },
          {
            key: "note",
            header: "Note",
            render: (r) =>
              r.note.includes("PENDING") || r.value === "BASELINE_PENDING" ? (
                <UncertaintyBadge text={r.note || String(r.value)} />
              ) : (
                r.note
              ),
          },
        ]}
      />
      <div className="card" style={{ marginTop: "0.75rem" }}>
        <h3>Raw diagnostics</h3>
        <pre className="mono">{JSON.stringify(diag.data, null, 2)}</pre>
      </div>
    </div>
  );
}
