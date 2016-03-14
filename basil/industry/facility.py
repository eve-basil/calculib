import requests

import basil_common.caching as cache


def facilities():
    url = 'https://public-crest.eveonline.com/industry/facilities/'
    return _items_from_url(url)


def systems():
    url = 'https://public-crest.eveonline.com/industry/systems/'
    return _items_from_url(url)


def _items_from_url(url):
    headers = {'user-agent': 'github.com/eve-basil/calculib[0.1.0-dev]'}
    return requests.get(url, headers=headers).json()['items']

FAC_CACHE = cache.FactCache(cache.ENGINE, 'fac', facilities)
SYS_CACHE = cache.FactCache(cache.ENGINE, 'sys', systems)


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
    global FAC_CACHE
    global SYS_CACHE

    def _facility_from_id():
        fac = FAC_CACHE[facility_id]
        system = SYS_CACHE.get(fac['solarSystem']['id'])
        if 'tax' in fac and fac['tax'] == 0.1:
            return NPCStation(fac['name'], system)
        else:
            if 'tax' in fac:
                tax_rate = fac['tax'] * 100
            else:
                tax_rate = 0
            return Outpost(fac.get('name', None), system, tax_rate,
                           me_bonus=kwargs.pop('me_bonus', 0),
                           te_bonus=kwargs.pop('te_bonus', 0))

    def _facility_from_dict(**kwargs):
        pass

    if facility_id:
        return _facility_from_id()
    else:
        return _facility_from_dict(**kwargs)


class IndustryFacility(object):

    def __init__(self, name, solar_system, tax_rate, material_bonus=0,
                 time_bonus=0, details=None):
        self.name = name
        self._tax_rate = tax_rate
        self._solar_system = solar_system
        self._material_bonus = material_bonus
        self._time_bonus = time_bonus
        self.details = details

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
                    for idx in self._solar_system['systemCostIndices']
                    if idx['activityName'] == activity)

    @property
    def tax_rate(self):
        return self._tax_rate

    @property
    def material_bonus(self):
        return self._material_bonus

    @property
    def time_bonus(self):
        return self._time_bonus

    def can_build(self, product):
        return True


class EquipmentAssemblyArray(IndustryFacility):
    """A mobile assembly facility where modules, implants, deployables,
    structures and containers can be manufactured more efficiently than the
    rapid equipment assembly array but at a reduced speed.
    """
    def __init__(self, name, system):
        super(EquipmentAssemblyArray, self).__init__(name, system, 0, 2, 25)

    def can_build(self, product):
        return False


class SmallShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where smaller ships such as Fighter and
    Fighter Bomber Drones, Frigates and Destroyers can be manufactured.
    """
    def __init__(self, name, system):
        super(SmallShipAssemblyArray, self).__init__(name, system, 0, 2, 25)


class AdvancedSmallShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where advanced small ships such as Assault
    Frigates, Covert Ops Frigates, Electronic Attack Frigates, Interceptors,
    Interdictors, Stealth Bombers and Tactical Destroyers can be manufactured.
    """
    def __init__(self, name, system):
        super(AdvancedSmallShipAssemblyArray, self).__init__(name, system, 0,
                                                             2, 25)


class MediumShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where medium sized ships such as Cruisers
    and Battlecruisers can be manufactured.
    """
    def __init__(self, name, system):
        super(MediumShipAssemblyArray, self).__init__(name, system, 0, 2, 25)


class AdvancedMediumShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where advanced medium sized ships such as
    Logistics Cruisers, Heavy Assault Cruisers, Recon Cruisers, Heavy
    Interdiction Cruisers and Command Battlecruisers can be manufactured.
    """
    def __init__(self, name, system):
        super(AdvancedMediumShipAssemblyArray, self).__init__(name, system, 0,
                                                              2, 25)


class LargeShipAssemblyArray(IndustryFacility):
    """ A mobile assembly facility where large ships such as Battleships,
    Freighters and Industrial Command Ships can be manufactured.
    """

    def __init__(self, name, system):
        super(LargeShipAssemblyArray, self).__init__(name, system, 0, 2, 25)


class AdvancedLargeShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where advanced large ships such as Black
    Ops, Marauder class battleships as well as Jump Freighters can be
    manufactured.
    """
    def __init__(self, name, system):
        super(AdvancedLargeShipAssemblyArray, self).__init__(name, system, 0,
                                                             2, 25)


class CapitalShipAssemblyArray(IndustryFacility):
    """A mobile assembly facility where large ships such as Battleships,
    Carriers, Dreadnoughts, Freighters, Industrial Command Ships and Capital
    Industrial Ships can be manufactured.
    """
    def __init__(self, name, system):
        super(CapitalShipAssemblyArray, self).__init__(name, system, 0, 2, 25)


class AmmunitionAssemblyArray(IndustryFacility):
    """A mobile assembly facility where most ammunition such as Missiles,
    Hybrid Charges, Projectile Ammo and Frequency Crystals can be
    manufactured.

    Fuel Blocks can also be manufactured here.
    """

    def __init__(self, name, system):
        super(AmmunitionAssemblyArray, self).__init__(name, system, 0, 2, 25)


class DroneAssemblyArray(IndustryFacility):
    """A mobile assembly facility where small unmanned drones can be
    manufactured.
    """

    def __init__(self, name, system):
        super(DroneAssemblyArray, self).__init__(name, system, 0, 2, 25)


class ComponentAssemblyArray(IndustryFacility):
    """A mobile assembly facility where Construction Components such as
    Capital Ship, Tech II and Hybrid (Tech III) Components of all sorts can
    be manufactured.

    Fuel Blocks can also be manufactured here.
    """

    def __init__(self, name, system):
        super(ComponentAssemblyArray, self).__init__(name, system, 0, 2, 25)


class ThukkerComponentAssemblyArray(IndustryFacility):
    """An assembly facility where Standard and Advanced Capital Ship
    Components can be manufactured.

    This facility is engineered by Thukker specialists to utilize certain
    unregulated opportunities for expediting construction in low security
    space.
    """

    def __init__(self, name, system):
        super(ThukkerComponentAssemblyArray, self).__init__(name, system, 0,
                                                            25, 15)


class NPCStation(IndustryFacility):
    def __init__(self, name, system):
        super(NPCStation, self).__init__(name, system, 10, 0, 0)


class Outpost(IndustryFacility):
    def __init__(self, name, system, tax_rate, me_bonus=0, te_bonus=0):
        super(Outpost, self).__init__(name, system, tax_rate, me_bonus,
                                      te_bonus)
