from __future__ import absolute_import
from datetime import timedelta

from tests import *

import basil.calculator.manufacturing as m


def test_calc_mats():
    assert_that(m.calc_mats(1, 12345, []), equal_to(12345))
    assert_that(m.calc_mats(1, 12345, 0), equal_to(12345))
    assert_that(m.calc_mats(1, 716, 9), equal_to(652))
    assert_that(m.calc_mats(3, 2250, -5), equal_to(7088))
    assert_that(m.calc_mats(20, 716, 10), equal_to(12888))
    assert_that(m.calc_mats(34, 473141, [6, 15]), equal_to(12853349))


def test_calc_time():
    assert_that(m.calc_time(1, 12000, []), equal_to(12000))
    assert_that(m.calc_time(1, 12000, 0), equal_to(12000))

    duration = timedelta(seconds=m.calc_time(3, 240000, [18, 35, 5, 25, 4]))
    assert_that(equal_to('3 days, 0:54:52'), str(duration))


def test_calc_install():
    install_cost = m.calc_install(runs=20, cost_index=333.33,
                                  system_index=0.011, tax_rate=10)
    assert_that(install_cost, nearly(80.66586))
