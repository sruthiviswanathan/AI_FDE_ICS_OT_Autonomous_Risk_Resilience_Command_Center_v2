import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { DetailGrid } from "../components/DetailGrid";
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

function findingKey(row: Record<string, unknown>): string {
  return String(row.finding_id || row.vuln_id || row.asset_id);
}

function FindingDetails({ row }: { row: Record<string, unknown> }) {
  const evidence = (row.evidence as Record<string, unknown>[] | undefined) ?? [];
  return (
    <div className="risk-finding-detail">
      <DetailGrid
        columns={4}
        items={[
          { label: "Severity", value: fmt(row.severity) },
          { label: "Status", value: fmt(row.status) },
          { label: "CVSS (input)", value: fmt(row.cvss) },
          { label: "Exploitability", value: fmt(row.exploitability) },
          { label: "Network reachable", value: fmt(row.network_reachable) },
          { label: "Compensating control", value: fmt(row.compensating_control) },
          { label: "Plant", value: fmt(row.plant_id) },
          { label: "Contextual score", value: scoreOf(row) },
        ]}
      />
      {row.factor_breakdown ? (
        <FactorBreakdown breakdown={row.factor_breakdown as Record<string, unknown>} />
      ) : (
        <p className="ai-off-note">No factor breakdown returned for this finding.</p>
      )}
      {evidence.length > 0 && (
        <>
          <h4 className="provenance-subheading">Evidence factors</h4>
          <ul className="provenance-evidence-list mono">
            {evidence.map((e, i) => (
              <li key={`ev-${i}`}>{JSON.stringify(e)}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export function RiskPage() {
  const { plantId, assetId, lookupKey } = useApp();
  const [mode, setMode] = useState<"contextual" | "cvss">("contextual");
  const [expandedKey, setExpandedKey] = useState<string | null>(null);
  const { data, error, loading } = useFetch(
    () =>
      api.risk({
        limit: assetId ? 50 : plantId ? 100 : 25,
        assetId: assetId || undefined,
        plantId: assetId ? undefined : plantId || undefined,
      }),
    [lookupKey, plantId, assetId],
  );

  useEffect(() => {
    setExpandedKey(null);
  }, [plantId, assetId, lookupKey]);

  const rows = useMemo(() => {
    let ranked = ((data?.rankings as Record<string, unknown>[]) || []).map((r, i) => ({
      ...r,
      _rank: i + 1,
    }));
    if (mode === "cvss") {
      ranked = [...ranked]
        .sort((a, b) => Number(b.cvss || 0) - Number(a.cvss || 0))
        .map((r, i) => ({ ...r, _rank: i + 1 }));
    }
    return ranked;
  }, [data, mode]);

  useEffect(() => {
    if (rows.length === 1) {
      setExpandedKey(findingKey(rows[0]));
    }
  }, [rows]);

  function toggleDetails(row: Record<string, unknown>) {
    const key = findingKey(row);
    setExpandedKey((prev) => (prev === key ? null : key));
  }

  if (loading) return <LoadingBlock />;
  if (error) return <ErrorBlock message={error} />;

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
      {rows.length === 0 && (
        <p className="ai-off-note">
          No vulnerability findings for{" "}
          {assetId ? `asset ${assetId}` : plantId ? `plant ${plantId}` : "estate"} in contextual rank corpus.
          {assetId && " This asset may have no rows in vulnerabilities.csv — try another asset or clear the filter."}
        </p>
      )}
      {assetId && (
        <p className="ai-off-note">
          Workshop corpus has one finding per asset — asset filter <span className="mono">{assetId}</span> shows at most
          one row. Choose <strong>All assets (plant-wide)</strong> in the Asset dropdown for the full plant list.
        </p>
      )}
      {rows.length > 0 && (assetId || plantId) && (
        <p className="ai-off-note">
          Scoped to {assetId ? `asset ${assetId}` : `plant ${plantId}`} · {fmt(data?.count)} finding(s) ranked
        </p>
      )}
      <DataTable
        rows={rows}
        rowKey={findingKey}
        expandedKey={expandedKey}
        renderExpanded={(row) => (
          <>
            <h3 className="section-title" style={{ marginTop: 0 }}>
              Factor breakdown — {fmt(row.finding_id || row.vuln_id)}
            </h3>
            <FindingDetails row={row} />
          </>
        )}
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
            render: (r) => {
              const key = findingKey(r);
              const open = expandedKey === key;
              return (
                <button type="button" className={open ? "active" : ""} onClick={() => toggleDetails(r)}>
                  {open ? "Hide" : "Details"}
                </button>
              );
            },
          },
        ]}
      />
    </div>
  );
}
