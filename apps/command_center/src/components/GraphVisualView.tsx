import { useId } from "react";
import { fmt } from "../utils/format";
import {
  layoutGraph,
  layoutPathRows,
  nodeById,
  shortNodeLabel,
  type LayoutEdge,
  type LayoutNode,
  type NodePosition,
} from "../utils/graphLayout";

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

function nodeColor(node: LayoutNode): string {
  if (node.type === "RecoveryComponent") {
    return node.recovery_ready ? "#6bcb77" : "#e6a23c";
  }
  if (node.type === "Barrier" && node.state && node.state !== "ACTIVE") {
    return "#e74c3c";
  }
  return TYPE_COLORS[node.type] || "#5dade2";
}

function nodeRadius(node: LayoutNode, hubId: string | undefined): number {
  if (node.id === hubId || node.type === "Plant") return 32;
  return 24;
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
  showFullId = false,
}: {
  node: LayoutNode;
  pos: NodePosition;
  r: number;
  focused?: boolean;
  showFullId?: boolean;
}) {
  const fill = nodeColor(node);
  const label = showFullId ? node.id : shortNodeLabel(node.id);
  const crit = node.production_criticality ? fmt(node.production_criticality) : null;

  return (
    <g className={`graph-node${focused ? " graph-node-focus" : ""}`} transform={`translate(${pos.x}, ${pos.y})`}>
      <circle r={r + (focused ? 4 : 0)} fill="none" className="graph-node-focus-ring" opacity={focused ? 1 : 0} />
      <circle r={r} fill={fill} className="graph-node-circle" />
      <title>
        {node.id} ({node.type})
        {crit ? ` · criticality ${crit}` : ""}
      </title>
      <text y={5} className="graph-node-type">
        {node.type === "RecoveryComponent" ? "RC" : node.type.slice(0, 4).toUpperCase()}
      </text>
      <text y={r + 18} className="graph-node-label">
        {label}
      </text>
      {crit && (
        <text y={r + 32} className="graph-node-meta">
          crit: {crit}
        </text>
      )}
    </g>
  );
}

