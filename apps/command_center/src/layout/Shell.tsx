import { Link, NavLink, useLocation, useNavigate } from "react-router-dom";
import { ContextIdPickers } from "../components/ContextIdPickers";
import { ScenarioBadgeStrip, ScenarioRail } from "../components/ScenarioRail";
import { useApp } from "../context/AppContext";
import { ProvenanceDrawer } from "./ProvenanceDrawer";
import { useFetch } from "../hooks/useFetch";
import { api } from "../api/client";
import { useEffect, useRef } from "react";
import { usePersona } from "../hooks/usePersona";
import {
  hasIncidentContext,
  isRouteAllowed,
  PERSONA_LIST,
  PERSONA_VIEWS,
  type PersonaId,
} from "../personas/registry";
import { Outlet } from "react-router-dom";

export function Shell() {
  const ctx = useApp();
  const location = useLocation();
  const navigate = useNavigate();
  const { nav, view, isFiltered, setPersona } = usePersona();
  const healthQuery = useFetch(() => api.health(), []);
  const catalog = useFetch(() => api.scenarioCatalog(), []);
  const health = healthQuery.data;
  const apiMismatch = health && !health.api_version;
  const apiDown = Boolean(healthQuery.error || catalog.error);

  const healthSynced = useRef(false);
  useEffect(() => {
    if (health && !healthSynced.current) {
      ctx.setAiEnabled(health.ai_enabled);
      healthSynced.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [health]);

  useEffect(() => {
    if (catalog.data && !ctx.activeBinding) {
      const nominal = catalog.data.scenarios.find((s) => s.id === "nominal");
      if (nominal) ctx.applyScenario(nominal);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [catalog.data]);

  const narrativeUnavailable = ctx.aiEnabled && health && !health.ai_enabled;
  const incidentPinned = hasIncidentContext(ctx.alertId, ctx.scenario);

  function onPersonaChange(next: PersonaId) {
    setPersona(next);
    const nextView = PERSONA_VIEWS[next];
    if (!isRouteAllowed(location.pathname, next, ctx.alertId, ctx.scenario)) {
      navigate(nextView.defaultRoute, { replace: true });
    }
  }

  return (
    <div className="shell">
      {(apiDown || apiMismatch) && (
        <div className="advisory-footer" style={{ margin: 0, borderRadius: 0 }}>
          {apiDown
            ? "API unreachable — start backend and check VITE_DEV_API_TARGET in .env.development.local"
            : "Wrong API on proxy target — point VITE_DEV_API_TARGET to your uvicorn port and restart npm run dev"}
        </div>
      )}
      {narrativeUnavailable && (
        <div className="advisory-footer" style={{ margin: 0, borderRadius: 0 }}>
          Narrative unavailable — showing deterministic tables only (EVAL-016).
        </div>
      )}
      {incidentPinned && isFiltered && ctx.personaId !== "executive" && (
        <div className="advisory-footer incident-banner" style={{ margin: 0, borderRadius: 0 }}>
          Incident context loaded —{" "}
          <Link to="/incident">Open Incident Graph</Link>
          {" · "}
          <Link to="/recommend">Recommendation Gate</Link>
        </div>
      )}
      <header className="topbar">
        <h1>ICS/OT Command Center</h1>
        <div className="topbar-controls">
          <span className="topbar-meta">Mode: {health?.mode || "…"}</span>
          {health?.api_version && <span className="topbar-meta mono">API {health.api_version}</span>}
          <label className="topbar-control">
            Persona
            <select
              value={ctx.personaId}
              title={view.description}
              onChange={(e) => onPersonaChange(e.target.value as PersonaId)}
            >
              {PERSONA_LIST.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.label}
                </option>
              ))}
            </select>
          </label>
          <label className="topbar-control">
            Narrative
            <select
              value={ctx.aiEnabled ? "on" : "off"}
              onChange={(e) => ctx.setAiEnabled(e.target.value === "on")}
            >
              <option value="off">Off</option>
              <option value="on">On</option>
            </select>
          </label>
          <span className="topbar-hint" title={view.description}>
            View filter only (OPEN-001)
          </span>
        </div>
      </header>

      <div className="context-bar lookup-bar">
        <ContextIdPickers fields={view.contextFields} />
        <span className="badge amber">{ctx.scenario}</span>
        <ScenarioBadgeStrip />
      </div>

      <div className="body-grid">
        <nav className="nav">
          {nav.map((g) => (
            <div key={g.group}>
              <div className="nav-group">{g.group}</div>
              {g.items.map((item) => (
                <NavLink key={item.to} to={item.to} end={item.to === "/"}>
                  {item.label}
                </NavLink>
              ))}
            </div>
          ))}
          {isFiltered && (
            <button type="button" className="persona-full-link" onClick={() => onPersonaChange("full")}>
              Show all screens (Full view)
            </button>
          )}
          {view.scenarioRailVisible && catalog.data && (
            <ScenarioRail scenarios={catalog.data.scenarios} />
          )}
        </nav>
        <main className="main">
          <Outlet />
        </main>
        <ProvenanceDrawer />
      </div>
    </div>
  );
}
