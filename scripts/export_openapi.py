"""Export FastAPI OpenAPI spec to contracts/openapi_command_center.yaml."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ot_command.api import app  # noqa: E402

try:
    import yaml
except ImportError:
    yaml = None

out_json = ROOT / "contracts" / "openapi_command_center.json"
out_yaml = ROOT / "contracts" / "openapi_command_center.yaml"
spec = app.openapi()
out_json.write_text(json.dumps(spec, indent=2), encoding="utf-8")
if yaml:
    out_yaml.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")
    print(f"Wrote {out_yaml.relative_to(ROOT)}")
else:
    print(f"Wrote {out_json.relative_to(ROOT)} (install pyyaml for .yaml)")
