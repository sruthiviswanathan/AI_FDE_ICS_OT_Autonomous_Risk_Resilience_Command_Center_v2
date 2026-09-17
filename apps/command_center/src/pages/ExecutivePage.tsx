import { Link } from "react-router-dom";
import { api } from "../api/client";
import { ErrorBlock, FreshnessBadge, LoadingBlock } from "../components/StateViews";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function ExecutivePage() {
  const diag = useFetch(() => api.diagnostics(), []);
  const slo = useFetch(() => api.opsSlo(), []);
  const estate = useFetch(() => api.estateByPlant({ includeTopAlerts: 0 }), []);

  if (diag.loading) return <LoadingBlock />;
  if (diag.error) return <ErrorBlock message={diag.error} />;

  const d = diag.data || {};

  return (
    <div>
      <h2 className="page-title">Executive Brief</h2>
      <FreshnessBadge freshness={estate.data?.freshness} />
      <div className="card-grid">
        <div className="card">
          <h3>Posture summary</h3>
          <ul>
            <li>Asset state conflicts: {fmt(d.asset_state_conflicts)}</li>
            <li>Safety degraded: {fmt(d.safety_bypassed_or_degraded)}</li>
            <li>Recovery gaps: {fmt(d.recovery_stale_or_unknown_backup)}</li>
            <li>Unapproved vendor sessions: {fmt(d.unapproved_remote_sessions)}</li>
          </ul>
        </div>
        <div className="card">
          <h3>CTQ checklist</h3>
          <ul>
            <li>
              SLO-OT:{" "}
              {(slo.data as { slos?: Record<string, { status?: string }> })?.slos?.["SLO-OT"]?.status}
            </li>
            <li>
              SLO-EVAL:{" "}
              {(slo.data as { slos?: Record<string, { status?: string }> })?.slos?.["SLO-EVAL"]?.status}
            </li>
            <li>AI default: OFF (ADR-12)</li>
            <li>Execute routes: 0</li>
          </ul>
        </div>
      </div>
      <div className="card">
        <h3>Residual risk &amp; drill links (read-only)</h3>
        <p>
          <Link to="/simulation">Simulation rail</Link> · <Link to="/audit">Audit traces</Link> ·{" "}
          <Link to="/">Control Tower</Link>
        </p>
        <p className="ai-off-note">No execute controls on this surface.</p>
      </div>
    </div>
  );
}
