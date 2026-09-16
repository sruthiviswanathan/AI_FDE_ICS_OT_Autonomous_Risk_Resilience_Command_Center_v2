import { useState } from "react";
import { api } from "../api/client";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";

export function RecommendPage() {
  const { plantId, assetId, alertId, aiEnabled, setLastPacket, scenario, activeBinding } = useApp();
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const ctqIsoComplete = activeBinding?.ctq_iso_complete !== false;

  async function runRecommend() {
    setLoading(true);
    setError(null);
    try {
      const body = {
        actor: "SOC analyst",
        purpose: scenario === "cascade_001" ? "CASCADE-001 triage" : "incident triage",
        plant_id: plantId,
        asset_id: assetId,
        alert_id: alertId,
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
      <div className="btn-row">
        <button type="button" className="primary" onClick={runRecommend} disabled={loading}>
          Request draft packet
        </button>
        <button type="button" disabled title="Export only — no execute path">
          Export packet
        </button>
        <button type="button" disabled={!result} onClick={() => navigator.clipboard.writeText(JSON.stringify(result, null, 2))}>
          Copy summary
        </button>
      </div>
      {loading && <LoadingBlock label="Running deterministic workflow…" />}
      {error && <ErrorBlock message={error} />}
      {result && (
        <>
          <div className="workflow-steps">
            {workflow.map((s, i) => (
              <span key={i} className="done">
                {String(s.state || s.name || i)}
              </span>
            ))}
          </div>
          <div className="card-grid">
            <div className="card">
              <h3>Recommendation</h3>
              <div className="metric">{String(packet.recommendation)}</div>
              <p>execute: {String(packet.execute)}</p>
              <p>safe_state: {String(packet.safe_state || "UNKNOWN")}</p>
              <p>process_impact: {String(packet.process_impact || "—")}</p>
              <p>safety_impact: {String(packet.safety_impact || "—")}</p>
            </div>
            <div className="card">
              <h3>Required authority (roles only — OPEN-001)</h3>
              <ul>
                {((packet.required_authority as string[]) || []).map((r) => (
                  <li key={r}>{r}</li>
                ))}
              </ul>
              <p>authorizable: {String(packet.authorizable)}</p>
            </div>
          </div>
          {!aiEnabled && (
            <p className="ai-off-note">AI OFF — tables and deterministic packet only (EVAL-016).</p>
          )}
          <div className="advisory-footer">
            Advisory only — no Execute Isolation · Write PLC · Modify SIS · One-click Authorize.
            <div className="btn-row">
              <button type="button" disabled={!ctqIsoComplete} title={!ctqIsoComplete ? "CTQ-ISO incomplete for CASCADE-001 (EVAL-020)" : undefined}>
                Authorize (disabled — OPEN-001)
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
