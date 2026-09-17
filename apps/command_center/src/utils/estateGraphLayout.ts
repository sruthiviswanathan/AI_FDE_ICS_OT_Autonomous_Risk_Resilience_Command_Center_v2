import type { PlantEstateRow, PostureLayerKey, PostureStatus } from "../api/client";

function postureCompositeFromPlant(plant: PlantEstateRow): PostureStatus {
  return plant.signals?.posture_composite ?? (plant.signals?.elevated ? "amber" : "ok");
}

export const ESTATE_GRAPH_REGIONS = ["NA", "EU", "APAC", "LATAM", "MEA"] as const;
export type EstateGraphRegion = (typeof ESTATE_GRAPH_REGIONS)[number];

export type EstateColorLayer =
  | "composite"
  | "cyber_exposure"
  | "safety_posture"
  | "recovery_credibility"
  | "evidence_quality";

export type EstateSizeMode = "criticality" | "assets";

export interface PlantNodeLayout {
  plant_id: string;
  x: number;
  y: number;
  region: string;
  radius: number;
}

const REGION_X: Record<string, number> = {
  NA: 96,
  EU: 288,
  APAC: 480,
  LATAM: 672,
  MEA: 864,
};

const ROW_HEIGHT = 100;
const START_Y = 100;
export const ESTATE_GRAPH_WIDTH = 960;
export const ESTATE_GRAPH_HEADER = 52;
const BOTTOM_PAD = 24;

export const COLOR_LAYER_OPTIONS: { id: EstateColorLayer; label: string }[] = [
  { id: "composite", label: "Composite" },
  { id: "cyber_exposure", label: "Cyber" },
  { id: "safety_posture", label: "Safety" },
  { id: "recovery_credibility", label: "Recovery" },
  { id: "evidence_quality", label: "Identity" },
];

export function layerStatusForPlant(plant: PlantEstateRow, mode: EstateColorLayer): PostureStatus {
  if (mode === "composite") return postureCompositeFromPlant(plant);
  const key = mode as PostureLayerKey;
  return plant.posture_layers?.[key]?.status ?? "ok";
}

export function layerReasonForPlant(plant: PlantEstateRow, mode: EstateColorLayer): string {
  if (mode === "composite") {
    if (!plant.posture_layers) return "All layers OK";
    const failing = Object.values(plant.posture_layers).filter((l) => l && l.status !== "ok");
    return failing.length ? failing.map((l) => l!.reason).join(" · ") : "All five layers OK";
  }
  const key = mode as PostureLayerKey;
  return plant.posture_layers?.[key]?.reason ?? "Layer OK";
}

export function postureFill(status: PostureStatus): string {
  if (status === "red") return "var(--red)";
  if (status === "amber") return "var(--amber)";
  return "var(--green)";
}

function nodeRadiusForPlant(
  plant: PlantEstateRow,
  mode: EstateSizeMode,
  plants: PlantEstateRow[],
  minR: number,
  maxR: number,
): number {
  if (mode === "criticality") {
    const c = (plant.criticality || "").toUpperCase();
    if (c === "HIGH") return maxR;
    if (c === "MEDIUM") return (minR + maxR) / 2;
    return minR;
  }
  const counts = plants.map((p) => p.counts?.assets ?? 0);
  const min = Math.min(...counts);
  const max = Math.max(...counts);
  const assets = plant.counts?.assets ?? 0;
  const t = max === min ? 0.5 : (assets - min) / (max - min);
  return minR + t * (maxR - minR);
}

export function layoutEstatePlantNodes(
  plants: PlantEstateRow[],
  sizeMode: EstateSizeMode,
): { nodes: PlantNodeLayout[]; height: number } {
  const byRegion: Record<string, PlantEstateRow[]> = {};
  for (const p of plants) {
    (byRegion[p.region] ??= []).push(p);
  }
  for (const list of Object.values(byRegion)) {
    list.sort((a, b) => a.plant_id.localeCompare(b.plant_id));
  }

  const maxRows = Math.max(1, ...Object.values(byRegion).map((l) => l.length));
  const height = START_Y + maxRows * ROW_HEIGHT + BOTTOM_PAD + 24;

  const nodes: PlantNodeLayout[] = [];
  for (const [region, list] of Object.entries(byRegion)) {
    const x = REGION_X[region] ?? REGION_X.NA;
    list.forEach((plant, index) => {
      nodes.push({
        plant_id: plant.plant_id,
        x,
        y: START_Y + index * ROW_HEIGHT,
        region,
        radius: nodeRadiusForPlant(plant, sizeMode, plants, 22, 36),
      });
    });
  }

  return { nodes, height };
}

export function plantByIdMap(plants: PlantEstateRow[]): Map<string, PlantEstateRow> {
  return new Map(plants.map((p) => [p.plant_id, p]));
}

export function regionLabelX(region: string): number {
  return REGION_X[region] ?? REGION_X.NA;
}

