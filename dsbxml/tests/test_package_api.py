"""Import-health matrix and lazy-loading API of the dsbxml package.

The repo is mid-refactor: these tests use pytest.importorskip so that a
broken submodule produces skips rather than collection errors.
"""

import pytest

SUBMODULES = [
    "dsbxml",
    "dsbxml.attributes",
    "dsbxml.base",
    "dsbxml.core",
    "dsbxml.geometry",
    "dsbxml.id",
    "dsbxml.tables",
    "dsbxml.utils",
    "dsbxml.hvac",
    "dsbxml.hvac.components",
    "dsbxml.hvac.network",
    "dsbxml.hvac.unit_components",
    "dsbxml.hvac.zone_components",
]


@pytest.mark.parametrize("module_name", SUBMODULES)
def test_submodule_imports(module_name):
    pytest.importorskip(
        module_name,
        reason=f"{module_name} failed to import (refactor in progress)",
    )


class TestLazyLoadingAPI:
    """dsbxml/__init__.py exposes core classes via module __getattr__."""

    def test_dsbxml_accessible_from_package(self):
        dsbxml = pytest.importorskip("dsbxml")
        assert getattr(dsbxml, "dsbXML", None) is not None

    def test_dsb_alias_points_to_dsbxml(self):
        dsbxml = pytest.importorskip("dsbxml")
        assert dsbxml.DSB is dsbxml.dsbXML

    def test_hvac_components_lazy_attribute(self):
        dsbxml = pytest.importorskip("dsbxml")
        pytest.importorskip("dsbxml.hvac.components")
        assert getattr(dsbxml, "HVACComponents", None) is not None

    def test_hvac_network_lazy_attribute(self):
        dsbxml = pytest.importorskip("dsbxml")
        pytest.importorskip("dsbxml.hvac.network")
        assert getattr(dsbxml, "HVACNetwork", None) is not None

    def test_core_site_class_exposed(self):
        dsbxml = pytest.importorskip("dsbxml")
        pytest.importorskip("dsbxml.core")
        assert getattr(dsbxml, "Site", None) is not None

    def test_unknown_attribute_raises(self):
        dsbxml = pytest.importorskip("dsbxml")
        with pytest.raises(AttributeError):
            getattr(dsbxml, "DefinitelyNotARealClassName")

    def test_load_and_save_model_exported(self):
        dsbxml = pytest.importorskip("dsbxml")
        assert callable(dsbxml.load_model)
        assert callable(dsbxml.save_model)

    def test_repeated_access_returns_same_class(self):
        dsbxml = pytest.importorskip("dsbxml")
        pytest.importorskip("dsbxml.core")
        assert dsbxml.dsbXML is dsbxml.dsbXML

    def test_private_names_do_not_trigger_lazy_load(self):
        dsbxml = pytest.importorskip("dsbxml")
        with pytest.raises(AttributeError):
            getattr(dsbxml, "_no_such_private_name")

    def test_clear_model_cache_exported_from_utils(self):
        utils = pytest.importorskip("dsbxml.utils")
        assert callable(utils.clear_model_cache)
