PYTHON ?= python
export AI_ENABLED ?= 0

.PHONY: test diagnostics run verify sdd-gates redteam eval-harness workshop-ci ops-slo ui-build
ui-build:
	cd apps/command_center && npm ci && npm run build
test:
	$(PYTHON) -m pytest -q

diagnostics:
	PYTHONPATH=src $(PYTHON) -m ot_command.cli diagnostics

run:
	AI_ENABLED=$(AI_ENABLED) PYTHONPATH=src $(PYTHON) -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
	@echo UI http://127.0.0.1:8000/ui

verify:
	$(PYTHON) scripts/verify_repo.py

sdd-gates:
	$(PYTHON) scripts/check_sdd_gates.py

redteam:
	$(PYTHON) -m pytest -q tests/red_team tests/test_denied_control.py tests/test_authority.py

eval-harness:
	$(PYTHON) evals/harness.py

ops-slo:
	PYTHONPATH=src $(PYTHON) -c "from ot_command.core.ops import slo_status, cost_per_incident; print(slo_status()['live_ot'], cost_per_incident()['measured_usd'])"

workshop-ci: verify sdd-gates eval-harness test
	@echo WORKSHOP_CI_OK
