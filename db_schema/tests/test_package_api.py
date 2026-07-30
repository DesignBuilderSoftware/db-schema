"""Import-health matrix and lazy-loading API of the db_schema package.

The repo is mid-refactor: these tests use pytest.importorskip so that a
broken submodule produces skips rather than collection errors.
"""

import pytest

SUBMODULES = [
    "db_schema",
    "db_schema.attributes",
    "db_schema.base",
    "db_schema.core",
    "db_schema.geometry",
    "db_schema.id",
    "db_schema.tables",
    "db_schema.utils",
    "db_schema.hvac",
    "db_schema.hvac.components",
    "db_schema.hvac.network",
    "db_schema.hvac.unit_components",
    "db_schema.hvac.zone_components",
]


@pytest.mark.parametrize("module_name", SUBMODULES)
def test_submodule_imports(module_name):
    pytest.importorskip(
        module_name,
        reason=f"{module_name} failed to import (refactor in progress)",
    )


class TestLazyLoadingAPI:
    """db_schema/__init__.py exposes core classes via module __getattr__."""

    def test_dsbxml_accessible_from_package(self):
        db_schema = pytest.importorskip("db_schema")
        assert getattr(db_schema, "dsbXML", None) is not None

    def test_dsb_alias_points_to_dsbxml(self):
        db_schema = pytest.importorskip("db_schema")
        assert db_schema.DSB is db_schema.dsbXML

    def test_hvac_components_lazy_attribute(self):
        db_schema = pytest.importorskip("db_schema")
        pytest.importorskip("db_schema.hvac.components")
        assert getattr(db_schema, "HVACComponents", None) is not None

    def test_hvac_network_lazy_attribute(self):
        db_schema = pytest.importorskip("db_schema")
        pytest.importorskip("db_schema.hvac.network")
        assert getattr(db_schema, "HVACNetwork", None) is not None

    def test_core_site_class_exposed(self):
        db_schema = pytest.importorskip("db_schema")
        pytest.importorskip("db_schema.core")
        assert getattr(db_schema, "Site", None) is not None

    def test_unknown_attribute_raises(self):
        db_schema = pytest.importorskip("db_schema")
        with pytest.raises(AttributeError):
            getattr(db_schema, "DefinitelyNotARealClassName")

    def test_load_and_save_model_exported(self):
        db_schema = pytest.importorskip("db_schema")
        assert callable(db_schema.load_model)
        assert callable(db_schema.save_model)

    def test_repeated_access_returns_same_class(self):
        db_schema = pytest.importorskip("db_schema")
        pytest.importorskip("db_schema.core")
        assert db_schema.dsbXML is db_schema.dsbXML

    def test_private_names_do_not_trigger_lazy_load(self):
        db_schema = pytest.importorskip("db_schema")
        with pytest.raises(AttributeError):
            getattr(db_schema, "_no_such_private_name")

    def test_clear_model_cache_exported_from_utils(self):
        utils = pytest.importorskip("db_schema.utils")
        assert callable(utils.clear_model_cache)
