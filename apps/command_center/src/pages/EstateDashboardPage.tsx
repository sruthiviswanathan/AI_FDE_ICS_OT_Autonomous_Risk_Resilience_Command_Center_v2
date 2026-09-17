import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api, type PlantEstateRow } from "../api/client";
import { DataTable } from "../components/DataTable";
import { EstateInventorySummary } from "../components/EstateInventorySummary";
import {
  CompositePostureBadge,
  PlantPostureBadges,
  PostureQuickLegend,
  postureComposite,
} from "../components/PlantPostureBadges";
import { GraphSliceView } from "../components/GraphSliceView";
import { ErrorBlock, LoadingBlock, StaleBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import {
  assetConflict,
  heatIntensity,
  REGIONS,
  sortPlants,
  type RegionFilter,
  type SortMode,
} from "../utils/estateDashboard";
import { fmt } from "../utils/format";

export function EstateDashboardPage() {
  const ctx = useApp();
  const [searchParams, setSearchParams] = useSearchParams();
  const drillRef = useRef<HTMLDivElement>(null);

  const [regionFilter, setRegionFilter] = useState<RegionFilter>("All");
  const [sortMode, setSortMode] = useState<SortMode>("elevated");
  const [assetSearch, setAssetSearch] = useState("");
  const [debouncedAssetSearch, setDebouncedAssetSearch] = useState("");
  const [localAssetId, setLocalAssetId] = useState(ctx.assetId);

  const estate = useFetch(() => api.estateByPlant({ includeTopAlerts: 5 }), []);
  const estateGlobal = useFetch(() => api.estate(), []);

  useEffect(() => {
    const t = window.setTimeout(() => setDebouncedAssetSearch(assetSearch.trim()), 250);
    return () => window.clearTimeout(t);
  }, [assetSearch]);

  useEffect(() => {
    const plant = searchParams.get("plant");
    const asset = searchParams.get("asset");
    const alert = searchParams.get("alert");
    if (plant) ctx.setPlantId(plant);
    if (asset) {
      ctx.setAssetId(asset);
      setLocalAssetId(asset);
    }
    if (alert) ctx.setAlertId(alert);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setLocalAssetId(ctx.assetId);
  }, [ctx.assetId]);

  const syncUrl = useCallback(
    (plant: string, asset: string, alert: string) => {
      const next = new URLSearchParams(searchParams);
      if (plant) next.set("plant", plant);
      else next.delete("plant");
      if (asset) next.set("asset", asset);
      else next.delete("asset");
      if (alert) next.set("alert", alert);
      else next.delete("alert");
      setSearchParams(next, { replace: true });
    },
    [searchParams, setSearchParams],
  );

  const scrollToDrillDown = useCallback(() => {
    window.requestAnimationFrame(() => {
      drillRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }, []);

  const selectPlant = useCallback(
    (plant: PlantEstateRow) => {
      ctx.setPlantId(plant.plant_id);
      const top = plant.top_alerts[0];
      if (top?.asset_id) {
        ctx.setAssetId(top.asset_id);
        setLocalAssetId(top.asset_id);
        ctx.setAlertId(top.alert_id || "");
        syncUrl(plant.plant_id, top.asset_id, top.alert_id || "");
      } else {
        ctx.setAlertId("");
        syncUrl(plant.plant_id, ctx.assetId, "");
      }
      ctx.triggerLookup();
      scrollToDrillDown();
    },
    [ctx, syncUrl, scrollToDrillDown],
  );

  const selectAsset = useCallback(
    (assetId: string) => {
      ctx.setAssetId(assetId);
      setLocalAssetId(assetId);
      ctx.setAlertId("");
      syncUrl(ctx.plantId, assetId, "");
      ctx.triggerLookup();
    },
    [ctx, syncUrl],
  );

  const selectAlert = useCallback(
    (alert: Record<string, string>) => {
      ctx.setAlertId(alert.alert_id);
      if (alert.asset_id) {
        ctx.setAssetId(alert.asset_id);
        setLocalAssetId(alert.asset_id);
      }
      syncUrl(ctx.plantId, alert.asset_id || ctx.assetId, alert.alert_id);
      ctx.triggerLookup();
    },
    [ctx, syncUrl],
  );

  const assetsQuery = useFetch(
    () =>
      ctx.plantId
        ? api.plantAssets(ctx.plantId, 500, debouncedAssetSearch || undefined)
        : Promise.reject(new Error("No plant selected")),
    [ctx.plantId, debouncedAssetSearch, ctx.lookupKey],
  );

  const alertsQuery = useFetch(
    () =>
      localAssetId
        ? api.assetAlerts(localAssetId, 50)
        : Promise.resolve({ asset_id: "", count: 0, limit: 50, alerts: [] as Record<string, string>[] }),
    [localAssetId, ctx.lookupKey],
  );

  const graphQuery = ctx.alertId ? "Q5" : localAssetId ? "Q1" : "Q4";
  const graph = useFetch(
    () =>
      ctx.plantId
        ? api.graphSlice({
            query: graphQuery,
            plant_id: ctx.plantId,
            asset_id: localAssetId || ctx.assetId,
            alert_id: ctx.alertId || undefined,
          })
        : Promise.reject(new Error("No plant selected")),
    [ctx.plantId, localAssetId, ctx.assetId, ctx.alertId, graphQuery, ctx.lookupKey],
  );

  const filteredPlants = useMemo(() => {
    const plants = estate.data?.plants || [];
    const regionFiltered = regionFilter === "All" ? plants : plants.filter((p) => p.region === regionFilter);
    return sortPlants(regionFiltered, sortMode);
  }, [estate.data, regionFilter, sortMode]);

  useEffect(() => {
    if (!assetsQuery.data?.assets?.length || !ctx.plantId) return;
    const assets = assetsQuery.data.assets;
    const hasLocal = assets.some((a) => a.asset_id === localAssetId);
    if (hasLocal) return;
    const topAlerts = estate.data?.plants.find((p) => p.plant_id === ctx.plantId)?.top_alerts || [];
    const hcAsset = assets.find((a) => topAlerts.some((al) => al.asset_id === a.asset_id));
    const next = hcAsset?.asset_id || assets[0]?.asset_id;
    if (next) {
      setLocalAssetId(next);
      ctx.setAssetId(next);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [assetsQuery.data, ctx.plantId, estate.data]);

  const selectedPlant = estate.data?.plants.find((p) => p.plant_id === ctx.plantId);

  return (
    <div>
      <h2 className="page-title">Estate Dashboard</h2>
      <StaleBadge />
      <p className="ai-off-note">
        <Link to="/">← Control Tower</Link>
        {" · "}
        Interactive plant / asset / alert view — inventory signals, not contextual risk rank.
      </p>

      {estate.loading && <LoadingBlock />}
      {estate.error && <ErrorBlock message={estate.error} />}

      {estate.data && (
        <>
          <EstateInventorySummary
            data={estate.data}
            estateGlobal={estateGlobal.data}
            selectedPlantId={ctx.plantId}
            onSelectPlant={selectPlant}
          />

          <div className="card estate-overview-card">
            <h3>Estate map — layered posture</h3>
            <PostureQuickLegend motto={estate.data.methodology.posture_motto} />
            <p className="ai-off-note" title={estate.data.methodology.posture_composite_rule}>
              {estate.data.methodology.not_operational_risk_rank}
            </p>
            <div className="estate-filters">
              <span className="filter-label">Region</span>
              {REGIONS.map((r) => (
                <button
                  key={r}
                  type="button"
                  className={regionFilter === r ? "chip active" : "chip"}
                  onClick={() => setRegionFilter(r)}
                >
                  {r}
                </button>
              ))}
              <label className="estate-sort">
                Sort
                <select value={sortMode} onChange={(e) => setSortMode(e.target.value as SortMode)}>
                  <option value="plant_id">Plant ID</option>
                  <option value="elevated">Elevated first</option>
                  <option value="alert_hc">Alert HC (inventory)</option>
                  <option value="conflicts">Asset conflicts</option>
                </select>
              </label>
            </div>
            <div className="plant-heatmap-grid">
              {filteredPlants.map((plant) => {
                const selected = plant.plant_id === ctx.plantId;
                const composite = postureComposite(plant);
                const intensity = heatIntensity(plant);
                const layerTooltip = plant.posture_layers
                  ? Object.values(plant.posture_layers)
                      .filter((l) => l && l.status !== "ok")
                      .map((l) => l!.reason)
                      .join(" · ")
                  : "";
                return (
                  <button
                    key={plant.plant_id}
                    type="button"
                    className={`plant-tile plant-tile-layered posture-${composite}${selected ? " selected" : ""}`}
                    title={layerTooltip || "All five posture layers OK"}
                    onClick={() => selectPlant(plant)}
                  >
                    <div className="plant-tile-head">
                      <span className="mono">{plant.plant_id}</span>
                      <CompositePostureBadge plant={plant} />
                    </div>
                    <div className="plant-tile-meta">
                      {plant.region} · {plant.counts.assets} assets · {plant.counts.alerts_total} alerts
                    </div>
                    <PlantPostureBadges plant={plant} compact />
                    <div
                      className={`plant-tile-bar posture-bar-${composite}`}
                      style={{ transform: `scaleX(${intensity})` }}
                      aria-hidden
                    />
                  </button>
                );
              })}
            </div>
          </div>

          {ctx.plantId && (
            <div className="card drill-down-panel" ref={drillRef}>
              <h3>
                Drill-down · {ctx.plantId}
                {selectedPlant && (
                  <span style={{ marginLeft: "0.5rem" }}>
                    <CompositePostureBadge plant={selectedPlant} />
                  </span>
                )}
              </h3>
              {selectedPlant?.posture_layers && (
                <div style={{ marginBottom: "0.5rem" }}>
                  <PlantPostureBadges plant={selectedPlant} />
                </div>
              )}
              <div className="drill-down-grid">
                <div className="drill-col">
                  <h4 className="section-title">Assets</h4>
                  <input
                    className="lookup-input"
                    placeholder="Search asset prefix…"
                    value={assetSearch}
                    onChange={(e) => setAssetSearch(e.target.value)}
                  />
                  {assetsQuery.loading && <LoadingBlock />}
                  {assetsQuery.error && <ErrorBlock message={assetsQuery.error} />}
                  {assetsQuery.data && assetsQuery.data.assets.length > 0 ? (
                    <DataTable
                      rows={assetsQuery.data.assets}
                      rowKey={(r) => r.asset_id}
                      highlight={(r) => r.asset_id === localAssetId}
                      cols={[
                        {
                          key: "id",
                          header: "Asset",
                          render: (r) => (
                            <button type="button" className="linkish" onClick={() => selectAsset(r.asset_id)}>
                              {r.asset_id}
                            </button>
                          ),
                        },
                        { key: "type", header: "Type", render: (r) => fmt(r.asset_type) },
                        { key: "zone", header: "Zone", render: (r) => fmt(r.zone) },
                        {
                          key: "alerts",
                          header: "Alerts",
                          render: (r) => fmt(r.alert_count ?? "0"),
                        },
                        {
                          key: "state",
                          header: "Reg / Obs",
                          render: (r) => (
                            <>
                              {fmt(r.registered_state)} / {fmt(r.observed_state)}
                              {assetConflict(r) && (
                                <Link to="/identity" className="badge red" style={{ marginLeft: "0.25rem" }}>
                                  conflict
                                </Link>
                              )}
                            </>
                          ),
                        },
                      ]}
                    />
                  ) : (
                    assetsQuery.data && <p className="ai-off-note">No assets in catalog for this plant.</p>
                  )}
                </div>

                <div className="drill-col">
                  <h4 className="section-title">Alerts {localAssetId ? `· ${localAssetId}` : ""}</h4>
                  {alertsQuery.loading && <LoadingBlock />}
                  {alertsQuery.error && <ErrorBlock message={alertsQuery.error} />}
                  {alertsQuery.data && alertsQuery.data.alerts.length > 0 ? (
                    <DataTable
                      rows={alertsQuery.data.alerts}
                      rowKey={(r) => r.alert_id}
                      highlight={(r) => r.alert_id === ctx.alertId}
                      cols={[
                        {
                          key: "id",
                          header: "Alert",
                          render: (r) => (
                            <button type="button" className="linkish" onClick={() => selectAlert(r)}>
                              {r.alert_id}
                            </button>
                          ),
                        },
                        { key: "sev", header: "Sev", render: (r) => fmt(r.severity) },
                        { key: "type", header: "Type", render: (r) => fmt(r.type) },
                        { key: "soc", header: "SOC", render: (r) => fmt(r.soc_status) },
                        {
                          key: "ctx",
                          header: "Process",
                          render: (r) =>
                            r.process_context === "UNKNOWN" ? (
                              <span className="badge amber">{fmt(r.process_context)}</span>
                            ) : (
                              fmt(r.process_context)
                            ),
                        },
                      ]}
                    />
                  ) : (
                    localAssetId && alertsQuery.data && <p className="ai-off-note">No alerts indexed for this asset.</p>
                  )}
                  {ctx.alertId && (
                    <div className="btn-row" style={{ marginTop: "0.5rem" }}>
                      <Link to="/incident">Incident graph →</Link>
                      <Link to="/risk">Risk workbench →</Link>
                      <Link to="/safety">Safety board →</Link>
                    </div>
                  )}
                </div>

                <div className="drill-col drill-graph-col">
                  <h4 className="section-title">Neighborhood graph</h4>
                  <p className="ai-off-note">Hop-capped slice — not full estate topology (NFR-CAP)</p>
                  {graph.loading && <LoadingBlock />}
                  {graph.error && <ErrorBlock message={graph.error} />}
                  {graph.data && (
                    <GraphSliceView
                      data={graph.data}
                      showVisualToggle
                      defaultView="visual"
                      focusAssetId={localAssetId}
                      expandable
                    />
                  )}
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
