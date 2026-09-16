import { fmt } from "../utils/format";

interface Factor {
  value?: unknown;
  points?: number;
  note?: string;
  adjustment?: number;
  evidence?: unknown[];
  status?: string;
  components?: string[];
}

export function FactorBreakdown({ breakdown }: { breakdown: Record<string, Factor | number | unknown> }) {
  const score = breakdown.contextual_score;
  const factors = Object.entries(breakdown).filter(([k]) => k !== "contextual_score");

  return (
    <div>
      {score !== undefined && (
        <div className="card score-card">
          <h3>Contextual score</h3>
          <div className="metric">{fmt(score)}</div>
          <p className="ai-off-note">CVSS is input only — not the sort key.</p>
        </div>
      )}
      <div className="card-grid">
        {factors.map(([name, raw]) => {
          const f = (raw || {}) as Factor;
          return (
            <div key={name} className="card factor-card">
              <h3>{name.replace(/_/g, " ")}</h3>
              <div className="metric">{fmt(f.points ?? f.adjustment ?? "—")} pts</div>
              {f.value !== undefined && <p>Value: {fmt(f.value)}</p>}
              {f.status && <p>Status: {fmt(f.status)}</p>}
              {f.components && f.components.length > 0 && (
                <p>Components: {f.components.join(", ")}</p>
              )}
              {f.note && <p className="ai-off-note">{f.note}</p>}
            </div>
          );
        })}
      </div>
    </div>
  );
}
