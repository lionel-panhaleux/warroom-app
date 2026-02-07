import collections
import copy

from . import enums
from . import state
from . import map


def get_unit(unit_kind: enums.UnitKind) -> enums.Unit:
    return enums.UNITS_FROM_ABBREV[unit_kind]


def compute_stress(state: state.CountryState):
    casualties = sum(get_unit(u).stress * count for u, count in state.losses.items())
    if casualties < 20:
        return 0
    if casualties < 36:
        return 1
    if casualties < 52:
        return 2
    if casualties < 70:
        return 3
    if casualties < 90:
        return 4
    if casualties < 110:
        return 5
    return 6


def compute_resources(country: enums.Country):
    results = collections.defaultdict(int)
    for territory in state.STATE.country_states[country].territories:
        results.update(territory.resources)
        if territory.embattled:
            if territory.resources.get(enums.Resource.OIL, 0):
                results[enums.Resource.OIL] -= 1
            elif territory.resources.get(enums.Resource.IRON, 0):
                results[enums.Resource.IRON] -= 1
            elif territory.resources.get(enums.Resource.OSR, 0):
                results[enums.Resource.OSR] -= 1
    return results


def exchange_territory(
    source: enums.Country, target: enums.Country, territory: map.Territory
):
    if territory not in state.STATE.country_states[source].territories:
        raise ValueError(f"Territory {territory} not controlled by {source}")
    state.STATE.country_states[source].territories.remove(territory)
    state.STATE.country_states[source].territories.add(territory)
