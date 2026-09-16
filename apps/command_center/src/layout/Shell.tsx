import { NavLink, Outlet } from "react-router-dom";
import { ScenarioBadgeStrip, ScenarioRail } from "../components/ScenarioRail";
import { useApp } from "../context/AppContext";
import { ProvenanceDrawer } from "./ProvenanceDrawer";
import { useFetch } from "../hooks/useFetch";
import { api } from "../api/client";
import { useEffect } from "react";

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
  const { data: health } = useFetch(() => api.health(), []);
  const catalog = useFetch(() => api.scenarioCatalog(), []);

  useEffect(() => {
    if (catalog.data && !ctx.activeBinding) {
      const nominal = catalog.data.scenarios.find((s) => s.id === "nominal");
      if (nominal) ctx.applyScenario(nominal);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [catalog.data]);

  return (
    <div className="shell">
      <header className="topbar">
        <h1>ICS/OT Command Center</h1>
        <div className="toggle">
          <span>Mode: {health?.mode || "…"}</span>
          <label>
            AI
            <select
              value={ctx.aiEnabled ? "on" : "off"}
              onChange={(e) => ctx.setAiEnabled(e.target.value === "on")}
            >
              <option value="off">OFF</option>
              <option value="on">ON</option>
            </select>
          </label>
        </div>
      </header>

      <div className="context-bar">
        <label>
          Plant
          <input value={ctx.plantId} onChange={(e) => ctx.setPlantId(e.target.value)} />
        </label>
        <label>
          Asset
          <input value={ctx.assetId} onChange={(e) => ctx.setAssetId(e.target.value)} />
        </label>
        <label>
          Alert
          <input value={ctx.alertId} onChange={(e) => ctx.setAlertId(e.target.value)} />
        </label>
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
