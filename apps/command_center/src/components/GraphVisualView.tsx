import { useId, useState } from "react";
import { GraphExpandModal } from "./GraphExpandModal";
import { fmt } from "../utils/format";
import {
  layoutDagreGraph,
  layoutPathRows,
  nodeById,
  shouldLabelEdge,
  shortNodeLabel,
  timelineRankForNode,
  type LayoutEdge,
  type LayoutNode,
  type NodePosition,
} from "../utils/graphLayout";
import { PanZoomSvg } from "./PanZoomSvg";

const TYPE_COLORS: Record<string, string> = {
  Plant: "#4a9eff",
  Asset: "#6bcb77",
  RecoveryComponent: "#e6a23c",
  Unit: "#9b59b6",
  Tag: "#1abc9c",
  Alert: "#e74c3c",
  Barrier: "#f39c12",
  Session: "#95a5a6",
  Alias: "#7f8c8d",
  UntrustedNote: "#c0392b",
};

const LEGEND_TYPES = ["Plant", "Asset", "Alert", "Barrier", "Session", "Unit", "Tag", "RecoveryComponent", "UntrustedNote"];

function nodeColor(node: LayoutNode): string {
  if (node.type === "RecoveryComponent") {
    return node.recovery_ready ? "#6bcb77" : "#e6a23c";
  }
  if (node.type === "Barrier" && node.state && node.state !== "ACTIVE") {
    return "#e74c3c";
  }
  return TYPE_COLORS[node.type] || "#5dade2";
}

function nodeRadius(node: LayoutNode, hubId: string | undefined, drawer: boolean): number {
  if (node.id === hubId || node.type === "Plant") return drawer ? 24 : 32;
  return drawer ? 18 : 24;
}

function edgeLineEndpoints(from: NodePosition, to: NodePosition, inset: number) {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  const len = Math.hypot(dx, dy) || 1;
  const ux = dx / len;
  const uy = dy / len;
  return {
    x1: from.x + ux * inset,
    y1: from.y + uy * inset,
    x2: to.x - ux * inset,
    y2: to.y - uy * inset,
  };
}

function GraphNodeGlyph({
  node,
  pos,
  r,
  focused,
  labelMaxLen,
}: {
  node: LayoutNode;
  pos: NodePosition;
  r: number;
  focused?: boolean;
  labelMaxLen: number;
}) {
  const fill = nodeColor(node);
  const label = shortNodeLabel(node.id, labelMaxLen);
  const crit = node.production_criticality ? fmt(node.production_criticality) : null;

  return (
    <g className={`graph-node${focused ? " graph-node-focus" : ""}`} transform={`translate(${pos.x}, ${pos.y})`}>
      <circle r={r + (focused ? 4 : 0)} fill="none" className="graph-node-focus-ring" opacity={focused ? 1 : 0} />
      <circle r={r} fill={fill} className="graph-node-circle" />
      <title>
        {node.id} ({node.type})
        {crit ? ` · criticality ${crit}` : ""}
      </title>
      <text y={4} className="graph-node-type">
        {node.type === "RecoveryComponent" ? "RC" : node.type.slice(0, 4).toUpperCase()}
      </text>
      <text y={r + 16} className="graph-node-label">
        {label}
      </text>
      {crit && (
        <text y={r + 28} className="graph-node-meta">
          crit: {crit}
        </text>
      )}
    </g>
  );
}

function GraphLegend({ types, focusAssetId }: { types: string[]; focusAssetId?: string }) {
  const ordered = LEGEND_TYPES.filter((t) => types.includes(t));
  const extra = types.filter((t) => !LEGEND_TYPES.includes(t));
  return (
    <div className="graph-legend">
      {[...ordered, ...extra].map((type) => (
        <span key={type} className="graph-legend-item">
          <span className="graph-legend-swatch" style={{ background: TYPE_COLORS[type] || "#5dade2" }} />
          {type}
        </span>
      ))}
      <span className="graph-legend-item">
        <span className="graph-legend-line graph-edge-undoc" />
        undocumented path
      </span>
      {focusAssetId && (
        <span className="graph-legend-item">
          <span className="graph-legend-ring" />
          focus {focusAssetId}
        </span>
      )}
    </div>
  );
}

