# Model structure

Python attribute names are snake_case versions of the XML tags; each XML
container element (`<Buildings>`, `<Zones>`, ...) is a model whose list of
children has the singular name:

```text
dsbXML                      model
└── Site                    model.site
    ├── Attributes          model.site.attributes.attribute[]
    ├── Tables              model.site.tables.table[]
    ├── AssemblyLibrary     model.site.assembly_library.assembly[]
    └── Buildings           model.site.buildings.building[]
        └── Building
            ├── Attributes      building.attributes.attribute[]
            ├── BuildingBlocks  building.building_blocks.building_block[]
            │   └── BuildingBlock
            │       └── Zones   block.zones.zone[]
            │           └── Zone
            │               └── Body          zone.body
            │                   ├── Vertices  zone.body.vertices
            │                   └── Surfaces  zone.body.surfaces.surface[]
            │                       └── Surface
            │                           └── Openings  surface.openings.opening[]
            └── HVACNetwork     building.hvac_network
                ├── HVACLoops       .hvac_loops.hvac_loop[]
                └── HVACZoneGroups  .hvac_zone_groups.hvac_zone_group[]
```

Many elements are optional, so check for `None` before going deeper:

```python
for building in model.site.buildings.building:
    for block in building.building_blocks.building_block:
        if block.zones is None:
            continue
        for zone in block.zones.zone:
            print(zone.body.volume, len(zone.body.surfaces.surface))
```

The [schema element reference](../schema/elements.md) lists every element,
attribute and child the file format allows; the API reference documents
each Python model.
