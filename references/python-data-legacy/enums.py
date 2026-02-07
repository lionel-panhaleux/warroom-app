import collections
import dataclasses
import enum


class Alliance(enum.Enum):
    ALLIES = "Allies Forces"
    AXIS = "Axis"


class Resource(enum.Enum):
    OIL = "Oil"
    IRON = "Iron"
    OSR = "OSR"


EXCHANGE_RATE = {
    Resource.OIL: 2,
    Resource.IRON: 3,
    Resource.OSR: 5,
}


class Country(enum.Enum):
    USA = "United States of America"
    BRITAIN = "British Empire"
    RUSSIA = "Russia"
    GERMANY = "Germany"
    JAPAN = "Japan"
    ITALY = "Italy"
    CHINA = "China"


class TroopType(enum.Enum):
    AIR = "A"
    NAVAL = "N"
    LAND = "L"


class Color(enum.Enum):
    YELLOW = "Y"
    BLUE = "B"
    GREEN = "G"
    RED = "R"
    BLACK = "K"
    WHITE = "W"


class UnitKind(enum.Enum):
    BOMBER = "BMR"
    FIGHTER = "FTR"
    ARMOR = "ARM"
    ARTILLERY = "ART"
    INFANTRY = "INF"
    BATTLESHIP = "BB"
    CARRIER = "CV"
    CRUISER = "CR"
    SUBMARINE = "SS"


class Stance(enum.Enum):
    STRATEGIC = "Strategic"
    DEFENSIVE = "Defensive"
    OFFENSIVE = "Offensive"
    ESCORT = "Escort"
    DIVE = "Dive"


class Status(enum.Enum):
    INITIAL = "Initial"
    LIGHTLY_DAMAGED = "Lightly damaged"
    DAMAGED = "Damaged"
    DIVE = "Dive"
    ELIMINATED = "Eliminated"


LIGHT_STATUSES = [Status.INITIAL, Status.ELIMINATED]
STANDARD_STATUSES = [Status.INITIAL, Status.DAMAGED, Status.ELIMINATED]
ARMORED_STATUSES = [
    Status.INITIAL,
    Status.LIGHTLY_DAMAGED,
    Status.DAMAGED,
    Status.ELIMINATED,
]
SUBMARINE_STATUSES = [Status.INITIAL, Status.DIVE, Status.ELIMINATED]


class HomelandStatus(enum.IntEnum):
    ACCEPTABLE_STRESS = 1
    LABOR_AND_CIVIL_UNREST = 2
    DYSFUNCTIONAL_INFRASTRUCTURE = 3
    SUPPLY_LINES_DISRUPTED = 4
    ECONOMIC_COLLAPSE = 5
    MASS_DESERTIONS = 6


STRESS_THRESHOLD = {
    Country.USA: 5,
    Country.BRITAIN: 6,
    Country.RUSSIA: 6,
    Country.GERMANY: 6,
    Country.JAPAN: 7,
    Country.ITALY: 4,
    Country.CHINA: 4,
}


class BattleType(enum.Enum):
    AIR = "Air"
    SURFACE = "Surface"


@dataclasses.dataclass(frozen=True)
class StanceAttributes:
    air_combat_value: int
    surface_combat_value: int
    statuses: list[Status]


@dataclasses.dataclass(frozen=True)
class Unit:
    name: str = dataclasses.field(compare=False)
    abbrev: str
    color: Color
    troop_type: TroopType
    cost: dict[Resource, int] = dataclasses.field(compare=False)
    stress: int = dataclasses.field(compare=False)
    stances = dict[Stance, StanceAttributes] = dataclasses.field(compare=False)


