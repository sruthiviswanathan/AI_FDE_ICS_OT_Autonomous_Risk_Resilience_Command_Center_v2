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

export function shortNodeLabel(id: string): string {
  const tail = id.includes(":") ? id.split(":").pop()! : id;
  return tail.length > 14 ? `${tail.slice(0, 12)}…` : tail;
}

export function nodeById(nodes: LayoutNode[]): Map<string, LayoutNode> {
  return new Map(nodes.map((n) => [n.id, n]));
}
