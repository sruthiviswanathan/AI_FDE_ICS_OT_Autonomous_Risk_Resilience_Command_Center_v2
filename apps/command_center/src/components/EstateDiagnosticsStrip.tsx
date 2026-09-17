import { fmt, labelize } from "../utils/format";

export const ESTATE_DIAG_ANCHORS: { key: string; label: string; hint?: string }[] = [
  {
    key: "asset_state_conflicts",
    label: "State conflicts",
    hint: "Registered ACTIVE vs observed OFFLINE/UNSEEN",
  },
  {
    key: "safety_bypassed_or_degraded",
    label: "Barriers degraded",
    hint: "Safety barriers not ACTIVE",
  },
  {
    key: "undocumented_network_paths",
    label: "Live undocumented paths",
    hint: "documented=NO and observed_last_24h=YES",
  },
  {
    key: "recovery_stale_or_unknown_backup",
    label: "Stale / unknown backup",
    hint: "Recovery readiness — backup not CURRENT",
  },
  {
    key: "recovery_stale_or_missing_runbooks",
    label: "Stale / missing runbooks",
    hint: "Runbook status not CURRENT",
  },
  {
    key: "recovery_unverified_dependencies",
    label: "Unverified recovery deps",
    hint: "dependency_verified ≠ YES",
  },
];

const EXTRA_DIAG_LABELS: Record<string, { label: string; hint?: string }> = {
  alias_collisions: { label: "Alias collisions", hint: "Duplicate alias strings across assets" },
  duplicate_telemetry_packets: { label: "Duplicate telemetry", hint: "Identical tag/time/value packets" },
  telemetry_bad_or_uncertain: { label: "Bad / uncertain telemetry", hint: "Quality ≠ GOOD" },
  telemetry_unit_mismatches: { label: "Telemetry unit mismatches", hint: "TEMP tags with unit ≠ engineering_unit" },
  safety_proof_test_due: { label: "Safety proof test due", hint: "proof_test_status ≠ CURRENT" },
  maintenance_state_conflicts: { label: "Maintenance conflicts", hint: "CMMS closed vs field not returned" },
  unapproved_remote_sessions: { label: "Unapproved remote sessions", hint: "approved_window ≠ YES" },
  remote_sessions_without_confirmed_mfa: { label: "Sessions without MFA", hint: "mfa ≠ YES" },
  vendor_session_anomalies: { label: "Vendor session anomalies", hint: "Derived session anomaly index" },
};

function diagEntries(data: Record<string, unknown>, showAll: boolean) {
  const anchorKeys = new Set(ESTATE_DIAG_ANCHORS.map((a) => a.key));
  const primary = ESTATE_DIAG_ANCHORS.map(({ key, label, hint }) => ({
    key,
    label,
    hint,
    value: data[key],
  }));

  if (!showAll) return primary;

  const secondary = Object.entries(data)
    .filter(([key]) => !anchorKeys.has(key))
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([key, value]) => {
      const meta = EXTRA_DIAG_LABELS[key];
      return {
        key,
        label: meta?.label ?? labelize(key),
        hint: meta?.hint,
        value,
      };
    });

  return [...primary, ...secondary];
}

export function EstateDiagnosticsStrip({
  data,
  showAll = false,
}: {
  data?: Record<string, unknown> | null;
  showAll?: boolean;
}) {
  if (!data) return null;

  const entries = diagEntries(data, showAll);

  return (
    <div className="card estate-diagnostics-strip">
      <h3>Estate diagnostics</h3>
      <p className="ai-off-note">
        Workshop inventory joins — estate-wide counts from deterministic engines, not contextual risk rank.
      </p>
      <div className="estate-diagnostics-grid">
        {entries.map(({ key, label, hint, value }) => (
          <div key={key} className="estate-diag-anchor" title={hint}>
            <span className="estate-diag-value">{fmt(value)}</span>
            <span className="estate-diag-label">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
