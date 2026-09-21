import { Fragment, type ReactNode } from "react";

interface Col<T> {
  key: string;
  header: string;
  render: (row: T) => ReactNode;
  className?: string;
  sortable?: boolean;
}

export function DataTable<T extends Record<string, unknown>>({
  rows,
  cols,
  rowKey,
  highlight,
  expandedKey,
  renderExpanded,
  sortKey,
  sortDir,
  onSort,
}: {
  rows: T[];
  cols: Col<T>[];
  rowKey: (row: T) => string;
  highlight?: (row: T) => boolean;
  expandedKey?: string | null;
  renderExpanded?: (row: T) => ReactNode;
  sortKey?: string;
  sortDir?: "asc" | "desc";
  onSort?: (key: string) => void;
}) {
  if (!rows.length) return null;
  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {cols.map((c) => {
              const active = sortKey === c.key;
              const ariaSort =
                !c.sortable || !onSort ? undefined : active ? (sortDir === "desc" ? "descending" : "ascending") : "none";
              return (
                <th
                  key={c.key}
                  className={c.sortable && onSort ? "sortable" : undefined}
                  aria-sort={ariaSort}
                >
                  {c.sortable && onSort ? (
                    <button type="button" className="th-sort" onClick={() => onSort(c.key)}>
                      {c.header}
                      <span className="th-sort-indicator">{active ? (sortDir === "desc" ? " ▼" : " ▲") : ""}</span>
                    </button>
                  ) : (
                    c.header
                  )}
                </th>
              );
            })}
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
