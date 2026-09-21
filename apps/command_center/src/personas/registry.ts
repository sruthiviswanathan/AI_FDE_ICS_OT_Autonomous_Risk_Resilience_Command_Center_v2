export type PersonaId =
  | "soc_analyst"
  | "process_engineer"
  | "safety_owner"
  | "executive"
  | "fde"
  | "full";

export type AiMode = "off" | "on" | "moonshot";

export const MOONSHOT_PERSONAS: PersonaId[] = ["full", "fde", "soc_analyst"];

export type ProvenanceChannel = "STRUCTURED" | "GRAPH" | "POLICY" | "MEMORY";

export interface ContextFieldVisibility {
  plant: boolean;
  asset: boolean;
  alert: boolean;
}

export interface PersonaView {
  id: PersonaId;
  label: string;
  description: string;
  defaultRoute: string;
  routes: string[];
  contextFields: ContextFieldVisibility;
  provenanceDefaultChannel: ProvenanceChannel;
  drawerDefaultOpen: boolean;
  scenarioRailVisible: boolean;
}

export interface NavItem {
  to: string;
  label: string;
  personas: PersonaId[];
}

export interface NavGroup {
  group: string;
  items: NavItem[];
}

/** Incident screens always reachable when alert context is pinned. */
export const INCIDENT_ROUTES = ["/incident", "/recommend"] as const;

export const ALL_ROUTES = [
  "/",
  "/estate",
  "/identity",
  "/telemetry",
  "/process",
  "/risk",
  "/safety",
  "/sessions",
  "/recovery",
  "/incident",
  "/recommend",
  "/audit",
  "/simulation",
  "/kpi",
  "/executive",
] as const;

export const PERSONA_VIEWS: Record<PersonaId, PersonaView> = {
  soc_analyst: {
    id: "soc_analyst",
    label: "SOC / OT Analyst",
    description: "Alert triage, contextual risk, draft recommendation packets",
    defaultRoute: "/",
    routes: [
      "/",
      "/estate",
      "/identity",
      "/telemetry",
      "/risk",
      "/safety",
      "/sessions",
      "/incident",
      "/recommend",
      "/audit",
    ],
    contextFields: { plant: true, asset: true, alert: true },
    provenanceDefaultChannel: "GRAPH",
    drawerDefaultOpen: true,
    scenarioRailVisible: true,
  },
  process_engineer: {
    id: "process_engineer",
    label: "Process Engineer",
    description: "Process dependencies, safe-state, recovery readiness",
    defaultRoute: "/process",
    routes: ["/process", "/recovery", "/telemetry", "/incident", "/recommend"],
    contextFields: { plant: true, asset: true, alert: false },
    provenanceDefaultChannel: "STRUCTURED",
    drawerDefaultOpen: true,
    scenarioRailVisible: true,
  },
  safety_owner: {
    id: "safety_owner",
    label: "Safety / SIS Owner",
    description: "Barrier bypass, cyber-vs-safety conflicts, policy context",
    defaultRoute: "/safety",
    routes: ["/safety", "/process", "/incident", "/recommend"],
    contextFields: { plant: true, asset: true, alert: false },
    provenanceDefaultChannel: "POLICY",
    drawerDefaultOpen: true,
    scenarioRailVisible: true,
  },
  executive: {
    id: "executive",
    label: "Executive / VP Ops",
    description: "Estate posture, KPI trends, residual risk — read-only",
    defaultRoute: "/executive",
    routes: ["/executive", "/kpi", "/recovery", "/recommend", "/", "/estate"],
    contextFields: { plant: true, asset: false, alert: false },
    provenanceDefaultChannel: "STRUCTURED",
    drawerDefaultOpen: false,
    scenarioRailVisible: false,
  },
  fde: {
    id: "fde",
    label: "FDE / Platform",
    description: "Full estate, eval harness, ops telemetry",
    defaultRoute: "/",
    routes: [...ALL_ROUTES],
    contextFields: { plant: true, asset: true, alert: true },
    provenanceDefaultChannel: "STRUCTURED",
    drawerDefaultOpen: true,
    scenarioRailVisible: true,
  },
  full: {
    id: "full",
    label: "Full workshop view",
    description: "All screens — demo and cross-role walkthrough",
    defaultRoute: "/",
    routes: [...ALL_ROUTES],
    contextFields: { plant: true, asset: true, alert: true },
    provenanceDefaultChannel: "GRAPH",
    drawerDefaultOpen: true,
    scenarioRailVisible: true,
  },
};

export const PERSONA_LIST: PersonaView[] = Object.values(PERSONA_VIEWS);

