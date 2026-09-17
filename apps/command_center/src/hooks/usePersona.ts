import { useMemo } from "react";
import { useApp } from "../context/AppContext";
import {
  filterNavForPersona,
  isRouteAllowed,
  PERSONA_VIEWS,
  type PersonaId,
  type PersonaView,
} from "../personas/registry";

export function usePersona() {
  const ctx = useApp();
  const view: PersonaView = PERSONA_VIEWS[ctx.personaId];

  return useMemo(
    () => ({
      personaId: ctx.personaId,
      view,
      nav: filterNavForPersona(ctx.personaId),
      setPersona: ctx.setPersonaId,
      isFiltered: ctx.personaId !== "full" && ctx.personaId !== "fde",
      isRouteAllowed: (pathname: string) =>
        isRouteAllowed(pathname, ctx.personaId, ctx.alertId, ctx.scenario),
    }),
    [ctx.personaId, ctx.setPersonaId, ctx.alertId, ctx.scenario, view],
  );
}

export type { PersonaId, PersonaView };
