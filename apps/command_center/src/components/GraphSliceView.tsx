import { useState } from "react";
import { fmt } from "../utils/format";
import { DetailGrid } from "./DetailGrid";
import { GraphVisualView } from "./GraphVisualView";
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

type GraphViewMode = "details" | "visual";

export function GraphSliceView({
  data,
  showVisualToggle = false,
  defaultView = "details",
  focusAssetId,
  expandable = false,
}: {
  data: Record<string, unknown>;
  showVisualToggle?: boolean;
  defaultView?: GraphViewMode;
  focusAssetId?: string;
  expandable?: boolean;
}) {
  const [view, setView] = useState<GraphViewMode>(defaultView);
  const nodes = (data.nodes as GraphNode[]) || [];
  const edges = (data.edges as GraphEdge[]) || [];
  const canVisualize = nodes.length > 0;

  return (
    <div>
      <DetailGrid
        columns={3}
        items={[
          { label: "Query", value: data.query },
          { label: "Hop cap", value: data.hop_cap },
          { label: "Undocumented paths (estate)", value: data.undocumented_total },
        ]}
      />
      {data.note && <p className="ai-off-note">{fmt(data.note)}</p>}

      {showVisualToggle && canVisualize && (
        <div className="btn-row graph-view-toggle">
          <button
            type="button"
            className={view === "visual" ? "primary" : ""}
            onClick={() => setView("visual")}
          >
            Visual graph
          </button>
          <button
            type="button"
            className={view === "details" ? "primary" : ""}
            onClick={() => setView("details")}
          >
            Node details
          </button>
        </div>
      )}

      {view === "visual" && canVisualize ? (
        <GraphVisualView data={data} focusAssetId={focusAssetId} expandable={expandable} />
      ) : (
        <>
      <h3 className="section-title">Nodes ({nodes.length})</h3>
      <div className="card-grid">
        {nodes.map((n) => (
          <div key={n.id} className="card node-card">
            <div className="node-type">{fmt(n.type)}</div>
            <div className="node-id">{n.id}</div>
            <DetailGrid
              columns={2}
              items={Object.entries(n)
                .filter(([k]) => !["id", "type"].includes(k))
                .map(([k, v]) => ({ label: k.replace(/_/g, " "), value: v }))}
            />
          </div>
        ))}
      </div>

      {edges.length > 0 && (
        <>
          <h3 className="section-title">Relationships ({edges.length})</h3>
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

      {Boolean(data.unit_join_missing) && (
        <div className="advisory-footer">Unit join missing — abstain / uncertainty required.</div>
      )}
        </>
      )}
    </div>
  );
}