function PathGraphVisual({
  nodes,
  edges,
  focusAssetId,
  variant = "default",
  markerUndocId,
}: {
  nodes: LayoutNode[];
  edges: LayoutEdge[];
  focusAssetId?: string;
  variant?: "default" | "drawer";
  markerUndocId: string;
}) {
  const width = variant === "drawer" ? 520 : 960;
  const { rows, height } = layoutPathRows(edges, width, variant === "drawer" ? 84 : 96);
  const lookup = nodeById(nodes);

  return (
    <div className={`graph-visual-wrap graph-visual-path${variant === "drawer" ? " graph-visual-drawer" : ""}`}>
      <p className="graph-path-hint ai-off-note">
        Each row is one observed undocumented path. Source → target read left to right.
      </p>
      <svg
        className="graph-visual"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={`Process path graph with ${edges.length} paths`}
      >
        <defs>
          <marker id={markerUndocId} markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
            <path d="M0,0 L10,5 L0,10 Z" fill="var(--amber)" />
          </marker>
        </defs>

        {rows.map(({ edge, source, target, rowY }, index) => {
          const sourceNode = lookup.get(edge.source) || { id: edge.source, type: "Asset" };
          const targetNode = lookup.get(edge.target) || { id: edge.target, type: "Asset" };
          const r = variant === "drawer" ? 20 : 24;
          const line = edgeLineEndpoints(source, target, r + 8);
          const sourceFocus = Boolean(focusAssetId && edge.source === focusAssetId);
          const targetFocus = Boolean(focusAssetId && edge.target === focusAssetId);

          return (
            <g key={`${edge.source}-${edge.target}-${index}`} className="graph-path-row">
              <line x1={60} x2={width - 60} y1={rowY} y2={rowY} className="graph-path-row-guide" />
              <line
                x1={line.x1}
                y1={line.y1}
                x2={line.x2}
                y2={line.y2}
                className="graph-edge graph-edge-undoc graph-path-edge"
                markerEnd={`url(#${markerUndocId})`}
              />
              <text x={(source.x + target.x) / 2} y={rowY - 14} className="graph-path-edge-label">
                undocumented path
              </text>
              <GraphNodeGlyph node={sourceNode} pos={source} r={r} focused={sourceFocus} showFullId />
              <GraphNodeGlyph node={targetNode} pos={target} r={r} focused={targetFocus} showFullId />
            </g>
          );
        })}
      </svg>

      <div className="graph-legend">
        <span className="graph-legend-item">
          <span className="graph-legend-swatch" style={{ background: TYPE_COLORS.Asset }} />
          Asset
        </span>
        <span className="graph-legend-item">
          <span className="graph-legend-line graph-edge-undoc" />
          undocumented · observed 24h
        </span>
        {focusAssetId && (
          <span className="graph-legend-item">
            <span className="graph-legend-ring" />
            focus asset {focusAssetId}
          </span>
        )}
      </div>
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
}: {
  nodes: LayoutNode[];
  edges: LayoutEdge[];
  data: Record<string, unknown>;
  focusAssetId?: string;
  variant?: "default" | "drawer";
  markerId: string;
  markerUndocId: string;
}) {
  const width = variant === "drawer" ? 520 : 960;
  const height =
    variant === "drawer"
      ? Math.max(360, Math.min(520, 140 + nodes.length * 30))
      : Math.max(420, Math.min(640, 160 + nodes.length * 36));
  const positions = layoutGraph(nodes, edges, width, height, focusAssetId);

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
  const showEdgeLabels = new Set(edges.map((e) => e.type)).size > 1;

  const baseR = variant === "drawer" ? 22 : 28;

  return (
    <div className={`graph-visual-wrap${variant === "drawer" ? " graph-visual-drawer" : ""}`}>
      <svg
        className="graph-visual"
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label={`Graph slice ${fmt(data.query)} with ${nodes.length} nodes`}
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
              {showEdgeLabels && (
                <text x={(from.x + to.x) / 2} y={(from.y + to.y) / 2 - 8} className="graph-edge-label">
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
              r={nodeRadius(node, hubId) - (variant === "drawer" ? 4 : 0)}
              focused={Boolean(focusAssetId && node.id === focusAssetId)}
            />
          );
        })}
      </svg>

      <div className="graph-legend">
        {types.map((type) => (
          <span key={type} className="graph-legend-item">
            <span className="graph-legend-swatch" style={{ background: TYPE_COLORS[type] || "#5dade2" }} />
            {type}
          </span>
        ))}
        <span className="graph-legend-item">
          <span className="graph-legend-line graph-edge-undoc" />
          undocumented path
        </span>
      </div>
    </div>
  );
}

export function GraphVisualView({
  data,
  focusAssetId,
  variant = "default",
}: {
  data: Record<string, unknown>;
  focusAssetId?: string;
  variant?: "default" | "drawer";
}) {
  const uid = useId().replace(/:/g, "");
  const markerId = `graph-arrow-${uid}`;
  const markerUndocId = `graph-arrow-undoc-${uid}`;
  const nodes = (data.nodes as LayoutNode[]) || [];
  const edges = (data.edges as LayoutEdge[]) || [];

  if (!nodes.length) {
    return <p className="ai-off-note">No nodes in this slice.</p>;
  }

  if (data.query === "Q2" && edges.length > 0) {
    return (
      <PathGraphVisual
        nodes={nodes}
        edges={edges}
        focusAssetId={focusAssetId}
        variant={variant}
        markerUndocId={markerUndocId}
      />
    );
  }

  return (
    <NetworkGraphVisual
      nodes={nodes}
      edges={edges}
      data={data}
      focusAssetId={focusAssetId}
      variant={variant}
      markerId={markerId}
      markerUndocId={markerUndocId}
    />
  );
}
