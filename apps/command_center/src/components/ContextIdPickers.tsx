import { useEffect, useState } from "react";
import { api, ApiError } from "../api/client";
import { useApp } from "../context/AppContext";

function catalogErrorMessage(err: unknown, label: string): string {
  if (err instanceof ApiError) {
    if (err.status === 404) {
      return `${label} catalog unavailable (404) — restart backend to pick up /plants routes`;
    }
    return `${label}: ${err.message}`;
  }
  return err instanceof Error ? err.message : `Failed to load ${label.toLowerCase()}`;
}

type LookupFields = {
  plant?: boolean;
  asset?: boolean;
  alert?: boolean;
};

interface CatalogPlant {
  plant_id: string;
  region?: string;
}

interface CatalogAsset {
  asset_id: string;
  asset_type?: string;
}

interface CatalogAlert {
  alert_id: string;
  severity?: string;
}

export function ContextIdPickers({
  fields = { plant: true, asset: true, alert: true },
  showSearch = true,
  onSearch,
}: {
  fields?: LookupFields;
  showSearch?: boolean;
  onSearch?: (values: { plantId: string; assetId: string; alertId: string }) => void;
}) {
  const ctx = useApp();
  const [plants, setPlants] = useState<CatalogPlant[]>([]);
  const [assets, setAssets] = useState<CatalogAsset[]>([]);
  const [alerts, setAlerts] = useState<CatalogAlert[]>([]);
  const [plantsLoading, setPlantsLoading] = useState(true);
  const [assetsLoading, setAssetsLoading] = useState(false);
  const [alertsLoading, setAlertsLoading] = useState(false);
  const [plantsError, setPlantsError] = useState<string | null>(null);
  const [assetsError, setAssetsError] = useState<string | null>(null);
  const [alertsError, setAlertsError] = useState<string | null>(null);
  useEffect(() => {
    let cancelled = false;
    setPlantsLoading(true);
    setPlantsError(null);
    api
      .plants()
      .then((res) => {
        if (!cancelled) setPlants(res.plants);
      })
      .catch((err) => {
        if (!cancelled) setPlantsError(catalogErrorMessage(err, "Plants"));
      })
      .finally(() => {
        if (!cancelled) setPlantsLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (fields.asset === false || !ctx.plantId || plantsLoading) return;
    let cancelled = false;
    setAssetsLoading(true);
    setAssetsError(null);
    api
      .plantAssets(ctx.plantId, 500)
      .then((res) => {
        if (cancelled) return;
        setAssets(res.assets);
        if (!res.assets.some((a) => a.asset_id === ctx.assetId)) {
          ctx.setAssetId(res.assets[0]?.asset_id || "");
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setAssetsError(catalogErrorMessage(err, "Assets"));
          setAssets([]);
        }
      })
      .finally(() => {
        if (!cancelled) setAssetsLoading(false);
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ctx.plantId, plantsLoading, fields.asset, ctx.lookupKey]);

  useEffect(() => {
    if (fields.alert === false || !ctx.assetId || assetsLoading) return;
    let cancelled = false;
    setAlertsLoading(true);
    setAlertsError(null);
    api
      .assetAlerts(ctx.assetId, 200)
      .then((res) => {
        if (cancelled) return;
        setAlerts(res.alerts);
        if (!res.alerts.some((a) => a.alert_id === ctx.alertId)) {
          ctx.setAlertId(res.alerts[0]?.alert_id || "");
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setAlertsError(catalogErrorMessage(err, "Alerts"));
          setAlerts([]);
        }
      })
      .finally(() => {
        if (!cancelled) setAlertsLoading(false);
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ctx.assetId, assetsLoading, fields.alert, ctx.lookupKey]);

  function onPlantChange(value: string) {
    ctx.setPlantId(value);
    if (fields.asset !== false) ctx.setAssetId("");
    if (fields.alert !== false) ctx.setAlertId("");
    ctx.triggerLookup();
  }

  function onAssetChange(value: string) {
    ctx.setAssetId(value);
    if (fields.alert !== false) ctx.setAlertId("");
    ctx.triggerLookup();
  }

  function onAlertChange(value: string) {
    ctx.setAlertId(value);
    ctx.triggerLookup();
  }

  function runSearch() {
    ctx.triggerLookup();
    onSearch?.({ plantId: ctx.plantId, assetId: ctx.assetId, alertId: ctx.alertId });
  }

  const catalogError = plantsError || assetsError || alertsError;
  const plantOptions =
    plants.length > 0
      ? plants
      : ctx.plantId
        ? [{ plant_id: ctx.plantId, region: undefined }]
        : [];
  const assetOptions =
    assets.length > 0
      ? assets
      : ctx.assetId
        ? [{ asset_id: ctx.assetId, asset_type: undefined }]
        : [];
  const alertOptions =
    alerts.length > 0
      ? alerts
      : ctx.alertId
        ? [{ alert_id: ctx.alertId, severity: undefined }]
        : [];

  return (
    <>
      {fields.plant !== false && (
        <label>
          Plant
          <select
            value={ctx.plantId}
            onChange={(e) => onPlantChange(e.target.value)}
            disabled={plantsLoading || (plantOptions.length === 0 && !plantsError)}
          >
            {plantsLoading && plantOptions.length === 0 && <option value="">Loading…</option>}
            {!plantsLoading && plantOptions.length === 0 && <option value="">No plants</option>}
            {plantOptions.map((p) => (
              <option key={p.plant_id} value={p.plant_id}>
                {p.plant_id}
                {p.region ? ` · ${p.region}` : ""}
              </option>
            ))}
          </select>
        </label>
      )}
      {fields.asset !== false && (
        <label>
          Asset
          <select
            value={ctx.assetId}
            onChange={(e) => onAssetChange(e.target.value)}
            disabled={!ctx.plantId || assetsLoading || (assetOptions.length === 0 && !assetsError)}
          >
            {assetsLoading && assetOptions.length === 0 && <option value="">Loading…</option>}
            {!assetsLoading && assetOptions.length === 0 && <option value="">No assets</option>}
            {assetOptions.map((a) => (
              <option key={a.asset_id} value={a.asset_id}>
                {a.asset_id}
                {a.asset_type ? ` · ${a.asset_type}` : ""}
              </option>
            ))}
          </select>
        </label>
      )}
      {fields.alert !== false && (
        <label>
          Alert
          <select
            value={ctx.alertId}
            onChange={(e) => onAlertChange(e.target.value)}
            disabled={!ctx.assetId || alertsLoading || (alertOptions.length === 0 && !alertsError)}
          >
            {alertsLoading && alertOptions.length === 0 && <option value="">Loading…</option>}
            {!alertsLoading && alertOptions.length === 0 && <option value="">No alerts</option>}
            {alertOptions.map((a) => (
              <option key={a.alert_id} value={a.alert_id}>
                {a.alert_id}
                {a.severity ? ` · ${a.severity}` : ""}
              </option>
            ))}
          </select>
        </label>
      )}
      {showSearch && (
        <button type="button" className="primary" onClick={runSearch}>
          Search
        </button>
      )}
      {catalogError && <span className="badge amber catalog-error">{catalogError}</span>}
    </>
  );
}
