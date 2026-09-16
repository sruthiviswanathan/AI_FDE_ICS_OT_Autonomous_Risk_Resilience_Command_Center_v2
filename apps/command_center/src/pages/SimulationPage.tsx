import { useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function SimulationPage() {
  const { applyScenario } = useApp();
  const catalog = useFetch(() => api.scenarioCatalog(), []);
  const [results, setResults] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function runHarness() {
    setLoading(true);
    setError(null);
    try {
      const res = await api.evalRun();
      setResults(res);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  if (catalog.loading) return <LoadingBlock label="Loading scenario catalog…" />;

  const scenarios = catalog.data?.scenarios || [];
  const caseRows = ((results?.results as Record<string, unknown>[]) || []);

  return (
    <div>
      <h2 className="page-title">Inject / Failure Simulation</h2>
      <div className="card-grid">
        {scenarios.map((s) => (
          <div key={s.id} className="card">
            <h3>{s.label}</h3>
            <p>{s.title}</p>
            <p className="mono">{s.eval_ids.join(", ") || "estate nominal"}</p>
            <div className="badge-row">
              {s.badges.slice(0, 4).map((b) => (
                <span key={b.id} className={`badge ${b.tone !== "neutral" ? b.tone : ""}`}>
                  {b.label}
                </span>
              ))}
            </div>
            <button type="button" onClick={() => applyScenario(s)}>
              Load scenario
            </button>
          </div>
        ))}
      </div>
      <div className="btn-row">
        <button type="button" className="primary" onClick={runHarness} disabled={loading}>
          Run full harness (EVAL-001…031)
        </button>
      </div>
      {loading && <LoadingBlock label="Running eval harness…" />}
      {error && <ErrorBlock message={error} />}
      {results && (
        <>
          <p>
            Summary: {String(results.passed)}/{String(results.total)} PASS
          </p>
          <DataTable
            rows={caseRows}
            rowKey={(r) => String(r.case_id)}
            highlight={(r) => r.status !== "PASS"}
            cols={[
              { key: "id", header: "case", render: (r) => String(r.case_id) },
              { key: "status", header: "status", render: (r) => String(r.status) },
              { key: "detail", header: "detail", render: (r) => fmt(r.detail ?? r.message) },
            ]}
          />
        </>
      )}
      <p className="ai-off-note">Do not hide conflicts to beautify demo. See SCENARIO_BINDINGS.md.</p>
    </div>
  );
}
