from operator import attrgetter

import basil.market as market
import basil.industry.manufacturing as imat
from basil.industry import IndustryException


def prospect(blueprint, facilities, runs=1, count=1):
    """Analyze Prospects for an industrial manufacturing job.

    :param blueprint: a blueprint to build from
    :param facilities: list of IndustryFacilities to evaluate
    :param runs: number of runs to calculate the prospect on
    :return: a list of Prospects, sorted from in order of decreasing profit
    """
    product = blueprint['products'][0]['typeID']
    product_price = market.PRICES_FUNC(product, blueprint['typeName'][:-10])
    if not product_price:
        raise IndustryException()
    product_value = market.VALUES_FUNC(product)
    if not product_value:
        raise IndustryException()

    prospects = []
    for fac in facilities:
        job = imat.ManufactureJob(runs, blueprint, fac, product_value)
        prospects.append(Prospect(job, product_price['sell']['min'], count))
    return sorted(prospects, key=attrgetter('cost_per_unit'))


class Prospect(object):
    def __init__(self, manufacture_job, sell_price, count):
        self.manufacture_job = manufacture_job
        self.price_per_unit = sell_price
        self.count = count

    @property
    def product(self):
        return self.manufacture_job.product

    @property
    def blueprint_me(self):
        return self.manufacture_job.blueprint_me

    @property
    def facility(self):
        return self.manufacture_job.facility

    @property
    def units_per_run(self):
        return self.manufacture_job.units_per_run

    @property
    def runs(self):
        return self.manufacture_job.runs

    @property
    def install_cost(self):
        return self.manufacture_job.install_cost

    @property
    def total_cost(self):
        return self.manufacture_job.total_cost

    @property
    def cost_per_unit(self):
        return float(self.total_cost) / self.units_per_run

    @property
    def profit_per_unit(self):
        return self.price_per_unit - self.cost_per_unit

    @property
    def profit_per_run(self):
        return self.profit_per_unit * self.units_per_run

    @property
    def revenue_per_run(self):
        return self.price_per_unit * self.units_per_run

    @property
    def total_revenue(self):
        return self.revenue_per_run * self.runs

    @property
    def total_profit(self):
        return self.profit_per_run * self.runs

    @property
    def profit_margin(self):
        return 100 * self.total_profit / self.total_cost

    @property
    def materials(self):
        return self.manufacture_job.final_materials
