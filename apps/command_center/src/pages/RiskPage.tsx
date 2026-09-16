import { useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { FactorBreakdown } from "../components/FactorBreakdown";
import { PageLookup } from "../components/PageLookup";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

function criticalityOf(row: Record<string, unknown>): string {
  const fb = row.factor_breakdown as Record<string, { value?: string }> | undefined;
  return fb?.process_criticality?.value ?? "—";
}

function reachOf(row: Record<string, unknown>): string {
  const fb = row.factor_breakdown as Record<string, { value?: string }> | undefined;
  return fb?.reachability?.value ?? fmt(row.network_reachable);
}

function scoreOf(row: Record<string, unknown>): string {
  const fb = row.factor_breakdown as Record<string, { contextual_score?: number }> | undefined;
  return fmt(fb?.contextual_score);
}

export function RiskPage() {
  const { assetId, lookupKey } = useApp();
  const [mode, setMode] = useState<"contextual" | "cvss">("contextual");
  const [selected, setSelected] = useState<Record<string, unknown> | null>(null);
  const { data, error, loading } = useFetch(() => api.risk(25), [lookupKey]);

  if (loading) return <LoadingBlock />;
  if (error) return <ErrorBlock message={error} />;

  let rows = ((data?.rankings as Record<string, unknown>[]) || []).map((r, i) => ({ ...r, _rank: i + 1 }));
  if (assetId) {
    rows = rows.filter((r) => String(r.asset_id) === assetId);
  }
  if (mode === "cvss") {
    rows = [...rows].sort((a, b) => Number(b.cvss || 0) - Number(a.cvss || 0)).map((r, i) => ({ ...r, _rank: i + 1 }));
  }

  const active = selected || rows[0] || null;

  return (
    <div>
      <h2 className="page-title">Contextual Risk Workbench</h2>
      <PageLookup fields={{ plant: true, asset: true, alert: false }} />
      <div className="btn-row">
        <button type="button" className={mode === "contextual" ? "primary" : ""} onClick={() => setMode("contextual")}>
          Contextual rank (default)
        </button>
        <button type="button" className={mode === "cvss" ? "primary" : ""} onClick={() => setMode("cvss")}>
          CVSS-only (warn)
        </button>
      </div>
      {mode === "cvss" && (
        <div className="advisory-footer">CVSS-only sort is anti-pattern (APP-AT-002).</div>
      )}
      {rows.length === 0 && <p className="ai-off-note">No findings for asset {assetId || "(all)"}.</p>}
      <DataTable
        rows={rows}
        rowKey={(r) => String(r.finding_id || r.vuln_id)}
        cols={[
          { key: "rank", header: "#", render: (r) => fmt(r._rank) },
          { key: "id", header: "Finding", render: (r) => fmt(r.finding_id || r.vuln_id) },
          { key: "asset", header: "Asset", render: (r) => fmt(r.asset_id) },
          { key: "cvss", header: "CVSS (input)", render: (r) => fmt(r.cvss) },
          { key: "reach", header: "Reach", render: (r) => reachOf(r) },
          { key: "crit", header: "Criticality", render: (r) => criticalityOf(r) },
          { key: "severity", header: "Severity", render: (r) => fmt(r.severity) },
          { key: "score", header: "Score", render: (r) => scoreOf(r) },
          {
            key: "sel",
            header: "",
            render: (r) => (
              <button type="button" onClick={() => setSelected(r)}>
                Details
              </button>
            ),
          },
        ]}
      />
      {active && active.factor_breakdown && (
        <div style={{ marginTop: "0.75rem" }}>
          <h3 className="section-title">Factor breakdown — {fmt(active.finding_id || active.vuln_id)}</h3>
          <FactorBreakdown breakdown={active.factor_breakdown as Record<string, unknown>} />
        </div>
      )}
    </div>
  );
}
