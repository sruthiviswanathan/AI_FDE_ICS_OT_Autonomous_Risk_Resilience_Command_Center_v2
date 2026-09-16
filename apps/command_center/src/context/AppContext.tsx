import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from "react";
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
  activeBinding: ScenarioBinding | null;
  aiEnabled: boolean;
  provenanceOpen: boolean;
  provenancePin: ProvenancePin | null;
  lastPacket: Record<string, unknown> | null;
  lookupKey: number;
  setPlantId: (v: string) => void;
  setAssetId: (v: string) => void;
  setAlertId: (v: string) => void;
  setScenario: (v: ScenarioId) => void;
  applyScenario: (binding: ScenarioBinding) => void;
  triggerLookup: () => void;
  setAiEnabled: (v: boolean) => void;
  setProvenanceOpen: (v: boolean) => void;
  pinProvenance: (p: ProvenancePin) => void;
  setLastPacket: (p: Record<string, unknown> | null) => void;
}

const AppContext = createContext<AppState | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [plantId, setPlantId] = useState("PLT-10");
  const [assetId, setAssetId] = useState("OT-01016");
  const [alertId, setAlertId] = useState("ALT-002783");
  const [scenario, setScenario] = useState<ScenarioId>("nominal");
  const [activeBinding, setActiveBinding] = useState<ScenarioBinding | null>(null);
  const [aiEnabled, setAiEnabled] = useState(false);
  const [provenanceOpen, setProvenanceOpen] = useState(true);
  const [provenancePin, setProvenancePin] = useState<ProvenancePin | null>(null);
  const [lastPacket, setLastPacket] = useState<Record<string, unknown> | null>(null);
  const [lookupKey, setLookupKey] = useState(0);

  const triggerLookup = useCallback(() => setLookupKey((k) => k + 1), []);

  const applyScenario = useCallback((binding: ScenarioBinding) => {
    setScenario(binding.id as ScenarioId);
    setActiveBinding(binding);
    if (binding.context.plant_id) setPlantId(binding.context.plant_id);
    if (binding.context.asset_id) setAssetId(binding.context.asset_id);
    setAlertId(binding.context.alert_id || "");
    setAiEnabled(binding.ai_enabled);
    setLookupKey((k) => k + 1);
  }, []);

  const value = useMemo(
    () => ({
      plantId,
      assetId,
      alertId,
      scenario,
      activeBinding,
      aiEnabled,
      provenanceOpen,
      provenancePin,
      lastPacket,
      lookupKey,
      setPlantId,
      setAssetId,
      setAlertId,
      setScenario,
      applyScenario,
      triggerLookup,
      setAiEnabled,
      setProvenanceOpen,
      pinProvenance: (p: ProvenancePin) => {
        setProvenancePin(p);
        setProvenanceOpen(true);
      },
      setLastPacket,
    }),
    [plantId, assetId, alertId, scenario, activeBinding, aiEnabled, provenanceOpen, provenancePin, lastPacket, lookupKey, applyScenario, triggerLookup],
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp outside provider");
  return ctx;
}
