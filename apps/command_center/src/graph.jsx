export function graphLayout(g) {
  const nodes = (g && g.nodes) || [];
  const edges = (g && g.edges) || [];
  if (!nodes.length) return null;
  const units = nodes.filter((n) => n.type === "process_unit");
  const bars = nodes.filter((n) => n.type === "safety_barrier");
  const byHop = {};
  units.forEach((n) => {
    const h = n.hop || 0;
    (byHop[h] = byHop[h] || []).push(n);
  });
  const pos = {};
  const colW = 180;
  const rowH = 64;
  const pad = 28;
  let maxY = 80;
  let maxX = 200;
  Object.keys(byHop).map(Number).sort((a, b) => a - b).forEach((h) => {
    (byHop[h] || []).forEach((n, i) => {
      const x = pad + h * colW;
      const y = pad + i * rowH;
      pos[n.id] = { x, y, n };
      maxY = Math.max(maxY, y + 50);
      maxX = Math.max(maxX, x + 150);
    });
  });
  bars.forEach((b, i) => {
    const parent = pos[b.unit_id];
    const x = parent ? parent.x + 40 : pad + (i % 4) * colW;
    const y = parent ? parent.y + 36 : pad + i * rowH;
    pos[b.id] = { x, y, n: b };
    maxY = Math.max(maxY, y + 40);
    maxX = Math.max(maxX, x + 140);
  });
  return { pos, edges, maxX, maxY, hops: g.hops, hop_cap: g.hop_cap, imputed: g.imputed_tag_to_unit };
}

export function graphSvg(g) {
  return <GraphSvg g={g} />;
}

export function GraphSvg({ g }) {
  const layout = graphLayout(g);
  if (!layout) {
    return <div className="empty">{(g && g.note) || "No slice. Missing tag→unit stays missing — not imputed."}</div>;
  }
  const { pos, edges, maxX, maxY, hops, hop_cap, imputed } = layout;
  return (
    <>
      <svg xmlns="http://www.w3.org/2000/svg" width={maxX + 40} height={maxY + 20}>
        {edges.map((e, i) => {
          const a = pos[e.from];
          const b = pos[e.to];
          if (!a || !b) return null;
          const dashed = String(e.documented).toUpperCase() === "NO";
          return (
            <line
              key={i}
              x1={a.x + 60}
              y1={a.y + 14}
              x2={b.x + 60}
              y2={b.y + 14}
              stroke="#2a3844"
              strokeDasharray={dashed ? "4 3" : undefined}
            />
          );
        })}
        {Object.keys(pos).map((key) => {
          const { x, y, n } = pos[key];
          const min = n.safe_state === "MIN_LOAD";
          const bypass = n.state && n.state !== "ACTIVE";
          const stroke = min || bypass ? "#d4564e" : (n.type === "safety_barrier" ? "#e6a23c" : "#3ec6c9");
          const sub = n.safe_state || n.state || n.type;
          const w = n.type === "safety_barrier" ? 120 : 140;
          const h = n.type === "safety_barrier" ? 28 : 32;
          return (
            <g key={key}>
              <rect x={x} y={y} width={w} height={h} rx="3" fill="#161e26" stroke={stroke} />
              <text x={x + 6} y={y + 12} fill="#d7e0e8" fontSize="9" fontFamily="Consolas,monospace">{n.id}</text>
              <text x={x + 6} y={y + 23} fill="#8a9aaa" fontSize="8">{sub}</text>
            </g>
          );
        })}
      </svg>
      <p className="muted">hop={String(hops)} · hop_cap={String(hop_cap)} · dashed = undocumented · red = MIN_LOAD or barrier not ACTIVE · imputed={String(imputed)}</p>
    </>
  );
}

export function TimelineView({ cascade, tel }) {
  const rows = (cascade && cascade.timeline) || [];
  return (
    <>
      <div className="card">
        <h3>Incident clock (analogue)</h3>
        {cascade && cascade.note ? <p className="muted">{cascade.note}</p> : null}
        {!rows.length ? <div className="empty">No cascade analogue on this case. Pick cascade_001 or ALT-002783.</div> : (
          <div className="tl">
            {rows.map((r, i) => {
              const ev = r.event || "";
              let cls = "tl-row";
              if (/SOC recommends/i.test(ev)) cls += " dissent-soc";
              if (/Process engineer/i.test(ev)) cls += " dissent-pe";
              return (
                <div className={cls} key={i}>
                  <div className="mono">{r.time || ""}</div>
                  <div>{ev}</div>
                </div>
              );
            })}
          </div>
        )}
      </div>
      {tel && tel.events ? (
        <div className="card">
          <h3>Historian clock (event_time order)</h3>
          <p className="muted">ingest is freshness. Inversions stay visible. GOOD is not process-healthy.</p>
        </div>
      ) : null}
    </>
  );
}
