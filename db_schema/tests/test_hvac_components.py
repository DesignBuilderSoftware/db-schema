# import json
# from db_schema.hvac_network import HVACComponents
# import pytest

filepaths = [
    r"C:\GitHub\db_schema\samples\fragments\DemandSubLoop_HVACComponents.json",
    r"C:\GitHub\db_schema\samples\fragments\SupplySubLoop_HVACComponents.json",
]


"""@pytest.mark.parametrize("filepath", filepaths)
def test_validate_component(filepath):
    with open(filepath, "r") as f:
        json_dict = json.load(f)
        assert HVACComponents.model_validate(json_dict["HVACComponents"])
"""
