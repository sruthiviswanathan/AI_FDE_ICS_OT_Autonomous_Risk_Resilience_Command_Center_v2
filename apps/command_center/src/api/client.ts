/** Dev: `/api` (Vite proxy). Integrated/single-port build: `` → `/health` on same host. */
const BASE = import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? "/api" : "");

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export type PostureStatus = "ok" | "amber" | "red";

export type PostureLayerKey =
  | "cyber_exposure"
  | "process_ops_disagreement"
  | "safety_posture"
  | "recovery_credibility"
  | "evidence_quality";

export interface PostureLayer {
  status: PostureStatus;
  reason: string;
  count?: number;
}

export interface PlantEstateRow {
  plant_id: string;
  region: string;
  country: string;
  plant_type: string;
  criticality: string;
  counts: {
    assets: number;
    alerts_total: number;
    alerts_high_critical: number;
    alerts_open_or_triaged: number;
    alerts_high_critical_open: number;
    asset_state_conflicts: number;
    safety_degraded_units: number;
    recovery_stale: number;
  };
  signals: {
    elevated: boolean;
    elevation_reasons: string[];
    posture_composite?: PostureStatus;
  };
  posture_layers?: Partial<Record<PostureLayerKey, PostureLayer>>;
  top_alerts: Record<string, string>[];
  assets_by_registered_state?: Record<string, number>;
  assets_by_observed_state?: Record<string, number>;
  top_assets_by_alerts?: { asset_id: string; alert_count: number }[];
}

export interface AssetStatusSummary {
  total_assets: number;
  by_registered_state: Record<string, number>;
  by_observed_state: Record<string, number>;
  state_conflicts: number;
  registered_observed_pairs: { pair: string; count: number }[];
}

export interface EstateByPlantResponse {
  provenance: string;
  freshness: string;
  plant_count: number;
  total_alerts?: number;
  asset_status_summary?: AssetStatusSummary;
  plants: PlantEstateRow[];
  methodology: {
    elevated_rule: string;
    posture_motto?: string;
    posture_composite_rule?: string;
    not_operational_risk_rank: string;
  };
}

export interface AdvisoryForecast {
  forecast_id: string;
  plant_id: string;
  asset_id?: string | null;
  category: string;
  layer: string;
  horizon_days: number;
  confidence: string;
  recommended_action: string;
  required_role: string;
  action_tier: number;
  twin_scenario_id: string;
  evidence_ids: string[];
  missing_evidence: string[];
  abstain_reason?: string | null;
  execute: boolean;
  alert_id?: string;
  session_id?: string;
  barrier_id?: string;
  component?: string;
}

export interface ForecastsResponse {
  mode: string;
  banner: string;
  execute: boolean;
  plant_id: string;
  forecasts: AdvisoryForecast[];
  note?: string;
}

export interface ExplainResponse {
  mode: string;
  plant_id: string;
  asset_id?: string | null;
  alert_id?: string | null;
  caption: string;
  sentence_count: number;
  evidence_ids: string[];
  source_files: string[];
  engine_authoritative: boolean;
  explainer: string;
  execute: boolean;
  note?: string;
}

