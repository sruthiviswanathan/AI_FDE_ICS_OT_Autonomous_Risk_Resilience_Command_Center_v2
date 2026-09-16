"""Structural Repo 2.0 gate. Does not exercise legacy risk functions."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sdd_required_paths_and_eval_stubs():
    script = ROOT / "scripts" / "check_sdd_gates.py"
    r = subprocess.run([sys.executable, str(script)], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "SDD_GATE_OK" in r.stdout
