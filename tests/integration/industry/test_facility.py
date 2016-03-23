from tests import *

import basil.industry.facility as facil


# Expecting something like
#     [{"systemCostIndices":
#           [{"costIndex": 0.001603724208963802, "activityID": 8,
#             "activityID_str": "8", "activityName": "Invention"},
#            {"costIndex": 0.028218277926758743, "activityID": 1,
#             "activityID_str": "1", "activityName": "Manufacturing"},
#            {"costIndex": 0.02078652725944311, "activityID": 3,
#             "activityID_str": "3",
#             "activityName": "Researching Time Efficiency"},
#            {"costIndex": 0.00545216917033242, "activityID": 4,
#             "activityID_str": "4", "activityName":
#             "Researching Material Efficiency"},
#            {"costIndex": 0.00580479643586028, "activityID": 5,
#             "activityID_str": "5", "activityName": "Copying"}],
#       "solarSystem": {"id_str": "30011392", "href":
#           "https://public-crest.eveonline.com/solarsystems/30011392/",
#                       "id": 30011392, "name": "Jouvulen"}},]

def test_crest_systems():
    response = facil.systems()
    systems = {n['solarSystem']['name']: n for n in response}
    jita = systems['Jita']
    assert_that(jita['systemCostIndices'][0]['costIndex'], greater_than(0))

# Expecting something like
#     {"facilityID": 60012160,
#      "solarSystem": {"id": 30000049, "id_str": "30000049"},
#      "name": "Camal IX - Ammatar Fleet Testing Facilities",
#      "region": {"id": 10000001, "id_str": "10000001"},
#      "tax": 0.1,
#      "facilityID_str": "60012160",
#      "owner": {"id": 1000123, "id_str": "1000123"},
#      "type": {"id": 2500, "id_str": "2500"}}


def test_crest_facilities():
    name = "Jita IV - Moon 4 - Caldari Navy Assembly Plant"
    response = facil.facilities()
    stations = {n['facilityID']: n for n in response}
    assert_that(stations, has_key(60003760))
    station = stations[60003760]
    assert_that(station['solarSystem']['id'], equal_to(30000142))
    assert_that(station['tax'], equal_to(0.1))
    assert_that(station['owner']['id'], equal_to(1000035))
    assert_that(station['name'], equal_to(name))
