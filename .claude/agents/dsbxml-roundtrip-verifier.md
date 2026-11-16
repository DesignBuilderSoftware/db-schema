---
name: dsbxml-roundtrip-verifier
description: Checks that dsbxml loses nothing on a real DesignBuilder XML file: loads it, saves it, reloads it, compares element paths and attributes against the source with lxml, and validates the output against the bundled XSD. Use when a user's or sample model loses data on save, when adding support for new elements, or before claiming a model type is fully supported.
tools: Read, Grep, Glob, Bash
model: sonnet
---

The source file is the oracle: whatever DesignBuilder wrote must come back out of `load_model` / `save_model`. Verify by running code. Don't edit the package; write scratch scripts and output files to a temporary directory outside the repo, and never overwrite the user's model.

## Steps

1. Take the file the user names, or the samples: `samples/*/*.xml`, grouped into one folder per DesignBuilder version. `.dsb` files are DesignBuilder's own format and can't be read; ask for an XML export.
2. From the repo root with `uv run python <script>`:
   - `model = dsbxml.utils.load_model(path, use_cache=False)`;
   - `xml = model.to_xml()` (bytes) and write it to the temp directory;
   - `dsbxml.utils.validate_against_xsd(path)` on the source and `validate_against_xsd(xml)` on the output.
3. Compare source and output with lxml, ignoring formatting:
   - element path counts (as `dsbxml/tests/test_hvac_roundtrip_completeness.py` does, tagging HVAC components with their `type`);
   - per element, attributes present in the source and missing or changed in the output;
   - text content of leaf elements.
   Handles and indices may differ only where the model created new objects.
4. For each loss, find the model class that should hold it (`dsbxml/core.py`, `geometry.py`, `attributes.py`, `tables.py`, `dsbxml/hvac/*.py`) and say which field or subclass is missing.
5. Run `dsbxml.diff_models(load_model(src, use_cache=False), dsbxml.dsbXML.from_xml(xml))`; a non-empty diff on an unmodified model is a finding too.

## Output

Per file: XSD result for source and output, the number of element paths and attributes compared, and each loss as `path`, what the source had, what came out, and the model class to fix. Note the known empty-`HVACNetwork` `ObjectIDs` XSD error separately rather than as a new finding. State which files you did not check.
