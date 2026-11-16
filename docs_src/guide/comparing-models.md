# Comparing two models

`diff_models` reports added and removed buildings, zones, surfaces and
openings, changed values, and HVAC changes. Handles and indices are
ignored because DesignBuilder renumbers them on every save.

```python
from dsbxml import diff_models

before = load_model("building.xml", use_cache=False)
after = load_model("building.xml", use_cache=False)
after.name = "Renamed"

diff = diff_models(before, after)
print(diff.has_changes)  # True
print(diff.summary())    # ~ name: '...' -> 'Renamed'
```
