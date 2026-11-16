# Examples

Short scripts from the
[`examples/`](https://github.com/DesignBuilderSoftware/db-schema/tree/main/examples)
folder. Each one loads a sample model from
[`samples/`](https://github.com/DesignBuilderSoftware/db-schema/tree/main/samples),
so run them from the root of a clone of the repository. The code below is
included from the scripts themselves, so it matches the repository.

## Read the model version

```python
--8<-- "examples/version.py"
```

## Load and save a model

```python
--8<-- "examples/load and save.py"
```

## Zone geometry

### Volume of the first zone

```python
--8<-- "examples/buildingblock body volume.py"
```

### Read and move a vertex

```python
--8<-- "examples/access point.py"
```

### Zone names and floor polygons

```python
--8<-- "examples/get zone name and floor polygon.py"
```

## Tables

Each table row is one string of `#`-prefixed values in `field_name` order.
This example reads and changes a value in the `Glazing` table.

```python
--8<-- "examples/table item acess.py"
```

## Detailed HVAC

### Component types in the air and plant loops

```python
--8<-- "examples/hvac component types.py"
```

### Zone component types

```python
--8<-- "examples/hvac zone component types.py"
```

### Components inside zone units

```python
--8<-- "examples/hvac unit component types.py"
```

### Zone groups and their zones

```python
--8<-- "examples/hvac_zone_groups_and_zones.py"
```
