# Loading and saving

```python
from dsbxml import load_model, save_model

model = load_model("building.xml")

print(model.name)     # model title, e.g. "~Shoebox261"
print(model.version)  # DesignBuilder version that wrote the file
print(model.date)     # datetime.date

model.name = "Updated building"
save_model(model, "building_updated.xml")
```

`load_model` and `save_model` accept a `str` or `pathlib.Path` and only
handle `.xml` files; any other suffix raises `ValueError`.

!!! warning "Loaded models are cached"
    `load_model` keeps the last 32 models in an LRU cache keyed by the
    file's resolved path, and returns the **same object** each time. A
    change made to one loaded model is therefore visible to every other
    caller that loaded the same path, and edits to the file on disk are not
    picked up. Pass `use_cache=False` to get a fresh, independent copy, or
    call `dsbxml.utils.clear_model_cache()`.

```python
from dsbxml.utils import clear_model_cache

fresh = load_model("building.xml", use_cache=False)
assert fresh is not load_model("building.xml")
clear_model_cache()
```
