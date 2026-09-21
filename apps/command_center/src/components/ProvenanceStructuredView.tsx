import { api } from "../api/client";
import type { ProvenancePin } from "../context/AppContext";
import { useFetch } from "../hooks/useFetch";
import { fmt } from "../utils/format";
import {
  WORKSHOP_FRESHNESS,
  type PageProvenance,
  type PageSource,
  type SourceTrust,
} from "../utils/pageProvenance";
import { ErrorBlock, LoadingBlock } from "./StateViews";

function trustLabel(trust: SourceTrust | undefined): string {
  if (trust === "UNTRUSTED") return "UNTRUSTED";
  if (trust === "policy") return "policy — not observation";
  return WORKSHOP_FRESHNESS;
}

function SourceCard({
  source,
  catalog,
  onPin,
}: {
  source: PageSource;
  catalog?: Record<string, unknown>;
  onPin: (p: ProvenancePin) => void;
}) {
  const count = catalog?.record_count;
  const exists = catalog?.exists;
  return (
    <button
      type="button"
      className={`provenance-source-card${source.trust === "UNTRUSTED" ? " untrusted-border" : ""}`}
      onClick={() =>
        onPin({
          source_path: source.source_path,
          freshness: trustLabel(source.trust),
          label: source.used_for,
        })
      }
    >
      <div className="mono provenance-source-path">{source.source_path}</div>
      <div className="provenance-source-used">{source.used_for}</div>
      <div className="provenance-source-meta mono">
        grain {source.grain}
        {typeof count === "number" ? ` · ${count} records` : ""}
        {exists === false ? " · file missing" : ""}
        {` · ${trustLabel(source.trust)}`}
      </div>
    </button>
  );
}

