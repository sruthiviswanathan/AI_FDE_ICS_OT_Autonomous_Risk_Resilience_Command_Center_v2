import type { ReactNode } from "react";

interface Col<T> {
  key: string;
  header: string;
  render: (row: T) => ReactNode;
  className?: string;
}

export function DataTable<T extends Record<string, unknown>>({
  rows,
  cols,
  rowKey,
  highlight,
}: {
  rows: T[];
  cols: Col<T>[];
  rowKey: (row: T) => string;
  highlight?: (row: T) => boolean;
}) {
  if (!rows.length) return null;
  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {cols.map((c) => (
              <th key={c.key}>{c.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={rowKey(row)} className={highlight?.(row) ? "row-highlight" : undefined}>
              {cols.map((c) => (
                <td key={c.key} className={c.className}>
                  {c.render(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
