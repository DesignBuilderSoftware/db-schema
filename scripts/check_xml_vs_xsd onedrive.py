from lxml import etree
from pathlib import Path

schema_file = etree.parse("DesignBuilder.xsd")
schema = etree.XMLSchema(schema_file)

path = Path(
    "C:\\Users\\thinkpad\\OneDrive - Designbuilder Software Ltd\\DesignBuilder - Validation\\schema dsbXML xsd\\dsbXML test files"
)

for dsb_xml_file in path.glob("*.xml"):
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
