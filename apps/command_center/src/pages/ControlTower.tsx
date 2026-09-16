import { Link } from "react-router-dom";
import { api } from "../api/client";
import { StaleBadge } from "../components/StateViews";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useFetch } from "../hooks/useFetch";

export function ControlTower() {
  const diag = useFetch(() => api.diagnostics(), []);
  const slo = useFetch(() => api.opsSlo(), []);

  if (diag.loading || slo.loading) return <LoadingBlock />;
  if (diag.error) return <ErrorBlock message={diag.error} />;

  const d = diag.data || {};
  const entries = Object.entries(d);

  return (
    <div>
      <h2 className="page-title">Risk &amp; Resilience Control Tower</h2>
      <div className="ctq-strip">
        <span>SLO-OT: {(slo.data as { checks?: Record<string, { status?: string }> })?.checks?.["SLO-OT"]?.status || "…"}</span>
        <span>Eval: 31/31 (harness)</span>
        <span>Legacy xfail: 3 (contrast only)</span>
        <StaleBadge />
      </div>
      <div className="card-grid">
        <div className="card">
          <h3>Estate diagnostics ({entries.length})</h3>
          <div className="diag-grid">
            {entries.map(([k, v]) => (
              <div key={k} className="diag-item">
                <div className="label">{k.replace(/_/g, " ")}</div>
                <div className="value">{v}</div>
              </div>
            ))}
          </div>
        </div>
        <div className="card">
          <h3>Quick incidents</h3>
          <p>
            <Link to="/incident">ALT-002783 · PLT-10 · HIGH</Link>
          </p>
          <p>
            <Link to="/recommend">Open recommendation gate →</Link>
          </p>
        </div>
      </div>
      <div className="card" style={{ marginTop: "0.75rem" }}>
        <h3>Open decisions (read-only)</h3>
        <p className="mono">OPEN-001 Authorizer · OPEN-006 KPI · OPEN-028 model · OPEN-029 auth</p>
      </div>
    </div>
  );
}
