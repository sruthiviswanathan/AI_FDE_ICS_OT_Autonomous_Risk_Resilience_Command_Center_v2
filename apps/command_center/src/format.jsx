import { DIAG_LABELS, FALSE_IS_SAFE, LABELS, SLO_HELP, recLabel, hitlState } from "./constants.js";

export function humanize(key) {
  return LABELS[key] || String(key).replace(/_/g, " ");
}

function isEmpty(v) {
  return v === null || v === undefined || v === "";
}

export function valClass(key, v) {
  if (isEmpty(v) || v === "UNKNOWN") return "unk";
  if (key === "unknown_is_not_approval") return v ? "ok" : "bad";
  if (FALSE_IS_SAFE[key] && v === false) return "ok";
  if (FALSE_IS_SAFE[key] && v === true) return "bad";
  if (key === "winner" && (v === null || v === "null")) return "warn";
  if (key === "recovery_ready" && v === false) return "warn";
  if (key === "status" && String(v) === "hold") return "warn";
  if (key === "recommendation" && String(v) === "ABSTAIN") return "warn";
  return "";
}

export function Scalar({ k, v }) {
  let text;
  if (isEmpty(v)) text = "UNKNOWN";
  else if (typeof v === "boolean") text = v ? "yes" : "no";
  else text = String(v);
  return <span className={"val " + valClass(k, v)}>{text}</span>;
}

export function Chips({ items, kind }) {
  if (!items || !items.length) return <Scalar k="" v={null} />;
  return (
    <span className="chips">
      {items.map((x, i) => (
        <span key={i} className={"pill " + (kind || "")}>{String(x)}</span>
      ))}
    </span>
  );
}

