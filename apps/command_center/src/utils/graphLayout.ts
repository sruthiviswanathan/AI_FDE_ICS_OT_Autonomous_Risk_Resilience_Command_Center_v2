import dagre from "dagre";

export interface LayoutNode {
  id: string;
  type: string;
  [key: string]: unknown;
}

export interface LayoutEdge {
  type: string;
  source: string;
  target: string;
  [key: string]: unknown;
}

export interface NodePosition {
  x: number;
  y: number;
}

export interface PathRowLayout {
  edge: LayoutEdge;
  source: NodePosition;
  target: NodePosition;
  rowY: number;
}

export interface DagreLayoutResult {
  positions: Map<string, NodePosition>;
  width: number;
  height: number;
}

function adjacency(nodes: LayoutNode[], edges: LayoutEdge[]): Map<string, string[]> {
  const adj = new Map<string, string[]>();
  for (const node of nodes) adj.set(node.id, []);
  for (const edge of edges) {
    adj.get(edge.source)?.push(edge.target);
    adj.get(edge.target)?.push(edge.source);
  }
  return adj;
}

function pickRoot(nodes: LayoutNode[], adj: Map<string, string[]>): string {
  const plant = nodes.find((n) => n.type === "Plant");
  if (plant) return plant.id;

  let best = nodes[0]?.id;
  let bestDegree = -1;
  for (const node of nodes) {
    const degree = adj.get(node.id)?.length ?? 0;
    if (degree > bestDegree) {
      best = node.id;
      bestDegree = degree;
    }
  }
  return best;
}

/** Hub-and-spoke / layered layout — best for recovery (Q4) and connected slices. */
export function layoutGraph(
  nodes: LayoutNode[],
  edges: LayoutEdge[],
  width: number,
  height: number,
  focusNodeId?: string,
): Map<string, NodePosition> {
  const positions = new Map<string, NodePosition>();
  if (!nodes.length) return positions;

  if (nodes.length === 1) {
    positions.set(nodes[0].id, { x: width / 2, y: height / 2 });
    return positions;
  }

  const adj = adjacency(nodes, edges);
  const root =
    focusNodeId && nodes.some((node) => node.id === focusNodeId) ? focusNodeId : pickRoot(nodes, adj);
  const layers: string[][] = [];
  const visited = new Set<string>();
  let frontier = [root];

  while (frontier.length) {
    layers.push([...frontier]);
    frontier.forEach((id) => visited.add(id));
    const next: string[] = [];
    for (const id of frontier) {
      for (const neighbor of adj.get(id) || []) {
        if (!visited.has(neighbor) && !next.includes(neighbor)) next.push(neighbor);
      }
    }
    frontier = next;
  }

  for (const node of nodes) {
    if (!visited.has(node.id)) layers.push([node.id]);
  }

  const padX = 96;
  const padY = 72;
  const innerW = width - padX * 2;
  const innerH = height - padY * 2;
  const layerGap = layers.length > 1 ? innerH / (layers.length - 1) : 0;

  layers.forEach((layer, layerIndex) => {
    const y = layers.length === 1 ? height / 2 : padY + layerGap * layerIndex;
    const gap = innerW / (layer.length + 1);
    layer.forEach((id, nodeIndex) => {
      positions.set(id, { x: padX + gap * (nodeIndex + 1), y });
    });
  });

  return positions;
}

/** One row per path edge — readable for Q2 undocumented network paths. */
export function layoutPathRows(
  edges: LayoutEdge[],
  width: number,
  rowHeight = 96,
): { rows: PathRowLayout[]; height: number; width: number } {
  const sourceX = 160;
  const targetX = width - 160;
  const topPad = 48;

  const rows = edges.map((edge, index) => {
    const rowY = topPad + index * rowHeight + rowHeight / 2;
    return {
      edge,
      source: { x: sourceX, y: rowY },
      target: { x: targetX, y: rowY },
      rowY,
    };
  });

  return {
    rows,
    width,
    height: topPad * 2 + edges.length * rowHeight,
  };
}

const TIMELINE_TYPE_ORDER: { keyword: string; types: string[] }[] = [
  { keyword: "vendor session", types: ["Session"] },
  { keyword: "barrier", types: ["Barrier"] },
  { keyword: "isolate", types: ["Alert"] },
  { keyword: "destabilize", types: ["UntrustedNote"] },
];

function timelineColumnForNode(node: LayoutNode, timeline: string[]): number {
  const idLower = node.id.toLowerCase();
  for (let i = 0; i < timeline.length; i += 1) {
    const marker = timeline[i].toLowerCase();
    const rule = TIMELINE_TYPE_ORDER.find((r) => marker.includes(r.keyword));
    if (rule?.types.includes(node.type)) return i;
    if (idLower.includes(marker.split(" ").pop() || "")) return i;
  }
  if (node.type === "Asset") return Math.max(0, Math.floor(timeline.length / 2));
  if (node.type === "Tag" || node.type === "Unit") return Math.max(0, Math.floor(timeline.length / 2));
  return timeline.length;
}

