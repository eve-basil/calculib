from __future__ import absolute_import

from tests.support import *

import basil.industry.manufacturing as m
from basil.industry.manufacturing import BillOfMaterials


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