export function Table({ headers, rows }) {
  if (!rows || !rows.length) return <div className="empty">UNKNOWN / empty — not a healthy zero.</div>;
  return (
    <div className="card">
      <table>
        <thead>
          <tr>{headers.map((h) => <th key={h}>{h}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i}>{r.map((c, j) => <td key={j} className="mono">{c == null ? "UNKNOWN" : String(c)}</td>)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function ObjectTable({ arr, cap }) {
  const slice = (arr || []).slice(0, cap || 16);
  if (!slice.length) return <div className="empty">UNKNOWN / empty — not a healthy zero.</div>;
  const keys = [];
  slice.forEach((o) => {
    Object.keys(o || {}).forEach((k) => {
      const val = o[k];
      if (keys.indexOf(k) < 0 && (val == null || typeof val !== "object")) keys.push(k);
    });
  });
  const rows = slice.map((o) => keys.map((k) => (isEmpty(o[k]) ? "UNKNOWN" : (typeof o[k] === "boolean" ? (o[k] ? "yes" : "no") : String(o[k])))));
  return (
    <>
      <Table headers={keys.map(humanize)} rows={rows} />
      {arr.length > slice.length ? (
        <p className="muted">showing {slice.length} of {arr.length} — remainder remain queryable, not cleaned</p>
      ) : null}
    </>
  );
}

export function Facts({ obj }) {
  return (
    <div className="facts">
      {Object.entries(obj || {}).map(([k, v]) => {
        if (v && typeof v === "object") return null;
        return (
          <div className="fact" key={k}>
            <span className="fact-k">{humanize(k)}</span>
            <span className="fact-v"><Scalar k={k} v={v} /></span>
          </div>
        );
      })}
    </div>
  );
}

function record(obj, title) {
  return <Record obj={obj} title={title} />;
}

export function Record({ obj, title }) {
  if (obj == null) return <div className="empty">UNKNOWN</div>;
  const nested = [];
  Object.entries(obj).forEach(([k, v]) => {
    if (Array.isArray(v)) {
      nested.push(
        <div key={k}>
          <h3>{humanize(k)}</h3>
          {!v.length ? <Scalar k={k} v={null} /> : typeof v[0] === "object" ? <ObjectTable arr={v} /> : <Chips items={v} kind={k === "forbidden_execute_tools" || k === "counter_metrics" ? "bad" : ""} />}
        </div>
      );
    } else if (v && typeof v === "object") {
      nested.push(
        <div key={k}>
          <h3>{humanize(k)}</h3>
          <Facts obj={v} />
          {Object.entries(v).map(([k2, v2]) => {
            if (Array.isArray(v2) && v2.length && typeof v2[0] === "object") {
              return <div key={k2}><h3>{humanize(k2)}</h3><ObjectTable arr={v2} /></div>;
            }
            if (Array.isArray(v2)) return <div key={k2}><h3>{humanize(k2)}</h3><Chips items={v2} kind="" /></div>;
            if (v2 && typeof v2 === "object") return <div key={k2}><h3>{humanize(k2)}</h3><Facts obj={v2} /></div>;
            return null;
          })}
        </div>
      );
    }
  });
  return (
    <div className="card">
      {title ? <h3>{title}</h3> : null}
      <Facts obj={obj} />
      {nested}
    </div>
  );
}

export function sloCard(slo) {
  return <SloCard slo={slo} />;
}

export function SloCard({ slo }) {
  const slos = slo.slos || {};
  const rows = Object.entries(slos).map(([id, row]) => {
    const target = row.target != null ? row.target : (row.target_p95_ms != null ? "p95 " + row.target_p95_ms + " ms" : "UNKNOWN");
    const extra = [];
    if (row.observed_execute_attempts != null) extra.push("observed executes " + row.observed_execute_attempts);
    if (row.error_budget != null) extra.push("error budget " + row.error_budget);
    if (row.joins_must_not_drop) extra.push("must not drop joins");
    if (row.plant_mtt) extra.push("plant MTT " + row.plant_mtt);
    if (row.harness) extra.push(row.harness);
    return [id, SLO_HELP[id] || humanize(id), String(target), extra.join("; ") || "—", row.status || "UNKNOWN"];
  });
  return (
    <>
      <div className="card">
        <h3>Operating bounds</h3>
        <div className="statbar">
          <div className="stat"><span>Live plant</span><b className={"val " + valClass("live_ot", slo.live_ot)}>{slo.live_ot ? "yes" : "no"}</b></div>
          <div className="stat"><span>Decision traces</span><b>{String(slo.trace_count)}</b></div>
          <div className="stat"><span>SLO-OT</span><b className="val warn">{(slos["SLO-OT"] && slos["SLO-OT"].status) || "hold"}</b></div>
        </div>
        <p className="muted">Hold means the execute budget is unused. This is not a plant health score.</p>
      </div>
      <Table headers={["SLO", "what it requires", "target", "notes", "status"]} rows={rows} />
      <div className="card">
        <h3>Actions this software cannot run</h3>
        <Chips items={slo.forbidden_execute_tools || []} kind="bad" />
      </div>
    </>
  );
}

export function Busy() {
  return <div className="busy">Loading evidence — not a health score.</div>;
}

export function Empty({ children }) {
  return <div className="empty">{children}</div>;
}

export function hitlQueue(traces, pkt) {
  return <HitlQueue traces={traces} pkt={pkt} />;
}

export function HitlQueue({ traces, pkt }) {
  const items = (traces && traces.items) || [];
  return (
    <div className="card">
      <h3>HITL queue (roles, not named people)</h3>
      <p className="answer">AwaitAuthorization cannot close without a named human (OPEN-001) and still must not execute. There is no Close-as-isolate control.</p>
      {pkt ? (
        <div className="hitl">
          <div className="card">
            <strong>{recLabel(pkt)}</strong>
            <Facts obj={{
              hitl_state: hitlState({ recommendation: recLabel(pkt), executed: pkt.executed }),
              executed: pkt.executed,
              required_role: (pkt.human_packet && pkt.human_packet.required_authority) || pkt.required_role,
              named_authorizer: "OPEN-001",
            }} />
          </div>
        </div>
      ) : null}
      {!items.length && !pkt ? <Empty>No drafts this session. Use Draft packet.</Empty> : null}
      {items.length ? (
        <Table
          headers={["decision_id", "recommendation", "executed", "HITL state", "tokens"]}
          rows={items.map((x) => [x.decision_id, x.recommendation, x.executed, hitlState(x), x.tokens])}
        />
      ) : null}
    </div>
  );
}

export function diagRows(diag) {
  return Object.entries(diag || {}).map(([k, v]) => [DIAG_LABELS[k] || humanize(k), v, k]);
}

export { record };
