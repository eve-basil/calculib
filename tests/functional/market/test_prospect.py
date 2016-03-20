import pytest

from basil.industry import facility as f
from basil.market import prospect as p
from tests import *


def test_myrmidon(mocker, system, prices, names):
    mocker.patch('basil.market.PRICES_FUNC', new=prices)
    mocker.patch('basil.market.NAMES_FUNC', new=names)
    mocker.patch('basil.market.VALUES_FUNC', return_value=35250667)

    blueprint = myrmidon_bp()
    facilities = [f.NPCStation('test station', system),
                  f.MediumShipAssemblyArray('test pos', system)]
    prospect = p.prospect(blueprint, facilities)

    assert_that(prospect, has_length(2))
    assert_that(prospect[0], has_property('facility', instance_of(
        f.MediumShipAssemblyArray)))
    assert_that(prospect[1], has_property('facility', instance_of(
        f.NPCStation)))
    assert_that(prospect[0], has_property('cost_per_unit', less_than(
        prospect[1].cost_per_unit)))


@pytest.fixture(scope="module")
def prices():
    data = {34: {"sell": {"max": 11.14, "avg": 6.68, "median": 6.53,
                          "stddev": 0.58, "min": 4.0},
                 "buy": {"max": 6.29, "avg": 5.96, "median": 6.17,
                         "stddev": 0.81, "min": 2.01},
                 "updated_at": "2006-01-19T07:37:25Z",
                 "system_id": 30000142,
                 "recorded_at": "2006-01-19T07:37:25Z", "id": 34},
            35: {"sell": {"max": 11.14, "avg": 6.68, "median": 6.53,
                          "stddev": 0.58, "min": 8.0},
                 "buy": {"max": 6.29, "avg": 5.96, "median": 6.17,
                         "stddev": 0.81, "min": 2.01},
                 "updated_at": "2006-01-19T07:37:25Z",
                 "system_id": 30000142,
                 "recorded_at": "2006-01-19T07:37:25Z", "id": 35},
            36: {"sell": {"max": 11.14, "avg": 6.68, "median": 6.53,
                          "stddev": 0.58, "min": 32.0},
                 "buy": {"max": 6.29, "avg": 5.96, "median": 6.17,
                         "stddev": 0.81, "min": 2.01},
                 "updated_at": "2006-01-19T07:37:25Z",
                 "system_id": 30000142,
                 "recorded_at": "2006-01-19T07:37:25Z", "id": 36},
            37: {"sell": {"max": 11.14, "avg": 6.68, "median": 6.53,
                          "stddev": 0.58, "min": 64.0},
                 "buy": {"max": 6.29, "avg": 5.96, "median": 6.17,
                         "stddev": 0.81, "min": 2.01},
                 "updated_at": "2006-01-19T07:37:25Z",
                 "system_id": 30000142,
                 "recorded_at": "2006-01-19T07:37:25Z", "id": 37},
            38: {"sell": {"max": 11.14, "avg": 6.68, "median": 6.53,
                          "stddev": 0.58, "min": 128.0},
                 "buy": {"max": 6.29, "avg": 5.96, "median": 6.17,
                         "stddev": 0.81, "min": 2.01},
                 "updated_at": "2006-01-19T07:37:25Z",
                 "system_id": 30000142,
                 "recorded_at": "2006-01-19T07:37:25Z", "id": 38},
            39: {"sell": {"max": 11.14, "avg": 6.68, "median": 6.53,
                          "stddev": 0.58, "min": 512.0},
                 "buy": {"max": 6.29, "avg": 5.96, "median": 6.17,
                         "stddev": 0.81, "min": 2.01},
                 "updated_at": "2006-01-19T07:37:25Z",
                 "system_id": 30000142,
                 "recorded_at": "2006-01-19T07:37:25Z", "id": 39},
            40: {"sell": {"max": 11.14, "avg": 6.68, "median": 6.53,
                          "stddev": 0.58, "min": 1024.0},
                 "buy": {"max": 6.29, "avg": 5.96, "median": 6.17,
                         "stddev": 0.81, "min": 2.01},
                 "updated_at": "2006-01-19T07:37:25Z",
                 "system_id": 30000142,
                 "recorded_at": "2006-01-19T07:37:25Z", "id": 40},
            24700: {"sell": {"max": 11.14, "avg": 6.68, "median": 6.53,
                             "stddev": 0.58, "min": 1024.0},
                    "buy": {"max": 58000000, "avg": 5.96, "median": 6.17,
                            "stddev": 0.81, "min": 2.01},
                    "updated_at": "2006-01-19T07:37:25Z",
                    "system_id": 30000142,
                    "recorded_at": "2006-01-19T07:37:25Z", "id": 24701},
            }

    def get_price(key):
        return data[key]

    return get_price


@pytest.fixture(scope="module")
def names():
    data = {34: "Tritanium", 35: "Pyerite", 36: "Mexallon", 38: "Nocxium",
            39: "Zydrine", 40: "Megacyte", 24700: "Myrmidon"}

    def get_name(key):
        return data[key]

    return get_name


@pytest.fixture(scope="module")
def system():
    root_url = 'https://public-crest.eveonline.com'
    system = {"systemCostIndices":
              [{"costIndex": 0.001603724208963802, "activityID": 8,
                "activityID_str": "8", "activityName": "Invention"},
               {"costIndex": 0.028218277926758743, "activityID": 1,
                "activityID_str": "1", "activityName": "Manufacturing"},
               {"costIndex": 0.02078652725944311, "activityID": 3,
                "activityID_str": "3",
                "activityName": "Researching Time Efficiency"},
               {"costIndex": 0.00545216917033242, "activityID": 4,
                "activityID_str": "4",
                "activityName": "Researching Material Efficiency"},
               {"costIndex": 0.00580479643586028, "activityID": 5,
                "activityID_str": "5", "activityName": "Copying"}],
              "solarSystem": {"id_str": "32112312",
                              "href": root_url + "/solarsystems/30011392/",
                              "id": 32112312, "name": "TestSystem"}}
    return system


def myrmidon_bp():
    return {"skills": [{"typeID": 3380, "level": 1}],
            "materials": [{"typeID": 34, "quantity": 3166667},
                          {"typeID": 35, "quantity": 711111},
                          {"typeID": 36, "quantity": 233333},
                          {"typeID": 38, "quantity": 14444},
                          {"typeID": 39, "quantity": 5556},
                          {"typeID": 40, "quantity": 2666}],
            "products": [{"typeID": 24700, "quantity": 1}],
            "time": 15000, "itemID": 317301623, "typeID": 24701, "flagID": 63,
            "locationID": 648230613, "typeName": "Myrmidon Blueprint",
            "quantity": -1, "timeEfficiency": 16, "materialEfficiency": 10,
            "runs": -1, "me": 10, "te": 16}
