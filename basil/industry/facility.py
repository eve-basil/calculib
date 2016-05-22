import requests

import basil_common.caching as cache
from basil import ENGINE


def facilities():
    url = 'https://crest-tq.eveonline.com/industry/facilities/'
    return {n['facilityID']: n for n in _items_from_url(url)}


def systems():
    url = 'https://crest-tq.eveonline.com/industry/systems/'
    return {n['solarSystem']['id']: n for n in _items_from_url(url)}


def _items_from_url(url):
    headers = {'user-agent': 'github.com/eve-basil/calculib[0.1.0-dev]'}
    return requests.get(url, headers=headers).json()['items']


FAC_CACHE = cache.FactCache(ENGINE, 'crest/ind/fac/', loader=facilities)
SYS_CACHE = cache.FactCache(ENGINE, 'crest/ind/sys/', loader=systems)


def fuel(race=None, size=None, faction=None, discount=0):
    fuels = [{}]
    if race is not None and size is not None:
        rate = 0
        if size.upper().startswith('S'):
            rate = 10
        elif size.upper().startswith('M'):
            rate = 20
        elif size.upper().startswith('L'):
            rate = 40
        rate *= (1 - discount)

        if race.upper().startswith('A'):
            fuels = [{'id': 4247, 'rate': rate}]
        elif race.upper().startswith('C'):
            fuels = [{'id': 4246, 'rate': rate}]
        elif race.upper().startswith('G'):
            fuels = [{'id': 4312, 'rate': rate}]
        elif race.upper().startswith('M'):
            fuels = [{'id': 4246, 'rate': rate}]

        if faction == 500003:
            fuels.append({'id': 24592, 'rate': 1})
        elif faction == 500001:
            fuels.append({'id': 24593, 'rate': 1})
        elif faction == 500004:
            fuels.append({'id': 24594, 'rate': 1})
        elif faction == 500002:
            fuels.append({'id': 24595, 'rate': 1})
        elif faction == 500008:
            fuels.append({'id': 24596, 'rate': 1})
        elif faction == 500007:
            fuels.append({'id': 24597, 'rate': 1})

    return fuels


def cost_per_hour(race=None, size=None, faction=None):
    from basil.market import PRICES_FUNC
    return sum([PRICES_FUNC(f['id']) * f['rate']
                for f in fuel(race, size, faction)])


def facility(facility_id=None, **kwargs):
    """Provide an IndustrialFacility based on parameters.

    If facility_id is provided, only me_bonus and te_bonus args are used.
    Otherwise a dict containing all the parameters necessary to completely
    specify the facility are required, and some additional, optional, values
    may be given as well (name, description).

    :param facility_id: optional id
    :param kwargs: other args used to define the facility
    :return: an IndustrialFacility
    """
    def _facility_from_id(**ikwargs):
        fac = FAC_CACHE.get(facility_id, blocking=True)
        if not fac:
            raise ValueError('Got None from FAC_CACHE!')
        system = SYS_CACHE.get(fac['solarSystem']['id'], blocking=True)
        if 'tax' in fac and fac['tax'] == 0.1:
            return NPCStation(fac['name'], system)
        else:
            if 'tax' in fac:
                tax_rate = fac['tax'] * 100
            else:
                tax_rate = 0
            return Outpost(fac.get('name', None), system, tax_rate,
                           me_bonus=ikwargs.pop('me_bonus', 0),
                           te_bonus=ikwargs.pop('te_bonus', 0))

    def _facility_from_dict(**ikwargs):

        structure = globals()[ikwargs.pop('structure')]
        system = SYS_CACHE.get(ikwargs.pop('solar_system_id'), blocking=True)
        params = {'solar_system': system}
        for p in _constructor_params(structure):
            if p not in params:
                params[p] = ikwargs.pop(p, None)
        return structure(**params)

    def _constructor_params(clas):
        import inspect
        return [x for x in inspect.getargspec(clas.__init__)[0]
                if x != 'self']

    if facility_id:
        return _facility_from_id(**kwargs)
    else:
        return _facility_from_dict(**kwargs)


