"""HVAC elements must survive a load/save round trip.

The HVAC network holds many parts nested inside components (the DX coil inside
a unitary coil, the parts of a heat pump water heater, the outdoor air
system's components, whole VRF loops, ...). A field missing from the schema is
silently dropped on load, so a saved file loses data DesignBuilder wrote.
"""

import collections
import functools
from pathlib import Path

import pytest
from lxml import etree

from dsbxml.utils import load_model

test_dir = Path(__file__).parent
repo_root = test_dir.parent.parent
detailed_hvac = repo_root / "samples" / "models" / "DetailedHVAC.xml"
models_dhvac = sorted((repo_root / "samples" / "models_dhvac").glob("*.xml"))
sample_files = [detailed_hvac, *models_dhvac]


def _paths(network):
    """Every element path under the HVAC network, with a count."""
    counts = collections.Counter()

    def walk(element, path):
        for child in element:
            if not isinstance(child.tag, str):
                continue
            tag = child.tag
            if child.get("type") and tag.endswith("Component"):
                tag += f"[{child.get('type')}]"
            counts[f"{path}/{tag}"] += 1
            walk(child, f"{path}/{tag}")

    walk(network, "")
    return counts


def _leaf_values(network):
    """Every (path, text) leaf under the HVAC network, numbers normalised.

    ObjectIDs carry attributes only and are covered by their own fixes.
    """
    counts = collections.Counter()

    def normalise(text):
        text = (text or "").strip()
        try:
            return f"{float(text):.5g}"
        except ValueError:
            return text

    def walk(element, path):
        for child in element:
            if not isinstance(child.tag, str):
                continue
            child_path = f"{path}/{child.tag}"
            if len(child) == 0 and child.tag != "ObjectIDs":
                counts[(child_path, normalise(child.text))] += 1
            walk(child, child_path)

    walk(network, "")
    return counts


@functools.lru_cache(maxsize=None)
def _round_trip_network(filepath):
    before = etree.parse(str(filepath)).getroot().find(".//HVACNetwork")
    xml = load_model(str(filepath)).to_xml()
    xml = xml if isinstance(xml, bytes) else xml.encode("utf-8")
    after = etree.fromstring(xml).find(".//HVACNetwork")
    return before, after


@pytest.mark.parametrize("filepath", sample_files, ids=lambda p: p.name)
def test_no_hvac_element_is_dropped(filepath):
    before, after = _round_trip_network(filepath)
    if before is None:
        pytest.skip("no HVAC network")
    lost = _paths(before) - _paths(after)
    assert not lost, f"dropped on round trip: {sorted(lost)[:5]}"


@pytest.mark.parametrize("filepath", sample_files, ids=lambda p: p.name)
def test_no_hvac_value_changes(filepath):
    before, after = _round_trip_network(filepath)
    if before is None:
        pytest.skip("no HVAC network")
    changed = _leaf_values(before) - _leaf_values(after)
    assert not changed, f"values changed on round trip: {sorted(changed)[:5]}"


# --- Parsed values, against DetailedHVAC.xml -------------------------------


@pytest.fixture(scope="module")
def network():
    if not detailed_hvac.exists():
        pytest.skip("DetailedHVAC.xml sample not found")
    return load_model(str(detailed_hvac)).site.buildings.building[0].hvac_network


@pytest.fixture(scope="module")
def loop_components(network):
    return [
        component
        for loop in network.hvac_loops.hvac_loop
        for sub_loop in (loop.supply_sub_loop, loop.demand_sub_loop)
        for component in sub_loop.hvac_components.hvac_component
    ]


@pytest.fixture(scope="module")
def zone_components(network):
    return [
        component
        for group in network.hvac_zone_groups.hvac_zone_group
        for component in (
            group.zone_element_list.hvac_zone_component if group.zone_element_list else []
        )
    ]


def _of_type(components, type_name):
    return [c for c in components if c.type == type_name]


def test_water_heater_heat_pump_parts_and_offsets(loop_components):
    (heat_pump,) = _of_type(loop_components, "Water heater heat pump")
    assert heat_pump.water_heater_y_offset == -83.5
    assert (heat_pump.supply_fan_x_offset, heat_pump.supply_fan_y_offset) == (27.0, 103.5)
    assert heat_pump.air_to_water_heat_pump_coil_x_offset == -37.5
    assert heat_pump.air_to_water_heat_pump_coil_y_offset == 103.5
    assert heat_pump.water_heater.image_rectangle is not None
    assert heat_pump.supply_fan.image_rectangle is not None
    assert heat_pump.air_to_water_heat_pump_coil.image_rectangle is not None
    assert len(heat_pump.air_to_water_hp_coil_connections.line_array.line) == 9
    # The tank itself carries a heater element and a hot water heat exchanger flag.
    assert heat_pump.water_heater.hot_water_heat_exchanger == 1
    assert heat_pump.water_heater.heater_element is not None


