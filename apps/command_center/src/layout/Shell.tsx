import { NavLink, Outlet } from "react-router-dom";
import { ContextIdPickers } from "../components/ContextIdPickers";
import { ScenarioBadgeStrip, ScenarioRail } from "../components/ScenarioRail";
import { useApp } from "../context/AppContext";
import { ProvenanceDrawer } from "./ProvenanceDrawer";
import { useFetch } from "../hooks/useFetch";
import { api } from "../api/client";
import { useEffect, useRef } from "react";

const NAV: { group: string; items: { to: string; label: string }[] }[] = [
  { group: "Home", items: [{ to: "/", label: "Control Tower" }] },
  {
    group: "Identity & data",
    items: [
      { to: "/identity", label: "Identity Reconciliation" },
      { to: "/telemetry", label: "Telemetry Quality" },
    ],
  },
  {
    group: "Risk & safety",
    items: [
      { to: "/risk", label: "Contextual Risk" },
      { to: "/safety", label: "Safety vs Security" },
      { to: "/sessions", label: "Vendor Sessions" },
    ],
  },
  {
    group: "Process & recovery",
    items: [
      { to: "/process", label: "Process Graph" },
      { to: "/recovery", label: "Recovery Graph" },
    ],
  },
  {
    group: "Incident",
    items: [
      { to: "/incident", label: "Incident Context" },
      { to: "/recommend", label: "Recommendation Gate" },
    ],
  },
  {
    group: "Evidence",
    items: [{ to: "/audit", label: "Decision Trace" }],
  },
  {
    group: "Quality",
    items: [
      { to: "/simulation", label: "Inject / Simulation" },
      { to: "/kpi", label: "KPI Before/After" },
      { to: "/executive", label: "Executive Brief" },
    ],
  },
];

export function Shell() {
  const ctx = useApp();
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
      <header className="topbar">
        <h1>ICS/OT Command Center</h1>
        <div className="toggle toggle-stack">
          <span>Mode: {health?.mode || "…"}</span>
          {health?.api_version && <span className="mono">API {health.api_version}</span>}
          <label>
            Advisory narrative
            <select
              value={ctx.aiEnabled ? "on" : "off"}
              onChange={(e) => ctx.setAiEnabled(e.target.value === "on")}
            >
              <option value="off">Off</option>
              <option value="on">On</option>
            </select>
          </label>
          <span className="ai-off-note toggle-subtitle">
            Deterministic engines active · Narrative layer not connected (OPEN-028)
          </span>
        </div>
      </header>

      <div className="context-bar lookup-bar">
        <ContextIdPickers />
        <span className="badge amber">{ctx.scenario}</span>
        <ScenarioBadgeStrip />
      </div>

      <div className="body-grid">
        <nav className="nav">
          {NAV.map((g) => (
            <div key={g.group}>
              <div className="nav-group">{g.group}</div>
              {g.items.map((item) => (
                <NavLink key={item.to} to={item.to} end={item.to === "/"}>
                  {item.label}
                </NavLink>
              ))}
            </div>
          ))}
          {catalog.data && <ScenarioRail scenarios={catalog.data.scenarios} />}
        </nav>
        <main className="main">
          <Outlet />
        </main>
        <ProvenanceDrawer />
      </div>
    </div>
  );
}
