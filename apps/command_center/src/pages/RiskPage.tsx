import { useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useFetch } from "../hooks/useFetch";

export function RiskPage() {
  const [mode, setMode] = useState<"contextual" | "cvss">("contextual");
  const [selected, setSelected] = useState<Record<string, unknown> | null>(null);
  const { data, error, loading } = useFetch(() => api.risk(25), []);

  if (loading) return <LoadingBlock />;
  if (error) return <ErrorBlock message={error} />;

  let rows = ((data?.rankings as Record<string, unknown>[]) || []).map((r, i) => ({ ...r, _rank: i + 1 }));
  if (mode === "cvss") {
    rows = [...rows].sort((a, b) => Number(b.cvss || 0) - Number(a.cvss || 0)).map((r, i) => ({ ...r, _rank: i + 1 }));
  }

  const active = selected || rows[0] || null;

  return (
    <div>
      <h2 className="page-title">Contextual Risk Workbench</h2>
      <div className="btn-row">
        <button type="button" className={mode === "contextual" ? "primary" : ""} onClick={() => setMode("contextual")}>
          Contextual rank (default)
        </button>
        <button type="button" className={mode === "cvss" ? "primary" : ""} onClick={() => setMode("cvss")}>
          CVSS-only (warn — not operational default)
        </button>
      </div>
      {mode === "cvss" && (
        <div className="advisory-footer">CVSS-only sort is anti-pattern (APP-AT-002). Use contextual rank for triage.</div>
      )}
      <DataTable
        rows={rows}
        rowKey={(r) => String(r.vuln_id || r.finding_id)}
        cols={[
          { key: "rank", header: "#", render: (r) => String(r._rank) },
          { key: "id", header: "Finding", render: (r) => String(r.vuln_id) },
          { key: "asset", header: "Asset", render: (r) => String(r.asset_id) },
          { key: "cvss", header: "CVSS (input)", render: (r) => String(r.cvss) },
          { key: "reach", header: "Reach", render: (r) => String(r.reachable) },
          { key: "crit", header: "Crit", render: (r) => String(r.criticality) },
          {
            key: "score",
            header: "Score",
            render: (r) => {
              const fb = r.factor_breakdown as Record<string, { contextual_score?: number }> | undefined;
              return String(fb?.contextual_score ?? "—");
            },
          },
          {
            key: "sel",
            header: "",
            render: (r) => (
              <button type="button" onClick={() => setSelected(r)}>
                breakdown
              </button>
            ),
          },
        ]}
      />
      {active && (
        <div className="card" style={{ marginTop: "0.75rem" }}>
          <h3>Factor breakdown — {String(active.vuln_id)}</h3>
          <pre className="mono">{JSON.stringify(active.factor_breakdown, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
