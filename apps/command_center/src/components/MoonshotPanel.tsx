import { useNavigate } from "react-router-dom";
import { api, type AdvisoryForecast } from "../api/client";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { DataTable } from "./DataTable";
import { ErrorBlock, LoadingBlock } from "./StateViews";
import { canUseMoonshot } from "../personas/registry";

export function MoonshotPanel() {
  const { plantId, assetId, alertId, aiMode, personaId, lookupKey, applyScenario, setAiMode } = useApp();
  const navigate = useNavigate();
  const allowed = canUseMoonshot(personaId);
  const catalog = useFetch(() => api.scenarioCatalog(), []);
  const query = useFetch(
    () =>
      aiMode !== "moonshot" || !allowed || !plantId
        ? Promise.resolve(null)
        : api.forecasts({ plantId, assetId: assetId || undefined, alertId: alertId || undefined }),
    [aiMode, allowed, plantId, assetId, alertId, lookupKey],
  );

  if (aiMode !== "moonshot" || !allowed) return null;
  if (!plantId) return <p className="ai-off-note">Select a plant to load Moonshot forecasts.</p>;
  if (query.loading) return <LoadingBlock label="Loading advisory forecasts…" />;
  if (query.error) return <ErrorBlock message={query.error} />;
  if (!query.data) return null;

  function loadInTwin(row: AdvisoryForecast) {
    const binding = catalog.data?.scenarios.find((s) => s.id === row.twin_scenario_id);
    if (binding) applyScenario(binding);
    setAiMode("moonshot");
    const params = new URLSearchParams(window.location.search);
    params.set("ai", "moonshot");
    if (row.twin_scenario_id) params.set("scenario", row.twin_scenario_id);
    params.set("forecast_id", row.forecast_id);
    navigate(`/simulation?${params.toString()}`);
  }

  const rows = query.data.forecasts as unknown as Record<string, unknown>[];

  return (
    <div className="card moonshot-panel">
      <div className="moonshot-banner" role="status">
        {query.data.banner}
      </div>
      <p className="ai-off-note">
        Ranked hypotheses from CSV joins — not a control action. execute={String(query.data.execute)}. No Authorize /
        Execute on this panel.
      </p>
      <DataTable
        rows={rows}
        rowKey={(r) => String(r.forecast_id)}
        highlight={(r) => r.recommended_action === "ABSTAIN"}
        cols={[
          { key: "forecast_id", header: "id", render: (r) => String(r.forecast_id) },
          { key: "category", header: "category", render: (r) => String(r.category) },
          { key: "layer", header: "layer", render: (r) => String(r.layer) },
          { key: "asset_id", header: "asset", render: (r) => String(r.asset_id || "—") },
          { key: "confidence", header: "conf", render: (r) => String(r.confidence) },
          { key: "recommended_action", header: "action", render: (r) => String(r.recommended_action) },
          { key: "role", header: "role", render: (r) => String(r.required_role) },
          {
            key: "evidence",
            header: "evidence",
            render: (r) => ((r.evidence_ids as string[]) || []).join(", ") || "—",
          },
          {
            key: "twin",
            header: "",
            render: (r) => (
              <button type="button" onClick={() => loadInTwin(r as unknown as AdvisoryForecast)}>
                Load in twin
              </button>
            ),
          },
        ]}
      />
      {query.data.note && <p className="ai-off-note">{query.data.note}</p>}
    </div>
  );
}