/** Left-to-right cascade layout for Q5 incident slices with scenario_markers.timeline. */
export function layoutTimelineGraph(
  nodes: LayoutNode[],
  edges: LayoutEdge[],
  width: number,
  height: number,
  timeline: string[],
  focusNodeId?: string,
): Map<string, NodePosition> {
  const positions = new Map<string, NodePosition>();
  if (!nodes.length) return positions;

  const columns = timeline.length + 1;
  const buckets: LayoutNode[][] = Array.from({ length: columns }, () => []);

  for (const node of nodes) {
    const col = timeline.length ? timelineColumnForNode(node, timeline) : 0;
    buckets[col].push(node);
  }

  const padX = 56;
  const padY = 48;
  const innerW = width - padX * 2;
  const innerH = height - padY * 2;
  const colGap = columns > 1 ? innerW / (columns - 1) : 0;

  buckets.forEach((bucket, colIndex) => {
    const x = columns === 1 ? width / 2 : padX + colGap * colIndex;
    const rowGap = bucket.length > 1 ? innerH / (bucket.length - 1) : 0;
    bucket.forEach((node, rowIndex) => {
      const y = bucket.length === 1 ? height / 2 : padY + rowGap * rowIndex;
      positions.set(node.id, { x, y });
    });
  });

  if (focusNodeId && positions.has(focusNodeId)) {
    const pos = positions.get(focusNodeId)!;
    positions.set(focusNodeId, { ...pos, y: height / 2 });
  }

  return positions;
}

const SAFETY_CRITICAL_EDGES = new Set(["PROTECTS", "ALERT_ON", "SESSION_ON", "RECOVERY_FOR"]);

export function shouldLabelEdge(edgeType: string, allEdges: LayoutEdge[]): boolean {
  if (SAFETY_CRITICAL_EDGES.has(edgeType)) return true;
  const types = new Set(allEdges.map((e) => e.type));
  return types.size > 1;
}

export function shortNodeLabel(id: string, maxLen = 14): string {
  const tail = id.includes(":") ? id.split(":").pop()! : id;
  if (tail.length <= maxLen) return tail;
  return `${tail.slice(0, maxLen - 1)}…`;
}

export function nodeById(nodes: LayoutNode[]): Map<string, LayoutNode> {
  return new Map(nodes.map((n) => [n.id, n]));
}

export interface DagreLayoutOptions {
  rankdir?: "TB" | "LR" | "BT" | "RL";
  compact?: boolean;
  nodeRank?: (node: LayoutNode) => number | undefined;
}

/** Dagre hierarchical layout — reduces edge crossings vs hub-and-spoke. */
export function layoutDagreGraph(
  nodes: LayoutNode[],
  edges: LayoutEdge[],
  options: DagreLayoutOptions = {},
): DagreLayoutResult {
  const positions = new Map<string, NodePosition>();
  if (!nodes.length) return { positions, width: 320, height: 240 };

  const compact = options.compact ?? false;
  const nodeW = compact ? 72 : 120;
  const nodeH = compact ? 52 : 72;

  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({
    rankdir: options.rankdir ?? "LR",
    nodesep: compact ? 28 : 48,
    ranksep: compact ? 48 : 72,
    marginx: compact ? 16 : 32,
    marginy: compact ? 16 : 32,
    acyclicer: "greedy",
    ranker: "network-simplex",
  });

  for (const node of nodes) {
    const rank = options.nodeRank?.(node);
    g.setNode(node.id, {
      width: nodeW,
      height: nodeH,
      ...(rank !== undefined ? { rank } : {}),
    });
  }

  const nodeIds = new Set(nodes.map((n) => n.id));
  for (const edge of edges) {
    if (nodeIds.has(edge.source) && nodeIds.has(edge.target) && edge.source !== edge.target) {
      g.setEdge(edge.source, edge.target);
    }
  }

  dagre.layout(g);

  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;

  g.nodes().forEach((id) => {
    const layout = g.node(id);
    if (!layout) return;
    minX = Math.min(minX, layout.x - nodeW / 2);
    minY = Math.min(minY, layout.y - nodeH / 2);
    maxX = Math.max(maxX, layout.x + nodeW / 2);
    maxY = Math.max(maxY, layout.y + nodeH / 2);
  });

  const pad = compact ? 16 : 28;
  const offsetX = Number.isFinite(minX) ? -minX + pad : pad;
  const offsetY = Number.isFinite(minY) ? -minY + pad : pad;

  g.nodes().forEach((id) => {
    const layout = g.node(id);
    if (!layout) return;
    positions.set(id, { x: layout.x + offsetX, y: layout.y + offsetY });
  });

  return {
    positions,
    width: Math.max(compact ? 300 : 520, maxX - minX + pad * 2),
    height: Math.max(compact ? 240 : 400, maxY - minY + pad * 2),
  };
}

/** Q5 timeline ranks for dagre left-to-right cascade. */
export function timelineRankForNode(node: LayoutNode, timeline: string[]): number | undefined {
  if (!timeline.length) return undefined;
  return timelineColumnForNode(node, timeline);
}
