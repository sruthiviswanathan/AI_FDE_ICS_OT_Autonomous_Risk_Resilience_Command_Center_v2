import type { ProvenanceChannel } from "../personas/registry";
import type { GraphQueryId } from "./provenanceContext";

export type SourceTrust = "workshop-static" | "UNTRUSTED" | "policy";

export interface PageSource {
  source_path: string;
  grain: string;
  used_for: string;
  trust?: SourceTrust;
}

export interface PageProvenance {
  route: string;
  screenId: string;
  title: string;
  summary: string;
  preferredChannel: ProvenanceChannel;
  graphQuery?: GraphQueryId;
  sources: PageSource[];
  policyNote: string;
  memoryNote: string;
}

const FRESHNESS = "workshop-static";

export const WORKSHOP_FRESHNESS = FRESHNESS;

const DIAGNOSTIC_SOURCES: PageSource[] = [
  { source_path: "data/raw/assets.csv", grain: "asset_id", used_for: "Registered vs observed state conflicts" },
  { source_path: "data/raw/asset_aliases.csv", grain: "alias", used_for: "Alias collisions" },
  { source_path: "data/raw/network_edges.csv", grain: "edge", used_for: "Undocumented observed paths" },
  {
    source_path: "data/telemetry/tag_telemetry.jsonl",
    grain: "event_id",
    used_for: "Bad/uncertain, duplicates, TEMP unit ≠ C",
  },
  { source_path: "data/raw/safety_barriers.csv", grain: "barrier_id", used_for: "Bypassed or degraded barriers" },
  { source_path: "data/raw/work_orders.csv", grain: "work_order_id", used_for: "CMMS CLOSED vs field not RTS" },
  {
    source_path: "data/raw/remote_access_sessions.csv",
    grain: "session_id",
    used_for: "Unapproved sessions and MFA gaps",
  },
  {
    source_path: "data/raw/recovery_readiness.csv",
    grain: "plant_id+component",
    used_for: "Stale backup, restore test, runbook",
  },
];