BOMBER = Unit(
    name="Bomber",
    abbrev="BMR",
    color=Color.RED,
    troop_type=TroopType.AIR,
    cost={Resource.OIL: 2, Resource.IRON: 2, Resource.OSR: 1},
    stress=6,
    stances={
        Stance.STRATEGIC: StanceAttributes(
            air_combat_value=1, surface_combat_value=0, statuses=STANDARD_STATUSES
        ),
        Stance.OFFENSIVE: StanceAttributes(
            air_combat_value=1, surface_combat_value=4, statuses=STANDARD_STATUSES
        ),
    },
)
FIGHTER = Unit(
    name="Fighter",
    abbrev="FTR",
    color=Color.GREEN,
    troop_type=TroopType.AIR,
    cost={Resource.OIL: 2, Resource.IRON: 1, Resource.OSR: 1},
    stress=4,
    stances={
        Stance.DEFENSIVE: StanceAttributes(
            air_combat_value=3, surface_combat_value=0, statuses=STANDARD_STATUSES
        ),
        Stance.OFFENSIVE: StanceAttributes(
            air_combat_value=0, surface_combat_value=3, statuses=STANDARD_STATUSES
        ),
    },
)
ARMOR = Unit(
    name="Armor",
    abbrev="ARM",
    color=Color.GREEN,
    troop_type=TroopType.LAND,
    cost={Resource.OIL: 1, Resource.IRON: 2, Resource.OSR: 1},
    stress=4,
    stances={
        Stance.DEFENSIVE: StanceAttributes(
            air_combat_value=1, surface_combat_value=2, statuses=ARMORED_STATUSES
        ),
        Stance.OFFENSIVE: StanceAttributes(
            air_combat_value=0, surface_combat_value=4, statuses=STANDARD_STATUSES
        ),
    },
)
ARTILLERY = Unit(
    name="Artillery",
    abbrev="ART",
    color=Color.BLUE,
    troop_type=TroopType.LAND,
    cost={Resource.IRON: 2, Resource.OSR: 1},
    stress=2,
    stances={
        Stance.DEFENSIVE: StanceAttributes(
            air_combat_value=2, surface_combat_value=1, statuses=STANDARD_STATUSES
        ),
        Stance.OFFENSIVE: StanceAttributes(
            air_combat_value=0, surface_combat_value=2, statuses=STANDARD_STATUSES
        ),
    },
)
INFANTRY = Unit(
    name="Infantry",
    abbrev="INF",
    color=Color.YELLOW,
    troop_type=TroopType.LAND,
    cost={Resource.OSR: 2},
    stress=2,
    stances={
        Stance.DEFENSIVE: StanceAttributes(
            air_combat_value=0, surface_combat_value=1, statuses=STANDARD_STATUSES
        ),
        Stance.OFFENSIVE: StanceAttributes(
            air_combat_value=0, surface_combat_value=2, statuses=LIGHT_STATUSES
        ),
    },
)
BATTLESHIP = Unit(
    name="Battleship",
    abbrev="BB",
    color=Color.RED,
    troop_type=TroopType.NAVAL,
    cost={Resource.OIL: 3, Resource.IRON: 4, Resource.OSR: 3},
    stress=20,
    stances={
        Stance.DEFENSIVE: StanceAttributes(
            air_combat_value=2, surface_combat_value=3, statuses=ARMORED_STATUSES
        ),
        Stance.OFFENSIVE: StanceAttributes(
            air_combat_value=1, surface_combat_value=4, statuses=ARMORED_STATUSES
        ),
    },
)
CARRIER = Unit(
    name="Carrier",
    abbrev="CV",
    color=Color.GREEN,
    troop_type=TroopType.NAVAL,
    cost={Resource.OIL: 4, Resource.IRON: 3, Resource.OSR: 3},
    stress=20,
    stances={
        Stance.DEFENSIVE: StanceAttributes(
            air_combat_value=2, surface_combat_value=1, statuses=ARMORED_STATUSES
        ),
        Stance.OFFENSIVE: StanceAttributes(
            air_combat_value=1, surface_combat_value=2, statuses=ARMORED_STATUSES
        ),
    },
)
CRUISER = Unit(
    name="Cruiser",
    abbrev="CR",
    color=Color.BLUE,
    troop_type=TroopType.NAVAL,
    cost={Resource.OIL: 2, Resource.IRON: 3, Resource.OSR: 2},
    stress=10,
    stances={
        Stance.DEFENSIVE: StanceAttributes(
            air_combat_value=2, surface_combat_value=2, statuses=STANDARD_STATUSES
        ),
        Stance.OFFENSIVE: StanceAttributes(
            air_combat_value=1, surface_combat_value=3, statuses=STANDARD_STATUSES
        ),
    },
)
SUBMARINE = Unit(
    name="Submarine",
    abbrev="SS",
    color=Color.YELLOW,
    troop_type=TroopType.NAVAL,
    cost={Resource.OIL: 1, Resource.IRON: 2, Resource.OSR: 1},
    stress=6,
    stances={
        Stance.OFFENSIVE: StanceAttributes(
            air_combat_value=0, surface_combat_value=2, statuses=SUBMARINE_STATUSES
        ),
    },
)

