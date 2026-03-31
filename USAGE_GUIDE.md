# DesignBuilder Schema - Usage Guide

A comprehensive guide to using the `designbuilder_schema` library for loading, modifying, and saving DesignBuilder XML models.

## Overview

The `designbuilder_schema` library provides Pydantic-based models for DesignBuilder simulation files. It enables you to:

- **Load** DesignBuilder XML files into Python objects
- **Modify** building models programmatically
- **Save** changes back to XML format
- **Validate** data integrity automatically via Pydantic

## Installation

```bash
pip install designbuilder-schema
```

## Quick Start

### Loading a Model

```python
from designbuilder_schema import load_model

# Load a DesignBuilder XML file
model = load_model("my_building.xml")

# Access top-level properties
print(f"Model name: {model.name}")
print(f"Version: {model.version}")
print(f"Date: {model.date}")

# Access site information
if model.site:
    print(f"Site name: {model.site.attributes.name if model.site.attributes else 'N/A'}")
    print(f"Site handle: {model.site.handle}")
```

### Modifying a Model

```python
from designbuilder_schema import load_model, save_model

# Load the model
model = load_model("my_building.xml")

# Modify the name
model.name = "Updated Building Model"

# Save changes back to XML
save_model(model, "my_building_updated.xml")
```

### Accessing Building Structures

```python
# Access buildings
if model.site and model.site.buildings:
    for building in model.site.buildings.building:
        print(f"Building: {building.attributes.name if building.attributes else 'Unknown'}")

        # Access building blocks within each building
        if building.building_blocks:
            for block in building.building_blocks.building_block:
                print(f"  Block: {block.attributes.name if block.attributes else 'Unknown'}")

                # Access zones within each building block
                if block.zones:
                    for zone in block.zones.zone:
                        print(f"    Zone: {zone.attributes.name if zone.attributes else 'Unknown'}")
```

## Common Tasks

### Creating a New Zone

```python
from designbuilder_schema.core import Zone
from designbuilder_schema.geometry import Point3D
from designbuilder_schema.attributes import NameAttributes
from designbuilder_schema.id import ObjectIDs, generate_site_handle

# Create a new zone
zone = Zone(
    object_ids=ObjectIDs(
        handle=generate_site_handle(),
        buildingHandle=-1,
        buildingBlockHandle=-1,
        zoneHandle=-1,
        surfaceIndex=-1,
        openingIndex=-1
    ),
    attributes=NameAttributes(
        name="New Zone",
        description=""
    ),
    zone_geometry=None,
    air_temperature_difference=0.0
)

# The zone is now ready to be added to a building block
```

### Working with Geometry

```python
from designbuilder_schema.geometry import Point3D, Vertices

# Create a 3D point
point = Point3D(value="0, 0, 0")

# Access coordinates
x = point.x  # float
y = point.y  # float
z = point.z  # float
coords = point.coords  # tuple[float, float, float]

# Create a polygon from vertices
vertices = Vertices()
vertices.append("0, 0, 0")
vertices.append("1, 0, 0")
vertices.append("1, 1, 0")
vertices.append("0, 1, 0")
```

### Accessing HVAC Systems

```python
# Lazy loading: HVAC modules are imported only when accessed
from designbuilder_schema import HVACNetwork, HVACComponents

# Access HVAC loops (if present)
if model.site and hasattr(model.site, 'hvac_network'):
    hvac = model.site.hvac_network
    if hvac and hvac.hvac_loops:
        for loop in hvac.hvac_loops.hvac_loop:
            print(f"Loop type: {loop.loopType}")
```

### Working with Attributes

The library supports named attributes for most model elements:

```python
from designbuilder_schema.attributes import NameAttributes

# Create or modify attributes
attrs = NameAttributes(
    name="Element Name",
    description="Element description"
)

# Access attributes
print(f"Name: {attrs.name}")
print(f"Description: {attrs.description}")
```

## Error Handling

### File Not Found

```python
from designbuilder_schema import load_model

try:
    model = load_model("nonexistent.xml")
except FileNotFoundError:
    print("File not found. Check the file path.")
```

### Invalid File Format

```python
from designbuilder_schema import load_model

try:
    model = load_model("document.pdf")  # Wrong format
except ValueError as e:
    print(f"Error: {e}")  # "Unsupported file format: .pdf"
```

### XML Parsing Errors

```python
from designbuilder_schema import load_model

try:
    model = load_model("corrupted.xml")
except Exception as e:
    print(f"Failed to parse XML: {e}")
```

