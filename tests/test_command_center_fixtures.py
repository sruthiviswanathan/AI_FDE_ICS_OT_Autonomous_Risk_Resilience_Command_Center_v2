"""APP-01 fixtures are exact slices of synthetic CSVs. No invented IDs."""

from pathlib import Path

from ot_command.repository import jsonl, rows

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "apps/command_center/fixtures/command_center_fixtures.json"


def test_fixture_exists_and_declares_no_invented_fields():
    import json

    assert FIXTURE.exists()
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["invented_fields"] is False
    assert data["live_ot"] is False
    assert data["forbidden_ui"]["execute_isolation"] is False
    assert data["forbidden_ui"]["write_plc"] is False
    assert data["untrusted_shift_text"]["is_command"] is False
    assert data["anti_cvss_pair"]["cvss_is_sort_key"] is False


def test_fixture_rows_exist_in_source_files():
    import json

    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assets = {r["asset_id"] for r in rows("data/raw/assets.csv")}
    vulns = {r["finding_id"] for r in rows("data/raw/vulnerabilities.csv")}
    barriers = {r["barrier_id"] for r in rows("data/raw/safety_barriers.csv")}
    sessions = {r["session_id"] for r in rows("data/raw/remote_access_sessions.csv")}
    tele_ids = {r["event_id"] for r in jsonl("data/telemetry/tag_telemetry.jsonl")}
    for row in data["identity_conflicts"]["assets"]:
        assert row["asset_id"] in assets
    for row in data["anti_cvss_pair"]["vulnerabilities"]:
        assert row["finding_id"] in vulns
        assert row["asset_id"] in assets
    for row in data["bypassed_barrier"]["rows"]:
        assert row["barrier_id"] in barriers
    for row in data["unapproved_vendor_session"]["rows"]:
        assert row["session_id"] in sessions
    for row in data["bad_telemetry"]["rows"]:
        assert row["event_id"] in tele_ids
    shift = (ROOT / "data/shadow/shift_handover_email.txt").read_text(encoding="utf-8")
    assert data["untrusted_shift_text"]["text"] == shift


def test_anti_cvss_pair_and_stale_restore_are_the_golden_records():
    import json

    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    ids = {r["finding_id"] for r in data["anti_cvss_pair"]["vulnerabilities"]}
    assert ids == {"VUL-00706", "VUL-00098"}
    stale = data["stale_restore"]["rows"]
    assert stale
    assert stale[0]["plant_id"] == "PLT-01"
    assert stale[0]["component"] == "IDENTITY"
    assert stale[0]["backup_status"] == "CURRENT"
    assert data["stale_restore"]["backup_current_is_not_recovery_ready"] is True
    aliases = {r.get("alias") for r in data["identity_conflicts"]["aliases"]}
    assert "PLT-01-DCS_CONTROLLER-105" in aliases
