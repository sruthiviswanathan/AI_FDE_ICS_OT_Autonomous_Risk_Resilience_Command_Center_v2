import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { api, type TwinPreviewResponse } from "../api/client";
import { AiCaption } from "../components/AiCaption";
import { DataTable } from "../components/DataTable";
import { MoonshotPanel } from "../components/MoonshotPanel";
import { ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { canUseMoonshot } from "../personas/registry";
import { fmt } from "../utils/format";

const TWIN_ACTIONS = ["do_nothing", "isolate_preview", "increase_logging", "open_ticket"] as const;

export function SimulationPage() {
  const { applyScenario, aiMode, personaId, plantId, assetId, alertId, scenario, setLastPacket } = useApp();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const catalog = useFetch(() => api.scenarioCatalog(), []);
  const [results, setResults] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [proposedAction, setProposedAction] = useState<(typeof TWIN_ACTIONS)[number]>("isolate_preview");
  const [twin, setTwin] = useState<TwinPreviewResponse | null>(null);
  const [twinError, setTwinError] = useState<string | null>(null);
  const [twinLoading, setTwinLoading] = useState(false);
  const [packetError, setPacketError] = useState<string | null>(null);

  const forecastId = searchParams.get("forecast_id") || undefined;
  const showTwin = aiMode === "moonshot" && canUseMoonshot(personaId);

  async function runHarness() {
    setLoading(true);
    setError(null);
    try {
      const res = await api.evalRun();
      setResults(res);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function runTwin(action: (typeof TWIN_ACTIONS)[number] = proposedAction) {
    setTwinLoading(true);
    setTwinError(null);
    try {
      const res = await api.twinPreview({
        scenarioId: scenario !== "nominal" ? scenario : undefined,
        forecastId,
        proposedAction: action,
      });
      setTwin(res);
    } catch (e) {
      setTwinError((e as Error).message);
    } finally {
      setTwinLoading(false);
    }
  }

  useEffect(() => {
    if (!showTwin) {
      setTwin(null);
      return;
    }
    void runTwin(proposedAction);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showTwin, scenario, forecastId]);

  async function createApprovalPacket() {
    if (!plantId || !assetId) {
      setPacketError("Plant ID and Asset ID are required");
      return;
    }
    setPacketError(null);
    try {
      const res = await api.recommend({
        actor: "SOC analyst",
        purpose: scenario === "cascade_001" ? "CASCADE-001 twin packet" : "twin lab packet",
        plant_id: plantId,
        asset_id: assetId,
        alert_id: alertId || undefined,
        severity: "HIGH",
        process_context: "UNKNOWN",
      });
      setLastPacket(res);
      const params = new URLSearchParams(window.location.search);
      params.set("ai", aiMode);
      navigate(`/recommend?${params.toString()}`);
    } catch (e) {
      setPacketError((e as Error).message);
    }
  }

  if (catalog.loading) return <LoadingBlock label="Loading scenario catalog…" />;

  const scenarios = catalog.data?.scenarios || [];
  const caseRows = ((results?.results as Record<string, unknown>[]) || []);

  return (
    <div>
      <h2 className="page-title">Inject / Simulation</h2>
      <AiCaption />
      {showTwin && (
        <div className="card twin-lab">
          <div className="moonshot-banner" role="status">
            ADVISORY FORECAST — NOT A CONTROL ACTION
          </div>
          <h3>Twin lab (consequence sketch)</h3>
          <p className="ai-off-note">
            Rehearse {forecastId || scenario || "current slice"}. Never write PLC, modify SIS, change a setpoint, or
            apply to plant.
          </p>
          <div className="btn-row">
            {TWIN_ACTIONS.map((action) => (
              <button
                key={action}
                type="button"
                className={proposedAction === action ? "chip active" : "chip"}
                onClick={() => {
                  setProposedAction(action);
                  void runTwin(action);
                }}
              >
                {action}
              </button>
            ))}
          </div>
          {twinLoading && <LoadingBlock variant="compact" label="Sketching consequence…" />}
          {twinError && <ErrorBlock message={twinError} />}
          {twin && (
            <div className="card-grid">
              <div className="card">
                <h3>lab_result</h3>
                <div className="metric">{twin.lab_result}</div>
                <p>{twin.detail}</p>
                <p className="ai-off-note">execute={String(twin.execute)} · apply_to_plant={String(twin.apply_to_plant)}</p>
              </div>
            </div>
          )}
          <div className="btn-row">
            <button type="button" className="primary" onClick={() => void createApprovalPacket()}>
              Create approval packet
            </button>
          </div>
          {packetError && <ErrorBlock message={packetError} />}
        </div>
      )}
      <MoonshotPanel />
      <div className="card-grid">
        {scenarios.map((s) => (
          <div key={s.id} className="card">
            <h3>{s.label}</h3>
            <p>{s.title}</p>
            <p className="mono">{s.eval_ids.join(", ") || "estate nominal"}</p>
            <div className="badge-row">
              {s.badges.slice(0, 4).map((b) => (
                <span key={b.id} className={`badge ${b.tone !== "neutral" ? b.tone : ""}`}>
                  {b.label}
                </span>
              ))}
            </div>
            <button type="button" onClick={() => applyScenario(s)}>
              Load scenario
            </button>
          </div>
        ))}
      </div>
      <div className="btn-row">
        <button type="button" className="primary" onClick={runHarness} disabled={loading}>
          Run full harness (EVAL-001…031)
        </button>
      </div>
      {loading && <LoadingBlock label="Running eval harness…" />}
      {error && <ErrorBlock message={error} />}
      {results && (
        <>
          <p>
            Summary: {String(results.passed)}/{String(results.total)} PASS
          </p>
          <DataTable
            rows={caseRows}
            rowKey={(r) => String(r.case_id)}
            highlight={(r) => r.status !== "PASS"}
            cols={[
              { key: "id", header: "case", render: (r) => String(r.case_id) },
              { key: "status", header: "status", render: (r) => String(r.status) },
              { key: "detail", header: "detail", render: (r) => fmt(r.detail ?? r.message) },
            ]}
          />
        </>
      )}
      <p className="ai-off-note">Do not hide conflicts to beautify demo. See SCENARIO_BINDINGS.md.</p>
    </div>
  );
}
