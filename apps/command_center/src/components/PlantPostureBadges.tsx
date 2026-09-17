import type { PlantEstateRow, PostureLayer, PostureLayerKey, PostureStatus } from "../api/client";

export const POSTURE_LAYER_DEFS: {
  key: PostureLayerKey;
  short: string;
  title: string;
  legend: string;
}[] = [
  {
    key: "cyber_exposure",
    short: "Cyber",
    title: "Cyber exposure (SOC alert queue)",
    legend: "HIGH/CRITICAL alerts still OPEN or TRIAGED in the SOC queue.",
  },
  {
    key: "process_ops_disagreement",
    short: "Process",
    title: "Process / ops disagreement (process_context)",
    legend: "HC alerts where SOC severity and process/ops context disagree (DEGRADED or UNKNOWN).",
  },
  {
    key: "safety_posture",
    short: "Safety",
    title: "Safety posture (barriers / bypass)",
    legend: "Safety barriers degraded, or bypass authorized/unknown — verify with safety owner.",
  },
  {
    key: "recovery_credibility",
    short: "Recovery",
    title: "Recovery credibility (backup / runbook / deps)",
    legend: "Backup or runbook stale, or recovery dependencies not verified.",
  },
  {
    key: "evidence_quality",
    short: "Evidence",
    title: "Evidence quality (identity / state conflicts)",
    legend: "Registered vs observed asset state conflicts in the catalog.",
  },
];

function statusClass(status: PostureStatus): string {
  if (status === "red") return "posture-red";
  if (status === "amber") return "posture-amber";
  return "posture-ok";
}

export function postureComposite(plant: PlantEstateRow): PostureStatus {
  return plant.signals?.posture_composite ?? (plant.signals?.elevated ? "amber" : "ok");
}

export function PlantPostureBadges({
  plant,
  compact = false,
}: {
  plant: PlantEstateRow;
  compact?: boolean;
}) {
  const layers = plant.posture_layers;
  if (!layers) {
    return <span className="badge amber">layers n/a</span>;
  }

  return (
    <div className={`plant-posture-badges${compact ? " compact" : ""}`}>
      {POSTURE_LAYER_DEFS.map(({ key, short, title }) => {
        const layer: PostureLayer | undefined = layers[key];
        const status = layer?.status ?? "ok";
        return (
          <span
            key={key}
            className={`posture-pill ${statusClass(status)}`}
            title={layer?.reason ? `${title}: ${layer.reason}` : title}
          >
            {short}
          </span>
        );
      })}
    </div>
  );
}

export function PostureQuickLegend({ motto }: { motto?: string }) {
  return (
    <div className="posture-quick-legend">
      <p className="ai-off-note posture-motto">
        {motto ?? "cyber ≠ operational ≠ safety ≠ recovery — composite OK only when all five layers are OK"}
      </p>
      <div className="posture-layer-legend-grid">
        {POSTURE_LAYER_DEFS.map(({ short, title, legend }) => (
          <div key={short} className="posture-layer-legend-item">
            <span className="posture-pill posture-ok">{short}</span>
            <div>
              <strong className="posture-layer-legend-title">{title}</strong>
              <p className="posture-layer-legend-desc">{legend}</p>
            </div>
          </div>
        ))}
      </div>
      <div className="posture-color-legend">
        <span className="posture-color-legend-label">Pill color on each plant tile:</span>
        <span className="posture-pill posture-ok">OK</span>
        <span className="posture-legend-color-text">layer clear</span>
        <span className="posture-pill posture-amber">Caution</span>
        <span className="posture-legend-color-text">watch / unresolved</span>
        <span className="posture-pill posture-red">At risk</span>
        <span className="posture-legend-color-text">blocks composite OK</span>
      </div>
    </div>
  );
}

export function CompositePostureBadge({ plant }: { plant: PlantEstateRow }) {
  const composite = postureComposite(plant);
  if (composite === "ok") {
    return <span className="badge green">all layers OK</span>;
  }
  if (composite === "red") {
    return <span className="badge red">not OK</span>;
  }
  return <span className="badge amber">caution</span>;
}
