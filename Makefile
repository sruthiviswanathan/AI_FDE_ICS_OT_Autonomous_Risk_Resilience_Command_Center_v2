PYTHON ?= python

.PHONY: test diagnostics run verify sdd-gates redteam workshop-ci
test:
	$(PYTHON) -m pytest -q

diagnostics:
	PYTHONPATH=src $(PYTHON) -m ot_command.cli diagnostics

run:
	PYTHONPATH=src $(PYTHON) -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000

verify:
	$(PYTHON) scripts/verify_repo.py

sdd-gates:
	$(PYTHON) scripts/check_sdd_gates.py

redteam:
	$(PYTHON) -m pytest -q tests/red_team tests/test_denied_control.py tests/test_authority.py

workshop-ci: verify sdd-gates test
	@echo WORKSHOP_CI_OK
