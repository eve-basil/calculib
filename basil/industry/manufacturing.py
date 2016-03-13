import operator

from basil.calculator import manufacturing as calc


def me_bonuses(blueprint, facility=None):
    bonuses = [blueprint['me']]
    if facility:
        bonuses.append(facility.material_bonus)
    return sorted([b for b in bonuses if b > 0], reverse=True)


def te_bonuses(blueprint, facility=None, builder=None):
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


class ManufactureMaterial(object):
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
    def __init__(self, materials):
        self._materials = self.flatten_materials(materials)

    def __iter__(self):
        n = 0
        while n < len(self._materials):
            yield self._materials[n]
            n += 1

    def total_cost(self):
        cost = 0.0
        for mat in self:
            cost += mat.quantity * mat.cost
        return cost

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
    def __init__(self, runs, recipe, me_bonuses=None, te_bonuses=None,
                 install_factors=None, description=None):
        self._product = recipe['products'][0]['name']
        self._runs = runs
        self._units_per_run = recipe['products'][0]['quantity']
        self._me_bonuses = me_bonuses or []
        self._te_bonuses = te_bonuses or []
        self._in_factors = install_factors  # dict: system_index, tax_rate
        self._description = description
        self._duration = calc.calc_time(runs, recipe['time'], te_bonuses)
        self._materials = self._make_bill(recipe, runs, me_bonuses)
        # TODO TODO TODO
        self._cost_index = recipe['products'][0]['cost_index']

    @property
    def runs(self):
        return self._runs

    @property
    def description(self):
        return self._description

    @property
    def duration(self):
        return self._duration

    @property
    def cost_per_unit(self):
        return self.total_cost / self._runs * self._units_per_run

    @property
    def total_cost(self):
        mat_cost = self._materials.total_cost()
        return mat_cost + calc.calc_install(self._runs, self._cost_index,
                                            **self._in_factors)

    @staticmethod
    def _make_bill(recipe, runs, me_bonuses):
        mats = []
        for spec in recipe['materials']:
            mat_id = spec['typeID']
            mat_name = recipe['materials'][mat_id]['name']
            qty = calc.calc_mats(runs, spec['quantity'], me_bonuses)
            cost = recipe['materials'][mat_id]['cost']
            material = ManufactureMaterial(mat_id, mat_name, qty, cost)
            mats.append(material)
        return BillOfMaterials(mats)
