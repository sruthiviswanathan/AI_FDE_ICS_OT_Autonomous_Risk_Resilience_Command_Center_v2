import { NavLink, Outlet } from "react-router-dom";
import { ScenarioBadgeStrip, ScenarioRail } from "../components/ScenarioRail";
import { useApp } from "../context/AppContext";
import { ProvenanceDrawer } from "./ProvenanceDrawer";
import { useFetch } from "../hooks/useFetch";
import { api } from "../api/client";
import { useEffect, useState } from "react";

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

  const [draftPlant, setDraftPlant] = useState(ctx.plantId);
  const [draftAsset, setDraftAsset] = useState(ctx.assetId);
  const [draftAlert, setDraftAlert] = useState(ctx.alertId);

  useEffect(() => {
    setDraftPlant(ctx.plantId);
    setDraftAsset(ctx.assetId);
    setDraftAlert(ctx.alertId);
  }, [ctx.plantId, ctx.assetId, ctx.alertId, ctx.lookupKey]);

  useEffect(() => {
    if (catalog.data && !ctx.activeBinding) {
      const nominal = catalog.data.scenarios.find((s) => s.id === "nominal");
      if (nominal) ctx.applyScenario(nominal);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [catalog.data]);

  function runGlobalLookup() {
    ctx.setPlantId(draftPlant.trim());
    ctx.setAssetId(draftAsset.trim());
    ctx.setAlertId(draftAlert.trim());
    ctx.triggerLookup();
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
      <header className="topbar">
        <h1>ICS/OT Command Center</h1>
        <div className="toggle">
          <span>Mode: {health?.mode || "…"}</span>
          {health?.api_version && <span className="mono">API {health.api_version}</span>}
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

      <div className="context-bar lookup-bar">
        <label>
          Plant ID
          <input
            value={draftPlant}
            onChange={(e) => setDraftPlant(e.target.value)}
            placeholder="PLT-10"
            onKeyDown={(e) => e.key === "Enter" && runGlobalLookup()}
          />
        </label>
        <label>
          Asset ID
          <input
            value={draftAsset}
            onChange={(e) => setDraftAsset(e.target.value)}
            placeholder="OT-01016"
            onKeyDown={(e) => e.key === "Enter" && runGlobalLookup()}
          />
        </label>
        <label>
          Alert ID
          <input
            value={draftAlert}
            onChange={(e) => setDraftAlert(e.target.value)}
            placeholder="ALT-002783"
            onKeyDown={(e) => e.key === "Enter" && runGlobalLookup()}
          />
        </label>
        <button type="button" className="primary" onClick={runGlobalLookup}>
          Search
        </button>
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
