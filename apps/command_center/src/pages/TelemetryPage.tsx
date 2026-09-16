import { useState } from "react";
import { api } from "../api/client";
import { DataTable } from "../components/DataTable";
import { ErrorBlock, LoadingBlock, UncertaintyBadge } from "../components/StateViews";
import { useFetch } from "../hooks/useFetch";

export function TelemetryPage() {
  const [tagFilter, setTagFilter] = useState("");
  const quality = useFetch(() => api.telemetryQuality(), []);
  const timeline = useFetch(() => api.telemetryTimeline(tagFilter || undefined), [tagFilter]);

  if (quality.loading) return <LoadingBlock />;
  if (quality.error) return <ErrorBlock message={quality.error} />;

  const q = quality.data || {};
  const events = ((timeline.data?.events as Record<string, unknown>[]) || []).slice(0, 40);

  return (
    <div>
      <h2 className="page-title">Telemetry Quality &amp; Timeline</h2>
      <div className="card-grid">
        <div className="card">
          <h3>bad/uncertain</h3>
          <div className="metric">{q.bad_or_uncertain as number}</div>
        </div>
        <div className="card">
          <h3>duplicate packets</h3>
          <div className="metric">{q.duplicate_packets as number}</div>
        </div>
        <div className="card">
          <h3>unit mismatches</h3>
          <div className="metric">{q.unit_mismatches as number}</div>
        </div>
      </div>
      <div className="btn-row">
        <input placeholder="tag_id filter" value={tagFilter} onChange={(e) => setTagFilter(e.target.value)} />
      </div>
      {timeline.loading ? <LoadingBlock label="Loading timeline (event_time order)…" /> : null}
      <DataTable
        rows={events}
        rowKey={(r) => String(r.event_id || r.tag_id)}
        highlight={(r) => Boolean(r.temporal_anomaly || r.unit_mismatch)}
        cols={[
          { key: "event_time", header: "event_time", render: (r) => String(r.event_time) },
          { key: "ingest", header: "ingest", render: (r) => String(r.ingest_time || r.received_time || "—") },
          { key: "lag", header: "lag(s)", render: (r) => String(r.ingest_lag_seconds ?? "—") },
          { key: "tag", header: "tag", render: (r) => String(r.tag_id) },
          { key: "quality", header: "quality", render: (r) => String(r.quality) },
          {
            key: "flags",
            header: "flags",
            render: (r) => (
              <>
                {r.temporal_anomaly ? <UncertaintyBadge text="temporal anomaly" /> : null}
                {r.unit_mismatch ? <UncertaintyBadge text="unit mismatch" /> : null}
                {r.uncertainty ? <UncertaintyBadge text={String(r.uncertainty)} /> : null}
              </>
            ),
          },
        ]}
      />
      <p className="ai-off-note">Ordered by event_time — not ingest alone. GOOD ≠ ProcessHealthy.</p>
    </div>
  );
}
