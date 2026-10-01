from pathlib import Path

import pytest

from dsbxml import load_model
from dsbxml.diffing import diff_models

repo_root = Path(__file__).parent.parent.parent


def _sample(name: str):
    path = repo_root / "samples/models_dhvac" / name
    if not path.exists():
        pytest.skip(f"{path} not found")
    return load_model(path, use_cache=False)


class TestDiffModels:
    def test_identical_model_has_no_changes(self):
        model = _sample("1.xml")
        diff = diff_models(model, model)
        assert not diff.has_changes
        assert not diff.added
        assert not diff.removed
        assert not diff.attribute_changes

    def test_handle_only_differences_are_ignored(self):
        model_a = _sample("1.xml")
        model_b = _sample("1.xml")

        surface = (
            model_b.site.buildings.building[0]
            .building_blocks.building_block[0]
            .zones.zone[0]
            .body.surfaces.surface[0]
        )
        surface.object_ids.buildingHandle = surface.object_ids.buildingHandle + 1000
        surface.object_ids.buildingBlockHandle = 999

        diff = diff_models(model_a, model_b)
        assert not diff.has_changes

    def test_changed_name_is_reported_as_attribute_change(self):
        model_a = _sample("1.xml")
        model_b = _sample("1.xml")
        model_b.name = "Renamed"

        diff = diff_models(model_a, model_b)
        matches = [c for c in diff.attribute_changes if c["path"] == "name"]
        assert matches == [{"path": "name", "old": model_a.name, "new": "Renamed"}]

    def test_added_and_removed_surfaces_are_reported(self):
        model_a = _sample("1.xml")
        model_b = _sample("1.xml")

        surfaces = (
            model_b.site.buildings.building[0]
            .building_blocks.building_block[0]
            .zones.zone[0]
            .body.surfaces.surface
        )
        surfaces.pop()

        diff = diff_models(model_a, model_b)
        assert len(diff.removed.get("surfaces", [])) == 1

    def test_summary_is_human_readable(self):
        model_a = _sample("1.xml")
        model_b = _sample("2.xml")
        diff = diff_models(model_a, model_b)
        summary = diff.summary()
        assert isinstance(summary, str)
        assert summary  # non-empty: 1.xml and 2.xml genuinely differ
