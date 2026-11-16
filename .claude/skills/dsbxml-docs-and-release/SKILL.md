---
name: dsbxml-docs-and-release
description: Use when editing or building the db-schema (dsbxml) docs site, the usage guide or the generated schema reference, or when releasing dsbxml to PyPI.
---

# dsbxml docs and releases

## Docs

- Sources: `docs_src/` (MkDocs Material, config `mkdocs.yml`). `docs_src/guide.md` is one line, `--8<-- "USAGE_GUIDE.md"`, so edit `USAGE_GUIDE.md` at the repo root, never the guide page.
- `USAGE_GUIDE.md`'s Python blocks are run in order by `dsbxml/tests/test_usage_guide.py` against `samples/2026.1.0.013/Shoebox261.xml` copied to `building.xml`. Run it after editing the guide: `uv run pytest dsbxml/tests/test_usage_guide.py -q`.
- The element reference page (`schema/elements.md`) is generated at build time from `dsbxml/DesignBuilder.xsd` by the MkDocs hook `scripts/docs_xsd_reference.py`; `uv run python scripts/docs_xsd_reference.py > elements.md` prints it.
- The API pages use mkdocstrings (Google docstring style) over the package.

Build as CI does, into an untracked folder:

```bash
uv sync --extra dev
uv run mkdocs build --strict -d site
```

`mkdocs.yml` sets `site_dir: docs`, and `docs/` is a committed built site (last rebuilt in September 2026, before the generated schema reference existed). A plain `uv run mkdocs build` overwrites `docs/`; do that only when the owner wants the published site refreshed, and in its own commit. The GitHub Pages deploy workflow was removed (`95323c0`).

## Release

1. Bump `version` in `pyproject.toml` (the history uses separate "Bump version to X.Y.Z" commits merged to `main`).
2. Create a GitHub Release with tag `vX.Y.Z`. `.github/workflows/publish.yml` runs on `release: published`, fails if the tag (without `v`) differs from `uv version --short`, then `uv build` and PyPI Trusted Publishing to `dsbxml`.
3. Publishing is the owner's call and can't be undone for that version; don't create the release unless asked.

Check before releasing: `uv run pytest -q` (about 8 minutes), the three lint commands in `run-tests.yml`, and the strict docs build. `uv build` locally shows what the wheel will contain; `DesignBuilder.xsd` must be in it (`[tool.setuptools.package-data]`).

Note: `.claude/` is git-ignored in this repo, so these skills and agents stay local.
