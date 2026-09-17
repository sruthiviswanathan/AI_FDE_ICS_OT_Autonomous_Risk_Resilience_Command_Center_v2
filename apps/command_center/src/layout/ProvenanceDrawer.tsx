import { useState } from "react";
import { api } from "../api/client";
import { GraphCitationView } from "../components/GraphCitationView";
import { GraphVisualView } from "../components/GraphVisualView";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";

const CHANNELS = ["STRUCTURED", "GRAPH", "VECTOR", "POLICY", "MEMORY"] as const;

export function ProvenanceDrawer() {
  const { provenancePin, lastPacket, aiEnabled, plantId, assetId, alertId, lookupKey } = useApp();
  const [channel, setChannel] = useState<(typeof CHANNELS)[number]>("STRUCTURED");
  const [graphView, setGraphView] = useState<"citations" | "visual">("visual");
  const health = useFetch(() => api.health(), []);
  const graph = useFetch(
    () =>
      channel === "GRAPH"
        ? api.graphSlice({
            query: "Q5",
            plant_id: plantId,
            asset_id: assetId || undefined,
            alert_id: alertId || undefined,
          })
        : Promise.resolve(null),
    [channel, plantId, assetId, alertId, lookupKey],
  );

  const packet = (lastPacket?.recommendation || {}) as Record<string, unknown>;
  const evidence = (packet.evidence || []) as Record<string, unknown>[];
  const backendNarrative = health.data?.ai_enabled === true;

  return (
    <aside className={`drawer${channel === "GRAPH" ? " drawer-graph-active" : ""}`}>
      <h3>Provenance &amp; Retrieval</h3>
      {provenancePin ? (
        <div className="card" style={{ marginBottom: "0.5rem" }}>
          <div className="mono">{provenancePin.source_path}</div>
          {provenancePin.record_id && <div>id: {provenancePin.record_id}</div>}
          {provenancePin.confidence !== undefined && <div>confidence: {provenancePin.confidence}</div>}
          <div>freshness: {provenancePin.freshness || "workshop-static"}</div>
        </div>
      ) : (
        <p className="ai-off-note">Click a source_path in tables to pin evidence.</p>
      )}

      <div className="channel-tabs">
        {CHANNELS.map((c) => (
          <button
            key={c}
            type="button"
            className={channel === c ? "active" : ""}
            onClick={() => setChannel(c)}
            disabled={c === "VECTOR"}
            title={c === "VECTOR" ? "VECTOR channel off — cannot set isolation or ACTION_TIERS" : undefined}
          >
            {c}
          </button>
        ))}
      </div>

      {channel === "STRUCTURED" && (
        <div>
          {evidence.length ? (
            <ul className="mono">
              {evidence.slice(0, 8).map((e, i) => (
                <li key={i}>{JSON.stringify(e)}</li>
              ))}
            </ul>
          ) : (
            <p className="ai-off-note">Structured evidence appears after recommendation packet.</p>
          )}
        </div>
      )}
      {channel === "GRAPH" && (
        <div>
          {graph.loading && <LoadingBlock label="Loading Q5 graph slice…" />}
          {graph.error && <ErrorBlock message={graph.error} />}
          {graph.data && (
            <>
              <div className="btn-row graph-view-toggle drawer-graph-toggle">
                <button
                  type="button"
                  className={graphView === "visual" ? "active" : ""}
                  onClick={() => setGraphView("visual")}
                >
                  Visual
                </button>
                <button
                  type="button"
                  className={graphView === "citations" ? "active" : ""}
                  onClick={() => setGraphView("citations")}
                >
                  Citations
                </button>
              </div>
              {graphView === "visual" ? (
                <GraphVisualView data={graph.data} focusAssetId={assetId || undefined} variant="drawer" />
              ) : (
                <GraphCitationView data={graph.data} />
              )}
            </>
          )}
          {!graph.loading && !graph.error && !graph.data && (
            <p className="ai-off-note">Graph slice unavailable for current context.</p>
          )}
        </div>
      )}
      {channel === "VECTOR" && (
        <p className="ai-off-note">VECTOR retrieval disabled. Cannot drive isolation or policy tiers.</p>
      )}
      {channel === "POLICY" && (
        <div className="mono">policy.py:ACTION_TIERS · tier 1 recommend · tier 3 requires human Authorize (OPEN-001)</div>
      )}
      {channel === "MEMORY" && <p className="ai-off-note">Decision traces append-only — not hidden CoT authority.</p>}

      <div className="card narrative-status" style={{ marginTop: "0.5rem" }}>
        {aiEnabled && backendNarrative ? (
          <>
            <strong>Narrative port reserved</strong>
            <p className="ai-off-note">
              Not connected. Tables and draft packets below are authoritative. Engines do not require a model (ADR-13).
            </p>
          </>
        ) : aiEnabled && !backendNarrative ? (
          <>
            <strong>Narrative unavailable</strong>
            <p className="ai-off-note">Backend reports ai_enabled=false — deterministic tables only (EVAL-016).</p>
          </>
        ) : (
          <>
            <strong>Deterministic advisory only</strong>
            <p className="ai-off-note">
              Ranks, recovery, and draft packets from rule engines. No narrative layer (ADR-12).
            </p>
          </>
        )}
      </div>
    </aside>
  );
}
