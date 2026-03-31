# DesignBuilder Schema - Optimization Roadmap

## Current State
- **Test Coverage:** 97 passed, 1 skipped
- **LOC:** ~1,400 lines across 24 Python modules
- **Architecture:** pydantic-xml based XML serialization with forward references
- **Status:** Fully functional, no active users (optimization freedom!)

## Phase 1: Architecture Simplification

### 1.1 Eliminate AlwaysList Pattern (HIGH IMPACT)
**Current Problem:**
- `AlwaysList` is a custom type wrapper that validates List fields
- Adds complexity and indirection without clear value
- Only used in hvac/components.py for one field

**Proposed Solution:**
- Replace with direct List[int] + element() specifications
- Use pydantic validators for critical validation logic
- Simplifies field definitions and improves readability

**Files Affected:**
- designbuilder_schema/base.py (remove AlwaysList)
- designbuilder_schema/hvac/components.py (use List[int] directly)

---

### 1.2 Standardize Field Naming Convention (MEDIUM IMPACT)
**Current Problem:**
- XML uses PascalCase (ConnectingPlantLoopHandle)
- Python fields use snake_case (connecting_plant_loop_handle)
- Requires field renaming logic in from_xml()/to_xml()
- Creates cognitive overhead

**Proposed Solution:**
- Use pydantic-xml's `alias` parameter to map XML names to Python names
- Eliminates custom lowercase_tags() function
- Makes field purpose clearer in code

**Example:**
```python
connecting_plant_loop_handle: List[int] = element(
    tag="ConnectingPlantLoopHandle",
    alias="ConnectingPlantLoopHandle"
)
```

**Files Affected:**
- designbuilder_schema/core.py (remove lowercase_tags function)
- All HVAC component classes

---

### 1.3 Consolidate Model Rebuilding (MEDIUM IMPACT)
**Current Problem:**
- __init__.py has manual model_rebuild() loop
- Uses inspect to find all BaseXmlModel subclasses
- Fragile and catches all exceptions silently

**Proposed Solution:**
- Explicitly list required models to rebuild (safer, faster)
- Use pydantic's model_rebuild() more strategically
- Add clear error reporting

**Files Affected:**
- designbuilder_schema/__init__.py

---

## Phase 2: Performance Optimization

### 2.1 Lazy Imports (LOW-MEDIUM IMPACT)
**Current Problem:**
- All imports happen at module load time
- Creates circular dependency risks
- Slows down initial import for users who only need part of the schema

**Proposed Solution:**
- Move non-essential imports to function level
- Use TYPE_CHECKING guard for type hints
- Defer HVAC imports until actually needed

---

### 2.2 Optimize XML Serialization (MEDIUM IMPACT)
**Current Problem:**
- from_xml() applies lowercase_tags() recursively to entire tree
- Tree traversal happens even for minimal parsing
- tag renaming in to_xml() regenerates XML

**Proposed Solution:**
- Use pydantic-xml's native field mapping
- Eliminate custom tag manipulation
- Let pydantic-xml handle serialization directly

---

### 2.3 Add Caching for Parsed Models (LOW IMPACT)
**Current Problem:**
- Large XML files reparsed each time
- No caching of model instances

**Proposed Solution:**
- Add optional LRU cache for load_model()
- Document when cache invalidation is needed

---

## Phase 3: Code Quality

### 3.1 Reduce Forward References (MEDIUM IMPACT)
**Current Problem:**
- Excessive use of string type hints ("Point3D", "Site", etc.)
- Requires model_rebuild() to resolve
- Creates potential circular import issues

**Proposed Solution:**
- Reorganize imports to minimize forward references
- Use TYPE_CHECKING for circular dependencies
- Import at module level where safe

---

### 3.2 Simplify Field Definitions (MEDIUM IMPACT)
**Current Problem:**
- Inconsistent use of element() vs plain fields
- Some fields missing tag specifications
- Optional fields sometimes missing default=None

**Proposed Solution:**
- Create field definition helpers for common patterns
- Enforce consistency with type hints
- Example helper:

```python
def optional_element(type_hint, tag=None, **kwargs):
    """Helper for optional nested model elements"""
    return element(tag=tag, default=None, **kwargs)
```

---

### 3.3 Add Comprehensive Type Hints (LOW IMPACT)
**Current Problem:**
- Some functions missing return type hints
- Generic types not fully specified
- Makes IDE support weaker

**Proposed Solution:**
- Add return types to all public functions
- Use TypeVar for generic types where appropriate

---

## Phase 4: Testing & Validation

### 4.1 Add Integration Tests (MEDIUM IMPACT)
**Current Problem:**
- Tests are unit-level, no full XML round-trip validation
- No large file performance testing
- No real-world XML files tested

**Proposed Solution:**
- Add round-trip tests (load → modify → save → load)
- Test with actual DesignBuilder XML files
- Performance benchmarks for large models

---

### 4.2 Add Validation Tests (LOW-MEDIUM IMPACT)
**Current Problem:**
- No tests for invalid XML handling
- No tests for malformed data recovery
- Error messages could be better

**Proposed Solution:**
- Test invalid XML gracefully degrades
- Test with corrupt/incomplete files
- Improve error reporting

---

## Phase 5: Documentation

### 5.1 Add Usage Examples (MEDIUM IMPACT)
- Loading and saving models
- Modifying specific elements
- Working with complex nested structures

### 5.2 Add Migration Guide (LOW IMPACT)
- For users coming from xmltodict version
- Best practices for this library

---

## Implementation Priority

### Must-Do (Impact/Effort = High/Low):
1. **Eliminate AlwaysList** - Simplifies codebase, no test changes
2. **Add field definition helpers** - Reduces boilerplate
3. **Add integration tests** - Catches real-world issues

### Should-Do (Impact/Effort = Medium):
1. **Standardize field naming with aliases** - Cleaner code
2. **Consolidate model rebuilding** - More reliable
3. **Reduce forward references** - Better IDE support

### Nice-To-Have (Impact/Effort = Medium/High):
1. **Lazy imports** - Minor perf gain
2. **Add caching** - Useful for large files
3. **Comprehensive type hints** - Better IDE experience

---

## Estimated Timeline

- **Phase 1 (Architecture):** 2-3 hours
- **Phase 2 (Performance):** 1-2 hours
- **Phase 3 (Quality):** 1-2 hours
- **Phase 4 (Testing):** 2-3 hours
- **Phase 5 (Docs):** 1-2 hours

**Total:** ~9-12 hours for full optimization

---

## Success Metrics

After optimization, the library should have:
- [ ] Faster import time (measure with `python -c "import designbuilder_schema" -m timeit`)
- [ ] Cleaner code (fewer lines, clearer structure)
- [ ] Better error handling
- [ ] Complete test coverage with integration tests
- [ ] Clear documentation with examples

---

## Breaking Changes Risk Assessment

Since no one is using this code:
- ✅ Safe to refactor field names (using aliases preserves XML compatibility)
- ✅ Safe to remove unused patterns (AlwaysList)
- ✅ Safe to restructure imports
- ⚠️ Must maintain XML file compatibility (preserve load_model/save_model API)

---

## Next Steps

1. Review this roadmap
2. Prioritize which phases to tackle first
3. Create skills for automated refactoring
4. Run comprehensive tests after each phase
5. Document the improvements
