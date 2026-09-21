import { Link, NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { ContextIdPickers } from "../components/ContextIdPickers";
import { ScenarioBadgeStrip, ScenarioRail } from "../components/ScenarioRail";
import { useApp } from "../context/AppContext";
import { ProvenanceDrawer } from "./ProvenanceDrawer";
import { useFetch } from "../hooks/useFetch";
import { api } from "../api/client";
import { useEffect } from "react";
import { usePersona } from "../hooks/usePersona";
import {
  canUseMoonshot,
  hasIncidentContext,
  isRouteAllowed,
  PERSONA_LIST,
  PERSONA_VIEWS,
  type PersonaId,
} from "../personas/registry";

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

  useEffect(() => {
    if (!catalog.data || ctx.activeBinding) return;
    const fromUrl = new URLSearchParams(window.location.search).get("scenario");
    const requested =
      catalog.data.scenarios.find((s) => s.id === fromUrl) ||
      catalog.data.scenarios.find((s) => s.id === "nominal");
    if (requested) ctx.applyScenario(requested);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [catalog.data]);

  const incidentPinned = hasIncidentContext(ctx.alertId, ctx.scenario);

  function onPersonaChange(next: PersonaId) {
    setPersona(next);
    const nextView = PERSONA_VIEWS[next];
    if (!isRouteAllowed(location.pathname, next, ctx.alertId, ctx.scenario)) {
      navigate({ pathname: nextView.defaultRoute, search: location.search }, { replace: true });
    }
  }

  const searchKeep = location.search;
  const moonshotAllowed = canUseMoonshot(ctx.personaId);
  const aiBadge =
    ctx.aiMode === "moonshot" ? "MOONSHOT" : ctx.aiMode === "on" ? "AI-ON" : "AI-DISABLED";
  const aiBadgeTone = ctx.aiMode === "moonshot" ? "orange" : ctx.aiMode === "on" ? "green" : "amber";

  return (
    <div className="shell">
      {(apiDown || apiMismatch) && (
        <div className="advisory-footer" style={{ margin: 0, borderRadius: 0 }}>
          {apiDown
            ? "API unreachable — start backend and check VITE_DEV_API_TARGET in .env.development.local"
            : "Wrong API on proxy target — point VITE_DEV_API_TARGET to your uvicorn port and restart npm run dev"}
        </div>
      )}
      {incidentPinned && isFiltered && ctx.personaId !== "executive" && (
        <div className="advisory-footer incident-banner" style={{ margin: 0, borderRadius: 0 }}>
          Incident context loaded —{" "}
          <Link to={{ pathname: "/incident", search: searchKeep }}>Open Incident Graph</Link>
          {" · "}
          <Link to={{ pathname: "/recommend", search: searchKeep }}>Recommendation Gate</Link>
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
            AI
            <span className="ai-seg" role="group" aria-label="AI mode">
              {(["off", "on"] as const).map((mode) => (
                <button
                  key={mode}
                  type="button"
                  className={ctx.aiMode === mode ? "chip active" : "chip"}
                  disabled={ctx.aiControlDisabled}
                  onClick={() => ctx.setAiMode(mode)}
                >
                  {mode.toUpperCase()}
                </button>
              ))}
              {moonshotAllowed && (
                <button
                  type="button"
                  className={ctx.aiMode === "moonshot" ? "chip active" : "chip"}
                  disabled={ctx.aiControlDisabled}
                  onClick={() => ctx.setAiMode("moonshot")}
                >
                  MOONSHOT
                </button>
              )}
            </span>
          </label>
          <span className={`badge ${aiBadgeTone}`} title={ctx.aiControlDisabled ? "ai_outage forces AI OFF (EVAL-016)" : undefined}>
            {aiBadge}
          </span>
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
                <NavLink key={item.to} to={{ pathname: item.to, search: searchKeep }} end={item.to === "/"}>
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
