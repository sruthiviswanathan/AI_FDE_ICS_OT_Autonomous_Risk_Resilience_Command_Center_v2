import { useEffect, useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { DetailGrid } from "../components/DetailGrid";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function TelemetryPage() {
  const { plantId, assetId, lookupKey, activeBinding } = useApp();
  const [tagFilter, setTagFilter] = useState("");
  const [searchTag, setSearchTag] = useState("");

  useEffect(() => {
    const scenarioTag = activeBinding?.context.tag_id;
    if (scenarioTag) {
      setTagFilter(scenarioTag);
      setSearchTag(scenarioTag);
    }
  }, [activeBinding]);

  const quality = useFetch(
    () => api.telemetryQuality({ plantId: plantId || undefined }),
    [plantId, lookupKey],
  );
  const timeline = useFetch(
    () =>
      api.telemetryTimeline({
        tagId: searchTag || undefined,
        plantId: searchTag ? undefined : plantId || undefined,
        limit: 200,
      }),
    [searchTag, plantId, lookupKey],
  );

  if (quality.loading) return <LoadingBlock />;
  if (quality.error) return <ErrorBlock message={quality.error} />;

  const q = quality.data || {};
  const lag = q.ingest_lag_seconds as Record<string, unknown> | undefined;
  const events = ((timeline.data?.events as Record<string, unknown>[]) || []).slice(0, 50);
  const scope = q.scope as Record<string, unknown> | undefined;
  const scopeNote = searchTag
    ? `Tag ${searchTag}`
    : plantId
      ? `Plant ${plantId}`
      : "Estate-wide (enter Plant ID in shell)";
  const scopeFallback = typeof scope?.scope_note === "string" ? scope.scope_note : null;
  const taggedInPlant =
    typeof scope?.tagged_assets_in_plant === "number" ? scope.tagged_assets_in_plant : null;

  function searchTimeline() {
    setSearchTag(tagFilter.trim());
  }

  function clearTagFilter() {
    setTagFilter("");
    setSearchTag("");
  }

  return (
    <div>
      <h2 className="page-title">Telemetry Quality &amp; Timeline</h2>
      <p className="ai-off-note">
        Scoped to <strong>{scopeNote}</strong>. Historian tags cover a subset of assets only (~182 estate-wide) —
        plant scope is default; search a tag for point-level timeline.
      </p>
      {scopeFallback ? <p className="ai-off-note">{scopeFallback}</p> : null}
      {taggedInPlant !== null && plantId && !searchTag ? (
        <p className="ai-off-note">
          {taggedInPlant} assets in {plantId} have historian tags
          {assetId ? ` (shell asset ${assetId} may not be tagged)` : ""}.
        </p>
      ) : null}
      <div className="card-grid">
        <div className="card">
          <h3>Bad / uncertain</h3>
          <div className="metric">{fmt(q.bad_or_uncertain)}</div>
          <p className="ai-off-note">{fmt(q.total_events)} events in scope</p>
        </div>
        <div className="card">
          <h3>Duplicate packets</h3>
          <div className="metric">{fmt(q.duplicate_packets)}</div>
        </div>
        <div className="card">
          <h3>Unit mismatches</h3>
          <div className="metric">{fmt(q.unit_mismatches)}</div>
        </div>
      </div>
      <div className="card">
        <h3>Ingest lag (seconds)</h3>
        <DetailGrid
          columns={3}
          items={[
            { label: "p50", value: lag?.p50 },
            { label: "max", value: lag?.max },
            { label: "negative count", value: lag?.negative_count },
          ]}
        />
      </div>
      <div className="lookup-bar">
        <label>
          Tag ID
          <input
            placeholder="PLT-01-U03_TEMP"
            value={tagFilter}
            onChange={(e) => setTagFilter(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && searchTimeline()}
          />
        </label>
        <button type="button" className="primary" onClick={searchTimeline}>
          Search timeline
        </button>
        {searchTag ? (
          <button type="button" className="chip" onClick={clearTagFilter}>
            Clear tag · use plant scope
          </button>
        ) : null}
      </div>
      {timeline.loading ? <LoadingBlock label="Loading timeline (event_time order)…" /> : null}
      <DataTable
        rows={events}
        rowKey={(r) => String(r.event_id || `${r.tag_id}-${r.event_time}`)}
        highlight={(r) => Boolean(r.temporal_anomaly || r.unit_mismatch)}
        cols={[
          { key: "event_time", header: "Event time", render: (r) => fmt(r.event_time) },
          { key: "ingest", header: "Ingest time", render: (r) => fmt(r.ingest_time || r.received_time) },
          { key: "lag", header: "Lag (s)", render: (r) => fmt(r.ingest_lag_seconds) },
          { key: "tag", header: "Tag", render: (r) => fmt(r.tag_id) },
          { key: "value", header: "Value", render: (r) => fmt(r.value) },
          { key: "unit", header: "Unit", render: (r) => fmt(r.unit) },
          { key: "quality", header: "Quality", render: (r) => fmt(r.quality) },
          {
            key: "flags",
            header: "Flags",
            render: (r) => (
              <>
                {r.temporal_anomaly ? <UncertaintyBadge text="temporal anomaly" /> : null}
                {r.unit_mismatch ? <UncertaintyBadge text="unit mismatch" /> : null}
                {r.uncertainty ? <UncertaintyBadge text={fmt(r.uncertainty)} /> : null}
              </>
            ),
          },
        ]}
      />
    </div>
  );
}
