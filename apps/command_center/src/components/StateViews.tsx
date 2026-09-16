export function LoadingBlock({ label = "Loading estate data…" }: { label?: string }) {
  return <div className="state-block skeleton">{label}</div>;
}

export function ErrorBlock({ message }: { message: string }) {
  return <div className="state-block error">Error: {message}</div>;
}

export function EmptyBlock({ message }: { message: string }) {
  return <div className="state-block empty">{message}</div>;
}

export function StaleBadge() {
  return <span className="badge amber">workshop-static</span>;
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
