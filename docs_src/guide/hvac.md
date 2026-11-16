# HVAC

Detailed HVAC lives on each building's `hvac_network`. Buildings without
detailed HVAC have an empty network, where `hvac_loops` is `None`.

```python
for building in model.site.buildings.building:
    network = building.hvac_network
    if network is None or network.hvac_loops is None:
        continue
    for loop in network.hvac_loops.hvac_loop:
        loop_name = {a.name: a.value for a in loop.attributes.attribute}.get("Title")
        print(loop.loopType, loop_name)
```