const PAGES: Record<string, PageProvenance> = {
  "/": {
    route: "/",
    screenId: "control-tower",
    title: "Control Tower",
    summary: "Estate disagreement tiles. Derived from diagnostics over the files below — not a CVE leaderboard.",
    preferredChannel: "STRUCTURED",
    sources: [
      ...DIAGNOSTIC_SOURCES,
      { source_path: "data/reference/plants.csv", grain: "plant_id", used_for: "18-plant estate rollup" },
      { source_path: "data/raw/cyber_alerts.csv", grain: "alert_id", used_for: "Plant alert samples on the tower" },
      {
        source_path: "src/ot_command/core/policy.py",
        grain: "ACTION_TIERS",
        used_for: "execute=false / no OT write from this wall",
        trust: "policy",
      },
    ],
    policyNote: "Tower numbers are inventory diagnostics. ACTION_TIERS still refuse isolate / PLC / SIS writes.",
    memoryNote: "Decision traces are not the source of the 4094 / 200 / 47 tiles. Those come from estate files.",
  },
  "/estate": {
    route: "/estate",
    screenId: "estate-dashboard",
    title: "Estate Dashboard",
    summary: "Per-plant inventory signals. Posture is disagreement, not operational risk rank.",
    preferredChannel: "GRAPH",
    sources: [
      { source_path: "data/reference/plants.csv", grain: "plant_id", used_for: "Plant nodes, region, type" },
      { source_path: "data/raw/assets.csv", grain: "asset_id", used_for: "Asset counts and state split" },
      { source_path: "data/raw/cyber_alerts.csv", grain: "alert_id", used_for: "Alerts-by-plant samples" },
      { source_path: "data/raw/safety_barriers.csv", grain: "barrier_id", used_for: "Degraded-unit count" },
      { source_path: "data/raw/recovery_readiness.csv", grain: "plant_id+component", used_for: "Stale recovery count" },
      ...DIAGNOSTIC_SOURCES.filter((s) =>
        ["data/raw/asset_aliases.csv", "data/raw/network_edges.csv", "data/telemetry/tag_telemetry.jsonl"].includes(
          s.source_path,
        ),
      ),
    ],
    policyNote: "Estate graph does not execute. Isolate remains tier 3 / human authorize.",
    memoryNote: "Traces are prior drafts. This screen reads plants, assets, alerts, barriers, recovery.",
  },
  "/identity": {
    route: "/identity",
    screenId: "identity-reconciliation",
    title: "Identity Reconciliation",
    summary: "Registered vs observed vs shadow. No CMDB winner. Alias collisions stay visible.",
    preferredChannel: "STRUCTURED",
    graphQuery: "Q1",
    sources: [
      { source_path: "data/raw/assets.csv", grain: "asset_id", used_for: "Registered and observed state" },
      { source_path: "data/raw/asset_aliases.csv", grain: "alias", used_for: "Alias → candidate assets" },
      {
        source_path: "data/shadow/ot_asset_inventory_FINAL_v8.csv",
        grain: "asset_id",
        used_for: "Shadow overlay — evidence only, not SoR",
        trust: "UNTRUSTED",
      },
      { source_path: "data/reference/tags.csv", grain: "tag_id", used_for: "Whether the asset has a historian tag" },
    ],
    policyNote: "Identity does not authorize merge or promote-shadow. Those are not ACTION_TIERS verbs here.",
    memoryNote: "A resolve-alias click is not a CMDB write. Traces do not replace assets.csv.",
  },
  "/telemetry": {
    route: "/telemetry",
    screenId: "telemetry-quality",
    title: "Telemetry Quality",
    summary:
      "Historian packets vs tag catalogue. Packet unit F is not engineering unit C. GOOD is not process healthy.",
    preferredChannel: "STRUCTURED",
    sources: [
      {
        source_path: "data/telemetry/tag_telemetry.jsonl",
        grain: "event_id",
        used_for: "Value, packet unit, quality, event_time, ingest_time",
      },
      {
        source_path: "data/reference/tags.csv",
        grain: "tag_id",
        used_for: "Engineering unit and 20–220 C limits for *_TEMP tags",
      },
    ],
    policyNote: "Dirty tags are not a control input. No convert-F-to-C verb; no PLC write from this screen.",
    memoryNote: "UNIT MISMATCH is on the packet vs tags.csv, not on a prior recommendation trace.",
  },
  "/process": {
    route: "/process",
    screenId: "process-graph",
    title: "Process Graph",
    summary: "Hop-capped undocumented paths (Q2). Blast radius unknown stays unknown.",
    preferredChannel: "GRAPH",
    graphQuery: "Q2",
    sources: [
      { source_path: "data/raw/network_edges.csv", grain: "edge", used_for: "Observed vs documented PATH edges" },
      { source_path: "data/raw/process_units.csv", grain: "unit_id", used_for: "Unit type and production criticality" },
      { source_path: "data/reference/tags.csv", grain: "tag_id", used_for: "Asset → unit join when present" },
    ],
    policyNote: "No regional isolate. isolate_endpoint remains tier 3 even if a path looks obvious.",
    memoryNote: "Graph slice is estate files, not the last recommend packet.",
  },
  "/risk": {
    route: "/risk",
    screenId: "contextual-risk",
    title: "Contextual Risk",
    summary:
      "network_reachable and process criticality outrank CVSS. The 9.8 with Reach NO is still in the same CSV as the 8.7 with Reach YES.",
    preferredChannel: "STRUCTURED",
    sources: [
      {
        source_path: "data/raw/vulnerabilities.csv",
        grain: "finding_id",
        used_for: "CVSS, network_reachable, compensating_control, status",
      },
      { source_path: "data/raw/assets.csv", grain: "asset_id", used_for: "Process criticality and plant join" },
      { source_path: "data/raw/recovery_readiness.csv", grain: "plant_id+component", used_for: "CURRENT ≠ RecoveryReady penalty" },
      { source_path: "data/raw/safety_barriers.csv", grain: "barrier_id", used_for: "Bypassed/degraded safety adjustment" },
    ],
    policyNote: "Ranking a finding is not isolate. CVSS-only sort is the warned anti-pattern, not a write.",
    memoryNote: "Reachable YES/NO is the vulnerabilities.csv column, not inferred from traces.",
  },
  "/safety": {
    route: "/safety",
    screenId: "safety-conflicts",
    title: "Safety vs Security",
    summary: "Barrier state and unauthorized bypass. UNKNOWN bypass is not YES. Isolation is not execute.",
    preferredChannel: "STRUCTURED",
    graphQuery: "Q3",
    sources: [
      {
        source_path: "data/raw/safety_barriers.csv",
        grain: "barrier_id",
        used_for: "State, bypass_authorized, proof_test_status",
      },
      {
        source_path: "data/raw/cyber_alerts.csv",
        grain: "alert_id",
        used_for: "HIGH/CRITICAL with process_context UNKNOWN",
      },
      { source_path: "data/raw/process_units.csv", grain: "unit_id", used_for: "Safe-state on the unit (displayed, not commanded)" },
      {
        source_path: "data/raw/process_dependencies.csv",
        grain: "upstream→downstream",
        used_for: "Safety vs material_flow dependencies in Q3",
      },
    ],
    policyNote: "bypass_interlock, modify_sis, write_plc_logic are tier 4 refuse. isolate_endpoint is tier 3 human authorize.",
    memoryNote: "Barrier BYPASSED is safety_barriers.csv, not a trace line.",
  },
  "/sessions": {
    route: "/sessions",
    screenId: "vendor-sessions",
    title: "Vendor Sessions",
    summary: "Who is already on the network. UNKNOWN identity is not approval.",
    preferredChannel: "STRUCTURED",
    sources: [
      {
        source_path: "data/raw/remote_access_sessions.csv",
        grain: "session_id",
        used_for: "Approved window, MFA, identity, asset",
      },
    ],
    policyNote: "change_remote_access is tier 3. This screen must not auto-kill VPN.",
    memoryNote: "Session rows are the CSV. Traces only appear after a recommend/audit flow.",
  },
  "/recovery": {
    route: "/recovery",
    screenId: "recovery-graph",
    title: "Recovery Graph",
    summary: "CURRENT backup is not RecoveryReady. Restore-test age, runbook, and dependency must all pass.",
    preferredChannel: "GRAPH",
    graphQuery: "Q4",
    sources: [
      {
        source_path: "data/raw/recovery_readiness.csv",
        grain: "plant_id+component",
        used_for: "Backup, restore-test days, runbook, dependency_verified, manual_fallback",
      },
    ],
    policyNote: "No live restore UI. RecoveryReady false is not a command to restore.",
    memoryNote: "Component blockers are recovery_readiness.csv, not prior drafts.",
  },
  "/incident": {
    route: "/incident",
    screenId: "incident-context",
    title: "Incident Context",
    summary: "Q5 cascade slice plus untrusted shift notes. Notes are not policy.",
    preferredChannel: "GRAPH",
    graphQuery: "Q5",
    sources: [
      { source_path: "data/raw/cyber_alerts.csv", grain: "alert_id", used_for: "Pinned alert on the cascade" },
      { source_path: "data/raw/assets.csv", grain: "asset_id", used_for: "Focal asset identity" },
      { source_path: "data/raw/safety_barriers.csv", grain: "barrier_id", used_for: "Barrier node on the timeline" },
      { source_path: "data/raw/remote_access_sessions.csv", grain: "session_id", used_for: "Vendor session node" },
      { source_path: "data/raw/process_units.csv", grain: "unit_id", used_for: "Safe-state displayed, not commanded" },
      { source_path: "scenarios/cascade_001.json", grain: "timeline", used_for: "CASCADE-001 marker times when that scenario is loaded" },
      {
        source_path: "data/shadow/shift_handover_email.txt",
        grain: "note",
        used_for: "Shift handover — UNTRUSTED, never authority",
        trust: "UNTRUSTED",
      },
    ],
    policyNote: "08:47 SOC isolate is still tier 3. execute=false on every path.",
    memoryNote: "The cascade graph is estate files + scenario markers. Traces are later drafts.",
  },
  "/recommend": {
    route: "/recommend",
    screenId: "recommendation-gate",
    title: "Recommendation Gate",
    summary: "Draft / abstain packet. Evidence rows must cite source_path. execute stays false.",
    preferredChannel: "POLICY",
    graphQuery: "Q5",
    sources: [
      {
        source_path: "src/ot_command/core/policy.py",
        grain: "ACTION_TIERS",
        used_for: "Tier of the requested action; unknown action defaults to refuse",
        trust: "policy",
      },
      { source_path: "data/raw/cyber_alerts.csv", grain: "alert_id", used_for: "Alert on the packet" },
      { source_path: "data/raw/assets.csv", grain: "asset_id", used_for: "Asset and plant join" },
      { source_path: "data/raw/safety_barriers.csv", grain: "barrier_id", used_for: "Barrier / safe-state evidence" },
      { source_path: "data/raw/process_units.csv", grain: "unit_id", used_for: "MIN_LOAD and unit context" },
      {
        source_path: "data/shadow/shift_handover_email.txt",
        grain: "note",
        used_for: "Cited as UNTRUSTED if present — not permission",
        trust: "UNTRUSTED",
      },
    ],
    policyNote: "observe/correlate/summarize are tier 0. isolate_endpoint is tier 3. PLC/SIS/interlock are tier 4 refuse.",
    memoryNote: "POST /recommend appends a trace with execute=false. That trace is MEMORY, not STRUCTURED estate truth.",
  },
  "/audit": {
    route: "/audit",
    screenId: "decision-trace",
    title: "Decision Trace",
    summary: "Append-only drafts. A log line is not plant state.",
    preferredChannel: "MEMORY",
    sources: [
      { source_path: "data/local/decision_traces.jsonl", grain: "decision_id", used_for: "Persisted recommend/audit traces" },
      { source_path: "contracts/decision_trace.yaml", grain: "schema", used_for: "Trace contract" },
    ],
    policyNote: "Traces that claim execute=true are SLO-OT violations. This UI does not execute.",
    memoryNote: "This screen is the MEMORY channel — traces, not vulnerabilities.csv or the historian.",
  },
  "/simulation": {
    route: "/simulation",
    screenId: "inject-simulator",
    title: "Inject / Simulation",
    summary: "Load named injects. Does not rewrite data/ or claim live OT.",
    preferredChannel: "STRUCTURED",
    sources: [
      {
        source_path: "apps/command_center/scenario_bindings.json",
        grain: "scenario_id",
        used_for: "Rail context: plant / asset / alert / expected badges",
      },
      { source_path: "scenarios/", grain: "scenario_id", used_for: "Inject and CASCADE timeline fixtures" },
      { source_path: "evals/harness.py", grain: "eval_id", used_for: "Harness cases (EVAL-002 …) when Run evals is used" },
    ],
    policyNote: "Twin preview and eval run stay read-only. proposed_action cannot become a PLC write.",
    memoryNote: "Eval results are harness output. They do not clean contradictions in data/.",
  },
  "/kpi": {
    route: "/kpi",
    screenId: "kpi-before-after",
    title: "KPI Before/After",
    summary: "Value is disagreement made visible, not isolate-speed. OPEN-006 baselines stay pending where unset.",
    preferredChannel: "STRUCTURED",
    sources: [
      ...DIAGNOSTIC_SOURCES,
      { source_path: "docs/05_kpis_baseline.md", grain: "kpi", used_for: "Baseline labels; numeric pass often BASELINE_PENDING" },
      { source_path: "data/local/decision_traces.jsonl", grain: "decision_id", used_for: "SLO-LAT / cost sample when traces exist" },
    ],
    policyNote: "KPIs do not add an execute control. SLO-OT must stay OK (no execute).",
    memoryNote: "Tile values are diagnostics over estate files. Traces only feed latency/cost samples.",
  },
  "/executive": {
    route: "/executive",
    screenId: "executive-brief",
    title: "Executive Brief",
    summary: "One-page posture. Unsafe recommendation avoided — not a prettier trend or isolate-speed.",
    preferredChannel: "STRUCTURED",
    sources: [
      { source_path: "data/reference/plants.csv", grain: "plant_id", used_for: "18-plant posture rollup" },
      { source_path: "data/raw/assets.csv", grain: "asset_id", used_for: "Inventory counts" },
      ...DIAGNOSTIC_SOURCES.filter((s) =>
        [
          "data/raw/safety_barriers.csv",
          "data/raw/recovery_readiness.csv",
          "data/telemetry/tag_telemetry.jsonl",
          "data/raw/remote_access_sessions.csv",
        ].includes(s.source_path),
      ),
    ],
    policyNote: "No execute controls on the brief. Authority remains policy.py ACTION_TIERS.",
    memoryNote: "Brief counts are estate diagnostics, not decision traces.",
  },
};

export function pageProvenanceFor(pathname: string): PageProvenance {
  const route = pathname.replace(/\/+$/, "") || "/";
  return PAGES[route] ?? PAGES["/"];
}
