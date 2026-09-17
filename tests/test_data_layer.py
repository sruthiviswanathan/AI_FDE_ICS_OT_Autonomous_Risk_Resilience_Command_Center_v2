"""Runtime data abstraction layer tests (APP-01)."""

from ot_command.core import data_layer


def test_canonical_sources_load():
    catalog = data_layer.sources_catalog()
    assert catalog["mode"] == "runtime-derived"
    assert len(catalog["sources"]) == 6
    assert data_layer.load_assets()
    assert data_layer.load_telemetry()
    assert data_layer.load_vulnerabilities()


def test_derived_views_consistent():
    assets_by_id = data_layer.derived_assets_by_id()
    assert "OT-01016" in assets_by_id
    estate = data_layer.estate_derived_view()
    assert estate["counts"]["assets"] == len(assets_by_id)


def test_estate_by_plant_view():
    view = data_layer.estate_by_plant_view(include_top_alerts=3)
    assert view["plant_count"] == 18
    assert view["total_alerts"] > 0
    assert view["asset_status_summary"]["total_assets"] > 0
    plt10 = next(p for p in view["plants"] if p["plant_id"] == "PLT-10")
    assert plt10["counts"]["assets"] > 0
    assert plt10["counts"]["alerts_total"] > 0
    assert plt10["signals"]["elevated"] is True
    assert plt10["signals"]["posture_composite"] != "ok"
    assert "posture_layers" in plt10
    assert "cyber_exposure" in plt10["posture_layers"]
    assert "top_assets_by_alerts" in plt10
    assert "methodology" in view


def test_clear_cache_roundtrip():
    data_layer.clear_cache()
    reloaded = data_layer.load_assets()
    assert len(reloaded) > 0
