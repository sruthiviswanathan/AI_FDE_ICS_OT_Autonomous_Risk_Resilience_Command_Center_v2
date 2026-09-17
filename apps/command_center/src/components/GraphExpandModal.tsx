import { useEffect, type ReactNode } from "react";
import { createPortal } from "react-dom";

export function GraphExpandModal({
  open,
  onClose,
  title,
  children,
}: {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
}) {
  useEffect(() => {
    if (!open) return;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = prevOverflow;
    };
  }, [open, onClose]);

  if (!open) return null;

  return createPortal(
    <div className="graph-modal-backdrop" onClick={onClose} role="presentation">
      <div
        className="graph-modal-panel"
        role="dialog"
        aria-modal="true"
        aria-label={title}
        onClick={(event) => event.stopPropagation()}
      >
        <header className="graph-modal-header">
          <h4 className="graph-modal-title">{title}</h4>
          <button type="button" className="graph-modal-close" onClick={onClose} aria-label="Close graph">
            Close
          </button>
        </header>
        <div className="graph-modal-body">{children}</div>
      </div>
    </div>,
    document.body,
  );
}
