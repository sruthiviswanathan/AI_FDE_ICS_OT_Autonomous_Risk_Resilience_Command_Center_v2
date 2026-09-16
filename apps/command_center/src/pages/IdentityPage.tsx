import { useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";

export function IdentityPage() {
  const { assetId, pinProvenance } = useApp();
  const [lookup, setLookup] = useState(assetId);
  const conflicts = useFetch(() => api.identityConflicts(), []);
  const bundle = useFetch(() => api.identity(lookup), [lookup]);

  return (
    <div>
      <h2 className="page-title">Asset Identity Reconciliation</h2>
      <div className="btn-row">
        <input value={lookup} onChange={(e) => setLookup(e.target.value)} placeholder="asset_id" />
        <button type="button" onClick={() => setLookup(lookup)}>
          Load
        </button>
      </div>

      {conflicts.loading ? <LoadingBlock /> : null}
      {conflicts.data && (
        <div className="card-grid">
          <div className="card">
            <h3>Alias collisions</h3>
            <div className="metric">{conflicts.data.alias_collisions as number}</div>
          </div>
          <div className="card">
            <h3>State conflicts</h3>
            <div className="metric">{conflicts.data.asset_state_conflicts as number}</div>
          </div>
        </div>
      )}

      {bundle.loading && <LoadingBlock />}
      {bundle.error && <ErrorBlock message={bundle.error} />}
      {bundle.data && (
        <>
          <div className="card-grid">
            <div className="card">
              <h3>Registered vs Observed</h3>
              <p>
                {String(bundle.data.registered_state)} / {String(bundle.data.observed_state)}
              </p>
              {Boolean(bundle.data.state_conflict) && <UncertaintyBadge text="state conflict" />}
            </div>
            <div className="card">
              <h3>Provenance</h3>
              <button
                type="button"
                className="mono"
                onClick={() =>
                  pinProvenance({
                    source_path: String((bundle.data.provenance as Record<string, string>)?.source_path || ""),
                    record_id: String(bundle.data.asset_uid),
                    freshness: "workshop-static",
                  })
                }
              >
                {(bundle.data.provenance as Record<string, string>)?.source_path}
              </button>
              <p>cmdb_winner: {String(bundle.data.cmdb_winner)} · merged: {String(bundle.data.merged)}</p>
            </div>
          </div>
          {Boolean(bundle.data.shadow_overlay) && (
            <div className="card">
              <h3>Shadow overlay (low confidence)</h3>
              <UncertaintyBadge text="shadow evidence only" />
            </div>
          )}
          <h3>Conflicts</h3>
          <DataTable
            rows={(bundle.data.conflicts as Record<string, unknown>[]) || []}
            rowKey={(r) => String(r.conflict_id)}
            cols={[
              { key: "type", header: "Type", render: (r) => String(r.type) },
              { key: "left", header: "Left", render: (r) => String(r.left_value) },
              { key: "right", header: "Right", render: (r) => JSON.stringify(r.right_value) },
            ]}
          />
          <p className="ai-off-note">Forbidden: merge aliases · CMDB winner · promote shadow</p>
        </>
      )}
    </div>
  );
}