export interface TwinPreviewResponse {
  mode: string;
  banner: string;
  execute: boolean;
  apply_to_plant: boolean;
  scenario_id: string;
  forecast_id?: string | null;
  proposed_action: string;
  lab_result: string;
  detail: string;
  create_approval_packet: { method: string; path: string; execute: boolean; note?: string };
  forbidden: string[];
  note?: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new ApiError(res.status, detail || res.statusText);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: () =>
    request<{ status: string; mode: string; api_version?: string }>("/health"),
  plants: () =>
    request<{ count: number; plants: Record<string, string>[] }>("/plants"),
  plantAssets: (plantId: string, limit = 100, q?: string) => {
    const params = new URLSearchParams({ limit: String(limit) });
    if (q) params.set("q", q);
    return request<{ plant_id: string; count: number; limit: number; assets: Record<string, string>[] }>(
      `/plants/${encodeURIComponent(plantId)}/assets?${params}`,
    );
  },
  assetAlerts: (assetId: string, limit = 50, severity?: string) => {
    const params = new URLSearchParams({ limit: String(limit) });
    if (severity) params.set("severity", severity);
    return request<{ asset_id: string; count: number; limit: number; alerts: Record<string, string>[] }>(
      `/assets/${encodeURIComponent(assetId)}/alerts?${params}`,
    );
  },
  diagnostics: () => request<Record<string, number>>("/diagnostics"),
  dataSources: () =>
    request<{ sources: Record<string, unknown>[]; note?: string; mode?: string }>("/data/sources"),
  opsSlo: () => request<Record<string, unknown>>("/ops/slo"),
  opsCost: () => request<Record<string, unknown>>("/ops/cost-per-incident"),
  estate: () => request<Record<string, unknown>>("/data/views/estate"),
  estateByPlant: (params?: { includeTopAlerts?: number; severityMin?: string }) => {
    const q = new URLSearchParams();
    if (params?.includeTopAlerts !== undefined) {
      q.set("include_top_alerts", String(params.includeTopAlerts));
    }
    if (params?.severityMin) q.set("severity_min", params.severityMin);
    const suffix = q.toString() ? `?${q}` : "";
    return request<EstateByPlantResponse>(`/data/views/estate-by-plant${suffix}`);
  },
  identity: (id: string) => request<Record<string, unknown>>(`/assets/${id}/identity`),
  identityConflicts: (plantId?: string) =>
    request<Record<string, unknown>>(
      `/identity/conflicts${plantId ? `?plant_id=${encodeURIComponent(plantId)}` : ""}`,
    ),
  telemetryQuality: (params?: { plantId?: string; assetId?: string }) => {
    const q = new URLSearchParams();
    if (params?.plantId) q.set("plant_id", params.plantId);
    if (params?.assetId) q.set("asset_id", params.assetId);
    const suffix = q.toString() ? `?${q}` : "";
    return request<Record<string, unknown>>(`/telemetry/quality${suffix}`);
  },
  telemetryTimeline: (params?: {
    tagId?: string;
    plantId?: string;
    assetId?: string;
    limit?: number;
    offset?: number;
    sortBy?: string;
    sortDir?: "asc" | "desc";
    quality?: string;
    flag?: string;
    q?: string;
  }) => {
    const q = new URLSearchParams({ order: "event_time" });
    if (params?.tagId) q.set("tag_id", params.tagId);
    if (params?.plantId) q.set("plant_id", params.plantId);
    if (params?.assetId) q.set("asset_id", params.assetId);
    if (params?.limit !== undefined) q.set("limit", String(params.limit));
    if (params?.offset !== undefined) q.set("offset", String(params.offset));
    if (params?.sortBy) q.set("sort_by", params.sortBy);
    if (params?.sortDir) q.set("sort_dir", params.sortDir);
    if (params?.quality) q.set("quality", params.quality);
    if (params?.flag) q.set("flag", params.flag);
    if (params?.q) q.set("q", params.q);
    return request<Record<string, unknown>>(`/telemetry/timeline?${q}`);
  },
  risk: (params?: { limit?: number; plantId?: string; assetId?: string }) => {
    const q = new URLSearchParams({ limit: String(params?.limit ?? 20) });
    if (params?.plantId) q.set("plant_id", params.plantId);
    if (params?.assetId) q.set("asset_id", params.assetId);
    return request<Record<string, unknown>>(`/risk/contextual?${q}`);
  },
  safetyConflicts: (plantId?: string) =>
    request<Record<string, unknown>>(
      `/safety/conflicts${plantId ? `?plant_id=${encodeURIComponent(plantId)}` : ""}`,
    ),
  recovery: (plant: string) => request<Record<string, unknown>>(`/recovery/${plant}`),
  graphSlice: (params: Record<string, string | number | undefined>) => {
    const q = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== "") q.set(k, String(v));
    });
    return request<Record<string, unknown>>(`/graph/slice?${q}`);
  },
  authority: () => request<Record<string, unknown>>("/authority/actions"),
  recommend: (body: Record<string, unknown>) =>
    request<Record<string, unknown>>("/recommend", { method: "POST", body: JSON.stringify(body) }),
  evalRun: (caseIds?: string[]) =>
    request<Record<string, unknown>>("/eval/run", {
      method: "POST",
      body: JSON.stringify(caseIds ? { case_ids: caseIds } : {}),
    }),
  traces: (limit = 50) => request<{ traces: Record<string, unknown>[] }>(`/audit/traces?limit=${limit}`),
  scenarioCatalog: () => request<import("../scenarios/types").ScenarioCatalog>("/scenarios/catalog"),
  scenario: (id: string) => request<Record<string, unknown>>(`/scenarios/${id}`),
  shiftNotes: (plantId?: string) =>
    request<{
      content: string;
      trust: string;
      source_path: string;
      requested_plant_id?: string | null;
      source_plant_id?: string | null;
      bound_to_requested_plant?: boolean;
      open_item?: string;
      scope?: string;
      note?: string;
    }>(
      `/data/shift-notes/untrusted${plantId ? `?plant_id=${encodeURIComponent(plantId)}` : ""}`,
    ),
  vendorSessions: (limit = 50) => request<Record<string, unknown>>(`/data/views/vendor-sessions?limit=${limit}`),
  demoWorkflow: () => request<Record<string, unknown>>("/agent/workflow/demo"),
  forecasts: (params: { plantId: string; assetId?: string; alertId?: string }) => {
    const q = new URLSearchParams({ plant_id: params.plantId, as_of: "workshop-static" });
    if (params.assetId) q.set("asset_id", params.assetId);
    if (params.alertId) q.set("alert_id", params.alertId);
    return request<ForecastsResponse>(`/forecasts?${q}`);
  },
  explain: (params: { plantId: string; assetId?: string; alertId?: string }) => {
    const q = new URLSearchParams({ plant_id: params.plantId });
    if (params.assetId) q.set("asset_id", params.assetId);
    if (params.alertId) q.set("alert_id", params.alertId);
    return request<ExplainResponse>(`/explain?${q}`);
  },
  twinPreview: (params: { scenarioId?: string; forecastId?: string; proposedAction?: string }) => {
    const q = new URLSearchParams();
    if (params.scenarioId) q.set("scenario_id", params.scenarioId);
    if (params.forecastId) q.set("forecast_id", params.forecastId);
    q.set("proposed_action", params.proposedAction || "do_nothing");
    return request<TwinPreviewResponse>(`/twin/preview?${q}`);
  },
};
