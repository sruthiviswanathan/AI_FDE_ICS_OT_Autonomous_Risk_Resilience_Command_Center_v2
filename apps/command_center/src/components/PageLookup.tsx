import { useState } from "react";
import { useApp } from "../context/AppContext";

type LookupFields = {
  plant?: boolean;
  asset?: boolean;
  alert?: boolean;
  tag?: boolean;
};

export function PageLookup({
  fields = { plant: true, asset: true, alert: true },
  onSearch,
}: {
  fields?: LookupFields;
  onSearch?: (values: { plantId: string; assetId: string; alertId: string; tagId?: string }) => void;
}) {
  const ctx = useApp();
  const [plant, setPlant] = useState(ctx.plantId);
  const [asset, setAsset] = useState(ctx.assetId);
  const [alert, setAlert] = useState(ctx.alertId);
  const [tag, setTag] = useState("");

  function runSearch() {
    if (fields.plant !== false) ctx.setPlantId(plant.trim());
    if (fields.asset !== false) ctx.setAssetId(asset.trim());
    if (fields.alert !== false) ctx.setAlertId(alert.trim());
    ctx.triggerLookup();
    onSearch?.({
      plantId: plant.trim(),
      assetId: asset.trim(),
      alertId: alert.trim(),
      tagId: tag.trim() || undefined,
    });
  }

  return (
    <div className="lookup-bar">
      {fields.plant !== false && (
        <label>
          Plant ID
          <input
            value={plant}
            onChange={(e) => setPlant(e.target.value)}
            placeholder="PLT-10"
            onKeyDown={(e) => e.key === "Enter" && runSearch()}
          />
        </label>
      )}
      {fields.asset !== false && (
        <label>
          Asset ID
          <input
            value={asset}
            onChange={(e) => setAsset(e.target.value)}
            placeholder="OT-01016"
            onKeyDown={(e) => e.key === "Enter" && runSearch()}
          />
        </label>
      )}
      {fields.alert !== false && (
        <label>
          Alert ID
          <input
            value={alert}
            onChange={(e) => setAlert(e.target.value)}
            placeholder="ALT-002783"
            onKeyDown={(e) => e.key === "Enter" && runSearch()}
          />
        </label>
      )}
      {fields.tag && (
        <label>
          Tag ID
          <input
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            placeholder="PLT-01-U03_TEMP"
            onKeyDown={(e) => e.key === "Enter" && runSearch()}
          />
        </label>
      )}
      <button type="button" className="primary" onClick={runSearch}>
        Search
      </button>
    </div>
  );
}