class IndustryFacility(object):
    def __init__(self, name, solar_system, tax_rate, material_bonus=0,
                 time_bonus=0, hourly_cost=0):
        self.name = name
        self.tax_rate = tax_rate
        self.solar_system = solar_system
        self.material_bonus = material_bonus
        self.time_bonus = time_bonus
        self.hourly_cost = hourly_cost

    @property
    def manufacture_index(self):
        activity = 'Manufacturing'
        return self._activity_index(activity)

    @property
    def invention_index(self):
        activity = 'Invention'
        return self._activity_index(activity)

    @property
    def copying_index(self):
        activity = 'Copying'
        return self._activity_index(activity)

    @property
    def material_research_index(self):
        activity = 'Researching Material Efficiency'
        return self._activity_index(activity)

    @property
    def time_research_index(self):
        activity = 'Researching Time Efficiency'
        return self._activity_index(activity)

    def _activity_index(self, activity):
        return next(idx['costIndex']
                    for idx in self.solar_system['systemCostIndices']
                    if idx['activityName'] == activity)

    def can_build(self, product):
        return True


class EquipmentAssemblyArray(IndustryFacility):
    """A mobile assembly facility where modules, implants, deployables,
    structures and containers can be manufactured more efficiently than the
    rapid equipment assembly array but at a reduced speed.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(EquipmentAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)

    def can_build(self, product):
        return False


class SmallShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where smaller ships such as Fighter and
    Fighter Bomber Drones, Frigates and Destroyers can be manufactured.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(SmallShipAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class AdvancedSmallShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where advanced small ships such as Assault
    Frigates, Covert Ops Frigates, Electronic Attack Frigates, Interceptors,
    Interdictors, Stealth Bombers and Tactical Destroyers can be manufactured.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(AdvancedSmallShipAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class MediumShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where medium sized ships such as Cruisers
    and Battlecruisers can be manufactured.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(MediumShipAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class AdvancedMediumShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where advanced medium sized ships such as
    Logistics Cruisers, Heavy Assault Cruisers, Recon Cruisers, Heavy
    Interdiction Cruisers and Command Battlecruisers can be manufactured.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(AdvancedMediumShipAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class LargeShipAssemblyArray(IndustryFacility):
    """ A mobile assembly facility where large ships such as Battleships,
    Freighters and Industrial Command Ships can be manufactured.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(LargeShipAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class AdvancedLargeShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where advanced large ships such as Black
    Ops, Marauder class battleships as well as Jump Freighters can be
    manufactured.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(AdvancedLargeShipAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class CapitalShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where large ships such as Battleships,
    Carriers, Dreadnoughts, Freighters, Industrial Command Ships and Capital
    Industrial Ships can be manufactured.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(CapitalShipAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class AmmunitionAssemblyArray(IndustryFacility):
    """A mobile assembly facility where most ammunition such as Missiles,
    Hybrid Charges, Projectile Ammo and Frequency Crystals can be
    manufactured.

    Fuel Blocks can also be manufactured here.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(AmmunitionAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class DroneAssemblyArray(IndustryFacility):
    """A mobile assembly facility where small unmanned drones can be
    manufactured.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(DroneAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class ComponentAssemblyArray(IndustryFacility):
    """A mobile assembly facility where Construction Components such as
    Capital Ship, Tech II and Hybrid (Tech III) Components of all sorts can
    be manufactured.

    Fuel Blocks can also be manufactured here.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(ComponentAssemblyArray, self).__init__(
            name, solar_system, 0, 2, 25, hourly_cost=hourly_cost)


class ThukkerComponentAssemblyArray(IndustryFacility):
    """An assembly facility where Standard and Advanced Capital Ship
    Components can be manufactured.

    This facility is engineered by Thukker specialists to utilize certain
    unregulated opportunities for expediting construction in low security
    space.
    """

    def __init__(self, name, solar_system, hourly_cost=0):
        super(ThukkerComponentAssemblyArray, self).__init__(
            name, solar_system, 0, 25, 15, hourly_cost=hourly_cost)


class NPCStation(IndustryFacility):
    def __init__(self, name, solar_system):
        super(NPCStation, self).__init__(name, solar_system, 10, 0, 0)


class Outpost(IndustryFacility):
    def __init__(self, name, solar_system, tax_rate, me_bonus=0, te_bonus=0):
        super(Outpost, self).__init__(name, solar_system, tax_rate, me_bonus,
                                      te_bonus)
