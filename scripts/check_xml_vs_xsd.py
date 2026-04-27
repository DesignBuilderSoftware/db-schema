from pathlib import Path

from lxml import etree

schema_file = etree.parse("DesignBuilder.xsd")
schema = etree.XMLSchema(schema_file)

for dsb_xml_file in Path("samples/models_dhvac").glob("*.xml"):
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