function PathGraphVisual({
  nodes,
  edges,
  focusAssetId,
  variant = "default",
  markerUndocId,
  interactive = true,
}: {
  nodes: LayoutNode[];
  edges: LayoutEdge[];
  focusAssetId?: string;
  variant?: "default" | "drawer";
  markerUndocId: string;
  interactive?: boolean;
}) {
  const drawer = variant === "drawer";
  const width = drawer ? 280 : 960;
  const { rows, height } = layoutPathRows(edges, width, drawer ? 72 : 96);
  const lookup = nodeById(nodes);

  return (
    <div className={`graph-visual-wrap graph-visual-path${drawer ? " graph-visual-drawer" : ""}`}>
      <p className="graph-path-hint ai-off-note">
        Each row is one observed undocumented path. Source → target read left to right.
      </p>
      <PanZoomSvg
        className="graph-visual"
        width={width}
        height={height}
        enabled={interactive && !drawer && nodes.length > 6}
        ariaLabel={`Process path graph with ${edges.length} paths`}
      >
        <defs>
          <marker id={markerUndocId} markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 Z" fill="var(--amber)" />
          </marker>
        </defs>

        {rows.map(({ edge, source, target, rowY }, index) => {
          const sourceNode = lookup.get(edge.source) || { id: edge.source, type: "Asset" };
          const targetNode = lookup.get(edge.target) || { id: edge.target, type: "Asset" };
          const r = drawer ? 16 : 24;
          const line = edgeLineEndpoints(source, target, r + 6);
          return (
            <g key={`${edge.source}-${edge.target}-${index}`} className="graph-path-row">
              <line x1={40} x2={width - 40} y1={rowY} y2={rowY} className="graph-path-row-guide" />
              <line
                x1={line.x1}
                y1={line.y1}
                x2={line.x2}
                y2={line.y2}
                className="graph-edge graph-edge-undoc graph-path-edge"
                markerEnd={`url(#${markerUndocId})`}
              />
              <text x={(source.x + target.x) / 2} y={rowY - 12} className="graph-path-edge-label">
                undocumented path
              </text>
              <GraphNodeGlyph
                node={sourceNode}
                pos={source}
                r={r}
                focused={Boolean(focusAssetId && edge.source === focusAssetId)}
                labelMaxLen={drawer ? 10 : 14}
              />
              <GraphNodeGlyph
                node={targetNode}
                pos={target}
                r={r}
                focused={Boolean(focusAssetId && edge.target === focusAssetId)}
                labelMaxLen={drawer ? 10 : 14}
              />
            </g>
          );
        })}
      </PanZoomSvg>
      <GraphLegend types={["Asset"]} focusAssetId={focusAssetId} />
    </div>
  );
}

