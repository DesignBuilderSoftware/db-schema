# Attributes

Most DesignBuilder settings are stored as attribute lists rather than as
typed fields. The site and HVAC objects use `name`/value pairs
(`NameAttributes`); buildings, blocks, bodies, surfaces and openings use
`key`/value pairs (`KeyAttributes`). Values are strings, or `None` when the
element is empty.

```python
site_settings = {a.name: a.value for a in model.site.attributes.attribute}

building = model.site.buildings.building[0]
building_settings = {a.key: a.value for a in building.attributes.attribute}

zone = building.building_blocks.building_block[0].zones.zone[0]
zone_settings = {a.key: a.value for a in zone.body.attributes.attribute}
print(zone_settings["Title"])  # e.g. "Zone 1"
```
