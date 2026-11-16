from pathlib import Path

from lxml import etree

schema_file = etree.parse("dsbxml/DesignBuilder.xsd")
schema = etree.XMLSchema(schema_file)

dhvac_samples = sorted(Path("samples/2026.1.0.004").glob("*.xml")) + [
    Path("samples/2025.1.0.095/HVAC_Zones_Coloured.xml")
]

for dsb_xml_file in dhvac_samples:
    try:
        model = etree.parse(str(dsb_xml_file))
        if schema.validate(model):
            print(f"[PASS] {dsb_xml_file.name}: Valid")
        else:
            print(f"[FAIL] {dsb_xml_file.name}: Invalid")
            for error in schema.error_log:
                print(f"  Line {error.line}: {error.message}")
    except Exception as e:
        print(f"[FAIL] {dsb_xml_file.name}: Parse error - {e}")
