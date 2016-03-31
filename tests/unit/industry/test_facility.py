from __future__ import absolute_import

import pytest

from tests import *

import basil.industry.facility as f


@pytest.fixture(scope="module")
def system():
    url = "https://public-crest.eveonline.com/solarsystems/30002054/"
    return {"systemCostIndices":
            [{"costIndex": 0.001, "activityID": 8, "activityID_str": "8",
              "activityName": "Invention"},
             {"costIndex": 0.005, "activityID": 1, "activityID_str": "1",
              "activityName": "Manufacturing"},
             {"costIndex": 0.004, "activityID": 3, "activityID_str": "3",
              "activityName": "Researching Time Efficiency"},
             {"costIndex": 0.003, "activityID": 4, "activityID_str": "4",
              "activityName": "Researching Material Efficiency"},
             {"costIndex": 0.002, "activityID": 5, "activityID_str": "5",
              "activityName": "Copying"}],
            "solarSystem":
                {"id_str": "30002054", "href": url, "id": 30002054,
                 "name": "Hror"}}


def test_manufacture_index(system):
    fac = f.IndustryFacility('test', system, 0)
    assert_that(fac, has_property('manufacture_index', equal_to(0.005)))


def test_invention_index(system):
    fac = f.IndustryFacility('test', system, 0)
    assert_that(fac, has_property('invention_index', equal_to(0.001)))


def test_copying_index(system):
    fac = f.IndustryFacility('test', system, 0)
    assert_that(fac, has_property('copying_index', equal_to(0.002)))


def test_material_research_index(system):
    fac = f.IndustryFacility('test', system, 0)
    assert_that(fac, has_property('material_research_index', equal_to(0.003)))


def test_time_research_index(system):
    fac = f.IndustryFacility('test', system, 0)
    assert_that(fac, has_property('time_research_index', equal_to(0.004)))


def test_facility_by_id_npc_station():
    with MockCaches(NPC_STATION):
        fac = f.facility(60002353)
        assert_that(fac, instance_of(f.NPCStation))
        assert_that(fac, has_property('tax_rate', equal_to(10)))
        assert_that(fac, has_property('material_bonus', equal_to(0)))
        assert_that(fac, has_property('time_bonus', equal_to(0)))
        assert_that(fac, has_property('manufacture_index',
                                      equal_to(0.031129044234844177)))
        assert_that(fac, has_property('invention_index',
                                      equal_to(0.07374034740779398)))


def test_facility_by_id_outpost():
    with MockCaches(OUTPOST):
        facts = {'me_bonus': 1, 'te_bonus': 20}
        fac = f.facility(61000123, **facts)
        assert_that(fac, instance_of(f.Outpost))
        assert_that(fac, has_property('tax_rate', equal_to(0)))
        assert_that(fac, has_property('material_bonus', equal_to(1)))
        assert_that(fac, has_property('time_bonus', equal_to(20)))
        assert_that(fac, has_property('manufacture_index',
                                      equal_to(0.0008284715648540996)))
        assert_that(fac, has_property('invention_index', equal_to(0.0006)))


def test_facility_by_dict():
    args = {'structure': 'EquipmentAssemblyArray', 'solar_system_id': 30000181}
    with MockCaches(NPC_STATION):
        fac = f.facility(None, **args)
        assert_that(fac, instance_of(f.EquipmentAssemblyArray))
        assert_that(fac, has_property('tax_rate', equal_to(0)))
        assert_that(fac, has_property('material_bonus', equal_to(2)))
        assert_that(fac, has_property('time_bonus', equal_to(25)))
        assert_that(fac, has_property('manufacture_index',
                                      equal_to(0.031129044234844177)))
        assert_that(fac, has_property('invention_index',
                                      equal_to(0.07374034740779398)))


