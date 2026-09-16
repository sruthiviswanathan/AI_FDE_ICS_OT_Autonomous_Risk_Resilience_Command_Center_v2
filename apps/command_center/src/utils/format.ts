export function labelize(key: string): string {
  return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtObject(obj: Record<string, unknown>, fallback: string): string {
  const parts = Object.entries(obj)
    .filter(([, v]) => v !== null && v !== undefined && v !== "")
    .map(([k, v]) => {
      const inner = fmt(v, "");
      return inner ? `${labelize(k)}: ${inner}` : "";
    })
    .filter(Boolean);
  return parts.length ? parts.join(" · ") : fallback;
}

export function fmt(value: unknown, fallback = "—"): string {
  if (value === null || value === undefined || value === "") return fallback;
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (typeof value === "number" || typeof value === "bigint") return String(value);
  if (typeof value === "string") return value;
  if (Array.isArray(value)) {
    if (!value.length) return fallback;
    return value.map((item) => fmt(item, "")).filter(Boolean).join(", ") || fallback;
  }
  if (typeof value === "object") {
    const obj = value as Record<string, unknown>;
    const preferred = ["label", "name", "text", "note", "status", "value", "id"];
    for (const key of preferred) {
      const preferredValue = obj[key];
      if (
        preferredValue !== undefined &&
        preferredValue !== null &&
        preferredValue !== "" &&
        typeof preferredValue !== "object"
      ) {
        return fmt(preferredValue, fallback);
      }
    }
    return fmtObject(obj, fallback);
  }
  return String(value);
}
