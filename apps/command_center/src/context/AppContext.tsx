import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import {
  clampAiMode,
  loadStoredAiMode,
  loadStoredPersona,
  persistPersona,
  persistSearch,
  PERSONA_VIEWS,
  type AiMode,
  type PersonaId,
} from "../personas/registry";
import type { ScenarioBinding } from "../scenarios/types";

export type ScenarioId =
  | "nominal"
  | "cascade_001"
  | "inject_01"
  | "inject_02"
  | "inject_03"
  | "inject_04"
  | "inject_05"
  | "inject_06"
  | "ai_outage";

export type { AiMode };

export interface ProvenancePin {
  source_path: string;
  record_id?: string;
  confidence?: number;
  freshness?: string;
  label?: string;
}

interface AppState {
  plantId: string;
  assetId: string;
  alertId: string;
  scenario: ScenarioId;
  personaId: PersonaId;
  aiMode: AiMode;
  aiControlDisabled: boolean;
  activeBinding: ScenarioBinding | null;
  provenanceOpen: boolean;
  provenancePin: ProvenancePin | null;
  lastPacket: Record<string, unknown> | null;
  lookupKey: number;
  setPlantId: (v: string) => void;
  setAssetId: (v: string) => void;
  setAlertId: (v: string) => void;
  setScenario: (v: ScenarioId) => void;
  setPersonaId: (v: PersonaId) => void;
  setAiMode: (v: AiMode) => void;
  applyScenario: (binding: ScenarioBinding) => void;
  triggerLookup: () => void;
  setProvenanceOpen: (v: boolean) => void;
  pinProvenance: (p: ProvenancePin) => void;
  setLastPacket: (p: Record<string, unknown> | null) => void;
}

const AppContext = createContext<AppState | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const initialPersona = loadStoredPersona();
  const [plantId, setPlantId] = useState("PLT-01");
  const [assetId, setAssetId] = useState("OT-00001");
  const [alertId, setAlertId] = useState("ALT-001744");
  const [scenario, setScenario] = useState<ScenarioId>("nominal");
  const [personaId, setPersonaIdState] = useState<PersonaId>(initialPersona);
  const [aiMode, setAiModeState] = useState<AiMode>(() =>
    clampAiMode(loadStoredAiMode(), initialPersona, "nominal"),
  );
  const [activeBinding, setActiveBinding] = useState<ScenarioBinding | null>(null);
  const [provenanceOpen, setProvenanceOpen] = useState(PERSONA_VIEWS[initialPersona].drawerDefaultOpen);
  const [provenancePin, setProvenancePin] = useState<ProvenancePin | null>(null);
  const [lastPacket, setLastPacket] = useState<Record<string, unknown> | null>(null);
  const [lookupKey, setLookupKey] = useState(0);

  useEffect(() => {
    persistSearch({ ai: aiMode });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const triggerLookup = useCallback(() => setLookupKey((k) => k + 1), []);

  const setPersonaId = useCallback((id: PersonaId) => {
    setPersonaIdState(id);
    persistPersona(id);
    setProvenanceOpen(PERSONA_VIEWS[id].drawerDefaultOpen);
    setAiModeState((prev) => {
      const next = clampAiMode(prev, id, scenario);
      persistSearch({ ai: next });
      return next;
    });
  }, [scenario]);

  const setAiMode = useCallback(
    (mode: AiMode) => {
      const next = clampAiMode(mode, personaId, scenario);
      setAiModeState(next);
      persistSearch({ ai: next });
    },
    [personaId, scenario],
  );

  const applyScenario = useCallback(
    (binding: ScenarioBinding) => {
      const nextScenario = binding.id as ScenarioId;
      setScenario(nextScenario);
      setActiveBinding(binding);
      if (binding.context.plant_id) setPlantId(binding.context.plant_id);
      if (binding.context.asset_id) setAssetId(binding.context.asset_id);
      setAlertId(binding.context.alert_id || "");
      setLookupKey((k) => k + 1);
      const nextAi = clampAiMode(aiMode, personaId, nextScenario);
      setAiModeState(nextAi);
      persistSearch({ scenario: binding.id, ai: nextAi });
    },
    [aiMode, personaId],
  );

  const value = useMemo(
    () => ({
      plantId,
      assetId,
      alertId,
      scenario,
      personaId,
      aiMode,
      aiControlDisabled: scenario === "ai_outage",
      activeBinding,
      provenanceOpen,
      provenancePin,
      lastPacket,
      lookupKey,
      setPlantId,
      setAssetId,
      setAlertId,
      setScenario,
      setPersonaId,
      setAiMode,
      applyScenario,
      triggerLookup,
      setProvenanceOpen,
      pinProvenance: (p: ProvenancePin) => {
        setProvenancePin(p);
        setProvenanceOpen(true);
      },
      setLastPacket,
    }),
    [
      plantId,
      assetId,
      alertId,
      scenario,
      personaId,
      aiMode,
      activeBinding,
      provenanceOpen,
      provenancePin,
      lastPacket,
      lookupKey,
      applyScenario,
      triggerLookup,
      setPersonaId,
      setAiMode,
    ],
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp outside provider");
  return ctx;
}
