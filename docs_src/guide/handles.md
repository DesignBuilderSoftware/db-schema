# Handles

Objects are identified by integer handles held in their `ObjectIDs`. Handles
read from a file are kept as they are. New `ObjectIDs` take the next handle
from a site-wide counter, which `load_model` resets to the loaded site's
`handle`; the site's `handle` is written back as the counter's current
value.

```python
from dsbxml.id import ObjectIDs, current_site_handle

next_handle = current_site_handle()
new_ids = ObjectIDs()
assert new_ids.handle == next_handle
```

The counter is a module-level global (guarded by a lock), so it is shared
by every model in the process.
