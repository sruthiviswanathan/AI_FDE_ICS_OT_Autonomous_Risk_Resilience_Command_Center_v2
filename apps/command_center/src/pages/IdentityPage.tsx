import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { DetailGrid } from "../components/DetailGrid";
import { PageLookup } from "../components/PageLookup";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

function formatConflictValue(value: unknown): string {
  if (Array.isArray(value)) return value.join(", ");
  return fmt(value);
}

function conflictTouchesAsset(row: Record<string, unknown>, id: string): boolean {
  if (!id) return true;
  if (String(row.asset_id) === id) return true;
  if (String(row.left_value) === id) return true;
  const right = row.right_value;
  if (Array.isArray(right) && right.map(String).includes(id)) return true;
  return false;
}

const CONFLICT_TYPE_LABELS: Record<string, string> = {
  REGISTERED_VS_OBSERVED: "State",
  ALIAS_COLLISION: "Alias",
};

export function IdentityPage() {
  const { plantId, assetId, lookupKey, pinProvenance, setAssetId, triggerLookup } = useApp();
  const [defaultingAsset, setDefaultingAsset] = useState(false);
  const [typeFilter, setTypeFilter] = useState<string>("all");
  const conflicts = useFetch(
    () => (plantId ? api.identityConflicts(plantId) : api.identityConflicts()),
    [lookupKey, plantId],
  );

  useEffect(() => {
    if (assetId || !plantId) return;
    let cancelled = false;
    setDefaultingAsset(true);
    api
      .plantAssets(plantId, 500)
      .then((res) => {
        if (cancelled) return;
        const first = res.assets[0]?.asset_id;
        if (first) {
          setAssetId(first);
          triggerLookup();
        }
      })
      .finally(() => {
        if (!cancelled) setDefaultingAsset(false);
      });
    return () => {
      cancelled = true;
    };
  }, [assetId, plantId, setAssetId, triggerLookup]);

  const bundle = useFetch(
    () => (assetId ? api.identity(assetId) : Promise.resolve(null)),
    [assetId, lookupKey],
  );

  const plantConflictRows = useMemo(
    () => (conflicts.data?.conflicts as Record<string, unknown>[] | undefined) ?? [],
    [conflicts.data],
  );

  useEffect(() => {
    setTypeFilter("all");
  }, [plantId, lookupKey]);

  const typeCounts = useMemo(() => {
    const counts: Record<string, number> = { all: plantConflictRows.length };
    for (const row of plantConflictRows) {
      const type = String(row.type || "UNKNOWN");
      counts[type] = (counts[type] || 0) + 1;
    }
    return counts;
  }, [plantConflictRows]);

  const conflictTypes = useMemo(
    () => ["all", ...Object.keys(typeCounts).filter((k) => k !== "all").sort()],
    [typeCounts],
  );

  const filteredConflictRows = useMemo(
    () =>
      typeFilter === "all"
        ? plantConflictRows
        : plantConflictRows.filter((row) => String(row.type) === typeFilter),
    [plantConflictRows, typeFilter],
  );

  const selectedAssetConflictCount = useMemo(
    () => (assetId ? plantConflictRows.filter((row) => conflictTouchesAsset(row, assetId)).length : 0),
    [plantConflictRows, assetId],
  );

  const selectedAliasConflicts = useMemo(
    () =>
      assetId
        ? plantConflictRows.filter(
            (row) => String(row.type) === "ALIAS_COLLISION" && conflictTouchesAsset(row, assetId),
          )
        : [],
    [plantConflictRows, assetId],
  );

  return (
    <div>
      <h2 className="page-title">Asset Identity Reconciliation</h2>
      <PageLookup fields={{ plant: false, alert: false }} />

      {conflicts.loading && <LoadingBlock variant="inline" label="Loading plant identity conflicts…" />}
      {conflicts.error && <ErrorBlock message={conflicts.error} />}
      {conflicts.data && (
        <>
          <p className="ai-off-note">
            Summary for {plantId ? `plant ${plantId}` : "estate-wide"} · {fmt(conflicts.data.conflict_count)} conflict
            row(s)
          </p>
          <div className="card-grid">
            <div className="card">
              <h3>Alias collisions</h3>
              <div className="metric">{fmt(conflicts.data.alias_collisions)}</div>
              {Array.isArray(conflicts.data.collision_aliases) &&
                (conflicts.data.collision_aliases as string[]).length > 0 && (
                  <p className="ai-off-note mono">
                    {(conflicts.data.collision_aliases as string[]).slice(0, 4).join(" · ")}
                    {(conflicts.data.collision_aliases as string[]).length > 4 ? " …" : ""}
                  </p>
                )}
            </div>
            <div className="card">
              <h3>State conflicts</h3>
              <div className="metric">{fmt(conflicts.data.asset_state_conflicts)}</div>
              <p className="ai-off-note">ACTIVE registered vs OFFLINE/UNSEEN observed</p>
            </div>
          </div>
        </>
      )}

      {!assetId && !defaultingAsset && plantId && (
        <p className="ai-off-note">No assets available for plant {plantId}.</p>
      )}
      {(defaultingAsset || (bundle.loading && assetId)) && (
        <LoadingBlock variant="inline" label="Loading asset identity…" />
      )}
      {bundle.error && <ErrorBlock message={bundle.error} />}
      {bundle.data && String(bundle.data.asset_uid) === assetId && (
        <>
          <div className="card">
            <h3>Asset {fmt(bundle.data.asset_uid)}</h3>
            <DetailGrid
              columns={4}
              items={[
                { label: "Plant", value: fmt(bundle.data.plant_id) },
                { label: "Asset type", value: fmt(bundle.data.asset_type) },
                { label: "Registered state", value: fmt(bundle.data.registered_state) },
                {
                  label: "Observed state",
                  value: fmt(bundle.data.observed_state),
                  hint: bundle.data.state_conflict ? "Differs from registered (BR-01)" : "Matches registered",
                },
                { label: "Criticality", value: fmt(bundle.data.asset_criticality) },
                { label: "Zone", value: fmt(bundle.data.zone) },
                { label: "Owner", value: fmt(bundle.data.owner) },
                { label: "State conflict", value: bundle.data.state_conflict ? "Yes" : "No" },
              ]}
            />
          </div>
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
              <h3>Alias conflict</h3>
              <div className="metric">{selectedAliasConflicts.length > 0 ? "Yes" : "No"}</div>
              {selectedAliasConflicts.length > 0 ? (
                <>
                  <p className="ai-off-note">
                    {selectedAliasConflicts.length} colliding alias mapping(s) in {fmt(plantId)} — do not merge
                    (ADR-01).
                  </p>
                  <ul className="provenance-evidence-list mono">
                    {selectedAliasConflicts.map((row) => (
                      <li key={String(row.conflict_id)}>
                        {formatConflictValue(row.left_value)} → peers {formatConflictValue(row.right_value)}
                      </li>
                    ))}
                  </ul>
                </>
              ) : (
                <p className="ai-off-note">
                  No alias collisions for this asset in {fmt(plantId)}.
                  {Array.isArray(bundle.data.aliases) && (bundle.data.aliases as unknown[]).length > 0
                    ? ` ${(bundle.data.aliases as unknown[]).length} alias record(s) without collision.`
                    : ""}
                </p>
              )}
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
                    freshness: String((bundle.data!.provenance as Record<string, string>)?.freshness || ""),
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
        </>
      )}

      <h3 className="section-title">Conflicts {plantId ? `· ${plantId}` : ""}</h3>
      {plantConflictRows.length > 0 && (
        <div className="card identity-conflict-toolbar">
          <div className="drill-table-toolbar">
            <label className="estate-sort">
              Filter by type
              <select
                value={typeFilter}
                aria-label="Filter conflicts by type"
                onChange={(e) => setTypeFilter(e.target.value)}
              >
                {conflictTypes.map((type) => (
                  <option key={type} value={type}>
                    {type === "all" ? "All types" : CONFLICT_TYPE_LABELS[type] || type} (
                    {typeCounts[type] ?? 0})
                  </option>
                ))}
              </select>
            </label>
            <p className="identity-filter-summary ai-off-note">
              Showing {filteredConflictRows.length} of {plantConflictRows.length} conflict rows
              {typeFilter !== "all"
                ? ` · ${CONFLICT_TYPE_LABELS[typeFilter] || typeFilter} only`
                : " · use the dropdown to narrow by conflict type"}
            </p>
          </div>
        </div>
      )}
      {assetId && selectedAssetConflictCount === 0 && plantConflictRows.length > 0 && (
        <p className="ai-off-note">
          Selected asset <span className="mono">{assetId}</span> has no identity conflicts — table shows all{" "}
          {plantConflictRows.length} plant conflict row(s). Matching rows would be highlighted.
        </p>
      )}
      {assetId && selectedAssetConflictCount > 0 && (
        <p className="ai-off-note">
          Selected asset <span className="mono">{assetId}</span> — {selectedAssetConflictCount} matching row(s)
          highlighted below ({plantConflictRows.length} total in plant).
        </p>
      )}
      {filteredConflictRows.length === 0 && !conflicts.loading && (
        <p className="ai-off-note">
          {typeFilter !== "all"
            ? `No ${CONFLICT_TYPE_LABELS[typeFilter] || typeFilter} conflicts for ${plantId || "scope"}.`
            : "No identity conflicts recorded for this scope."}
        </p>
      )}
      {filteredConflictRows.length > 0 && (
        <DataTable
          rows={filteredConflictRows}
          rowKey={(r) => String(r.conflict_id)}
          highlight={(r) => Boolean(assetId) && conflictTouchesAsset(r, assetId)}
          cols={[
            { key: "asset", header: "Asset", render: (r) => fmt(r.asset_id) },
            { key: "type", header: "Type", render: (r) => fmt(r.type) },
            {
              key: "registered",
              header: "Registered",
              render: (r) => fmt(r.registered_state ?? r.left_value),
            },
            {
              key: "observed",
              header: "Observed",
              render: (r) =>
                String(r.type) === "ALIAS_COLLISION" ? "—" : fmt(r.observed_state ?? r.right_value),
            },
            {
              key: "detail",
              header: "Conflict detail",
              render: (r) =>
                String(r.type) === "ALIAS_COLLISION"
                  ? `Peers: ${formatConflictValue(r.right_value)}`
                  : String(r.state_conflict) === "true" || r.state_conflict === true
                    ? "Registered ≠ observed"
                    : formatConflictValue(r.right_value),
            },
            { key: "rule", header: "Rule", render: (r) => fmt(r.rule_id) },
          ]}
        />
      )}
    </div>
  );
}
