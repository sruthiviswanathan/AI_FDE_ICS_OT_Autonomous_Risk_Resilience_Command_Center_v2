import { Fragment, type ReactNode } from "react";

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
  expandedKey,
  renderExpanded,
}: {
  rows: T[];
  cols: Col<T>[];
  rowKey: (row: T) => string;
  highlight?: (row: T) => boolean;
  expandedKey?: string | null;
  renderExpanded?: (row: T) => ReactNode;
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
          {rows.map((row) => {
            const key = rowKey(row);
            const expanded = expandedKey === key;
            return (
              <Fragment key={key}>
                <tr className={highlight?.(row) || expanded ? "row-highlight" : undefined}>
                  {cols.map((c) => (
                    <td key={c.key} className={c.className}>
                      {c.render(row)}
                    </td>
                  ))}
                </tr>
                {expanded && renderExpanded && (
                  <tr className="row-expanded">
                    <td colSpan={cols.length}>{renderExpanded(row)}</td>
                  </tr>
                )}
              </Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
