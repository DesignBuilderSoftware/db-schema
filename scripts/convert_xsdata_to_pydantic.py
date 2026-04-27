#!/usr/bin/env python
"""Convert xsdata-generated dataclasses to Pydantic models with pydantic_xml support."""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class XsdataConverter:
    """Converts xsdata dataclasses to Pydantic models."""

    def __init__(self, xsdata_file: str):
        self.xsdata_file = xsdata_file
        with open(xsdata_file, 'r', encoding='utf-8') as f:
            self.tree = ast.parse(f.read())
        self.classes: Dict[str, Dict[str, Any]] = {}
        self.extract_classes()
        self.name_map: Dict[str, str] = {}  # dotted_name -> output_class_name
        self.build_name_map()

    # -------------------------------------------------------------------------
    # Extraction
    # -------------------------------------------------------------------------

    def extract_classes(self):
        """Extract all class definitions from the AST, including nested ones."""
        def walk_classes(node, prefix=""):
            if isinstance(node, ast.ClassDef):
                class_name = node.name if not prefix else f"{prefix}.{node.name}"
                self.classes[class_name] = self.extract_class_info(node)
                for item in node.body:
                    if isinstance(item, ast.ClassDef):
                        walk_classes(item, class_name)

        for node in self.tree.body:
            walk_classes(node)

    def extract_class_info(self, node: ast.ClassDef) -> Dict[str, Any]:
        """Extract information about a single class."""
        fields = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign):
                field_info = self.extract_field_info(item)
                if field_info:
                    fields.append(field_info)

        meta_name = None
        for item in node.body:
            if isinstance(item, ast.ClassDef) and item.name == 'Meta':
                for meta_item in item.body:
                    if isinstance(meta_item, ast.Assign):
                        if isinstance(meta_item.targets[0], ast.Name):
                            if meta_item.targets[0].id == 'name':
                                if isinstance(meta_item.value, ast.Constant):
                                    meta_name = meta_item.value.value

        return {
            'fields': fields,
            'meta_name': meta_name,
            'nested_classes': [n.name for n in node.body if isinstance(n, ast.ClassDef) and n.name != 'Meta']
        }

    def extract_field_info(self, node: ast.AnnAssign) -> Optional[Dict[str, Any]]:
        """Extract information about a single field."""
        if not isinstance(node.target, ast.Name):
            return None

        field_name = node.target.id
        if field_name.startswith('_'):
            return None

        field_type = ast.unparse(node.annotation) if node.annotation else "Any"

        field_meta = {
            'name': field_name,
            'type': field_type,
            'is_list': 'list[' in field_type or 'List[' in field_type,
            'is_optional': 'None |' in field_type or '| None' in field_type or field_type.startswith('None'),
            'xml_tag': field_name,
            'is_attribute': False,
            'has_default': node.value is not None
        }

        if node.value and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name) and node.value.func.id == 'field':
                for keyword in node.value.keywords:
                    if keyword.arg == 'metadata' and isinstance(keyword.value, ast.Dict):
                        for key_node, val_node in zip(keyword.value.keys, keyword.value.values):
                            if isinstance(key_node, ast.Constant):
                                key = key_node.value
                                if key == 'name' and isinstance(val_node, ast.Constant):
                                    field_meta['xml_tag'] = val_node.value
                                elif key == 'type' and isinstance(val_node, ast.Constant):
                                    field_meta['is_attribute'] = val_node.value == 'Attribute'

        return field_meta

    # -------------------------------------------------------------------------
    # Name mapping: dotted_name -> output class name
    # -------------------------------------------------------------------------

    @staticmethod
    def _normalize_type(type_str: str) -> str:
        """Strip dotted xsdata paths to leaf names for structural comparison."""
        return re.sub(r'\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\b',
                      lambda m: m.group(0).split('.')[-1], type_str)

    def _fields_signature(self, class_name: str) -> tuple:
        """Hashable signature of a class's fields for equality comparison.
        Uses normalized (leaf-only) type names so structurally identical classes
        that only differ in their xsdata path context are treated as the same."""
        fields = self.classes[class_name]['fields']
        return tuple((f['name'], self._normalize_type(f['type']), f['is_attribute'], f['xml_tag']) for f in fields)

    def build_name_map(self):
        """
        Assign an output class name to every dotted xsdata class name.

        Strategy:
        1. Group all dotted names by field signature — structurally identical classes
           share one output name (the shortest leaf name among them).
        2. For classes with the same leaf name but different fields, qualify with the
           immediate parent name (e.g. BuildingAttributes, SiteAttributes).
        3. If parent+leaf is still not unique across different signatures, append a
           numeric suffix (_2, _3, ...) rather than going deeper into the path.
        """
        self.name_map['DsbXml'] = 'dsbXML'
        dotted_names = [n for n in self.classes if n != 'DsbXml']

        # --- Step 1: group by field signature → each unique structure gets one name ---
        sig_to_dotted: Dict[tuple, List[str]] = {}
        for dn in dotted_names:
            sig = self._fields_signature(dn)
            sig_to_dotted.setdefault(sig, []).append(dn)

        # Assign a preliminary name per signature group (shortest leaf name)
        # and mark all but the canonical as duplicates
        sig_to_name: Dict[tuple, str] = {}
        for sig, group in sig_to_dotted.items():
            # Prefer the shortest dotted path as canonical (most "generic" location)
            canonical = min(group, key=lambda n: (len(n.split('.')), n))
            leaf = canonical.split('.')[-1]
            sig_to_name[sig] = leaf
            for dn in group:
                self.name_map[dn] = leaf
                if dn != canonical:
                    self.classes[dn]['_duplicate_of'] = canonical

        # --- Step 2: resolve leaf-name collisions across different signatures ---
        # Find output names claimed by more than one signature
        name_to_sigs: Dict[str, List[tuple]] = {}
        for sig, name in sig_to_name.items():
            name_to_sigs.setdefault(name, []).append(sig)

        for name, sigs in name_to_sigs.items():
            if len(sigs) == 1:
                continue  # no collision

            # Qualify each conflicting signature with its canonical class's parent name
            new_names: Dict[tuple, str] = {}
            for sig in sigs:
                canonical = min(sig_to_dotted[sig], key=lambda n: (len(n.split('.')), n))
                parts = canonical.split('.')
                parent = parts[-2] if len(parts) >= 2 else ''
                qualified = parent + name if parent else name
                new_names[sig] = qualified

            # Iteratively try deeper ancestors until all names are unique
            # (ancestor_level=1 is parent, 2 is grandparent, etc.)
            for ancestor_level in range(2, 8):
                still_colliding: Dict[str, List[tuple]] = {}
                for sig, qname in new_names.items():
                    still_colliding.setdefault(qname, []).append(sig)

                any_collision = False
                for qname, qsigs in still_colliding.items():
                    if len(qsigs) <= 1:
                        continue
                    any_collision = True
                    for sig in qsigs:
                        canonical = min(sig_to_dotted[sig], key=lambda n: (len(n.split('.')), n))
                        parts = canonical.split('.')
                        idx = max(0, len(parts) - 1 - ancestor_level)
                        ancestor = parts[idx] if idx < len(parts) - 1 else ''
                        new_names[sig] = ancestor + name if ancestor else name

                if not any_collision:
                    break

            # Numeric suffix only as absolute last resort
            final_check: Dict[str, List[tuple]] = {}
            for sig, qname in new_names.items():
                final_check.setdefault(qname, []).append(sig)

            for qname, qsigs in final_check.items():
                if len(qsigs) <= 1:
                    continue
                for i, sig in enumerate(qsigs[1:], start=2):
                    new_names[sig] = f"{qname}_{i}"

            # Apply the resolved names
            for sig, resolved_name in new_names.items():
                sig_to_name[sig] = resolved_name
                for dn in sig_to_dotted[sig]:
                    self.name_map[dn] = resolved_name

    # -------------------------------------------------------------------------
    # Type reference resolution
    # -------------------------------------------------------------------------

    def resolve_type_ref(self, type_name: str, context_dotted: str) -> str:
        """
        Given a bare type name (e.g. 'Attributes') and the dotted path of the class
        that contains the reference, walk up the scope chain to find the matching
        dotted class name, then return its output name.
        """
        parts = context_dotted.split('.')
        # Walk from innermost scope outward
        for i in range(len(parts), 0, -1):
            candidate = '.'.join(parts[:i]) + '.' + type_name
            if candidate in self.name_map:
                return self.name_map[candidate]
        # Top-level reference
        if type_name in self.name_map:
            return self.name_map[type_name]
        # Not found — return as-is (primitive or external)
        return type_name

    def resolve_type_string(self, type_str: str, context_dotted: str) -> str:
        """Resolve all class references inside a type annotation string."""
        primitives = {'str', 'int', 'float', 'bool', 'Decimal', 'Any', 'object', 'None',
                      'Optional', 'List', 'list', 'Tuple', 'Dict', 'Set'}

        def replace_ref(m: re.Match) -> str:
            token = m.group(0)
            # Dotted reference (e.g. DsbXml.Site.Buildings) — look up directly in name_map
            if '.' in token:
                if token in self.name_map:
                    return self.name_map[token]
                return token
            # Simple identifier
            if token in primitives:
                return token
            return self.resolve_type_ref(token, context_dotted)

        # Match dotted identifiers first, then simple identifiers
        return re.sub(r'\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\b|\b[A-Za-z_][A-Za-z0-9_]*\b',
                      replace_ref, type_str)

    # -------------------------------------------------------------------------
    # Code generation
    # -------------------------------------------------------------------------

    def generate_pydantic_models(self) -> str:
        """Generate Pydantic model code from extracted classes."""
        lines = [
            "# Auto-generated Pydantic models from xsdata",
            "# DO NOT EDIT MANUALLY - regenerate using convert_xsdata_to_pydantic.py",
            "",
            "from __future__ import annotations",
            "",
            "from decimal import Decimal",
            "from typing import Any, Optional",
            "from pydantic_xml import attr, element",
            "from db_schema.base import BaseModel",
            "",
        ]

        # Emit root class first, then all others sorted
        lines.extend(self.generate_dsbxml_class())
        lines.append("")

        emitted_names: set = {'dsbXML'}

        for class_name in sorted(self.classes.keys()):
            if class_name == 'DsbXml':
                continue
            if '_duplicate_of' in self.classes[class_name]:
                continue

            output_name = self.name_map.get(class_name)
            if not output_name or output_name in emitted_names:
                continue

            class_lines = self.generate_pydantic_class(class_name)
            if class_lines:
                lines.extend(class_lines)
                lines.append("")
                emitted_names.add(output_name)

        return "\n".join(lines)

    def generate_dsbxml_class(self) -> List[str]:
        """Generate the special dsbXML root class."""
        return [
            "class dsbXML(BaseModel):",
            "    name: str = attr()",
            "    date: str = attr()  # TODO: convert to datetime.date",
            "    version: str = attr()",
            "    objects: str = attr()",
            "    site: 'Site' = element(tag='Site')",
            "",
            "    @classmethod",
            "    def from_xml(cls, source: str | bytes) -> dsbXML:",
            "        from lxml import etree",
            "        if isinstance(source, (str, bytes)):",
            "            root = etree.fromstring(source)",
            "        else:",
            "            root = source",
            "        return super().from_xml_tree(root)",
        ]

    def generate_pydantic_class(self, class_name: str) -> List[str]:
        """Generate a single Pydantic model class."""
        class_info = self.classes[class_name]

        if not class_info['fields'] or class_name.startswith('_'):
            return []

        output_name = self.name_map[class_name]
        lines = [f"class {output_name}(BaseModel):"]

        for field in class_info['fields']:
            lines.append(self.generate_field_line(field, class_name))

        return lines

    def generate_field_line(self, field: Dict[str, Any], context_dotted: str = "") -> str:
        """Generate a single field definition line."""
        name = field['name']
        field_type = field['type']
        is_attr = field['is_attribute']
        xml_tag = field['xml_tag']
        is_optional = field['is_optional']

        # Resolve type references through the scope graph
        field_type = self.resolve_type_string(field_type, context_dotted)

        # Handle 'object' type
        if field_type == 'object':
            field_type = 'Any'

        # Normalize union syntax to Optional
        field_type = field_type.replace('None | ', 'Optional[').replace(' | None', ']')
        if field_type.startswith('Optional[') and not field_type.endswith(']'):
            field_type += ']'

        # Quote complex forward references
        primitives_prefixes = ('str', 'int', 'float', 'bool', 'Decimal', 'list', 'Optional', 'Any')
        if not is_attr and not any(field_type.startswith(p) for p in primitives_prefixes):
            if field_type.startswith('Optional['):
                inner = field_type[9:-1]
                field_type = f"Optional['{inner}']"
            elif not field_type.startswith("'"):
                field_type = f"'{field_type}'"

        # Build field definition
        if is_attr:
            field_def = "attr()"
        else:
            field_def = f"element(tag='{xml_tag}')" if xml_tag != name else "element()"
            if is_optional and ', default=None' not in field_def:
                field_def = field_def.replace(")", ", default=None)")

        return f"    {name}: {field_type} = {field_def}"


def main():
    """Main entry point."""
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    converter = XsdataConverter(str(script_dir / "designbuilder_schema_generated.py"))

    print(f"Extracted {len(converter.classes)} xsdata classes")

    unique_output = len({n for n in converter.name_map.values()})
    print(f"Unique output classes after deduplication: {unique_output}")

    pydantic_code = converter.generate_pydantic_models()

    output_file = project_root / "db_schema" / "generated_models.py"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pydantic_code)

    print(f"Generated {output_file}")


if __name__ == '__main__':
    main()
