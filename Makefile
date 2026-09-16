PYTHON ?= python

.PHONY: test diagnostics run verify sdd-gates red-team eval ops ci
test:
	PYTHONPATH=src $(PYTHON) -m pytest -q

red-team:
	PYTHONPATH=src $(PYTHON) -m pytest tests/red_team -q

eval:
	PYTHONPATH=src $(PYTHON) evals/harness.py

ops:
	PYTHONPATH=src $(PYTHON) -m pytest tests/test_ops_telemetry.py -q

diagnostics:
	PYTHONPATH=src $(PYTHON) -m ot_command.cli diagnostics

run:
	PYTHONPATH=src $(PYTHON) -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000

verify:
	$(PYTHON) scripts/verify_repo.py

sdd-gates:
	$(PYTHON) scripts/check_sdd_gates.py

ci: sdd-gates verify test eval ops red-team
	@echo CI_OK