export const APP_NAV: NavGroup[] = [
  {
    group: "Home",
    items: [
      { to: "/", label: "Control Tower", personas: ["soc_analyst", "fde", "full", "executive"] },
      { to: "/estate", label: "Estate Dashboard", personas: ["soc_analyst", "fde", "full", "executive"] },
    ],
  },
  {
    group: "Identity & data",
    items: [
      { to: "/identity", label: "Identity Reconciliation", personas: ["soc_analyst", "fde", "full"] },
      { to: "/telemetry", label: "Telemetry Quality", personas: ["soc_analyst", "process_engineer", "fde", "full"] },
    ],
  },
  {
    group: "Risk & safety",
    items: [
      { to: "/risk", label: "Contextual Risk", personas: ["soc_analyst", "fde", "full"] },
      { to: "/safety", label: "Safety vs Security", personas: ["soc_analyst", "safety_owner", "fde", "full"] },
      { to: "/sessions", label: "Vendor Sessions", personas: ["soc_analyst", "fde", "full"] },
    ],
  },
  {
    group: "Process & recovery",
    items: [
      { to: "/process", label: "Process Graph", personas: ["process_engineer", "safety_owner", "fde", "full"] },
      { to: "/recovery", label: "Recovery Graph", personas: ["process_engineer", "executive", "fde", "full"] },
    ],
  },
  {
    group: "Incident",
    items: [
      { to: "/incident", label: "Incident Context", personas: ["soc_analyst", "process_engineer", "safety_owner", "fde", "full"] },
      { to: "/recommend", label: "Recommendation Gate", personas: ["soc_analyst", "process_engineer", "safety_owner", "executive", "fde", "full"] },
    ],
  },
  {
    group: "Evidence",
    items: [{ to: "/audit", label: "Decision Trace", personas: ["soc_analyst", "fde", "full"] }],
  },
  {
    group: "Quality",
    items: [
      { to: "/simulation", label: "Inject / Simulation", personas: ["fde", "full"] },
      { to: "/kpi", label: "KPI Before/After", personas: ["executive", "fde", "full"] },
      { to: "/executive", label: "Executive Brief", personas: ["executive", "fde", "full"] },
    ],
  },
];

const STORAGE_KEY = "cc_persona";

export function isPersonaId(value: string | null | undefined): value is PersonaId {
  return value != null && value in PERSONA_VIEWS;
}

export function loadStoredPersona(): PersonaId {
  if (typeof window === "undefined") return "full";
  const fromUrl = new URLSearchParams(window.location.search).get("persona");
  if (isPersonaId(fromUrl)) return fromUrl;
  const stored = window.localStorage.getItem(STORAGE_KEY);
  if (isPersonaId(stored)) return stored;
  return "full";
}

export function persistSearch(updates: Record<string, string | null>) {
  if (typeof window === "undefined") return;
  const url = new URL(window.location.href);
  Object.entries(updates).forEach(([key, value]) => {
    if (value === null || value === "") url.searchParams.delete(key);
    else url.searchParams.set(key, value);
  });
  window.history.replaceState({}, "", url.toString());
}

export function persistPersona(id: PersonaId) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEY, id);
  persistSearch({ persona: id });
}

export function canUseMoonshot(id: PersonaId): boolean {
  return MOONSHOT_PERSONAS.includes(id);
}

export function isAiMode(value: string | null | undefined): value is AiMode {
  return value === "off" || value === "on" || value === "moonshot";
}

export function loadStoredAiMode(): AiMode {
  if (typeof window === "undefined") return "off";
  const fromUrl = new URLSearchParams(window.location.search).get("ai");
  if (isAiMode(fromUrl)) return fromUrl;
  return "off";
}

export function clampAiMode(mode: AiMode, personaId: PersonaId, scenario: string): AiMode {
  if (scenario === "ai_outage") return "off";
  if (mode === "moonshot" && !canUseMoonshot(personaId)) return "off";
  return mode;
}

export function hasIncidentContext(alertId: string, scenario: string): boolean {
  if (alertId.trim()) return true;
  return scenario !== "nominal";
}

export function isRouteAllowed(
  pathname: string,
  personaId: PersonaId,
  alertId: string,
  scenario: string,
): boolean {
  const path = pathname === "" ? "/" : pathname.replace(/\/$/, "") || "/";
  const view = PERSONA_VIEWS[personaId];
  if (view.routes.includes(path)) return true;
  if (INCIDENT_ROUTES.includes(path as (typeof INCIDENT_ROUTES)[number]) && hasIncidentContext(alertId, scenario)) {
    return true;
  }
  return false;
}

export function filterNavForPersona(personaId: PersonaId): NavGroup[] {
  return APP_NAV.map((group) => ({
    ...group,
    items: group.items.filter((item) => item.personas.includes(personaId)),
  })).filter((group) => group.items.length > 0);
}
