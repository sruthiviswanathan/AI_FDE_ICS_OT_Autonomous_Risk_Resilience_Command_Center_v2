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


def test_clear_cache_roundtrip():
    data_layer.clear_cache()
    reloaded = data_layer.load_assets()
    assert len(reloaded) > 0
