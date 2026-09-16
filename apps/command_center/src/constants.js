export const SCREENS = [
  ["sc-tower", "1 Control Tower"],
  ["sc-identity", "2 Identity"],
  ["sc-telemetry", "3 Telemetry"],
  ["sc-graph", "4 Process graph"],
  ["sc-risk", "5 Contextual risk"],
  ["sc-safety", "6 Safety vs cyber"],
  ["sc-sessions", "7 Vendor sessions"],
  ["sc-recovery", "8 Recovery"],
  ["sc-incident", "9 Incident graph"],
  ["sc-retrieval", "10 Retrieval"],
  ["sc-authority", "11 Authority gate"],
  ["sc-trace", "12 Decision trace"],
  ["sc-inject", "13 Inject sim"],
  ["sc-kpi", "14 KPI"],
  ["sc-exec", "15 Executive"],
];

export const INJECTS = [
  ["inject_01", "Inventory mismatch"],
  ["inject_02", "Historian quality"],
  ["inject_03", "Unapproved session"],
  ["inject_04", "Safety bypass aging"],
  ["inject_05", "Regional SCADA outage"],
  ["inject_06", "Restore failure drill"],
  ["cascade_001", "CASCADE-001"],
  ["ai_outage", "Explainer outage (EVAL-016)"],
];

export const ROLES = [
  ["soc", "SOC", "sc-risk"],
  ["pe", "Process Eng", "sc-safety"],
  ["safety", "Safety", "sc-safety"],
  ["ops", "Ops", "sc-recovery"],
  ["exec", "Exec", "sc-exec"],
  ["fde", "FDE", "sc-tower"],
];

export const ROLE_HELP = {
  soc: "Start at contextual risk. Draft a packet; do not isolate.",
  pe: "Safety vs cyber first. MIN_LOAD is a stop, not a green light.",
  safety: "Barrier state is recorded. Existing bypass is not bypass_interlock.",
  ops: "Recovery triple, not a CURRENT badge. Vendor sessions are observe-only.",
  exec: "Recoverable this weekend? Not if restore-test or runbook is stale.",
  fde: "Estate conflicts stay countable. This is not a health score.",
};

export const LABELS = {
  permit_allowed: "Permit allowed",
  permit_refused: "Permit refused",
  permit_tier: "Permit tier",
  approval: "Approval",
  where_to_read_it: "Where to read it",
  api_ai_enabled: "Explainer flag (env AI_ENABLED)",
  explainer: "Placeholder explainer",
  explainer_is_authority: "Explainer is authority",
  model_selected: "LLM selected",
  ai_enabled: "Placeholder explainer on",
  fallback: "Explainer-off fallback",
  trace_count: "Decision traces logged",
  forbidden_execute_tools: "Actions this software cannot run",
  all_plants_export: "All-plants export",
  unknown_is_not_approval: "UNKNOWN is not approval",
  change_remote_access_execute: "VPN / access execute",
  auto_disable_vendor_vpn: "Auto-disable vendor VPN",
  unapproved_in_scope: "Unapproved sessions in this plant",
  isolation_recommendation: "Isolation recommendation",
  executed: "Executed on the plant",
  ot_action: "OT write issued",
  one_click_isolate: "One-click isolate",
  execute_control: "Execute control",
  safe_state: "Process safe state",
  required_role: "Required human role",
  permit: "Authority permit",
  blank_screen: "Blank screen",
  hidden_cot_as_authority: "Hidden model text as authority",
  n: "Traces shown",
  plant_id: "Plant",
  hops: "Hops used",
  hop_cap: "Hop cap",
  whole_graph_dump: "Whole-estate dump",
  imputed_tag_to_unit: "Missing tag→unit filled in",
  node_count: "Nodes in slice",
  edge_count: "Edges in slice",
  registered_state: "Registered state",
  observed_state: "Observed state",
  aliases: "Aliases",
  conflicts: "Conflicts",
  winner: "Chosen winner",
  confidence: "Confidence",
  recovery_ready: "Recover-ready",
  freshness_sla: "Freshness SLA",
  asset_id: "Asset",
  process_healthy_inferred: "GOOD treated as process-healthy",
  imputed_bad_to_good: "BAD rewritten to GOOD",
  unit_mismatches_vs_engineering_unit: "Unit mismatches vs engineering unit",
  duplicates: "Duplicate packets",
  sort_key: "Sort key",
  source_path: "Source",
  note: "Note",
  counts: "Quality counts",
  measured_usd: "Measured USD",
  dollar_sla_invented: "Dollar SLA invented",
  named_authorizer: "Named authorizer",
  legal_class: "Legal class",
  question: "Question",
  answer: "Answer",
  after_note: "After modernization",
  counter_metrics: "Must not count as improvement",
  scenario: "Scenario",
  slice: "Bound estate slice",
  process_impact: "Process impact",
  safety_impact: "Safety impact",
};

