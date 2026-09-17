import { fmt } from "../utils/format";
import { UncertaintyBadge } from "./StateViews";

interface GraphNode {
  id: string;
  type: string;
  [key: string]: unknown;
}

interface GraphEdge {
  type: string;
  source: string;
  target: string;
  [key: string]: unknown;
}

export function GraphCitationView({ data }: { data: Record<string, unknown> }) {
  const nodes = (data.nodes as GraphNode[]) || [];
  const edges = (data.edges as GraphEdge[]) || [];
  const markers = data.scenario_markers as { timeline?: string[] } | undefined;

  return (
    <div className="graph-citation">
      <div className="graph-citation-meta">
        <span className="badge">{fmt(data.query)}</span>
        <span>
          {nodes.length} nodes · {edges.length} edges
        </span>
      </div>
      {data.note && <p className="ai-off-note">{fmt(data.note)}</p>}
      {Boolean(data.unit_join_missing) && (
        <p className="ai-off-note">Unit join missing — abstain required.</p>
      )}

      {Array.isArray(data.source_paths) && (data.source_paths as string[]).length > 0 && (
        <>
          <h4 className="graph-citation-heading">Source paths</h4>
          <ul className="graph-citation-list mono">
            {(data.source_paths as string[]).map((p) => (
              <li key={p}>{p}</li>
            ))}
          </ul>
        </>
      )}

      <h4 className="graph-citation-heading">Nodes</h4>
      <ul className="graph-citation-list mono">
        {nodes.map((n) => (
          <li key={n.id}>
            <span className="graph-citation-type">{fmt(n.type)}</span> {n.id}
          </li>
        ))}
      </ul>

      {edges.length > 0 && (
        <>
          <h4 className="graph-citation-heading">Relationships</h4>
          <div className="edge-list">
            {edges.map((e, i) => (
              <div key={i} className="edge-row">
                <span className="badge">{fmt(e.type)}</span>
                <span className="mono">{e.source}</span>
                <span>→</span>
                <span className="mono">{e.target}</span>
                {e.documented === "NO" && <UncertaintyBadge text="undocumented" />}
              </div>
            ))}
          </div>
        </>
      )}

      {markers?.timeline && markers.timeline.length > 0 && (
        <>
          <h4 className="graph-citation-heading">Timeline markers</h4>
          <ul className="graph-citation-list">
            {markers.timeline.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
