export interface ScenarioBadge {
  id: string;
  label: string;
  tone: "neutral" | "amber" | "orange" | "red" | "green";
}

export interface ScenarioContext {
  plant_id: string;
  asset_id: string;
  alert_id: string;
  unit_id?: string;
  safe_state?: string;
  barrier_id?: string;
  tag_id?: string;
  component?: string;
}

export interface ScenarioBinding {
  id: string;
  label: string;
  title: string;
  eval_ids: string[];
  source: string | null;
  context: ScenarioContext;
  badges: ScenarioBadge[];
  primary_routes: string[];
  ai_enabled: boolean;
  show_conflicts: boolean;
  ctq_iso_complete?: boolean;
  show_untrusted_shift_notes?: boolean;
  timeline_must_surface?: string[];
  must_not_hide?: string[];
}

export interface ScenarioCatalog {
  version: string;
  note: string;
  scenarios: ScenarioBinding[];
}