## Performance Considerations

### Import Time Optimization

The library uses lazy loading to minimize import overhead:

```python
# Fast import - HVAC modules not loaded yet
import designbuilder_schema

# Only when accessed, HVAC modules are loaded
hvac_net = designbuilder_schema.HVACNetwork  # Lazy load happens here
```

If you know you'll be using HVAC features, you can import explicitly to avoid the lazy loading overhead:

```python
from designbuilder_schema import HVACNetwork, HVACComponents
```

### Large File Handling

For very large DesignBuilder files:

```python
from designbuilder_schema import load_model

# Load the file (will use all available memory)
model = load_model("large_model.xml")

# Process specific elements
if model.site:
    # Work with data incrementally
    for building in model.site.buildings.building:
        process_building(building)
        # Optionally clear processed data to free memory
```

## Validation and Type Checking

The library uses Pydantic for automatic validation:

```python
from designbuilder_schema.attributes import NameAttributes

# Valid creation
attrs = NameAttributes(name="Test", description="Desc")

# Pydantic validates types automatically
attrs.name = "New Name"  # OK - string
try:
    attrs.name = 123  # Would fail - wrong type
except Exception as e:
    print(f"Validation error: {e}")
```

## Advanced Topics

### Accessing Forward References

Some nested models use forward references (string type hints). These are resolved automatically:

```python
# No need to worry about forward references - they're resolved internally
if model.site:
    # This works seamlessly
    site = model.site
    buildings = site.buildings  # Type annotations work correctly
```

### Working with Handles and ObjectIDs

All model elements have unique handles:

```python
from designbuilder_schema.id import current_site_handle, generate_site_handle

# Get the current highest handle
current = current_site_handle()

# Generate a new unique handle
new_handle = generate_site_handle()

# These are used in ObjectIDs for tracking unique elements
```

### Round-Trip Integrity

The library maintains data integrity through save/load cycles:

```python
from designbuilder_schema import load_model, save_model

# Load original
model1 = load_model("original.xml")

# Modify and save
model1.name = "Modified"
save_model(model1, "modified.xml")

# Load modified version
model2 = load_model("modified.xml")

# Verify changes persisted
assert model2.name == "Modified"
```

## API Reference

### Core Functions

#### `load_model(filepath: str | Path) -> dsbXML`

Load and validate a DesignBuilder XML file.

- **Parameters:**
  - `filepath`: Path to the XML file (str or Path)
- **Returns:** dsbXML model instance
- **Raises:** FileNotFoundError, ValueError

#### `save_model(model: dsbXML, filepath: str | Path) -> None`

Save a DesignBuilder model to XML file.

- **Parameters:**
  - `model`: dsbXML instance to save
  - `filepath`: Output path (str or Path)
- **Raises:** ValueError for invalid formats

### Model Classes

The library provides Pydantic models for all DesignBuilder elements:

- **dsbXML** - Root model (alias: DSB)
- **Site** - Building site container
- **Building** - Individual building
- **BuildingBlock** - Building subdivision
- **Zone** - Thermal zone
- **Surface** - Building surface
- **Body** - Surface geometry

### Geometry Classes

- **Point3D** - 3D coordinates
- **Vertices** - Polygon vertices
- **Line** - Line segment with object IDs
- **Range** - Numeric range specification

### HVAC Classes (Lazy Loaded)

- **HVACNetwork** - HVAC system network
- **HVACComponents** - HVAC component collection

## Troubleshooting

### "Module has no attribute X"

Check that the module is correctly imported. For HVAC features, make sure to access them correctly:

```python
# Wrong
from designabilder_schema import HVACNetwork  # Typo!

# Right
from designbuilder_schema import HVACNetwork
# Or
import designbuilder_schema
hvac_net = designbuilder_schema.HVACNetwork
```

### Model attributes are None

Some elements are optional in the DesignBuilder format:

```python
if model.site is not None:
    # Safe to access
    ...

if model.site and model.site.buildings:
    # Nested check for optional elements
    for building in model.site.buildings.building:
        ...
```

### Changes not saved

Always use `save_model()` to persist changes:

```python
model = load_model("file.xml")
model.name = "New Name"

# This is necessary to save changes
save_model(model, "file.xml")
```

## Contributing

Contributions are welcome! The library is structured for extensibility:

- Model classes are in `designbuilder_schema/`
- Tests are in `designbuilder_schema/tests/`
- Integration tests verify round-trip integrity
- Type hints are used throughout for IDE support

## License

See the main project README for license information.
