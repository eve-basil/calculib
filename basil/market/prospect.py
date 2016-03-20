from operator import attrgetter

import basil.market as market
import basil.calculator.manufacturing as cmat
import basil.industry.manufacturing as imat


def prospect(blueprint, facilities):
    """Analyze Prospects for an industrial manufacturing job.

    :param blueprint: a blueprint to build from
    :param facilities: list of IndustryFacilitys to evaluate
    :param prices: dictionary of prices for all materials and product(s) by
           typeID
    :return: a list of Prospects, sorted from in order of decreasing profit
    """
    raw_mats = blueprint['materials']
    product = blueprint['products'][0]['typeID']
    product_value = market.VALUES_FUNC(product)
    sell = market.PRICES_FUNC(product)
    blueprint['products'][0]['name'] = market.NAMES_FUNC(product)

    prospects = []
    for fac in facilities:
        bonuses = imat.me_bonuses(blueprint, fac)
        mats = _required_material(raw_mats, bonuses)
        index = fac.manufacture_index
        install = cmat.calc_install(1, product_value, index, fac.tax_rate)
        prospects.append(Prospect(blueprint, fac, mats[1], install, sell))
    return sorted(prospects, key=attrgetter('cost_per_unit'))


def _required_material(raw_mats, bonuses):
    final_mats = []
    init_mats = []
    for m in raw_mats:
        mat_name = market.NAMES_FUNC(m['typeID'])
        mat_price = market.PRICES_FUNC(m['typeID'])['sell']['min']
        qty_used = cmat.calc_mats(1, m['quantity'], bonuses)
        final_mats.append(imat.ManufactureMaterial(m['typeID'], mat_name,
                                                   qty_used, mat_price))
        init_mats.append(imat.ManufactureMaterial(m['typeID'], mat_name,
                                                  m['quantity'], mat_price))
    return imat.BillOfMaterials(init_mats), imat.BillOfMaterials(final_mats)


class Prospect(object):
    def __init__(self, blueprint, facility, mats, install_cost, sell_price):
        self.blueprint = blueprint
        self.facility = facility
        self.bill_of_materials = mats
        self.install_cost = install_cost
        self.price_per_unit = sell_price

    @property
    def cost_per_unit(self):
        units_per_run = self.blueprint['products'][0]['quantity']
        return float(self.bill_of_materials.total_cost +
                     self.install_cost) / units_per_run
