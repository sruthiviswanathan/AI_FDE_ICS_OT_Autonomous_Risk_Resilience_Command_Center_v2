/** Dev: `/api` (Vite proxy). Integrated/single-port build: `` → `/health` on same host. */
const BASE = import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? "/api" : "");

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
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
  opsSlo: () => request<Record<string, unknown>>("/ops/slo"),
  opsCost: () => request<Record<string, unknown>>("/ops/cost-per-incident"),
  estate: () => request<Record<string, unknown>>("/data/views/estate"),
  identity: (id: string) => request<Record<string, unknown>>(`/assets/${id}/identity`),
  identityConflicts: () => request<Record<string, unknown>>("/identity/conflicts"),
  telemetryQuality: () => request<Record<string, unknown>>("/telemetry/quality"),
  telemetryTimeline: (tagId?: string) =>
    request<Record<string, unknown>>(
      `/telemetry/timeline?order=event_time${tagId ? `&tag_id=${encodeURIComponent(tagId)}` : ""}`,
    ),
  risk: (limit = 20) => request<Record<string, unknown>>(`/risk/contextual?limit=${limit}`),
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
  shiftNotes: () => request<{ content: string; trust: string; source_path: string }>("/data/shift-notes/untrusted"),
  vendorSessions: (limit = 50) => request<Record<string, unknown>>(`/data/views/vendor-sessions?limit=${limit}`),
  demoWorkflow: () => request<Record<string, unknown>>("/agent/workflow/demo"),
};
