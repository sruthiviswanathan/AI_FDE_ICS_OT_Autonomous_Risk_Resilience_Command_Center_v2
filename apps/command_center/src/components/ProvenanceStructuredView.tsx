import { api } from "../api/client";
import { useFetch } from "../hooks/useFetch";
import { ErrorBlock, LoadingBlock } from "./StateViews";
import { fmt } from "../utils/format";

export function ProvenanceStructuredView({
  plantId,
  assetId,
  alertId,
  lookupKey,
  packetEvidence,
}: {
  plantId: string;
  assetId: string;
  alertId: string;
  lookupKey: number;
  packetEvidence: Record<string, unknown>[];
}) {
  const structured = useFetch(async () => {
    const blocks: { title: string; items: Record<string, unknown>[] }[] = [];

    if (assetId) {
      const identity = await api.identity(assetId);
      blocks.push({
        title: `Identity · ${assetId}`,
        items: [
          identity.provenance as Record<string, unknown>,
          ...(identity.conflicts as Record<string, unknown>[] | undefined)?.map((c) => ({
            conflict_id: c.conflict_id,
            type: c.type,
            severity: c.severity,
          })) ?? [],
        ].filter(Boolean),
      });
      if (alertId) {
        const alerts = await api.assetAlerts(assetId, 20);
        const match = alerts.alerts.find((a) => a.alert_id === alertId);
        if (match) {
          blocks.push({ title: `Alert · ${alertId}`, items: [match] });
        }
      }
    }

    if (plantId) {
      const [recovery, safety] = await Promise.all([
        api.recovery(plantId),
        api.safetyConflicts(plantId),
      ]);
      const recoveryRows = (recovery.components as Record<string, unknown>[] | undefined) ?? [];
      blocks.push({
        title: `Recovery · ${plantId}`,
        items: recoveryRows.length
          ? recoveryRows.slice(0, 5)
          : [{ plant_id: recovery.plant_id, note: recovery.note }],
      });
      const safetyRows =
        (safety.sample_bypassed_unauthorized as Record<string, unknown>[] | undefined) ?? [];
      blocks.push({
        title: `Safety · ${plantId}`,
        items: safetyRows.length
          ? safetyRows.slice(0, 5)
          : [
              {
                degraded_barrier_count: safety.degraded_barrier_count,
                bypassed_unauthorized_count: safety.bypassed_unauthorized_count,
                high_critical_unknown_process_context: safety.high_critical_unknown_process_context,
                note: safety.note,
              },
            ],
      });
    }

    if (!plantId && !assetId) {
      const conflicts = await api.identityConflicts(plantId || undefined);
      blocks.push({ title: "Estate identity conflicts", items: [conflicts as Record<string, unknown>] });
    }

    const sources = await api.dataSources();
    blocks.push({
      title: "Canonical sources",
      items: (sources.sources as Record<string, unknown>[] | undefined)?.slice(0, 6) ?? [],
    });

    return blocks;
  }, [plantId, assetId, alertId, lookupKey]);

  if (structured.loading) return <LoadingBlock label="Loading structured evidence…" />;
  if (structured.error) return <ErrorBlock message={structured.error} />;

  const blocks = structured.data ?? [];

  return (
    <div className="provenance-structured">
      {packetEvidence.length > 0 && (
        <>
          <h4 className="provenance-subheading">Recommendation packet</h4>
          <ul className="provenance-evidence-list mono">
            {packetEvidence.slice(0, 8).map((e, i) => (
              <li key={`pkt-${i}`}>{JSON.stringify(e)}</li>
            ))}
          </ul>
        </>
      )}
      {blocks.map((block) => (
        <div key={block.title} className="provenance-evidence-block">
          <h4 className="provenance-subheading">{block.title}</h4>
          {block.items.length === 0 ? (
            <p className="ai-off-note">No records for current selection.</p>
          ) : (
            <ul className="provenance-evidence-list mono">
              {block.items.map((item, i) => (
                <li key={`${block.title}-${i}`}>{JSON.stringify(item)}</li>
              ))}
            </ul>
          )}
        </div>
      ))}
      {!blocks.length && !packetEvidence.length && (
        <p className="ai-off-note">Select plant / asset / alert in the context bar to load evidence.</p>
      )}
    </div>
  );
}
