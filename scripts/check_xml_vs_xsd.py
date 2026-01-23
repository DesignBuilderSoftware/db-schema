from lxml import etree
from pathlib import Path

schema_doc = etree.parse('DesignBuilder.xsd')
schema = etree.XMLSchema(schema_doc)

for xml_file in Path('samples/models_dhvac').glob('*.xml'):
    try:
        doc = etree.parse(str(xml_file))
        if schema.validate(doc):
            print(f"[PASS] {xml_file.name}: Valid")
        else:
            print(f"[FAIL] {xml_file.name}: Invalid")
            for error in schema.error_log:
                print(f"  Line {error.line}: {error.message}")
    except Exception as e:
        print(f"[FAIL] {xml_file.name}: Parse error - {e}")