export const DIAG_LABELS = {
  asset_state_conflicts: "Register says ACTIVE, field is OFFLINE or UNSEEN",
  alias_collisions: "Same name maps to more than one asset ID",
  undocumented_network_paths: "Observed network paths not on the diagram",
  duplicate_telemetry_packets: "Duplicate historian packets",
  telemetry_bad_or_uncertain: "Telemetry quality BAD or UNCERTAIN",
  telemetry_unit_mismatches: "Temperature tags not in °C",
  safety_bypassed_or_degraded: "Safety barriers not ACTIVE",
  safety_proof_test_due: "Proof tests not CURRENT",
  maintenance_state_conflicts: "CMMS CLOSED but field not returned to service",
  unapproved_remote_sessions: "Remote sessions without approved window",
  remote_sessions_without_confirmed_mfa: "Sessions without confirmed MFA",
  recovery_stale_or_unknown_backup: "Backup not CURRENT",
  recovery_unverified_dependencies: "Recovery dependencies unverified",
  recovery_stale_or_missing_runbooks: "Runbooks stale or missing",
};

export const SLO_HELP = {
  "SLO-OT": "Zero plant execute attempts",
  "SLO-CTQ0": "No OT write routes in the API",
  "SLO-ISO": "Isolate drafts must carry safe state and a required role",
  "SLO-EVAL": "Golden cases keep their must-not rules",
  "SLO-LAT": "p95 under 8s without dropping evidence joins",
};

export const FALSE_IS_SAFE = {
  live_ot: 1, executed: 1, ot_action: 1, one_click_isolate: 1, execute_control: 1,
  change_remote_access_execute: 1, auto_disable_vendor_vpn: 1, all_plants_export: 1,
  whole_graph_dump: 1, imputed_tag_to_unit: 1, hidden_cot_as_authority: 1,
  dollar_sla_invented: 1, process_healthy_inferred: 1, imputed_bad_to_good: 1,
  explainer_is_authority: 1, model_selected: 1,
};

export function emptyCase() {
  return {
    plant_id: null, asset_id: null, asset_ids: [], alias: null, alert_id: null,
    unit_id: null, tag_id: null, finding_id: null, barrier_id: null,
  };
}

export function idsFrom(c) {
  const assets = (c.asset_ids && c.asset_ids.length) ? c.asset_ids.slice() : (c.asset_id ? [c.asset_id] : []);
  return {
    bound: !!(c.plant_id || assets.length || c.alert_id || c.alias || c.tag_id || c.finding_id),
    plant: c.plant_id,
    asset: c.asset_id || assets[0] || null,
    assets,
    alias: c.alias,
    alert: c.alert_id,
    unit: c.unit_id,
    tag: c.tag_id,
    finding: c.finding_id,
    barrier: c.barrier_id,
  };
}

export function demoFrom(c) {
  const i = idsFrom(c);
  const unbound = !i.bound;
  return {
    plantGraph: i.plant || (unbound ? "PLT-10" : i.plant),
    plantRecovery: i.plant || (unbound ? "PLT-01" : i.plant),
    plantSessions: i.plant || (unbound ? "PLT-10" : i.plant),
    assets: i.assets.length ? i.assets : (unbound ? ["OT-00012", "OT-00033"] : []),
    alias: i.alias || (unbound ? "PLT-01-DCS_CONTROLLER-105" : i.alias),
    alert: i.alert || (unbound ? "ALT-002783" : null),
    assetRec: i.asset || (unbound ? "OT-01016" : i.asset),
    tag: i.tag || (unbound ? "PLT-01-U03_TEMP" : i.tag),
  };
}

export function caseChip(c) {
  const i = idsFrom(c);
  if (!i.bound) return "no case — demo slices still load; conflicts stay visible";
  return ["plant=" + (i.plant || "—"), "asset=" + (i.assets.join(",") || "—"), "alert=" + (i.alert || "—"), "alias=" + (i.alias || "—"), "winner=null"].join(" · ");
}

export function recLabel(pkt) {
  const rec = pkt && (pkt.recommendation || pkt.isolation_recommendation || (pkt.draft && pkt.draft.isolation_recommendation));
  if (rec && typeof rec === "object") return rec.code || rec.decision || rec.isolation_recommendation || "UNKNOWN";
  return rec || "UNKNOWN";
}

export function hitlState(item) {
  if (item && (item.executed || item.execute_control)) return "must_not_execute";
  const rec = String((item && (item.recommendation || item.isolation_recommendation)) || "");
  if (/refuse|denied|REFUSED/i.test(rec)) return "refused";
  if (/ABSTAIN|MONITOR|DO_NOT_ISOLATE|ISOLATE_DRAFT|RECOMMEND/i.test(rec)) return "AwaitAuthorization";
  return "Recommend";
}

export function mergeCase(prev, partial) {
  const next = { ...emptyCase(), ...prev, ...partial };
  if (partial && Object.prototype.hasOwnProperty.call(partial, "asset_ids") && !partial.asset_id && (partial.asset_ids || [])[0]) {
    next.asset_id = partial.asset_ids[0];
  }
  if (next.asset_id && (next.asset_ids || []).indexOf(next.asset_id) < 0) {
    next.asset_ids = [next.asset_id].concat(next.asset_ids || []);
  }
  return next;
}