def test_water_heater_parts(loop_components):
    heaters = _of_type(loop_components, "Water heater")
    assert len(heaters) == 2
    for heater in heaters:
        assert heater.hot_water_heat_exchanger == 1
        assert heater.heater_element.image_rectangle is not None


def test_heat_exchanger_storage_and_condenser_parts(loop_components):
    (storage,) = _of_type(loop_components, "Chilled water storage")
    assert storage.chilled_water_storage_heat_exchanger.image_rectangle is not None
    for exchanger in _of_type(loop_components, "Fluid-to-fluid heat exchanger"):
        assert exchanger.heat_exchanger_element.image_rectangle is not None
    for name in ("Heat pump cooling", "Heat pump heating"):
        (heat_pump,) = _of_type(loop_components, name)
        assert heat_pump.heat_pump_condenser.image_rectangle is not None


def test_domestic_water_connections_equipment(loop_components):
    (connections,) = _of_type(loop_components, "Domestic water connections")
    (equipment,) = connections.water_equipment_list.hvac_component
    assert equipment.type == "Domestic water equipment"


def test_unitary_system_reheat_coil(loop_components):
    (unitary,) = _of_type(loop_components, "Unitary system")
    assert unitary.has_reheat_coil == 0
    assert unitary.reheat_coil.image_rectangle is not None


def test_outdoor_air_system_component_list(loop_components):
    lists = [
        unit.outdoor_air_system.component_list
        for unit in _of_type(loop_components, "Air handling unit")
    ]
    assert all(component_list is not None for component_list in lists)
    counts = sorted(
        len(component_list.outdoor_air_system_hvac_component) for component_list in lists
    )
    assert counts == [0] * 7 + [1]
    (part,) = [p for cl in lists for p in cl.outdoor_air_system_hvac_component]
    assert part.type == "Generic heating coil"


def test_unitary_coil_dx_coil(loop_components):
    coils = [
        component
        for unit in _of_type(loop_components, "Air handling unit")
        if unit.intake_unit_component_list
        for component in unit.intake_unit_component_list.air_handling_unit_hvac_component
        if component.type == "Unitary cooling coil"
    ]
    assert coils
    for coil in coils:
        assert coil.dx_cooling_coil.image_rectangle.imageTextureIndex == 12


def test_zone_units_keep_their_missing_parts(zone_components):
    (dual_duct,) = _of_type(zone_components, "Zone ADU dual duct VAV")
    assert (dual_duct.warm_air_in_connected, dual_duct.cold_air_in_connected) == (1, 1)
    assert dual_duct.dual_duct_mixing_box.image_rectangle.imageTextureIndex == 77
    (series_piu,) = _of_type(zone_components, "Zone ADU series PIU")
    assert series_piu.supply_louvre.image_rectangle.imageTextureIndex == 65


def test_outdoor_air_supply_flag(zone_components):
    flags = [
        (c.type, c.outdoor_air_supply)
        for c in zone_components
        if c.outdoor_air_supply is not None
    ]
    assert len(flags) == 6
    assert sum(flag for _, flag in flags) == 1
    assert [t for t, flag in flags if flag] == ["Zone fan-coil unit"]


def test_radiant_surface_elements(zone_components):
    (radiant,) = _of_type(zone_components, "Zone radiant surface")
    assert (radiant.has_heating_element, radiant.has_cooling_element) == (1, 1)
    assert radiant.heating_element.image_rectangle is not None
    assert radiant.cooling_element.image_rectangle is not None


def test_vrf_loop(network):
    (vrf_loop,) = network.hvac_loops.hvac_vrf_loop
    unit = vrf_loop.vrf_air_conditioner_unit
    assert unit.refrigerant_connected == 1
    assert unit.refrigerant_connection_coordinate is not None
    assert unit.water_cooled_condenser is not None
    assert len(vrf_loop.hvac_connections.hvac_connection) == 1
    # The ordinary loops are unaffected.
    assert len(network.hvac_loops.hvac_loop) == 43
