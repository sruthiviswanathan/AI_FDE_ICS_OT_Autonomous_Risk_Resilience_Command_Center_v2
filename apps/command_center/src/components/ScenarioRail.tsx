import { Link } from "react-router-dom";
import { useApp } from "../context/AppContext";
import type { ScenarioBinding } from "../scenarios/types";

function Badge({ badge }: { badge: ScenarioBinding["badges"][0] }) {
  const cls = badge.tone === "neutral" ? "badge" : `badge ${badge.tone === "green" ? "green" : badge.tone}`;
  return <span className={cls}>{badge.label}</span>;
}

export function ScenarioRail({ scenarios }: { scenarios: ScenarioBinding[] }) {
  const { scenario, applyScenario, activeBinding } = useApp();

  return (
    <div className="scenario-rail">
      <div className="nav-group">Scenario rail</div>
      {scenarios.map((s) => (
        <button
          key={s.id}
          type="button"
          className={`scenario-btn${scenario === s.id ? " active" : ""}`}
          onClick={() => applyScenario(s)}
          title={s.title}
        >
          {s.label}
          {s.eval_ids.length > 0 && <span className="eval-ids">{s.eval_ids.join(", ")}</span>}
        </button>
      ))}
      {activeBinding && (
        <div className="scenario-detail">
          <div className="scenario-title">{activeBinding.title}</div>
          <div className="badge-row">
            {activeBinding.badges.map((b) => (
              <Badge key={b.id} badge={b} />
            ))}
          </div>
          {activeBinding.show_conflicts && (
            <p className="ai-off-note">Conflicts visible — not hidden for demo.</p>
          )}
          <div className="route-chips">
            {activeBinding.primary_routes.map((r) => (
              <Link key={r} to={r}>
                {r}
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export function ScenarioBadgeStrip() {
  const { activeBinding } = useApp();
  if (!activeBinding) return null;
  return (
    <div className="context-badges">
      {activeBinding.badges.map((b) => (
        <Badge key={b.id} badge={b} />
      ))}
    </div>
  );
}
