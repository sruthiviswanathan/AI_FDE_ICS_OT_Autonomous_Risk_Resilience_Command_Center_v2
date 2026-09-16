"""Fail if Repo 2.0 SDD layout files are missing. Does not change legacy behavior."""
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "specs/README.md",
    "specs/01_mandate.md",
    "specs/02_current_state.md",
    "specs/03_forensics_96.md",
    "specs/04_problem_value.md",
    "specs/05_use_case.md",
    "specs/06_domain.md",
    "specs/07_data_knowledge.md",
    "specs/08_evals_risks.md",
    "specs/09_options.md",
    "specs/10_information_architecture.md",
    "specs/11_ai_app_architecture.md",
    "specs/12_agentic.md",
    "specs/13_security_guardrails.md",
    "specs/14_delivery_spec.md",
    "specs/PRD.md",
    "specs/APP_ACCEPTANCE_TESTS.md",
    "specs/REQUIREMENTS_TRACEABILITY.md",
    "specs/REPO_2_0_GATE.md",
    "specs/REPO_3_0_GATE.md",
    "specs/as_built_c4.md",
    "specs/TRACEABILITY.csv",
    "specs/adrs/README.md",
    "specs/adrs/ADR_REGISTER.md",
    "adrs/README.md",
    "adrs/ADR-00-index.md",
    "adrs/ADR-KG-evidence-graph.md",
    "adrs/ADR-01-identity.md",
    "adrs/ADR-02-telemetry-provenance.md",
    "adrs/ADR-03-contextual-risk.md",
    "adrs/ADR-04-safety-policy.md",
    "adrs/ADR-05-recovery.md",
    "adrs/ADR-06-retrieval-mix.md",
    "adrs/ADR-07-agent-boundary.md",
    "adrs/ADR-08-evidence-feedback.md",
    "adrs/ADR-09-persistence.md",
    "adrs/ADR-10-v1-anticorruption.md",
    "adrs/ADR-11-readonly-api.md",
    "adrs/ADR-12-ai-disabled.md",
    "adrs/ADR-13-model-port.md",
    "adrs/ADR-14-autonomy.md",
    "adrs/ADR-15-guardrails.md",
    "adrs/ADR-16-supply-chain.md",
    "evals/golden_cases.jsonl",
    "evals/scenarios.md",
    "traceability/TRACEABILITY.csv",
    "traceability/OPEN_DECISIONS.md",
    "participant/work/FDE_96_COVERAGE.csv",
    "participant/work/sdd_15/REPO_2_0_GATE.md",
    "participant/work/enh_10/REPO_3_0_GATE.md",
    "participant/work/prd/PRD.md",
    "participant/work/prd/APP_ACCEPTANCE_TESTS.md",
    "apps/command_center/fixtures/command_center_fixtures.json",
    "apps/command_center/index.html",
    "apps/command_center/static/app.js",
    "apps/command_center/SCENARIO_BINDINGS.md",
    "apps/command_center/fixtures/scenario_bindings.json",
    "src/ot_command/modern/README.md",
    "src/ot_command/modern/AS_BUILT_C4.md",
    "assurance/README.md",
    "ops/README.md",
    "ops/RACI.md",
    "ops/runbooks.md",
    "ops/incident_rollback.md",
    "ops/ai_incident_response.md",
    "ops/bcdr.md",
    "ops/production_readiness_checklist.md",
    "ops/handover.md",
    "ops/training_outline.md",
    "ops/finops_cost_dashboard.md",
    "ops/drift_management.md",
    "contracts/decision_trace.yaml",
    ".cursor/rules/sdd.mdc",
]

def main():
    missing = [rel for rel in REQUIRED if not (ROOT / rel).exists()]
    gc = ROOT / "evals/golden_cases.jsonl"
    ids = []
    if gc.exists():
        for line in gc.read_text(encoding="utf-8").splitlines():
            if line.strip():
                ids.append(json.loads(line)["case_id"])
    need = [f"EVAL-{i:03d}" for i in range(1, 7)]
    eval_miss = [e for e in need if e not in ids]
    cov = ROOT / "participant/work/FDE_96_COVERAGE.csv"
    cov_err = None
    if cov.exists():
        n = sum(1 for i, _ in enumerate(cov.read_text(encoding="utf-8").splitlines()) if i)
        if n < 96:
            cov_err = f"FDE_96_COVERAGE.csv has {n} data rows, need 96"
    errors = [f"missing {m}" for m in missing]
    errors += [f"golden_cases missing {e}" for e in eval_miss]
    if cov_err:
        errors.append(cov_err)
    if errors:
        print("SDD_GATE_FAIL")
        for e in errors:
            print(e)
        sys.exit(1)
    print("SDD_GATE_OK", len(REQUIRED), "paths;", len(ids), "eval cases")
    sys.exit(0)

if __name__ == "__main__":
    main()
