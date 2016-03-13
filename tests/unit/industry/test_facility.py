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
