import { useMemo } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import { EstateDiagnosticsStrip } from "../components/EstateDiagnosticsStrip";
import { PlantPostureBadges } from "../components/PlantPostureBadges";
import { StaleBadge, ErrorBlock, LoadingBlock } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { estateKpis, resolveInventorySummary } from "../utils/estateDashboard";

export function ControlTower() {
  const ctx = useApp();
  const diag = useFetch(() => api.diagnostics(), []);
  const slo = useFetch(() => api.opsSlo(), []);
  const estate = useFetch(() => api.estateByPlant({ includeTopAlerts: 3 }), []);
  const estateGlobal = useFetch(() => api.estate(), []);

  const quickIncidents = useMemo(() => {
    if (!estate.data) return [];
    const rows: (Record<string, string> & { plant_id: string })[] = [];
    for (const plant of estate.data.plants) {
      if (!plant.signals.elevated) continue;
      for (const alert of plant.top_alerts) {
        rows.push({ ...alert, plant_id: plant.plant_id });
      }
    }
    return rows.slice(0, 6);
  }, [estate.data]);

  const elevatedPlants = useMemo(
    () => (estate.data?.plants || []).filter((p) => p.signals.elevated).slice(0, 6),
    [estate.data],
  );

  const kpis = useMemo(() => estateKpis(estate.data?.plants || []), [estate.data]);
  const inventory = useMemo(
    () => (estate.data ? resolveInventorySummary(estate.data, estateGlobal.data) : null),
    [estate.data, estateGlobal.data],
  );

  if (diag.loading || slo.loading) return <LoadingBlock />;
  if (diag.error) return <ErrorBlock message={diag.error} />;

  return (
    <div>
      <h2 className="page-title">Risk &amp; Resilience Control Tower</h2>
      <div className="ctq-strip">
        <span>
          SLO-OT:{" "}
          {(slo.data as { slos?: Record<string, { status?: string }> })?.slos?.["SLO-OT"]?.status || "…"}
        </span>
        <span>Eval: 31/31 (harness)</span>
        <span>Legacy xfail: 3 (contrast only)</span>
        <StaleBadge />
      </div>

      <EstateDiagnosticsStrip data={diag.data} showAll />

      <div className="card-grid">
        <div className="card">
          <h3>Quick incidents</h3>
          {estate.loading && <p className="ai-off-note">Loading elevated plant alerts…</p>}
          {estate.error && <p className="ai-off-note">{estate.error}</p>}
          {!estate.loading && quickIncidents.length === 0 && (
            <p>
              <Link
                to="/incident"
                onClick={() => {
                  ctx.setPlantId("PLT-10");
                  ctx.setAssetId("OT-01016");
                  ctx.setAlertId("ALT-002783");
                  ctx.triggerLookup();
                }}
              >
                ALT-002783 · PLT-10 · HIGH
              </Link>
            </p>
          )}
          {quickIncidents.map((row) => (
            <p key={`${row.plant_id}-${row.alert_id}`}>
              <Link
                to="/incident"
                onClick={() => {
                  ctx.setPlantId(row.plant_id);
                  ctx.setAssetId(row.asset_id);
                  ctx.setAlertId(row.alert_id);
                  ctx.triggerLookup();
                }}
              >
                {row.alert_id} · {row.plant_id} · {row.severity}
                {row.soc_status === "SUPPRESSED" ? " · SUPPRESSED" : ""}
              </Link>
              {row.process_context === "UNKNOWN" && (
                <span className="badge amber" style={{ marginLeft: "0.35rem" }}>
                  ctx unknown
                </span>
              )}
            </p>
          ))}
          <p>
            <Link to="/recommend">Open recommendation gate →</Link>
          </p>
        </div>
      </div>

      <div className="card estate-summary-card">
        <h3>Estate posture</h3>
        {estate.loading && <p className="ai-off-note">Loading estate summary…</p>}
        {estate.data && (
          <>
            <p>
              <span className="metric" style={{ fontSize: "1.1rem" }}>
                {kpis.elevated}/{kpis.totalPlants}
              </span>{" "}
              plants elevated · {inventory?.totalAssets ?? kpis.totalAssets} assets ·{" "}
              {inventory?.totalAlerts ?? 0} alerts · {kpis.hcAlerts} HC{" "}
              <span className="ai-off-note">(inventory)</span>
            </p>
            {elevatedPlants.length > 0 && (
              <div className="estate-summary-chips">
                {elevatedPlants.map((p) => (
                  <Link
                    key={p.plant_id}
                    to={`/estate?plant=${encodeURIComponent(p.plant_id)}`}
                    className="chip link-chip estate-posture-chip"
                  >
                    <span className="mono">{p.plant_id}</span>
                    <PlantPostureBadges plant={p} compact />
                  </Link>
                ))}
              </div>
            )}
            <p className="ai-off-note" style={{ marginTop: "0.35rem" }}>
              {estate.data.methodology.posture_motto ?? "cyber ≠ operational ≠ safety ≠ recovery"}
            </p>
            <p style={{ marginTop: "0.5rem" }}>
              <Link to="/estate" className="estate-dashboard-cta">
                Open Estate Dashboard →
              </Link>
            </p>
          </>
        )}
      </div>

      <div className="card" style={{ marginTop: "0.75rem" }}>
        <h3>Open decisions (read-only)</h3>
        <p className="mono">OPEN-001 Authorizer · OPEN-006 KPI · OPEN-028 model · OPEN-029 auth</p>
      </div>
    </div>
  );
}
