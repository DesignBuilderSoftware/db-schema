"""Tests for the load_model cache and file-format guards in dsbxml.utils."""

from pathlib import Path

import pytest

utils = pytest.importorskip("dsbxml.utils", reason="dsbxml.utils failed to import")

load_model = utils.load_model
save_model = utils.save_model
clear_model_cache = utils.clear_model_cache

repo_root = Path(__file__).parent.parent.parent
EMPTY_SITE = repo_root / "samples" / "models" / "EmptySite.xml"


@pytest.fixture()
def sample_path():
    if not EMPTY_SITE.exists():
        pytest.skip("EmptySite.xml sample not found")
    return EMPTY_SITE


@pytest.fixture(autouse=True)
def _fresh_cache():
    clear_model_cache()
    yield
    clear_model_cache()


class TestFileFormatGuards:
    @pytest.mark.parametrize("bad_name", ["model.dsb", "model.json", "model"])
    def test_load_model_rejects_non_xml(self, bad_name):
        with pytest.raises(ValueError, match="Unsupported file format"):
            load_model(bad_name)

    def test_save_model_rejects_non_xml(self, sample_path):
        model = load_model(sample_path, use_cache=False)
        with pytest.raises(ValueError, match="Unsupported file format"):
            save_model(model, "out.dsb")

    def test_load_model_accepts_path_object(self, sample_path):
        model = load_model(Path(sample_path), use_cache=False)
        assert model is not None


class TestModelCache:
    def test_cached_loads_return_same_object(self, sample_path):
        m1 = load_model(sample_path)
        m2 = load_model(sample_path)
        assert m1 is m2

    def test_uncached_load_returns_new_object(self, sample_path):
        m1 = load_model(sample_path)
        m2 = load_model(sample_path, use_cache=False)
        assert m1 is not m2

    def test_clear_model_cache_forces_reload(self, sample_path):
        m1 = load_model(sample_path)
        clear_model_cache()
        m2 = load_model(sample_path)
        assert m1 is not m2

    def test_cache_key_uses_resolved_path(self, sample_path):
        # A relative-style path spelling of the same file hits the same entry.
        alias = sample_path.parent / ".." / "models" / sample_path.name
        m1 = load_model(sample_path)
        m2 = load_model(alias)
        assert m1 is m2


class TestSiteCounterSync:
    def test_load_model_updates_site_counter(self, sample_path):
        from dsbxml.id import current_site_handle, set_site_counter

        set_site_counter(0)
        model = load_model(sample_path, use_cache=False)
        if model.site is None:
            pytest.skip("Sample has no parsed site")
        assert current_site_handle() == model.site.handle
