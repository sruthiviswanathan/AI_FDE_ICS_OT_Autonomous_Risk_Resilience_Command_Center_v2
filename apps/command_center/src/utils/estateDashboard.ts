import type { EstateByPlantResponse, PlantEstateRow } from "../api/client";

export interface ResolvedInventorySummary {
  totalAssets: number;
  totalAlerts: number;
  stateConflicts: number;
  byRegisteredState: Record<string, number>;
  byObservedState: Record<string, number>;
  source: "api_summary" | "plants_aggregate" | "estate_view";
}

function mergeCountMaps(...maps: (Record<string, number> | undefined)[]): Record<string, number> {
  const out: Record<string, number> = {};
  for (const m of maps) {
    if (!m) continue;
    for (const [k, v] of Object.entries(m)) {
      out[k] = (out[k] ?? 0) + v;
    }
  }
  return out;
}

function aggregateFromPlants(plants: PlantEstateRow[]) {
  return {
    totalAssets: plants.reduce((s, p) => s + (p.counts?.assets ?? 0), 0),
    totalAlerts: plants.reduce((s, p) => s + (p.counts?.alerts_total ?? 0), 0),
    stateConflicts: plants.reduce((s, p) => s + (p.counts?.asset_state_conflicts ?? 0), 0),
    byRegisteredState: mergeCountMaps(...plants.map((p) => p.assets_by_registered_state)),
    byObservedState: mergeCountMaps(...plants.map((p) => p.assets_by_observed_state)),
  };
}

/** Map BE fields to inventory KPIs — falls back through plants[] and /data/views/estate. */
export function resolveInventorySummary(
  estateByPlant: EstateByPlantResponse,
  estateGlobal?: Record<string, unknown> | null,
): ResolvedInventorySummary {
  const plants = estateByPlant.plants ?? [];
  const fromPlants = aggregateFromPlants(plants);
  const apiSummary = estateByPlant.asset_status_summary;
  const globalCounts = estateGlobal?.counts as Record<string, number> | undefined;
  const globalSignals = estateGlobal?.derived_signals as Record<string, number> | undefined;

  if (apiSummary?.total_assets != null && apiSummary.total_assets > 0) {
    return {
      totalAssets: apiSummary.total_assets,
      totalAlerts: estateByPlant.total_alerts ?? fromPlants.totalAlerts,
      stateConflicts: apiSummary.state_conflicts ?? fromPlants.stateConflicts,
      byRegisteredState: apiSummary.by_registered_state ?? fromPlants.byRegisteredState,
      byObservedState: apiSummary.by_observed_state ?? fromPlants.byObservedState,
      source: "api_summary",
    };
  }

  if (globalCounts?.assets != null && globalCounts.assets > 0) {
    return {
      totalAssets: globalCounts.assets,
      totalAlerts: estateByPlant.total_alerts ?? fromPlants.totalAlerts,
      stateConflicts: globalSignals?.asset_state_conflicts ?? fromPlants.stateConflicts,
      byRegisteredState:
        Object.keys(fromPlants.byRegisteredState).length > 0
          ? fromPlants.byRegisteredState
          : (apiSummary?.by_registered_state ?? {}),
      byObservedState:
        Object.keys(fromPlants.byObservedState).length > 0
          ? fromPlants.byObservedState
          : (apiSummary?.by_observed_state ?? {}),
      source: "estate_view",
    };
  }

  if (fromPlants.totalAssets > 0 || fromPlants.totalAlerts > 0) {
    return {
      totalAssets: fromPlants.totalAssets,
      totalAlerts: estateByPlant.total_alerts ?? fromPlants.totalAlerts,
      stateConflicts: fromPlants.stateConflicts,
      byRegisteredState: fromPlants.byRegisteredState,
      byObservedState: fromPlants.byObservedState,
      source: "plants_aggregate",
    };
  }

  return {
    totalAssets: globalCounts?.assets ?? 0,
    totalAlerts: estateByPlant.total_alerts ?? 0,
    stateConflicts: globalSignals?.asset_state_conflicts ?? 0,
    byRegisteredState: apiSummary?.by_registered_state ?? {},
    byObservedState: apiSummary?.by_observed_state ?? {},
    source: "estate_view",
  };
}

export type SortMode = "plant_id" | "elevated" | "alert_hc" | "conflicts";

export const REGIONS = ["All", "NA", "EU", "APAC", "LATAM"] as const;
export type RegionFilter = (typeof REGIONS)[number];

export const REGION_ORDER = ["NA", "EU", "APAC", "LATAM"] as const;

export function assetConflict(row: Record<string, string>): boolean {
  return row.registered_state === "ACTIVE" && (row.observed_state === "OFFLINE" || row.observed_state === "UNSEEN");
}

export function postureCompositeRank(plant: PlantEstateRow): number {
  const c = plant.signals?.posture_composite ?? (plant.signals?.elevated ? "amber" : "ok");
  if (c === "red") return 2;
  if (c === "amber") return 1;
  return 0;
}

export function sortPlants(plants: PlantEstateRow[], mode: SortMode): PlantEstateRow[] {
  const copy = [...plants];
  switch (mode) {
    case "elevated":
      return copy.sort((a, b) => {
        const rankDiff = postureCompositeRank(b) - postureCompositeRank(a);
        if (rankDiff !== 0) return rankDiff;
        return a.plant_id.localeCompare(b.plant_id);
      });
    case "alert_hc":
      return copy.sort(
        (a, b) => b.counts.alerts_high_critical - a.counts.alerts_high_critical || a.plant_id.localeCompare(b.plant_id),
      );
    case "conflicts":
      return copy.sort(
        (a, b) => b.counts.asset_state_conflicts - a.counts.asset_state_conflicts || a.plant_id.localeCompare(b.plant_id),
      );
    default:
      return copy.sort((a, b) => a.plant_id.localeCompare(b.plant_id));
  }
}

export function heatIntensity(plant: PlantEstateRow): number {
  const rank = postureCompositeRank(plant);
  if (rank === 0) return 0.15;
  const redLayers = plant.posture_layers
    ? Object.values(plant.posture_layers).filter((l) => l?.status === "red").length
    : plant.signals.elevation_reasons.length;
  if (rank === 2) return Math.min(0.55 + redLayers * 0.12, 1);
  return Math.min(0.35 + redLayers * 0.08, 0.75);
}

export function estateKpis(plants: PlantEstateRow[]) {
  return {
    totalPlants: plants.length,
    elevated: plants.filter((p) => p.signals.elevated).length,
    totalAssets: plants.reduce((n, p) => n + p.counts.assets, 0),
    hcAlerts: plants.reduce((n, p) => n + p.counts.alerts_high_critical, 0),
    hcOpenKnown: plants.reduce((n, p) => n + p.counts.alerts_high_critical_open, 0),
  };
}
