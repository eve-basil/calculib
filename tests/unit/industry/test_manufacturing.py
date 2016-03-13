from __future__ import absolute_import

from tests import *

import basil.industry.facility as f
import basil.industry.manufacturing as m
from basil.industry.manufacturing import BillOfMaterials


def test_me_blueprint_bonuses():
    assert_that(m.me_bonuses({'me': 0}), equal_to([]))
    for x in range(1-11):
        assert_that(m.me_bonuses({'me': x}), equal_to([x]))


def test_me_bonuses_equipment_assembly_array():
    fac = f.EquipmentAssemblyArray(None, None)
    assert_that(m.me_bonuses({'me': 1}, fac), equal_to([2, 1]))
    assert_that(m.me_bonuses({'me': 2}, fac), equal_to([2, 2]))
    assert_that(m.me_bonuses({'me': 4}, fac), equal_to([4, 2]))


def test_me_bonuses_small_ship_assembly_array():
    fac = f.SmallShipAssemblyArray(None, None)
    assert_that(m.me_bonuses({'me': 1}, fac), equal_to([2, 1]))
    assert_that(m.me_bonuses({'me': 2}, fac), equal_to([2, 2]))
    assert_that(m.me_bonuses({'me': 4}, fac), equal_to([4, 2]))


def test_me_bonuses_npc_station():
    fac = f.NPCStation(None, None)
    assert_that(m.me_bonuses({'me': 1}, fac), equal_to([1]))
    assert_that(m.me_bonuses({'me': 2}, fac), equal_to([2]))
    assert_that(m.me_bonuses({'me': 4}, fac), equal_to([4]))


def test_me_bonuses_thukker_component_assembly_array():
    fac = f.ThukkerComponentAssemblyArray(None, None)
    assert_that(m.me_bonuses({'me': 1}, fac), equal_to([25, 1]))
    assert_that(m.me_bonuses({'me': 2}, fac), equal_to([25, 2]))
    assert_that(m.me_bonuses({'me': 4}, fac), equal_to([25, 4]))


def test_te_blueprint_bonuses():
    assert_that(m.te_bonuses({'te': 0}), equal_to([]))
    for x in range(2, 21, 2):
        assert_that(m.te_bonuses({'te': x}), equal_to([x]))


def test_te_bonuses_equipment_assembly_array():
    fac = f.EquipmentAssemblyArray(None, None)
    assert_that(m.te_bonuses({'te': 2}, fac), equal_to([25, 2]))
    assert_that(m.te_bonuses({'te': 6}, fac), equal_to([25, 6]))
    assert_that(m.te_bonuses({'te': 8}, fac), equal_to([25, 8]))


def test_te_bonuses_npc_station():
    fac = f.NPCStation(None, None)
    assert_that(m.te_bonuses({'te': 2}, fac), equal_to([2]))
    assert_that(m.te_bonuses({'te': 6}, fac), equal_to([6]))
    assert_that(m.te_bonuses({'te': 8}, fac), equal_to([8]))


def test_te_bonuses_thukker_component_assembly_array():
    fac = f.ThukkerComponentAssemblyArray(None, None)
    assert_that(m.te_bonuses({'te': 2}, fac), equal_to([15, 2]))
    assert_that(m.te_bonuses({'te': 6}, fac), equal_to([15, 6]))
    assert_that(m.te_bonuses({'te': 16}, fac), equal_to([16, 15]))


def test_te_bonuses_unskilled_builder():
    fac = f.ThukkerComponentAssemblyArray(None, None)
    bldr = {'skills': {}, 'implants': {}}
    assert_that(m.te_bonuses({'te': 2}, fac, bldr), equal_to([15, 2]))
    assert_that(m.te_bonuses({'te': 6}, fac, bldr), equal_to([15, 6]))
    assert_that(m.te_bonuses({'te': 16}, fac, bldr), equal_to([16, 15]))


def test_te_bonuses_midskilled_builder():
    fac = f.ThukkerComponentAssemblyArray(None, None)
    bldr = {'skills': {3380: 4, }, 'implants': {}}
    assert_that(m.te_bonuses({'te': 2}, fac, bldr), equal_to([16, 15, 2]))
    assert_that(m.te_bonuses({'te': 6}, fac, bldr), equal_to([16, 15, 6]))
    assert_that(m.te_bonuses({'te': 16}, fac, bldr), equal_to([16, 16, 15]))


def test_te_bonuses_skilled_builder():
    fac = f.NPCStation(None, None)
    bldr = {'skills': {3380: 5, 3388: 5}, 'implants': {}}
    assert_that(m.te_bonuses({'te': 2}, fac, bldr), equal_to([20, 15, 2]))
    assert_that(m.te_bonuses({'te': 6}, fac, bldr), equal_to([20, 15, 6]))
    assert_that(m.te_bonuses({'te': 16}, fac, bldr), equal_to([20, 16, 15]))


def test_te_bonuses_implanted_builder():
    fac = f.NPCStation(None, None)
    bldr = {'skills': {3380: 5}, 'implants': {27171: 1}}
    assert_that(m.te_bonuses({'te': 2}, fac, bldr), equal_to([20, 4, 2]))
    assert_that(m.te_bonuses({'te': 6}, fac, bldr), equal_to([20, 6, 4]))
    assert_that(m.te_bonuses({'te': 16}, fac, bldr), equal_to([20, 16, 4]))


def test_flatten_single():
    material = m.ManufactureMaterial(12, "egg", 10, 1)
    result = BillOfMaterials.flatten_materials([material])
    assert_that(result[0], same_instance(material))


def test_flatten():
    mats = [m.ManufactureMaterial(12, "egg", 10, n) for n in range(0, 4)]
    result = BillOfMaterials.flatten_materials(mats)

    assert_that(result, has_length(1))
    assert_that(result[0], instance_of(m.ManufactureMaterial))
    assert_that(result[0], has_property("id", equal_to(12)))
    assert_that(result[0], has_property("name", equal_to("egg")))
    assert_that(result[0], has_property("quantity", equal_to(40)))
    assert_that(result[0], has_property("cost", equal_to(1.5)))


def test_flatten_unsorted():
    mats = [m.ManufactureMaterial(12 - n, str(n), 10, 2.1 * n)
            for n in range(0, 4)]
    result = BillOfMaterials.flatten_materials(mats)

    assert_that(result, has_length(4))
    assert_that(result[0], instance_of(m.ManufactureMaterial))
    assert_that(result[0], has_property("id", equal_to(9)))
    assert_that(result[0], has_property("name", equal_to("3")))
    assert_that(result[0], has_property("quantity", equal_to(10)))
    assert_that(result[0], has_property("cost", nearly(6.3)))


def test_total_cost():
    mats = [m.ManufactureMaterial(12, "egg", 10, n) for n in range(0, 4)]
    result = BillOfMaterials(mats)

    assert_that(result.total_cost(), equal_to(60))
