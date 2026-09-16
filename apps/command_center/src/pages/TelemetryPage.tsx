import { useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { DetailGrid } from "../components/DetailGrid";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useApp } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";

export function TelemetryPage() {
  const { lookupKey } = useApp();
  const [tagFilter, setTagFilter] = useState("");
  const [searchTag, setSearchTag] = useState("");
  const quality = useFetch(() => api.telemetryQuality(), [lookupKey]);
  const timeline = useFetch(() => api.telemetryTimeline(searchTag || undefined), [searchTag, lookupKey]);

  if (quality.loading) return <LoadingBlock />;
  if (quality.error) return <ErrorBlock message={quality.error} />;

  const q = quality.data || {};
  const lag = q.ingest_lag_seconds as Record<string, unknown> | undefined;
  const events = ((timeline.data?.events as Record<string, unknown>[]) || []).slice(0, 50);

  function searchTimeline() {
    setSearchTag(tagFilter.trim());
  }

  return (
    <div>
      <h2 className="page-title">Telemetry Quality &amp; Timeline</h2>
      <div className="card-grid">
        <div className="card">
          <h3>Bad / uncertain</h3>
          <div className="metric">{fmt(q.bad_or_uncertain)}</div>
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
