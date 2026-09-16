import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { DetailGrid, ObjectCard } from "../components/DetailGrid";
import { PageLookup } from "../components/PageLookup";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function IdentityPage() {
  const { assetId, lookupKey, pinProvenance } = useApp();
  const conflicts = useFetch(() => api.identityConflicts(), [lookupKey]);
  const bundle = useFetch(() => (assetId ? api.identity(assetId) : Promise.reject(new Error("Enter an asset ID"))), [
    assetId,
    lookupKey,
  ]);

  return (
    <div>
      <h2 className="page-title">Asset Identity Reconciliation</h2>
      <PageLookup fields={{ plant: false, alert: false }} />

      {conflicts.loading ? <LoadingBlock /> : null}
      {conflicts.data && (
        <div className="card-grid">
          <div className="card">
            <h3>Alias collisions</h3>
            <div className="metric">{fmt(conflicts.data.alias_collisions)}</div>
          </div>
          <div className="card">
            <h3>State conflicts</h3>
            <div className="metric">{fmt(conflicts.data.asset_state_conflicts)}</div>
          </div>
        </div>
      )}

      {!assetId && <p className="ai-off-note">Enter an Asset ID above and click Search.</p>}
      {bundle.loading && assetId && <LoadingBlock />}
      {bundle.error && <ErrorBlock message={bundle.error} />}
      {bundle.data && (
        <>
          <ObjectCard
            title={`Asset ${fmt(bundle.data.asset_uid)}`}
            data={bundle.data as Record<string, unknown>}
            keys={["plant_id", "asset_type", "registered_state", "observed_state", "asset_criticality", "zone", "owner"]}
          />
          <div className="card-grid">
            <div className="card">
              <h3>Trust flags</h3>
              <DetailGrid
                items={[
                  { label: "State conflict", value: bundle.data.state_conflict ? "Yes" : "No" },
                  { label: "CMDB winner", value: bundle.data.cmdb_winner },
                  { label: "Merged", value: bundle.data.merged },
                  { label: "Unit join missing", value: bundle.data.unit_join_missing ? "Yes" : "No" },
                ]}
              />
            </div>
            <div className="card">
              <h3>Provenance</h3>
              <button
                type="button"
                className="mono linkish"
                onClick={() =>
                  pinProvenance({
                    source_path: String((bundle.data!.provenance as Record<string, string>)?.source_path || ""),
                    record_id: String(bundle.data!.asset_uid),
                    freshness: "workshop-static",
                  })
                }
              >
                {fmt((bundle.data.provenance as Record<string, string>)?.source_path)}
              </button>
            </div>
          </div>
          {Boolean(bundle.data.shadow_overlay) && (
            <div className="card untrusted-border">
              <h3>
                Shadow overlay <UncertaintyBadge text="low confidence" />
              </h3>
              <p>{fmt((bundle.data.shadow_overlay as Record<string, string>)?.note)}</p>
            </div>
          )}
          <h3 className="section-title">Conflicts</h3>
          <DataTable
            rows={(bundle.data.conflicts as Record<string, unknown>[]) || []}
            rowKey={(r) => String(r.conflict_id)}
            cols={[
              { key: "type", header: "Type", render: (r) => fmt(r.type) },
              { key: "left", header: "Left", render: (r) => fmt(r.left_value) },
              { key: "right", header: "Right", render: (r) => fmt(r.right_value) },
              { key: "rule", header: "Rule", render: (r) => fmt(r.rule_id) },
            ]}
          />
        </>
      )}
    </div>
  );
}
