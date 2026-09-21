import { useEffect, useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { DetailGrid } from "../components/DetailGrid";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

const PAGE_SIZES = [25, 50, 100, 200];

export function TelemetryPage() {
  const { plantId, assetId, lookupKey, activeBinding } = useApp();
  const [tagFilter, setTagFilter] = useState("");
  const [searchTag, setSearchTag] = useState("");
  const [rowQuery, setRowQuery] = useState("");
  const [qualityFilter, setQualityFilter] = useState("all");
  const [flagFilter, setFlagFilter] = useState("all");
  const [sortBy, setSortBy] = useState("event_time");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("asc");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);

  useEffect(() => {
    const scenarioTag = activeBinding?.context.tag_id;
    if (scenarioTag) {
      setTagFilter(scenarioTag);
      setSearchTag(scenarioTag);
    }
  }, [activeBinding]);

  useEffect(() => {
    setPage(1);
  }, [plantId, lookupKey, searchTag, rowQuery, qualityFilter, flagFilter, sortBy, sortDir, pageSize]);

  const quality = useFetch(
    () => api.telemetryQuality({ plantId: plantId || undefined }),
    [plantId, lookupKey],
  );
  const timeline = useFetch(
    () =>
      api.telemetryTimeline({
        tagId: searchTag || undefined,
        plantId: searchTag ? undefined : plantId || undefined,
        limit: pageSize,
        offset: (page - 1) * pageSize,
        sortBy,
        sortDir,
        quality: qualityFilter === "all" ? undefined : qualityFilter,
        flag: flagFilter === "all" ? undefined : flagFilter,
        q: rowQuery.trim() || undefined,
      }),
    [searchTag, plantId, lookupKey, page, pageSize, sortBy, sortDir, qualityFilter, flagFilter, rowQuery],
  );

  if (quality.loading) return <LoadingBlock />;
  if (quality.error) return <ErrorBlock message={quality.error} />;

  const q = quality.data || {};
  const lag = q.ingest_lag_seconds as Record<string, unknown> | undefined;
  const events = (timeline.data?.events as Record<string, unknown>[]) || [];
  const totalCount = Number(timeline.data?.total_count ?? events.length);
  const matchedCount = Number(timeline.data?.matched_count ?? events.length);
  const totalPages = Math.max(1, Math.ceil(matchedCount / pageSize));
  const pageStart = matchedCount === 0 ? 0 : (page - 1) * pageSize + 1;
  const pageEnd = Math.min(page * pageSize, matchedCount);
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

  function toggleSort(key: string) {
    if (sortBy === key) {
      setSortDir((dir) => (dir === "asc" ? "desc" : "asc"));
      return;
    }
    setSortBy(key);
    setSortDir("asc");
  }

  return (
    <div>
      <h2 className="page-title">Telemetry Quality &amp; Timeline</h2>
      <p className="ai-off-note">
        Scoped to <strong>{scopeNote}</strong>. Historian tags cover a subset of assets only (~182 estate-wide) —
        plant scope is default; search a tag for point-level timeline. Default row order is event_time (ADR-02).
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
      <div className="card identity-conflict-toolbar">
        <div className="drill-table-toolbar">
          <label className="drill-search">
            Filter rows
            <input
              className="lookup-input"
              placeholder="tag, asset, unit, quality…"
              value={rowQuery}
              onChange={(e) => setRowQuery(e.target.value)}
              aria-label="Filter timeline rows"
            />
          </label>
          <label className="estate-sort">
            Quality
            <select
              value={qualityFilter}
              aria-label="Filter by quality"
              onChange={(e) => setQualityFilter(e.target.value)}
            >
              <option value="all">All</option>
              <option value="not_GOOD">Bad / uncertain</option>
              <option value="BAD">BAD</option>
              <option value="UNCERTAIN">UNCERTAIN</option>
              <option value="GOOD">GOOD</option>
            </select>
          </label>
          <label className="estate-sort">
            Flags
            <select value={flagFilter} aria-label="Filter by flag" onChange={(e) => setFlagFilter(e.target.value)}>
              <option value="all">All</option>
              <option value="unit_mismatch">Unit mismatch</option>
              <option value="temporal_anomaly">Temporal anomaly</option>
            </select>
          </label>
          <label className="estate-sort">
            Rows
            <select
              value={String(pageSize)}
              aria-label="Rows per page"
              onChange={(e) => setPageSize(Number(e.target.value))}
            >
              {PAGE_SIZES.map((size) => (
                <option key={size} value={size}>
                  {size} / page
                </option>
              ))}
            </select>
          </label>
          <p className="identity-filter-summary ai-off-note">
            Showing {matchedCount === 0 ? 0 : pageStart}–{pageEnd} of {matchedCount}
            {matchedCount !== totalCount ? ` filtered from ${totalCount}` : ` events`}
            {sortBy !== "event_time" ? ` · sorted by ${sortBy}` : " · event_time order"}
          </p>
        </div>
      </div>
      {timeline.loading ? <LoadingBlock label="Loading timeline (event_time order)…" /> : null}
      {timeline.error ? <ErrorBlock message={timeline.error} /> : null}
      {!timeline.loading && events.length === 0 ? (
        <p className="ai-off-note">No telemetry rows match this filter.</p>
      ) : null}
      <DataTable
        rows={events}
        rowKey={(r) => String(r.event_id || `${r.tag_id}-${r.event_time}`)}
        highlight={(r) => Boolean(r.temporal_anomaly || r.unit_mismatch)}
        sortKey={sortBy}
        sortDir={sortDir}
        onSort={toggleSort}
        cols={[
          { key: "event_time", header: "Event time", sortable: true, render: (r) => fmt(r.event_time) },
          {
            key: "ingest_time",
            header: "Ingest time",
            sortable: true,
            render: (r) => fmt(r.ingest_time || r.received_time),
          },
          { key: "ingest_lag_seconds", header: "Lag (s)", sortable: true, render: (r) => fmt(r.ingest_lag_seconds) },
          { key: "tag_id", header: "Tag", sortable: true, render: (r) => fmt(r.tag_id) },
          { key: "value", header: "Value", sortable: true, render: (r) => fmt(r.value) },
          { key: "unit", header: "Unit", sortable: true, render: (r) => fmt(r.unit) },
          { key: "quality", header: "Quality", sortable: true, render: (r) => fmt(r.quality) },
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
      {matchedCount > 0 && (
        <div className="table-pager">
          <button type="button" className="chip" disabled={page <= 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>
            Previous
          </button>
          <label className="estate-sort">
            Page
            <input
              type="number"
              min={1}
              max={totalPages}
              value={Math.min(page, totalPages)}
              aria-label="Page number"
              onChange={(e) => {
                const next = Number(e.target.value);
                if (!Number.isFinite(next)) return;
                setPage(Math.min(totalPages, Math.max(1, Math.trunc(next))));
              }}
            />
            <span> of {totalPages}</span>
          </label>
          <button
            type="button"
            className="chip"
            disabled={page >= totalPages}
            onClick={() => setPage((p) => p + 1)}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
