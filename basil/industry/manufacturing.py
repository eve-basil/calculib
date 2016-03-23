import operator

from basil.calculator import manufacturing as calc
import basil.market as market


def me_bonuses(blueprint, facility=None):
    """Collect Material Efficiency bonuses.

    :param blueprint: dict representing the blueprint to be built
    :param facility: IndustrialFacility representation the build location
    :return: a sorted list of modifiers
    """
    # TODO some decryptors will break this, as ME penalties are filtered out
    bonuses = [blueprint['me']]
    if facility:
        bonuses.append(facility.material_bonus)
    return sorted([b for b in bonuses if b > 0], reverse=True)


def te_bonuses(blueprint, facility=None, builder=None):
    """Collect Time Efficiency bonuses.

    :param blueprint: dict representing the blueprint to be built
    :param facility: IndustrialFacility representation the build location
    :param builder: dict characterizing the builder's skills and implants
    :return: a sorted list of modifiers
    """
    # TODO some decryptors may break this, as TE penalties are filtered out
    bonuses = [blueprint['te']]
    if facility:
        bonuses.append(facility.time_bonus)
    if builder:
        if 'skills' in builder:
            skills = builder['skills']
            bonuses.append(skills.get(3380, 0) * 4)  # Industry
            bonuses.append(skills.get(3388, 0) * 3)  # Advanced Industry
        if 'implants' in builder:
            implants = builder['implants']
            bonuses.append(implants.get(27170, 0) * 1)  # BX-801
            bonuses.append(implants.get(27167, 0) * 2)  # BX-802
            bonuses.append(implants.get(27171, 0) * 4)  # BX-804
    return sorted([b for b in bonuses if b > 0], reverse=True)


def required_material(raw_mats, bonuses):
    final_mats = []
    init_mats = []
    for m in raw_mats:
        mat_name = market.NAMES_FUNC(m['typeID'])
        mat_price = market.PRICES_FUNC(m['typeID'])['sell']['min']
        qty_used = calc.calc_mats(1, m['quantity'], bonuses)
        final_mats.append(ManufactureMaterial(m['typeID'], mat_name,
                                              qty_used, mat_price))
        init_mats.append(ManufactureMaterial(m['typeID'], mat_name,
                                             m['quantity'], mat_price))
    return BillOfMaterials(init_mats), BillOfMaterials(final_mats)


class ManufactureMaterial(object):
    """A spec for a single Material in a Manufacturing process
    """
    def __init__(self, type_id, name, quantity, cost=None):
        self._id = type_id
        self._name = name
        self._quantity = quantity
        self._cost = cost

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def quantity(self):
        return self._quantity

    @property
    def cost(self):
        return self._cost


class BillOfMaterials(object):
    """Collection of ManufactureMaterials required for a process
    """
    def __init__(self, materials):
        self._materials = self.flatten_materials(materials)

    def __iter__(self):
        return iter(self._materials)

    @property
    def total_cost(self):
        return sum(mat.quantity * mat.cost for mat in self)

    @staticmethod
    def flatten_materials(materials):
        if not isinstance(materials, list):
            materials = [materials]

        def _merge(left, right):
            qty = left.quantity + right.quantity
            lprod = left.quantity * float(left.cost)
            rprod = right.quantity * float(right.cost)
            avg = (lprod + rprod) / qty
            return ManufactureMaterial(type_id=left.id, name=left.name,
                                       quantity=qty, cost=avg)

        materials.sort(key=operator.attrgetter('id'))
        prev = materials.pop(0)
        result = []
        for curr in materials:
            if prev.id == curr.id:
                prev = _merge(prev, curr)
            else:
                result.append(prev)
                prev = curr
        result.append(prev)
        return result


class ManufactureJob(object):
    def __init__(self, runs, blueprint, facility, product_value):
        self.runs = runs
        self._blueprint = blueprint
        self.facility = facility
        self._product_value = product_value
        # calculate materials required
        raw_mats = blueprint['materials']
        mat_bonuses = me_bonuses(blueprint, facility)
        mats = required_material(raw_mats, mat_bonuses)
        self.raw_materials, self.final_materials = mats
        # calculate duration
        time_bonuses = te_bonuses(blueprint, facility)
        self.duration = calc.calc_time(runs, blueprint['time'], time_bonuses)

    @property
    def product(self):
        return self._blueprint['products'][0]['name']

    @property
    def units_per_run(self):
        return self._blueprint['products'][0]['quantity']

    @property
    def install_cost(self):
        index = self.facility.manufacture_index
        tax = self.facility.tax_rate
        return calc.calc_install(self.runs, self._product_value, index, tax)

    @property
    def cost_per_run(self):
        return self.total_cost / self.runs

    @property
    def cost_per_unit(self):
        return self.cost_per_run() * self.units_per_run

    @property
    def total_cost(self):
        return self.final_materials.total_cost + self.install_cost
