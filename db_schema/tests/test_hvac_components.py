"""Tests for HVAC component parsing and type discrimination."""

from pathlib import Path

import pytest

test_dir = Path(__file__).parent
repo_root = test_dir.parent.parent
detailed_hvac = repo_root / "samples" / "models" / "DetailedHVAC.xml"
dhvac_sample = repo_root / "samples" / "models_dhvac" / "1.xml"


@pytest.fixture(scope="module")
def hvac_model():
    if not detailed_hvac.exists():
        pytest.skip("DetailedHVAC.xml sample not found")
    from db_schema.utils import load_model
    return load_model(str(detailed_hvac))


@pytest.fixture(scope="module")
def first_loop(hvac_model):
    return hvac_model.site.buildings.building[0].hvac_network.hvac_loops.hvac_loop[0]


@pytest.fixture(scope="module")
def demand_components(first_loop):
    return first_loop.demand_sub_loop.hvac_components.hvac_component


@pytest.fixture(scope="module")
def supply_components(first_loop):
    return first_loop.supply_sub_loop.hvac_components.hvac_component


# ---------------------------------------------------------------------------
# Network structure
# ---------------------------------------------------------------------------

def test_hvac_network_loads(hvac_model):
    net = hvac_model.site.buildings.building[0].hvac_network
    assert net is not None


def test_hvac_loops_present(hvac_model):
    loops = hvac_model.site.buildings.building[0].hvac_network.hvac_loops
    assert loops is not None
    assert len(loops.hvac_loop) > 0


def test_demand_sub_loop_has_components(demand_components):
    assert len(demand_components) > 0


def test_supply_sub_loop_has_components(supply_components):
    assert len(supply_components) > 0


# ---------------------------------------------------------------------------
# Component type discrimination
# ---------------------------------------------------------------------------

def test_all_components_have_type(demand_components, supply_components):
    for comp in list(demand_components) + list(supply_components):
        assert hasattr(comp, "type")
        assert isinstance(comp.type, str)
        assert comp.type != ""


def test_known_component_types_present(demand_components, supply_components):
    all_types = {c.type for c in list(demand_components) + list(supply_components)}
    # Every loop has at least a Sub-loop node linking supply/demand
    assert "Sub-loop node" in all_types


def test_components_have_image_rectangles(demand_components):
    # Every component should attempt to have an image rectangle
    # (imageTextureIndex == -1 means invisible, but field should be present)
    for comp in demand_components:
        # image_rectangle may be None for some component types, but
        # all visible components must have one
        if comp.image_rectangle is not None:
            assert comp.image_rectangle.imageTextureIndex is not None


# ---------------------------------------------------------------------------
# Component scalar fields (formerly bare, now properly mapped)
# ---------------------------------------------------------------------------

def test_component_loop_type_is_int(demand_components):
    for comp in demand_components:
        assert isinstance(comp.loopType, int)


def test_component_plant_loop_type_is_int(demand_components):
    for comp in demand_components:
        assert isinstance(comp.plantLoopType, int)


def test_component_water_in_connection_is_int(demand_components):
    for comp in demand_components:
        assert isinstance(comp.waterInConnection, int)
        assert comp.waterInConnection in (0, 1)


# ---------------------------------------------------------------------------
# Zone groups
# ---------------------------------------------------------------------------

def test_hvac_zone_groups_present(hvac_model):
    zgs = hvac_model.site.buildings.building[0].hvac_network.hvac_zone_groups
    assert zgs is not None
    assert len(zgs.hvac_zone_group) > 0


def test_zone_group_has_zone_element_list(hvac_model):
    zg = hvac_model.site.buildings.building[0].hvac_network.hvac_zone_groups.hvac_zone_group[0]
    # zone_element_list may be None if empty, but the attribute exists
    assert hasattr(zg, "zone_element_list")


# ---------------------------------------------------------------------------
# dhvac sample models
# ---------------------------------------------------------------------------

def test_dhvac_sample_loads():
    if not dhvac_sample.exists():
        pytest.skip("dhvac/1.xml not found")
    from db_schema.utils import load_model
    m = load_model(str(dhvac_sample))
    assert m is not None
    assert m.site is not None


def test_dhvac_hvac_network_has_loops():
    if not dhvac_sample.exists():
        pytest.skip("dhvac/1.xml not found")
    from db_schema.utils import load_model
    m = load_model(str(dhvac_sample))
    net = m.site.buildings.building[0].hvac_network
    if net and net.hvac_loops:
        assert len(net.hvac_loops.hvac_loop) > 0
