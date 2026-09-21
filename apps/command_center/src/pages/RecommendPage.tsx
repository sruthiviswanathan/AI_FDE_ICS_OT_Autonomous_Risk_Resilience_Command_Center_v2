import { useState } from "react";
import { api } from "../api/client";
import { AiCaption } from "../components/AiCaption";
import { DetailGrid } from "../components/DetailGrid";
import { MoonshotPanel } from "../components/MoonshotPanel";
import { PageLookup } from "../components/PageLookup";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { fmt } from "../utils/format";

export function RecommendPage() {
  const { plantId, assetId, alertId, setLastPacket, scenario, activeBinding } = useApp();
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const ctqIsoComplete = activeBinding?.ctq_iso_complete !== false;

  async function runRecommend() {
    if (!plantId || !assetId) {
      setError("Plant ID and Asset ID are required");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const body = {
        actor: "SOC analyst",
        purpose: scenario === "cascade_001" ? "CASCADE-001 triage" : "incident triage",
        plant_id: plantId,
        asset_id: assetId,
        alert_id: alertId || undefined,
        severity: "HIGH",
        process_context: "UNKNOWN",
      };
      const res = await api.recommend(body);
      setResult(res);
      setLastPacket(res);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  const packet = (result?.recommendation || {}) as Record<string, unknown>;
  const workflow = (result?.workflow_states as Record<string, unknown>[]) || [];

  return (
    <div>
      <h2 className="page-title">Authority Gate / Recommendation</h2>
      <PageLookup />
      <AiCaption />
      <div className="btn-row">
        <button type="button" className="primary" onClick={runRecommend} disabled={loading}>
          Request draft packet
        </button>
      </div>
      {loading && <LoadingBlock label="Running deterministic workflow…" />}
      {error && <ErrorBlock message={error} />}
      {result && (
        <>
          <h3 className="section-title">Workflow progress</h3>
          <div className="workflow-steps">
            {workflow.map((s, i) => (
              <span key={i} className="done">
                {fmt(s.state || s.name || `Step ${i + 1}`)}
              </span>
            ))}
          </div>
          <div className="card-grid">
            <div className="card">
              <h3>Recommendation</h3>
              <div className="metric">{fmt(packet.recommendation)}</div>
              <DetailGrid
                items={[
                  { label: "Execute", value: packet.execute },
                  { label: "Safe state", value: packet.safe_state },
                  { label: "Process impact", value: packet.process_impact },
                  { label: "Safety impact", value: packet.safety_impact },
                  { label: "Authorizable", value: packet.authorizable },
                ]}
              />
            </div>
            <div className="card">
              <h3>Required authority (OPEN-001)</h3>
              <ul>
                {((packet.required_authority as string[]) || []).map((r) => (
                  <li key={r}>{r}</li>
                ))}
              </ul>
              {((packet.required_authority as string[]) || []).length === 0 && <p>—</p>}
            </div>
            {Boolean(packet.missing_fields) && (
              <div className="card">
                <h3>Missing fields</h3>
                <p>{fmt((packet.missing_fields as string[])?.join(", "))}</p>
              </div>
            )}
          </div>
          <div className="advisory-footer">
            Advisory only — no Execute Isolation · Write PLC · Modify SIS. Packet is the engine.
            <div className="btn-row">
              <button type="button" disabled={!ctqIsoComplete} title={!ctqIsoComplete ? "CTQ-ISO incomplete (CASCADE-001)" : undefined}>
                Authorize (disabled — OPEN-001)
              </button>
            </div>
          </div>
        </>
      )}
      {!result && <p className="ai-off-note">Search for plant/asset, then request a draft packet.</p>}
      <MoonshotPanel />
    </div>
  );
}
