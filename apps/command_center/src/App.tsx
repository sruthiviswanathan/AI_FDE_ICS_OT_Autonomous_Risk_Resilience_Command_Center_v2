import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AppProvider } from "./context/AppContext";
import { PersonaRouteGuard } from "./components/PersonaRouteGuard";
import { Shell } from "./layout/Shell";
import { AuditPage } from "./pages/AuditPage";
import { ControlTower } from "./pages/ControlTower";
import { ExecutivePage } from "./pages/ExecutivePage";
import { IdentityPage } from "./pages/IdentityPage";
import { IncidentPage } from "./pages/IncidentPage";
import { KPIPage } from "./pages/KPIPage";
import { ProcessGraphPage } from "./pages/ProcessGraphPage";
import { RecommendPage } from "./pages/RecommendPage";
import { RecoveryPage } from "./pages/RecoveryPage";
import { RiskPage } from "./pages/RiskPage";
import { SafetyPage } from "./pages/SafetyPage";
import { SimulationPage } from "./pages/SimulationPage";
import { TelemetryPage } from "./pages/TelemetryPage";
import { VendorSessionsPage } from "./pages/VendorSessionsPage";

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Shell />}>
            <Route element={<PersonaRouteGuard />}>
              <Route index element={<ControlTower />} />
              <Route path="identity" element={<IdentityPage />} />
              <Route path="telemetry" element={<TelemetryPage />} />
              <Route path="process" element={<ProcessGraphPage />} />
              <Route path="risk" element={<RiskPage />} />
              <Route path="safety" element={<SafetyPage />} />
              <Route path="sessions" element={<VendorSessionsPage />} />
              <Route path="recovery" element={<RecoveryPage />} />
              <Route path="incident" element={<IncidentPage />} />
              <Route path="recommend" element={<RecommendPage />} />
              <Route path="audit" element={<AuditPage />} />
              <Route path="simulation" element={<SimulationPage />} />
              <Route path="kpi" element={<KPIPage />} />
              <Route path="executive" element={<ExecutivePage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AppProvider>
  );
}
