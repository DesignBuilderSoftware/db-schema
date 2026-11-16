import importlib.util
from pathlib import Path

from dsbxml.core import Plane
from dsbxml.hvac.network import PlantOperationRanges

AUDIT = Path(__file__).resolve().parents[2] / "scripts" / "audit_classes_vs_xsd.py"


def load_audit():
    spec = importlib.util.spec_from_file_location("audit_classes_vs_xsd", AUDIT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_classes_read_everything_the_xsd_declares():
    # "any-order" (an unbounded xs:choice) and "untyped" (open XSD content) are the XSD's
    # looseness, not the classes' gaps, so they are left out.
    strict = {"dropped", "extra", "location", "single", "required"}
    found = [f for f in load_audit().audit() if f[0] in strict]
    assert found == []


def test_a_plane_keeps_its_attributes():
    plane = Plane.from_xml(
        '<Plane type="1"><Polygon auxiliaryType="0"><Vertices><Point3D>0; 0; 0</Point3D>'
        "</Vertices></Polygon>"
        '<Attributes><Attribute key="Title">Grid</Attribute></Attributes></Plane>'
    )
    assert plane.attributes.attribute[0].value == "Grid"


def test_a_scheme_keeps_every_operation_range():
    ranges = PlantOperationRanges.from_xml(
        "<PlantOperationRanges>"
        '<PlantOperationRange><Attributes><Attribute name="Upper">1000</Attribute></Attributes>'
        "</PlantOperationRange>"
        '<PlantOperationRange><Attributes><Attribute name="Upper">5000</Attribute></Attributes>'
        "</PlantOperationRange>"
        "</PlantOperationRanges>"
    )
    assert [r.attributes.attribute[0].value for r in ranges.plant_operation_range] == [
        "1000",
        "5000",
    ]
