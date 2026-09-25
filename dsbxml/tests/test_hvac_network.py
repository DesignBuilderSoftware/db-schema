"""Tests for dsbxml.hvac.network model construction and serialisation."""

import pytest

network = pytest.importorskip(
    "dsbxml.hvac.network",
    reason="dsbxml.hvac.network failed to import",
)
components = pytest.importorskip(
    "dsbxml.hvac.components",
    reason="dsbxml.hvac.components failed to import",
)

HVACNetwork = network.HVACNetwork
HVACLoops = network.HVACLoops
HVACZoneGroup = network.HVACZoneGroup
BuildingZoneHandle = network.BuildingZoneHandle
NoTypeHVACComponent = components.NoTypeHVACComponent


@pytest.fixture(scope="module", autouse=True)
def _resolve_forward_refs():
    """Touch the lazy package API so model_rebuild() has run for HVAC models."""
    dsbxml = pytest.importorskip("dsbxml")
    getattr(dsbxml, "dsbXML", None)


class TestHVACNetworkModel:
    def test_default_construction(self):
        n = HVACNetwork()
        assert n.ObjectHandle is None
        assert n.hvac_loops is None
        assert n.hvac_zone_groups is None
        assert n.object_ids is not None

    def test_object_ids_handle_generated(self):
        a = HVACNetwork()
        b = HVACNetwork()
        assert a.object_ids.handle != b.object_ids.handle

    def test_xml_round_trip(self):
        n = HVACNetwork(ObjectHandle=42)
        again = HVACNetwork.from_xml(n.to_xml())
        assert again.ObjectHandle == 42
        assert again.object_ids.handle == n.object_ids.handle

    def test_empty_loops_container(self):
        loops = HVACLoops()
        assert loops.hvac_loop == []


class TestHVACZoneGroup:
    def test_is_no_type_component_subclass(self):
        # HVACZoneGroup inherits its fields from NoTypeHVACComponent
        # (documented workaround for a pydantic-xml nested serializer bug).
        assert issubclass(HVACZoneGroup, NoTypeHVACComponent)


class TestBuildingZoneHandle:
    def test_parses_handle_list(self):
        b = BuildingZoneHandle.from_xml(
            b"<BuildingZoneHandle>"
            b"<BuildingZoneHandle>3</BuildingZoneHandle>"
            b"<BuildingZoneHandle>4</BuildingZoneHandle>"
            b"</BuildingZoneHandle>"
        )
        assert b.building_zone_handle == ["3", "4"]

    def test_default_is_empty(self):
        assert BuildingZoneHandle().building_zone_handle == []
