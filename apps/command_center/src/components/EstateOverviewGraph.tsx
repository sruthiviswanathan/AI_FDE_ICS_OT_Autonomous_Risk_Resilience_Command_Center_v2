import { useMemo, useState } from "react";
import type { PlantEstateRow } from "../api/client";
import { PanZoomSvg } from "./PanZoomSvg";
import {
  COLOR_LAYER_OPTIONS,
  ESTATE_GRAPH_HEADER,
  ESTATE_GRAPH_REGIONS,
  ESTATE_GRAPH_WIDTH,
  type EstateColorLayer,
  type EstateSizeMode,
  layerReasonForPlant,
  layerStatusForPlant,
  layoutEstatePlantNodes,
  plantByIdMap,
  postureFill,
  regionLabelX,
} from "../utils/estateGraphLayout";

function PlantNode({
  plant,
  node,
  dimmed,
  selected,
  colorLayer,
  onSelectPlant,
  onHover,
}: {
  plant: PlantEstateRow;
  node: { x: number; y: number; radius: number; plant_id: string };
  dimmed: boolean;
  selected: boolean;
  colorLayer: EstateColorLayer;
  onSelectPlant: (plant: PlantEstateRow) => void;
  onHover: (id: string | null) => void;
}) {
  const status = layerStatusForPlant(plant, colorLayer);
  const fill = postureFill(status);
  const reason = layerReasonForPlant(plant, colorLayer);

  return (
    <g
      data-panzoom-interactive
      className={`estate-plant-node${selected ? " selected" : ""}${dimmed ? " dimmed" : ""}`}
      transform={`translate(${node.x}, ${node.y})`}
      onClick={() => onSelectPlant(plant)}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onSelectPlant(plant);
        }
      }}
      onMouseEnter={() => onHover(node.plant_id)}
      onMouseLeave={() => onHover(null)}
      role="button"
      tabIndex={0}
      aria-label={`${node.plant_id} ${plant.region} ${plant.counts.assets} assets`}
    >
      <title>
        {node.plant_id} · {plant.region} · {plant.counts.assets} assets · {plant.counts.alerts_total} alerts · {reason}
      </title>
      <circle
        r={node.radius}
        fill={fill}
        fillOpacity={dimmed ? 0.25 : 0.9}
        stroke={selected ? "var(--accent)" : "var(--border)"}
        strokeWidth={selected ? 3 : 1.5}
      />
      {selected && (
        <circle r={node.radius + 8} fill="none" stroke="var(--accent)" strokeWidth={1.5} strokeDasharray="4 3" />
      )}
      <text className="estate-node-id" y={4} textAnchor="middle">
        {node.plant_id.replace("PLT-", "")}
      </text>
      <text className="estate-node-meta" y={node.radius + 16} textAnchor="middle">
        {plant.counts.assets}a · {plant.criticality}
      </text>
    </g>
  );
}

export function EstateOverviewGraph({
  plants,
  selectedPlantId,
  regionFilter,
  onSelectPlant,
}: {
  plants: PlantEstateRow[];
  selectedPlantId: string;
  regionFilter: string;
  onSelectPlant: (plant: PlantEstateRow) => void;
}) {
  const [colorLayer, setColorLayer] = useState<EstateColorLayer>("composite");
  const [sizeMode, setSizeMode] = useState<EstateSizeMode>("criticality");
  const [hoverId, setHoverId] = useState<string | null>(null);

  const plantMap = useMemo(() => plantByIdMap(plants), [plants]);
  const { nodes, height } = useMemo(
    () => layoutEstatePlantNodes(plants, sizeMode),
    [plants, sizeMode],
  );

  const orderedNodes = useMemo(() => {
    const unselected = nodes.filter((n) => n.plant_id !== selectedPlantId);
    const selected = nodes.find((n) => n.plant_id === selectedPlantId);
    return selected ? [...unselected, selected] : nodes;
  }, [nodes, selectedPlantId]);

  const hoverPlant = hoverId && hoverId !== selectedPlantId ? plantMap.get(hoverId) : null;

  return (
    <div className="estate-graph-panel">
      <div className="estate-graph-controls">
        <span className="filter-label">Color by</span>
        {COLOR_LAYER_OPTIONS.map(({ id, label }) => (
          <button
            key={id}
            type="button"
            className={colorLayer === id ? "chip active" : "chip"}
            onClick={() => setColorLayer(id)}
          >
            {label}
          </button>
        ))}
        <label className="estate-sort">
          Size
          <select value={sizeMode} onChange={(e) => setSizeMode(e.target.value as EstateSizeMode)}>
            <option value="criticality">Criticality</option>
            <option value="assets">Asset count</option>
          </select>
        </label>
      </div>
      <p className="ai-off-note estate-graph-hint">
        Composite = worst layer wins (cyber ≠ ops ≠ safety ≠ recovery). Click a plant → drill-down. Drag or scroll
        inside the map to pan/zoom.
      </p>
      <div className="estate-graph-viewport">
        <PanZoomSvg
          width={ESTATE_GRAPH_WIDTH}
          height={height}
          enabled
          className="estate-overview-svg"
          ariaLabel="Interactive estate plant map"
        >
        {ESTATE_GRAPH_REGIONS.map((region) => (
          <text
            key={region}
            x={regionLabelX(region)}
            y={ESTATE_GRAPH_HEADER}
            className="estate-region-label"
            textAnchor="middle"
          >
            {region}
          </text>
        ))}

        {orderedNodes.map((node) => {
          const plant = plantMap.get(node.plant_id);
          if (!plant) return null;
          const dimmed = regionFilter !== "All" && plant.region !== regionFilter;
          const selected = node.plant_id === selectedPlantId;

          return (
            <PlantNode
              key={node.plant_id}
              plant={plant}
              node={node}
              dimmed={dimmed}
              selected={selected}
              colorLayer={colorLayer}
              onSelectPlant={onSelectPlant}
              onHover={setHoverId}
            />
          );
        })}

        {hoverPlant && hoverId && (
          <foreignObject x={16} y={12} width={320} height={120} className="estate-graph-tooltip">
            <div xmlns="http://www.w3.org/1999/xhtml" className="estate-graph-tooltip-inner">
              <strong>{hoverPlant.plant_id}</strong>
              <div>
                {hoverPlant.region} · {hoverPlant.counts.assets} assets · {hoverPlant.counts.alerts_total} alerts
              </div>
              <div>{layerReasonForPlant(hoverPlant, colorLayer)}</div>
            </div>
          </foreignObject>
        )}
        </PanZoomSvg>
      </div>
    </div>
  );
}
