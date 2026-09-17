import type { ReactNode } from "react";

export function LoadingBlock({
  label = "Loading estate data…",
  variant = "default",
}: {
  label?: string;
  variant?: "default" | "graph" | "inline" | "compact";
}) {
  return (
    <div
      className={`state-block skeleton loading-block loading-${variant}`}
      role="status"
      aria-live="polite"
      aria-busy="true"
    >
      <span className="loading-spinner" aria-hidden="true" />
      <span className="loading-label">{label}</span>
    </div>
  );
}

export function GraphAsyncContent({
  loading,
  error,
  label = "Loading graph…",
  children,
}: {
  loading: boolean;
  error?: string | null;
  label?: string;
  children: ReactNode;
}) {
  if (loading) return <LoadingBlock variant="graph" label={label} />;
  if (error) return <ErrorBlock message={error} />;
  return <>{children}</>;
}

export function ErrorBlock({ message }: { message: string }) {
  return <div className="state-block error">Error: {message}</div>;
}

export function EmptyBlock({ message }: { message: string }) {
  return <div className="state-block empty">{message}</div>;
}

export function FreshnessBadge({ freshness }: { freshness?: string | null }) {
  if (!freshness) return null;
  const tone = freshness.includes("static") || freshness.includes("PENDING") ? "amber" : "green";
  return <span className={`badge ${tone}`}>{freshness}</span>;
}

export function UncertaintyBadge({ text = "UNKNOWN" }: { text?: string }) {
  return <span className="badge amber">{text}</span>;
}

export function UntrustedBadge() {
  return <span className="badge red">UNTRUSTED</span>;
}

export function SafetyBadge() {
  return <span className="badge orange">safety degraded</span>;
}
