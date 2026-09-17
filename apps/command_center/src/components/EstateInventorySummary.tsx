import type { EstateByPlantResponse, PlantEstateRow } from "../api/client";
import { resolveInventorySummary } from "../utils/estateDashboard";
import { CompositePostureBadge, PlantPostureBadges } from "./PlantPostureBadges";
import { DataTable } from "./DataTable";
import { fmt } from "../utils/format";

export function EstateInventorySummary({
  data,
  estateGlobal,
  selectedPlantId,
  onSelectPlant,
}: {
  data: EstateByPlantResponse;
  estateGlobal?: Record<string, unknown> | null;
  selectedPlantId: string;
  onSelectPlant: (plant: PlantEstateRow) => void;
}) {
  const inventory = resolveInventorySummary(data, estateGlobal);
  const selected = data.plants.find((p) => p.plant_id === selectedPlantId);

  return (
    <div className="card estate-inventory-summary">
      <h3>Inventory summary</h3>
      <div className="estate-kpi-strip">
        <span className="kpi-item">
          <strong>{inventory.totalAssets}</strong> assets
        </span>
        <span className="kpi-item">
          <strong>{inventory.totalAlerts}</strong> alerts recorded
        </span>
        <span className="kpi-item">
          <strong>{inventory.stateConflicts}</strong> state conflicts
        </span>
      </div>

      <h4 className="section-title">Alerts by plant</h4>
      {data.plants.length === 0 ? (
        <p className="ai-off-note">No plant inventory returned from API — restart backend to load /data/views/estate-by-plant.</p>
      ) : (
        <DataTable
          rows={data.plants}
          rowKey={(r) => r.plant_id}
          highlight={(r) => r.plant_id === selectedPlantId}
          cols={[
            {
              key: "plant",
              header: "Plant",
              render: (r) => (
                <button type="button" className="linkish" onClick={() => onSelectPlant(r)}>
                  {r.plant_id}
                </button>
              ),
            },
            { key: "region", header: "Region", render: (r) => fmt(r.region) },
            { key: "assets", header: "Assets", render: (r) => fmt(r.counts?.assets) },
            { key: "alerts", header: "Alerts", render: (r) => fmt(r.counts?.alerts_total) },
          { key: "hc", header: "HC", render: (r) => fmt(r.counts?.alerts_high_critical) },
          {
            key: "layers",
            header: "Posture layers",
            render: (r) => <PlantPostureBadges plant={r} compact />,
          },
          {
            key: "composite",
            header: "Composite",
            render: (r) => <CompositePostureBadge plant={r} />,
          },
          ]}
        />
      )}

      {selected && selected.top_assets_by_alerts && selected.top_assets_by_alerts.length > 0 && (
        <>
          <h4 className="section-title">Top assets by alert count · {selected.plant_id}</h4>
          <DataTable
            rows={selected.top_assets_by_alerts}
            rowKey={(r) => r.asset_id}
            cols={[
              { key: "asset", header: "Asset", render: (r) => fmt(r.asset_id) },
              { key: "alerts", header: "Alerts recorded", render: (r) => fmt(r.alert_count) },
            ]}
          />
        </>
      )}
    </div>
  );
}
