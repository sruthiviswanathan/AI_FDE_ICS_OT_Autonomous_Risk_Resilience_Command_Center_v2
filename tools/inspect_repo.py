import json
from ot_command.diagnostics import run_diagnostics
print(json.dumps(run_diagnostics(),indent=2))
