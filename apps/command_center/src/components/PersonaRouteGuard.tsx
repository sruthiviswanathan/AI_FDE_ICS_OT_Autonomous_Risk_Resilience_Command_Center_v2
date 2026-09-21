import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { useApp } from "../context/AppContext";
import { usePersona } from "../hooks/usePersona";
import { hasIncidentContext } from "../personas/registry";

export function PersonaRouteGuard() {
  const location = useLocation();
  const navigate = useNavigate();
  const ctx = useApp();
  const { view, isRouteAllowed, setPersona } = usePersona();
  const allowed = isRouteAllowed(location.pathname);

  useEffect(() => {
    if (!allowed) {
      navigate({ pathname: view.defaultRoute, search: location.search }, { replace: true });
    }
  }, [allowed, navigate, view.defaultRoute]);

  if (!allowed) {
    return (
      <div className="card persona-blocked">
        <h2 className="page-title">Not in {view.label} view</h2>
        <p className="ai-off-note">
          This screen is outside the filtered navigation for your current persona. View filter only — does not
          grant authority (OPEN-001).
        </p>
        <div className="btn-row">
          <Link to={{ pathname: view.defaultRoute, search: location.search }} className="primary">
            Open {view.label} home
          </Link>
          <button type="button" onClick={() => setPersona("full")}>
            Switch to Full workshop view
          </button>
        </div>
        {hasIncidentContext(ctx.alertId, ctx.scenario) && (
          <p className="ai-off-note" style={{ marginTop: "0.75rem" }}>
            Incident context is pinned —{" "}
            <Link to={{ pathname: "/incident", search: location.search }}>Open Incident Context Graph</Link> or{" "}
            <Link to={{ pathname: "/recommend", search: location.search }}>Recommendation Gate</Link>.
          </p>
        )}
      </div>
    );
  }

  return <Outlet />;
}