UNITS = {
    BOMBER,
    FIGHTER,
    ARMOR,
    ARTILLERY,
    INFANTRY,
    BATTLESHIP,
    CARRIER,
    CRUISER,
    SUBMARINE,
}

LAND_UNITS = {u for u in UNITS if u.troop_type == TroopType.LAND}
AIR_UNITS = {u for u in UNITS if u.troop_type == TroopType.AIR}
NAVAL_UNITS = {u for u in UNITS if u.troop_type == TroopType.NAVAL}
UNITS_FROM_ABBREV = {u.abbrev: u for u in UNITS}


# COMMANDS = {
#     Country.USA: {
#         TroopType.NAVAL: [1, 2, 3, 4, 5, 6, 7, 8],
#         TroopType.AIR: [11, 12, 13, 14, 15, 16, 17, 18, 19],
#         TroopType.LAND: [27, 31, 35, 42, 43, 50, 51, 64, 69, 73, 79, 82],
#     },
#     Country.BRITAIN: {
#         TroopType.NAVAL: [1, 2, 3, 4, 5, 6, 7, 8],
#         TroopType.AIR: [11, 12, 13, 14, 15, 16, 17, 18],
#         TroopType.LAND: [28, 32, 36, 45, 47, 53, 60, 63, 68, 71, 75, 80, 88, 90, 96],
#     },
#     Country.RUSSIA: {
#         TroopType.NAVAL: [1, 2, 3],
#         TroopType.AIR: [11, 12, 13, 14, 15, 16],
#         TroopType.LAND: [74, 94, 98, 67, 29, 23, 21, 57, 66, 26, 34, 58],
#     },
#     Country.GERMANY: {
#         TroopType.NAVAL: [1, 2, 3, 4, 5, 6],
#         TroopType.AIR: [11, 12, 13, 14, 15, 16, 17, 18],
#         TroopType.LAND: [84, 86, 91, 55, 38, 72, 48, 22, 56, 33, 37, 61, 40, 49, 59],
#     },
#     Country.JAPAN: {
#         TroopType.NAVAL: [1, 2, 3, 4, 5, 6, 7, 8, 9],
#         TroopType.AIR: [11, 12, 13, 14, 15, 16, 17, 18, 19],
#         TroopType.LAND: [
#             24,
#             25,
#             30,
#             39,
#             41,
#             44,
#             46,
#             52,
#             54,
#             62,
#             65,
#             76,
#             77,
#             78,
#             81,
#             85,
#             87,
#             89,
#             92,
#             95,
#             97,
#         ],
#     },
#     Country.ITALY: {
#         TroopType.NAVAL: [1, 2, 3, 4],
#         TroopType.AIR: [11, 12, 13, 14, 15],
#         TroopType.LAND: [108, 109, 110, 111, 112, 113, 114, 115],
#     },
#     Country.CHINA: {
#         TroopType.NAVAL: [],
#         TroopType.AIR: [],
#         TroopType.LAND: [100, 101, 102, 103, 104, 105, 106, 107],
#     },
# }
