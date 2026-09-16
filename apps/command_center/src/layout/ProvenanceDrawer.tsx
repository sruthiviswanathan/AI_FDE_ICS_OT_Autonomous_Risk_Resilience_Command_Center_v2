import { useState } from "react";
import { useApp } from "../context/AppContext";

const CHANNELS = ["STRUCTURED", "GRAPH", "VECTOR", "POLICY", "MEMORY"] as const;

export function ProvenanceDrawer() {
  const { provenancePin, lastPacket, aiEnabled } = useApp();
  const [channel, setChannel] = useState<(typeof CHANNELS)[number]>("STRUCTURED");

  const packet = (lastPacket?.recommendation || {}) as Record<string, unknown>;
  const evidence = (packet.evidence || []) as Record<string, unknown>[];

  return (
    <aside className="drawer">
      <h3>Provenance &amp; Retrieval</h3>
      {provenancePin ? (
        <div className="card" style={{ marginBottom: "0.5rem" }}>
          <div className="mono">{provenancePin.source_path}</div>
          {provenancePin.record_id && <div>id: {provenancePin.record_id}</div>}
          {provenancePin.confidence !== undefined && <div>confidence: {provenancePin.confidence}</div>}
          <div>
            freshness: {provenancePin.freshness || "workshop-static"}
          </div>
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
      {channel === "GRAPH" && <p className="ai-off-note">Graph slice citations from incident context (Q5).</p>}
      {channel === "VECTOR" && (
        <p className="ai-off-note">VECTOR retrieval disabled. Cannot drive isolation or policy tiers.</p>
      )}
      {channel === "POLICY" && (
        <div className="mono">policy.py:ACTION_TIERS · tier 1 recommend · tier 3 requires human Authorize (OPEN-001)</div>
      )}
      {channel === "MEMORY" && <p className="ai-off-note">Decision traces append-only — not hidden CoT authority.</p>}

      {aiEnabled ? (
        <div className="card" style={{ marginTop: "0.5rem" }}>
          <strong>Optional explainer</strong>
          <p className="ai-off-note">Narrative is advisory only (OPEN-028). Engines remain authoritative.</p>
        </div>
      ) : (
        <p className="ai-off-note">AI OFF — deterministic tables only (ADR-12).</p>
      )}
    </aside>
  );
}
