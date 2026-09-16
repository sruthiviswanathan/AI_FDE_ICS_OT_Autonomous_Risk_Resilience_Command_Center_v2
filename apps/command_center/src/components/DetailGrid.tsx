import { fmt, labelize } from "../utils/format";

export function DetailGrid({
  items,
  columns = 2,
}: {
  items: { label: string; value: unknown; hint?: string }[];
  columns?: 2 | 3 | 4;
}) {
  return (
    <div className={`detail-grid cols-${columns}`}>
      {items.map((item) => (
        <div key={item.label} className="detail-item">
          <div className="detail-label">{item.label}</div>
          <div className="detail-value">{fmt(item.value)}</div>
          {item.hint && <div className="detail-hint">{item.hint}</div>}
        </div>
      ))}
    </div>
  );
}

export function ObjectCard({
  title,
  data,
  keys,
  className,
}: {
  title: string;
  data: Record<string, unknown>;
  keys?: string[];
  className?: string;
}) {
  const entries = (keys || Object.keys(data)).map((k) => ({
    label: labelize(k),
    value: data[k],
  }));
  return (
    <div className={`card ${className || ""}`.trim()}>
      <h3>{title}</h3>
      <DetailGrid items={entries} columns={2} />
    </div>
  );
}
