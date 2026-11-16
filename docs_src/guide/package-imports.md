# Package imports

`dsbxml` loads its model classes lazily. Every class in `dsbxml.core`
(`dsbXML`, `Site`, `Building`, `Zone`, ...) is available from the package
root, as are `HVACNetwork`, `HVACComponents`, `diff_models`, `ModelDiff`
and `ModelValidationError`; `DSB` is a backwards-compatible alias for
`dsbXML`. Classes in the other modules are imported from their module,
e.g. `from dsbxml.geometry import Point3D`.
