"""Intentionally simplistic legacy logic for participant modernization."""
def legacy_risk_score(cvss: float, criticality: str) -> float:
    multiplier={"CRITICAL":1.15,"HIGH":1.05,"MEDIUM":0.95,"LOW":0.8}.get(criticality,1.0)
    return min(10.0, round(cvss*multiplier,2))

def legacy_rank(findings):
    return sorted(findings,key=lambda x: float(x.get("cvss",0)),reverse=True)

def legacy_recovery_ready(backup_status: str) -> bool:
    return backup_status == "CURRENT"  # ignores restore tests/runbooks/dependencies

def legacy_isolation_recommendation(alert_severity: str) -> str:
    return "ISOLATE" if alert_severity in {"HIGH","CRITICAL"} else "MONITOR"  # safety-blind by design
