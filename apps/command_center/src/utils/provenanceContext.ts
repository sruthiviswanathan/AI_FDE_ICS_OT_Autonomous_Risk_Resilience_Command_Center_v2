export type GraphQueryId = "Q1" | "Q2" | "Q3" | "Q4" | "Q5";

export function deriveGraphQuery(params: {
  alertId?: string;
  assetId?: string;
  plantId?: string;
}): GraphQueryId {
  if (params.alertId) return "Q5";
  if (params.assetId) return "Q1";
  if (params.plantId) return "Q4";
  return "Q4";
}

export function graphQueryLabel(query: GraphQueryId): string {
  switch (query) {
    case "Q1":
      return "Identity neighborhood";
    case "Q2":
      return "Undocumented paths";
    case "Q3":
      return "Safety + cyber tension";
    case "Q4":
      return "Recovery posture";
    case "Q5":
      return "Incident cascade";
    default:
      return query;
  }
}

export function traceMatchesContext(
  trace: Record<string, unknown>,
  plantId: string,
  assetId: string,
  alertId: string,
): boolean {
  if (!plantId && !assetId && !alertId) return true;
  const ctx = (trace.context || trace.inputs || {}) as Record<string, unknown>;
  if (alertId && (ctx.alert_id === alertId || trace.alert_id === alertId)) return true;
  if (assetId && (ctx.asset_id === assetId || trace.asset_id === assetId)) return true;
  if (plantId && (ctx.plant_id === plantId || trace.plant_id === plantId)) return true;
  const purpose = String(trace.purpose || trace.action || "").toLowerCase();
  if (assetId && purpose.includes(assetId.toLowerCase())) return true;
  if (plantId && purpose.includes(plantId.toLowerCase())) return true;
  return false;
}
