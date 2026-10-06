"""AssemblyLibrary.assemblyHandle is the next free assembly handle."""

from lxml import etree

from dsbxml.core import AssemblyLibrary
from dsbxml.utils import load_model


def _library(handles):
    return AssemblyLibrary.from_xml_tree(_tree(handles))


def _tree(handles):
    root = etree.Element("AssemblyLibrary", assemblyHandle="99")
    for handle in handles:
        assembly = etree.SubElement(
            root,
            "Assembly",
            assemblyHandle=str(handle),
            componentBlockHandle="0",
            reference="Occupant",
        )
        etree.SubElement(etree.SubElement(assembly, "HandlePoint"), "Point3D").text = "0; 0; 0"
        etree.SubElement(assembly, "ComponentBlocks")
    return root


def _written_handle(library) -> str:
    return etree.fromstring(library.to_xml()).get("assemblyHandle")


def test_handle_follows_the_highest_assembly_handle():
    assert _written_handle(_library([0, 1, 2])) == "3"


def test_handle_follows_an_added_assembly():
    library = _library([0, 1])
    library.assembly.append(library.assembly[0].model_copy(update={"assemblyHandle": 7}))
    assert _written_handle(library) == "8"


def test_handle_follows_a_removed_assembly():
    library = _library([0, 1, 2])
    library.assembly.pop()
    assert _written_handle(library) == "2"


def test_empty_library_keeps_its_handle():
    assert _written_handle(_library([])) == "99"


def test_loaded_library_is_written_unchanged():
    model = load_model("samples/models/Tutorial Model.xml", use_cache=False)
    library = model.site.assembly_library
    assert library.assemblyHandle == len(library.assembly) == 8
    assert _written_handle(library) == "8"