def test_facility_by_dict_with_name():
    args = {'structure': 'EquipmentAssemblyArray',
            'solar_system_id': 30000181, 'name': 'TTP'}
    with MockCaches(NPC_STATION):
        fac = f.facility(None, **args)
        assert_that(fac, instance_of(f.EquipmentAssemblyArray))
        assert_that(fac, has_property('name', equal_to('TTP')))
        assert_that(fac, has_property('tax_rate', equal_to(0)))
        assert_that(fac, has_property('material_bonus', equal_to(2)))
        assert_that(fac, has_property('time_bonus', equal_to(25)))
        assert_that(fac, has_property('manufacture_index',
                                      equal_to(0.031129044234844177)))
        assert_that(fac, has_property('invention_index',
                                      equal_to(0.07374034740779398)))


class MockCaches(object):
    def __init__(self, cache):
        self._cache = cache

    def __enter__(self):
        self._orig_fac_cache = f.FAC_CACHE
        self._orig_sys_cache = f.SYS_CACHE
        f.FAC_CACHE = Wrapper(self._cache)
        f.SYS_CACHE = Wrapper(self._cache)

    def __exit__(self, exc_type, exc_val, exc_tb):
        f.FAC_CACHE = self._orig_fac_cache
        f.SYS_CACHE = self._orig_sys_cache


class Wrapper(object):
    def __init__(self, dictionary):
        self._dict = dictionary

    def get(self, key, blocking=False):
        return self._dict.get(key)


ROOT = 'https://public-crest.eveonline.com'
NPC_FAC = {"facilityID": 60002353,
           "solarSystem": {"id": 30000181, "id_str": "30000181"},
           "name": "Korsiki III - Moon 5 - Lai Dai Corporation Factory",
           "region": {"id": 10000002, "id_str": "10000002"},
           "tax": 0.1, "facilityID_str": "60002353",
           "owner": {"id": 1000020, "id_str": "1000020"},
           "type": {"id": 1529, "id_str": "1529"}}
NPC_SYS = {"systemCostIndices":
           [{"costIndex": 0.07374034740779398, "activityID": 8,
             "activityID_str": "8", "activityName": "Invention"},
            {"costIndex": 0.031129044234844177, "activityID": 1,
             "activityID_str": "1", "activityName": "Manufacturing"},
            {"costIndex": 0.05923129129743867, "activityID": 3,
             "activityID_str": "3",
             "activityName": "Researching Time Efficiency"},
            {"costIndex": 0.05672293125464553, "activityID": 4,
             "activityID_str": "4",
             "activityName": "Researching Material Efficiency"},
            {"costIndex": 0.05369976316936276, "activityID": 5,
             "activityID_str": "5", "activityName": "Copying"}],
           "solarSystem": {"id_str": "30000181",
                           "href": ROOT + "/solarsystems/30000181/",
                           "id": 30000181, "name": "Korsiki"}}
NPC_STATION = {60002353: NPC_FAC, 30000181: NPC_SYS}

OUT_FAC = {"facilityID": 61000123,
           "solarSystem": {"id": 30003767, "id_str": "30003767"},
           "name": "N8XA-L IV - MANIFEST DESTINY 15012",
           "region": {"id": 10000047, "id_str": "10000047"},
           "facilityID_str": "61000123",
           "owner": {"id": 1618223652, "id_str": "1618223652"},
           "type": {"id": 21646, "id_str": "21646"}}
OUT_SYS = {"systemCostIndices":
           [{"costIndex": 0.0006, "activityID": 8, "activityID_str": "8",
             "activityName": "Invention"},
            {"costIndex": 0.0008284715648540996, "activityID": 1,
             "activityID_str": "1", "activityName": "Manufacturing"},
            {"costIndex": 0.0006, "activityID": 3, "activityID_str": "3",
             "activityName": "Researching Time Efficiency"},
            {"costIndex": 0.0006, "activityID": 4, "activityID_str": "4",
             "activityName": "Researching Material Efficiency"},
            {"costIndex": 0.0006, "activityID": 5, "activityID_str": "5",
             "activityName": "Copying"}],
           "solarSystem": {"id_str": "30003767",
                           "href": ROOT + "/solarsystems/30003767/",
                           "id": 30003767, "name": "N8XA-L"}}
OUTPOST = {61000123: OUT_FAC, 30003767: OUT_SYS}
