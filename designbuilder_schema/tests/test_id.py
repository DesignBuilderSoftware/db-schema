"""Tests for the id module"""

import pytest

from designbuilder_schema.id import (
    ObjectIDs,
    current_site_handle,
    generate_site_handle,
    set_site_counter,
)


class TestSiteHandleFunctions:
    """Test site handle management functions"""

    def test_set_site_counter(self):
        """Test setting the site counter"""
        set_site_counter(100)
        assert current_site_handle() == 100

    def test_generate_site_handle_increments(self):
        """Test that generate_site_handle increments the counter"""
        set_site_counter(50)
        handle1 = generate_site_handle()
        handle2 = generate_site_handle()
        assert handle1 == 50
        assert handle2 == 51
        assert current_site_handle() == 52

    def test_current_site_handle(self):
        """Test getting current site handle"""
        set_site_counter(42)
        assert current_site_handle() == 42


class TestObjectIDs:
    """Test ObjectIDs class functionality"""

    def test_object_ids_creation_with_defaults(self):
        """Test creating ObjectIDs with default values"""
        set_site_counter(0)
        obj_id = ObjectIDs()
        assert obj_id.handle == 0
        assert obj_id.buildingHandle == -1
        assert obj_id.buildingBlockHandle == -1
        assert obj_id.zoneHandle == -1
        assert obj_id.surfaceIndex == -1
        assert obj_id.openingIndex == -1

    def test_object_ids_auto_increment_handle(self):
        """Test that handle auto-increments for new instances"""
        set_site_counter(0)
        obj1 = ObjectIDs()
        obj2 = ObjectIDs()
        obj3 = ObjectIDs()
        assert obj1.handle == 0
        assert obj2.handle == 1
        assert obj3.handle == 2

    def test_object_ids_creation_with_custom_values(self):
        """Test creating ObjectIDs with custom values"""
        obj_id = ObjectIDs(
            buildingHandle=10,
            buildingBlockHandle=20,
            zoneHandle=30,
            surfaceIndex=5,
            openingIndex=3,
        )
        assert obj_id.buildingHandle == 10
        assert obj_id.buildingBlockHandle == 20
        assert obj_id.zoneHandle == 30
        assert obj_id.surfaceIndex == 5
        assert obj_id.openingIndex == 3

    def test_object_ids_unique_handles(self):
        """Test that each ObjectID gets a unique handle"""
        set_site_counter(0)
        handles = [ObjectIDs().handle for _ in range(10)]
        assert len(handles) == len(set(handles))
        assert handles == list(range(10))

    def test_object_ids_undefined_handle_is_negative_one(self):
        """Test that undefined handles default to -1"""
        obj_id = ObjectIDs()
        assert obj_id.buildingHandle == -1
        assert obj_id.buildingBlockHandle == -1
        assert obj_id.zoneHandle == -1
        assert obj_id.surfaceIndex == -1
        assert obj_id.openingIndex == -1
