# Geometry

Coordinates are stored as `"x;y;z"` text in `Point3D.value`; the `x`, `y`,
`z` and `coords` properties parse it, and assigning to them rewrites the
text.

```python
vertices = zone.body.vertices
point = vertices[0]
print(point.coords)  # [x, y, z] as floats

for point in vertices:
    print(point.x, point.y, point.z)

point.z = 3.0
```
