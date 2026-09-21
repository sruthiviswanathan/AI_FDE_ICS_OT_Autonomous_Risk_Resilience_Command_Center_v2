import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { api } from "../api/client";
import { GraphCitationView } from "../components/GraphCitationView";
import { GraphVisualView } from "../components/GraphVisualView";
import { ProvenanceMemoryView } from "../components/ProvenanceMemoryView";
import { ProvenancePolicyView } from "../components/ProvenancePolicyView";
import { ProvenanceStructuredView } from "../components/ProvenanceStructuredView";
import { GraphAsyncContent } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { usePersona } from "../hooks/usePersona";
import { useFetch } from "../hooks/useFetch";
import { pageProvenanceFor } from "../utils/pageProvenance";
import { deriveGraphQuery, graphQueryLabel } from "../utils/provenanceContext";

const CHANNELS = ["STRUCTURED", "GRAPH", "VECTOR", "POLICY", "MEMORY"] as const;

export function ProvenanceDrawer() {
  const location = useLocation();
  const page = useMemo(() => pageProvenanceFor(location.pathname), [location.pathname]);
  const {
    provenancePin,
    lastPacket,
    plantId,
    assetId,
    alertId,
    lookupKey,
    personaId,
    provenanceOpen,
    setProvenanceOpen,
    pinProvenance,
    clearProvenancePin,
  } = useApp();
  const { view } = usePersona();
  const [channel, setChannel] = useState<(typeof CHANNELS)[number]>(page.preferredChannel);

  useEffect(() => {
    setChannel(page.preferredChannel);
    clearProvenancePin();
    // Pin from the previous screen is not evidence for this one.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page.route]);

  useEffect(() => {
    setChannel(page.preferredChannel);
  }, [personaId, page.preferredChannel]);

  const [graphView, setGraphView] = useState<"citations" | "visual">("visual");

  const graphQuery = useMemo(
    () => page.graphQuery ?? deriveGraphQuery({ alertId, assetId, plantId }),
    [page.graphQuery, alertId, assetId, plantId],
  );

  const graph = useFetch(
    () =>
      channel === "GRAPH" && plantId
        ? api.graphSlice({
            query: graphQuery,
            plant_id: plantId,
            asset_id: assetId || undefined,
            alert_id: alertId || undefined,
          })
        : Promise.resolve(null),
    [channel, graphQuery, plantId, assetId, alertId, lookupKey],
  );

  const packet = (lastPacket?.recommendation || lastPacket || {}) as Record<string, unknown>;
  const packetEvidence = (packet.evidence || []) as Record<string, unknown>[];

  if (!provenanceOpen && view.id === "executive") {
    return (
      <aside className="drawer drawer-collapsed">
        <h3>Provenance</h3>
        <p className="ai-off-note">Collapsed for Executive view — expand when reviewing evidence.</p>
        <button type="button" className="primary" onClick={() => setProvenanceOpen(true)}>
          Show provenance drawer
        </button>
      </aside>
    );
  }

  return (
    <aside className={`drawer${channel === "GRAPH" ? " drawer-graph-active" : ""}`}>
      <h3>Provenance &amp; Retrieval</h3>
      <p className="provenance-screen-title">{page.title}</p>

      <div className="provenance-context-strip mono">
        <span>{page.screenId}</span>
        {plantId && <span>{plantId}</span>}
        {assetId && <span>{assetId}</span>}
        {alertId && <span>{alertId}</span>}
        {!plantId && !assetId && !alertId && <span className="ai-off-note">No plant / asset / alert pinned</span>}
      </div>

      {provenancePin ? (
        <div className="card" style={{ marginBottom: "0.5rem" }}>
          {provenancePin.label && <div>{provenancePin.label}</div>}
          <div className="mono">{provenancePin.source_path}</div>
          {provenancePin.record_id && <div>id: {provenancePin.record_id}</div>}
          {provenancePin.confidence !== undefined && <div>confidence: {provenancePin.confidence}</div>}
          <div>freshness: {provenancePin.freshness || "—"}</div>
        </div>
      ) : (
        <p className="ai-off-note">Click a source below, or a provenance link in the table, to pin it here.</p>
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
        <ProvenanceStructuredView
          page={page}
          plantId={plantId}
          assetId={assetId}
          alertId={alertId}
          lookupKey={lookupKey}
          packetEvidence={packetEvidence}
          onPin={pinProvenance}
        />
      )}

      {channel === "GRAPH" && (
        <div>
          <p className="ai-off-note provenance-graph-label">
            {page.graphQuery
              ? `${graphQueryLabel(graphQuery)} (${graphQuery}) — graph for this screen`
              : `${graphQueryLabel(graphQuery)} (${graphQuery}) — neighborhood of pinned context (this screen is not a graph workbench)`}
            {!plantId && " — select a plant"}
          </p>
          {!plantId && <p className="ai-off-note">Graph slice requires plant context.</p>}
          {plantId && (
            <GraphAsyncContent
              loading={graph.loading}
              error={graph.error}
              label={`Loading ${graphQueryLabel(graphQuery)} graph (${graphQuery})…`}
            >
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
                    <GraphVisualView
                      data={graph.data}
                      focusAssetId={assetId || undefined}
                      variant="drawer"
                      expandable
                    />
                  ) : (
                    <GraphCitationView data={graph.data} />
                  )}
                </>
              )}
            </GraphAsyncContent>
          )}
        </div>
      )}

      {channel === "VECTOR" && (
        <p className="ai-off-note">VECTOR retrieval disabled. Cannot drive isolation or policy tiers.</p>
      )}

      {channel === "POLICY" && <ProvenancePolicyView lookupKey={lookupKey} page={page} />}

      {channel === "MEMORY" && (
        <ProvenanceMemoryView
          plantId={plantId}
          assetId={assetId}
          alertId={alertId}
          lookupKey={lookupKey}
          page={page}
        />
      )}
    </aside>
  );
}
