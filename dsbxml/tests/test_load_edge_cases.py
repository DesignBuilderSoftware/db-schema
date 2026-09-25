"""Loading real-world dsbXML shapes that DesignBuilder exports.

Found by db-testing's dsbXML corpus: models with no assemblies, and models
whose EDD dump attribute is one text node over libxml2's 10 MB limit.
"""

from dsbxml.utils import load_model

HEAD = (
    '<dsbXML name="t" date="2026-01-01" version="8.0" objects="all"><Site count="0" handle="1">'
)


def _load(tmp_path, xml: str):
    path = tmp_path / "model.xml"
    path.write_bytes(xml.encode())
    return load_model(path, use_cache=False)


def test_empty_assembly_library_loads(tmp_path):
    """DesignBuilder writes <AssemblyLibrary assemblyHandle="0"/> with no
    <Assembly> children when a model has no assemblies."""
    model = _load(tmp_path, HEAD + '<AssemblyLibrary assemblyHandle="0"/></Site></dsbXML>')

    assert model.site.assembly_library.assembly == []


def test_text_node_over_10_mb_loads(tmp_path):
    """An EDD dump stored in one attribute, starting with entity references
    like the real ones. Entity references split the text into chunks, and
    libxml2 enforces its 10 MB text limit when joining them unless the
    parser is created with huge_tree=True."""
    first = "! &lt;EnergyManagementSystem:Actuator Available&gt;, Component Unique Name\n"
    line = "EnergyManagementSystem:Actuator Available,NODE 1,System Node Setpoint,Temperature\n"
    text = first + line * 140_000
    assert len(text) > 10_000_000

    model = _load(
        tmp_path,
        HEAD
        + f'<Attributes><Attribute name="EDDFile">{text}</Attribute></Attributes>'
        + "</Site></dsbXML>",
    )

    (attribute,) = model.site.attributes.attribute
    assert attribute.value.startswith("! <EnergyManagementSystem:Actuator Available>")