function NetworkGraphVisual({
  nodes,
  edges,
  data,
  focusAssetId,
  variant = "default",
  markerId,
  markerUndocId,
  interactive = true,
}: {
  nodes: LayoutNode[];
  edges: LayoutEdge[];
  data: Record<string, unknown>;
  focusAssetId?: string;
  variant?: "default" | "drawer";
  markerId: string;
  markerUndocId: string;
  interactive?: boolean;
}) {
  const drawer = variant === "drawer";
  const markers = (data.scenario_markers as { timeline?: string[] } | undefined)?.timeline;
  const useTimeline = data.query === "Q5" && markers && markers.length > 0;
  const query = String(data.query ?? "");

  const dagreLayout = layoutDagreGraph(nodes, edges, {
    rankdir: query === "Q4" ? "TB" : "LR",
    compact: drawer,
    nodeRank: useTimeline ? (node) => timelineRankForNode(node, markers!) : undefined,
  });
  const positions = dagreLayout.positions;
  const width = dagreLayout.width;
  const height = dagreLayout.height;

  const hubId =
    focusAssetId ??
    nodes.find((n) => n.type === "Plant")?.id ??
    nodes.reduce<{ id: string; degree: number } | null>((best, node) => {
      const degree = edges.filter((e) => e.source === node.id || e.target === node.id).length;
      if (!best || degree > best.degree) return { id: node.id, degree };
      return best;
    }, null)?.id;

  const types = [...new Set(nodes.map((n) => n.type))];
  const lookup = nodeById(nodes);
  const baseR = drawer ? 18 : 28;
  const labelMaxLen = drawer ? 10 : 14;
  const panZoom = interactive && !drawer && nodes.length > 5;

  return (
    <div className={`graph-visual-wrap${drawer ? " graph-visual-drawer" : ""}`}>
      {useTimeline && (
        <p className="graph-path-hint ai-off-note">Timeline cascade — read left to right (vendor → barrier → isolate → destabilize).</p>
      )}
      {panZoom && <p className="graph-path-hint ai-off-note">Drag to pan · scroll to zoom</p>}
      <PanZoomSvg
        className="graph-visual"
        width={width}
        height={height}
        enabled={panZoom}
        ariaLabel={`Graph slice ${fmt(data.query)} with ${nodes.length} nodes`}
      >
        <defs>
          <marker id={markerId} markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 Z" fill="var(--text-dim)" />
          </marker>
          <marker id={markerUndocId} markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 Z" fill="var(--amber)" />
          </marker>
        </defs>

        {edges.map((edge, index) => {
          const from = positions.get(edge.source);
          const to = positions.get(edge.target);
          if (!from || !to) return null;
          const undocumented = edge.documented === "NO";
          const line = edgeLineEndpoints(from, to, baseR);
          const labelEdge = shouldLabelEdge(edge.type, edges);
          return (
            <g key={`${edge.source}-${edge.target}-${index}`}>
              <line
                x1={line.x1}
                y1={line.y1}
                x2={line.x2}
                y2={line.y2}
                className={undocumented ? "graph-edge graph-edge-undoc" : "graph-edge"}
                markerEnd={undocumented ? `url(#${markerUndocId})` : `url(#${markerId})`}
              />
              {labelEdge && (
                <text x={(from.x + to.x) / 2} y={(from.y + to.y) / 2 - 6} className="graph-edge-label">
                  {fmt(edge.type)}
                </text>
              )}
            </g>
          );
        })}

        {nodes.map((node) => {
          const pos = positions.get(node.id);
          if (!pos) return null;
          return (
            <GraphNodeGlyph
              key={node.id}
              node={lookup.get(node.id) || node}
              pos={pos}
              r={nodeRadius(node, hubId, drawer)}
              focused={Boolean(focusAssetId && node.id === focusAssetId)}
              labelMaxLen={labelMaxLen}
            />
          );
        })}
      </PanZoomSvg>
      <GraphLegend types={types} focusAssetId={focusAssetId} />
    </div>
  );
}

export function GraphVisualView({
  data,
  focusAssetId,
  variant = "default",
  expandable = false,
}: {
  data: Record<string, unknown>;
  focusAssetId?: string;
  variant?: "default" | "drawer";
  expandable?: boolean;
}) {
  const [expanded, setExpanded] = useState(false);
  const uid = useId().replace(/:/g, "");
  const markerId = `graph-arrow-${uid}`;
  const markerUndocId = `graph-arrow-undoc-${uid}`;
  const nodes = (data.nodes as LayoutNode[]) || [];
  const edges = (data.edges as LayoutEdge[]) || [];
  const queryLabel = fmt(data.query);

  if (!nodes.length) {
    return <p className="ai-off-note">No nodes in this slice.</p>;
  }

  const previewInteractive = !expandable;

  const graphBody =
    data.query === "Q2" && edges.length > 0 ? (
      <PathGraphVisual
        nodes={nodes}
        edges={edges}
        focusAssetId={focusAssetId}
        variant={variant}
        markerUndocId={markerUndocId}
        interactive={previewInteractive}
      />
    ) : (
      <NetworkGraphVisual
        nodes={nodes}
        edges={edges}
        data={data}
        focusAssetId={focusAssetId}
        variant={variant}
        markerId={markerId}
        markerUndocId={markerUndocId}
        interactive={previewInteractive}
      />
    );

  if (!expandable) {
    return graphBody;
  }

  return (
    <>
      <button
        type="button"
        className="graph-expand-preview"
        onClick={() => setExpanded(true)}
        aria-label={`Open enlarged graph for ${queryLabel}`}
      >
        {graphBody}
        <span className="graph-expand-hint">Click to enlarge</span>
      </button>
      <GraphExpandModal
        open={expanded}
        onClose={() => setExpanded(false)}
        title={`Graph slice ${queryLabel}`}
      >
        <GraphVisualView data={data} focusAssetId={focusAssetId} variant="default" />
      </GraphExpandModal>
    </>
  );
}
