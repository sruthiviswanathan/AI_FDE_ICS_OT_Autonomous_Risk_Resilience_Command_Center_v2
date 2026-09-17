import { useCallback, useRef, useState, type ReactNode, type WheelEvent } from "react";

export function PanZoomSvg({
  width,
  height,
  enabled,
  children,
  className,
  ariaLabel,
  preserveAspectRatio = "xMidYMid meet",
}: {
  width: number;
  height: number;
  enabled: boolean;
  children: ReactNode;
  className?: string;
  ariaLabel?: string;
  preserveAspectRatio?: string;
}) {
  const [view, setView] = useState({ x: 0, y: 0, scale: 1 });
  const dragRef = useRef<{ x: number; y: number; vx: number; vy: number; active: boolean } | null>(null);

  const isInteractiveTarget = (target: EventTarget | null) => {
    if (!(target instanceof Element)) return false;
    return Boolean(target.closest("[data-panzoom-interactive]"));
  };

  const onWheel = useCallback(
    (event: WheelEvent<SVGSVGElement>) => {
      if (!enabled) return;
      event.preventDefault();
      const delta = event.deltaY > 0 ? 0.9 : 1.1;
      setView((prev) => ({
        ...prev,
        scale: Math.min(3, Math.max(0.5, prev.scale * delta)),
      }));
    },
    [enabled],
  );

  const onPointerDown = useCallback(
    (event: React.PointerEvent<SVGSVGElement>) => {
      if (!enabled || isInteractiveTarget(event.target)) return;
      dragRef.current = { x: event.clientX, y: event.clientY, vx: view.x, vy: view.y, active: false };
    },
    [enabled, view.x, view.y],
  );

  const onPointerMove = useCallback((event: React.PointerEvent<SVGSVGElement>) => {
    if (!dragRef.current) return;
    const dx = event.clientX - dragRef.current.x;
    const dy = event.clientY - dragRef.current.y;
    if (!dragRef.current.active && Math.hypot(dx, dy) < 5) return;
    if (!dragRef.current.active) {
      dragRef.current.active = true;
      event.currentTarget.setPointerCapture(event.pointerId);
    }
    setView((prev) => ({
      ...prev,
      x: dragRef.current!.vx + dx,
      y: dragRef.current!.vy + dy,
    }));
  }, []);

  const onPointerUp = useCallback((event: React.PointerEvent<SVGSVGElement>) => {
    if (dragRef.current?.active) {
      try {
        event.currentTarget.releasePointerCapture(event.pointerId);
      } catch {
        /* already released */
      }
    }
    dragRef.current = null;
  }, []);

  const viewBox = enabled
    ? `${-view.x / view.scale} ${-view.y / view.scale} ${width / view.scale} ${height / view.scale}`
    : `0 0 ${width} ${height}`;

  return (
    <svg
      className={className}
      viewBox={viewBox}
      preserveAspectRatio={preserveAspectRatio}
      role="img"
      aria-label={ariaLabel}
      onWheel={onWheel}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerLeave={onPointerUp}
      style={enabled ? { cursor: "grab", touchAction: "none" } : undefined}
    >
      {children}
    </svg>
  );
}