export function ProvenanceStructuredView({
  page,
  plantId,
  assetId,
  alertId,
  lookupKey,
  packetEvidence,
  onPin,
}: {
  page: PageProvenance;
  plantId: string;
  assetId: string;
  alertId: string;
  lookupKey: number;
  packetEvidence: Record<string, unknown>[];
  onPin: (p: ProvenancePin) => void;
}) {
  const catalog = useFetch(() => api.dataSources(), [lookupKey]);

  const live = useFetch(async () => {
    const items: { title: string; lines: string[] }[] = [];

    async function collect(title: string, run: () => Promise<string[]>) {
      try {
        items.push({ title, lines: await run() });
      } catch (err) {
        items.push({ title, lines: [(err as Error).message || "Citation unavailable for this selection."] });
      }
    }

    if (page.route === "/identity" && assetId) {
      await collect(`Pinned asset ${assetId}`, async () => {
        const identity = await api.identity(assetId);
        const prov = (identity.provenance || {}) as Record<string, unknown>;
        return [
          `source_path ${fmt(prov.source_path)}`,
          `claim ${fmt(prov.claim_type)} · freshness ${fmt(prov.freshness)}`,
        ];
      });
    }

    if (page.route === "/telemetry") {
      await collect("Historian quality (this scope)", async () => {
        const quality = await api.telemetryQuality({
          plantId: plantId || undefined,
          assetId: assetId || undefined,
        });
        return [
          `source_path ${fmt(quality.source_path)}`,
          `bad/uncertain ${fmt(quality.bad_or_uncertain)} · mismatches ${fmt(quality.unit_mismatches)}`,
          fmt(quality.note),
        ];
      });
    }

    if (page.route === "/risk" && (assetId || plantId)) {
      await collect(assetId ? `Findings on ${assetId}` : `Top ranked in ${plantId}`, async () => {
        const ranked = await api.risk({
          limit: 3,
          assetId: assetId || undefined,
          plantId: assetId ? undefined : plantId || undefined,
        });
        const findings = (ranked.rankings as Record<string, unknown>[]) || [];
        if (!findings.length) {
          return ["No findings in this scope. Source is still data/raw/vulnerabilities.csv."];
        }
        return findings.map((f) => {
          const fb = f.factor_breakdown as
            | { reachability?: { value?: unknown }; contextual_score?: unknown }
            | undefined;
          return `${fmt(f.finding_id)} cvss ${fmt(f.cvss)} reach ${fmt(fb?.reachability?.value ?? f.network_reachable)} score ${fmt(fb?.contextual_score)}`;
        });
      });
    }

    if (page.route === "/recovery" && plantId) {
      await collect(`Recovery ${plantId}`, async () => {
        const recovery = await api.recovery(plantId);
        const first = ((recovery.components as Record<string, unknown>[]) || [])[0];
        const prov = (first?.provenance || {}) as Record<string, unknown>;
        return [
          `source_path ${fmt(prov.source_path)}`,
          `ready ${fmt(recovery.recovery_ready_count)} / ${fmt(recovery.component_count)}`,
          fmt(recovery.note),
        ];
      });
    }

    if (page.route === "/sessions") {
      await collect("Vendor sessions", async () => {
        const sessions = await api.vendorSessions(1);
        return [`source_path ${fmt(sessions.source_path)}`, fmt(sessions.note)];
      });
    }

    if (page.route === "/incident") {
      await collect("Shift notes", async () => {
        const notes = await api.shiftNotes(plantId || undefined);
        return [`source_path ${fmt(notes.source_path)}`, `trust ${fmt(notes.trust)} — not policy`];
      });
    }

    if (page.route === "/identity" && !assetId) {
      await collect(plantId ? `Conflicts in ${plantId}` : "Estate identity conflicts", async () => {
        const conflicts = await api.identityConflicts(plantId || undefined);
        return [
          `state conflicts ${fmt(conflicts.asset_state_conflicts)} · alias collisions ${fmt(conflicts.alias_collisions)} · rows ${fmt(conflicts.conflict_count)}`,
        ];
      });
    }

    if (alertId && (page.route === "/incident" || page.route === "/recommend") && assetId) {
      await collect(`Alert ${alertId}`, async () => {
        const alerts = await api.assetAlerts(assetId, 20);
        const match = alerts.alerts.find((a) => a.alert_id === alertId);
        if (!match) return ["Alert not on this asset in cyber_alerts.csv"];
        return [`${fmt(match.severity)} · ${fmt(match.status)} · process_context ${fmt(match.process_context)}`];
      });
    }

    return items;
  }, [page.route, plantId, assetId, alertId, lookupKey]);

  if (catalog.loading) return <LoadingBlock label="Loading sources for this screen…" />;
  if (catalog.error) return <ErrorBlock message={catalog.error} />;

  const catalogByPath = new Map(
    ((catalog.data?.sources as Record<string, unknown>[]) || []).map((s) => [String(s.path), s]),
  );

  return (
    <div className="provenance-structured">
      <p className="ai-off-note">{page.summary}</p>

      <h4 className="provenance-subheading">This screen reads</h4>
      <div className="provenance-source-list">
        {page.sources.map((source) => (
          <SourceCard
            key={source.source_path + source.used_for}
            source={source}
            catalog={catalogByPath.get(source.source_path)}
            onPin={onPin}
          />
        ))}
      </div>

      {packetEvidence.length > 0 && (page.route === "/recommend" || page.route === "/incident") && (
        <>
          <h4 className="provenance-subheading">Recommendation packet evidence</h4>
          <ul className="provenance-evidence-list mono">
            {packetEvidence.slice(0, 8).map((e, i) => (
              <li key={`pkt-${i}`}>
                {fmt(e.source_path)}
                {e.record_id ? ` · ${fmt(e.record_id)}` : ""}
                {e.field ? ` · ${fmt(e.field)}=${fmt(e.value)}` : ""}
              </li>
            ))}
          </ul>
        </>
      )}

      {live.loading && <p className="ai-off-note">Loading live citation for current plant/asset…</p>}
      {live.error && <ErrorBlock message={live.error} />}
      {(live.data ?? []).map((block) => (
        <div key={block.title} className="provenance-evidence-block">
          <h4 className="provenance-subheading">{block.title}</h4>
          <ul className="provenance-evidence-list mono">
            {block.lines.map((line, i) => (
              <li key={`${block.title}-${i}`}>{line}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
