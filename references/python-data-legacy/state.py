import pydantic

from . import enums
from . import map


class Command(pydantic.BaseModel):
    country: enums.Country
    tag: int
    troop_type: enums.TroopType
    units: dict[enums.UnitKind, int] = {}
    region: map.Territory | map.SeaRegion | None = None


class CountryState(pydantic.BaseModel):
    resources: dict[enums.Resource, int] = {}
    stress: int = 0
    medals: int = 0
    civilian_goods: int = 0
    losses: dict[enums.UnitKind, int] = {}
    homeland_status: enums.HomelandStatus = enums.HomelandStatus.ACCEPTABLE_STRESS
    territories: set[map.Territory]
    commands: set[Command] = set()


INITIAL_COUNTRY_STATE = {
    enums.Country.USA.name: CountryState(
        territories={
            map.U1,
            map.U2,
            map.U3,
            map.U4,
            map.U5,
            map.U6,
            map.U7,
            map.U8,
            map.U9,
            map.U10,
        },
        commands={
            Command(
                country=enums.Country.USA,
                tag=1,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.BATTLESHIP: 1, enums.UnitKind.CRUISER: 1},
                region=map.A10,
            ),
            Command(
                country=enums.Country.USA,
                tag=2,
                troop_type=enums.TroopType.NAVAL,
                units={
                    enums.UnitKind.BATTLESHIP: 1,
                    enums.UnitKind.CRUISER: 1,
                    enums.UnitKind.SUBMARINE: 1,
                },
                region=map.P5,
            ),
            Command(
                country=enums.Country.USA,
                tag=3,
                troop_type=enums.TroopType.NAVAL,
                units={
                    enums.UnitKind.CARRIER: 1,
                    enums.UnitKind.CRUISER: 1,
                    enums.UnitKind.SUBMARINE: 1,
                },
                region=map.P9,
            ),
            Command(
                country=enums.Country.USA,
                tag=4,
                troop_type=enums.TroopType.NAVAL,
                units={
                    enums.UnitKind.CARRIER: 1,
                    enums.UnitKind.CRUISER: 2,
                    enums.UnitKind.SUBMARINE: 1,
                },
                region=map.P19,
            ),
            Command(country=enums.Country.USA, tag=5, troop_type=enums.TroopType.NAVAL),
            Command(country=enums.Country.USA, tag=6, troop_type=enums.TroopType.NAVAL),
            Command(country=enums.Country.USA, tag=7, troop_type=enums.TroopType.NAVAL),
            Command(country=enums.Country.USA, tag=8, troop_type=enums.TroopType.NAVAL),
            Command(
                country=enums.Country.USA,
                tag=11,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.U1,
            ),
            Command(
                country=enums.Country.USA,
                tag=12,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.U2,
            ),
            Command(
                country=enums.Country.USA,
                tag=13,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.U3,
            ),
            Command(
                country=enums.Country.USA,
                tag=14,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 1},
                region=map.B1,
            ),
            Command(
                country=enums.Country.USA,
                tag=15,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 1},
                region=map.U10,
            ),
            Command(
                country=enums.Country.USA,
                tag=16,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.U6,
            ),
            Command(
                country=enums.Country.USA,
                tag=17,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.U7,
            ),
            Command(country=enums.Country.USA, tag=18, troop_type=enums.TroopType.AIR),
            Command(country=enums.Country.USA, tag=17, troop_type=enums.TroopType.AIR),
            Command(
                country=enums.Country.USA,
                tag=27,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARMOR: 1, enums.UnitKind.INFANTRY: 1},
                region=map.U2,
            ),
            Command(
                country=enums.Country.USA,
                tag=31,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.U5,
            ),
            Command(
                country=enums.Country.USA,
                tag=35,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.U4,
            ),
            Command(country=enums.Country.USA, tag=42, troop_type=enums.TroopType.LAND),
            Command(
                country=enums.Country.USA,
                tag=43,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.J25,
            ),
            Command(
                country=enums.Country.USA,
                tag=50,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.B27,
            ),
            Command(
                country=enums.Country.USA,
                tag=51,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 2,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.U1,
            ),
            Command(
                country=enums.Country.USA,
                tag=64,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 2},
                region=map.U6,
            ),
            Command(
                country=enums.Country.USA,
                tag=69,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 2,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.U3,
            ),
            Command(
                country=enums.Country.USA,
                tag=73,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.U10,
            ),
            Command(
                country=enums.Country.USA,
                tag=79,
                troop_type=enums.TroopType.LAND,
            ),
            Command(
                country=enums.Country.USA,
                tag=82,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARMOR: 1, enums.UnitKind.INFANTRY: 2},
                region=map.B1,
            ),
        },
    ),
    enums.Country.BRITAIN.name: CountryState(
        territories={
            map.B1,
            map.B2,
            map.B3,
            map.B4,
            map.B5,
            map.B6,
            map.B7,
            map.B8,
            map.B9,
            map.B10,
            map.B11,
            map.B12,
            map.B13,
            map.B14,
            map.B15,
            map.B16,
            map.B17,
            map.B18,
            map.B19,
            map.B20,
            map.B21,
            map.B22,
            map.B23,
            map.B24,
            map.B25,
            map.B26,
            map.B27,
            map.B28,
            map.B29,
            map.B30,
        },
        commands={
            Command(
                country=enums.Country.BRITAIN, tag=1, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=2,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.CARRIER: 1, enums.UnitKind.CRUISER: 1},
                region=map.I2,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=3,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.CRUISER: 1, enums.UnitKind.SUBMARINE: 1},
                region=map.M3,
            ),
            Command(
                country=enums.Country.BRITAIN, tag=4, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.BRITAIN, tag=5, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=6,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.BATTLESHIP: 1, enums.UnitKind.CRUISER: 1},
                region=map.A6,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=7,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.BATTLESHIP: 1, enums.UnitKind.CRUISER: 1},
                region=map.A7,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=8,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.CRUISER: 1, enums.UnitKind.SUBMARINE: 1},
                region=map.P18,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=11,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 3},
                region=map.B1,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=12,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.B22,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=13,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.B3,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=14,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 1},
                region=map.B29,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=15,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 1},
                region=map.B5,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=16,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.B18,
            ),
            Command(
                country=enums.Country.BRITAIN, tag=17, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.BRITAIN, tag=18, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.BRITAIN, tag=28, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.BRITAIN, tag=32, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=36,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 1,
                },
                region=map.B24,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=45,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 1,
                },
                region=map.B29,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=47,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 2,
                    enums.UnitKind.ARTILLERY: 2,
                    enums.UnitKind.INFANTRY: 1,
                },
                region=map.B5,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=53,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 1,
                },
                region=map.B1,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=60,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 3,
                },
                region=map.B18,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=63,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.B16,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=68,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.INFANTRY: 1},
                region=map.B22,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=71,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.B25,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=75,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.B10,
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=80,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.B23,
            ),
            Command(
                country=enums.Country.BRITAIN, tag=88, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.BRITAIN,
                tag=90,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.B28,
            ),
            Command(
                country=enums.Country.BRITAIN, tag=96, troop_type=enums.TroopType.LAND
            ),
        },
    ),
    enums.Country.RUSSIA.name: CountryState(
        territories={
            map.R1,
            map.R2,
            map.R3,
            map.R4,
            map.R5,
            map.R6,
            map.R7,
            map.R8,
            map.R9,
            map.R10,
            map.R11,
            map.R12,
            map.R13,
            map.R14,
            map.R15,
            map.R16,
            map.R17,
            map.R18,
        },
        commands={
            Command(
                country=enums.Country.RUSSIA,
                tag=1,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.CRUISER: 1, enums.UnitKind.SUBMARINE: 1},
                region=map.A4,
            ),
            Command(
                country=enums.Country.RUSSIA, tag=2, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.RUSSIA, tag=3, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=11,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.R1,
            ),
            Command(
                country=enums.Country.RUSSIA, tag=12, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=13,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.R3,
            ),
            Command(
                country=enums.Country.RUSSIA, tag=14, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=15,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.R5,
            ),
            Command(
                country=enums.Country.RUSSIA, tag=16, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=21,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARMOR: 1, enums.UnitKind.INFANTRY: 3},
                region=map.R7,
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=23,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 2,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 4,
                },
                region=map.R5,
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=26,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 2,
                    enums.UnitKind.ARTILLERY: 2,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.R1,
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=29,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 2, enums.UnitKind.INFANTRY: 4},
                region=map.R4,
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=34,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.R14,
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=57,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARMOR: 1, enums.UnitKind.INFANTRY: 4},
                region=map.R6,
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=58,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 2},
                region=map.R16,
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=66,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 2},
                region=map.R2,
            ),
            Command(
                country=enums.Country.RUSSIA,
                tag=67,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 3},
                region=map.R3,
            ),
            Command(
                country=enums.Country.RUSSIA, tag=74, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.RUSSIA, tag=94, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.RUSSIA, tag=98, troop_type=enums.TroopType.LAND
            ),
        },
    ),
    enums.Country.CHINA.name: CountryState(
        territories={
            map.C1,
            map.C2,
            map.C3,
            map.C4,
            map.C5,
        },
        commands={
            Command(
                country=enums.Country.CHINA, tag=100, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.CHINA,
                tag=101,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 3},
                region=map.C1,
            ),
            Command(
                country=enums.Country.CHINA,
                tag=102,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 3},
                region=map.C2,
            ),
            Command(
                country=enums.Country.CHINA,
                tag=103,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 2},
                region=map.C3,
            ),
            Command(
                country=enums.Country.CHINA,
                tag=104,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 3},
                region=map.C4,
            ),
            Command(
                country=enums.Country.CHINA,
                tag=105,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.INFANTRY: 2},
                region=map.C5,
            ),
            Command(
                country=enums.Country.CHINA, tag=106, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.CHINA, tag=107, troop_type=enums.TroopType.LAND
            ),
        },
    ),
    enums.Country.GERMANY.name: CountryState(
        territories={
            map.G1,
            map.G2,
            map.G3,
            map.G4,
            map.G5,
            map.G6,
            map.G7,
            map.G8,
            map.G9,
            map.G10,
            map.G11,
            map.G12,
            map.G13,
            map.G14,
            map.G15,
            map.G16,
        },
        commands={
            Command(
                country=enums.Country.GERMANY,
                tag=1,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.CRUISER: 2, enums.UnitKind.SUBMARINE: 1},
                region=map.A5,
            ),
            Command(
                country=enums.Country.GERMANY, tag=2, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=3,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.SUBMARINE: 2},
                region=map.A13,
            ),
            Command(
                country=enums.Country.GERMANY, tag=4, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=5,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.SUBMARINE: 3},
                region=map.A15,
            ),
            Command(
                country=enums.Country.GERMANY, tag=6, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=11,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.G1,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=12,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.G10,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=13,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.G3,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=14,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.G4,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=15,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.G5,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=16,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.G6,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=17,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.T5,
            ),
            Command(
                country=enums.Country.GERMANY, tag=18, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=22,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 2,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.G8,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=33,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.G5,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=37,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.G7,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=38,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.G2,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=40,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.G9,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=48,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 2,
                    enums.UnitKind.ARTILLERY: 2,
                    enums.UnitKind.INFANTRY: 3,
                },
                region=map.G1,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=49,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.T5,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=55,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 3,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.G10,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=56,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.G4,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=59,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 1,
                },
                region=map.G13,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=61,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 2,
                    enums.UnitKind.ARTILLERY: 2,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.G6,
            ),
            Command(
                country=enums.Country.GERMANY,
                tag=72,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 2,
                    enums.UnitKind.ARTILLERY: 3,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.G3,
            ),
            Command(
                country=enums.Country.GERMANY, tag=84, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.GERMANY, tag=86, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.GERMANY, tag=91, troop_type=enums.TroopType.LAND
            ),
        },
    ),
    enums.Country.JAPAN.name: CountryState(
        territories={
            map.J1,
            map.J2,
            map.J3,
            map.J4,
            map.J5,
            map.J6,
            map.J7,
            map.J8,
            map.J9,
            map.J10,
            map.J11,
            map.J12,
            map.J13,
            map.J14,
            map.J15,
            map.J16,
            map.J17,
            map.J18,
            map.J19,
            map.J20,
            map.J21,
            map.J22,
            map.J23,
            map.J24,
            map.J25,
            map.J26,
            map.J27,
            map.J28,
        },
        commands={
            Command(
                country=enums.Country.JAPAN,
                tag=1,
                troop_type=enums.TroopType.NAVAL,
                units={
                    enums.UnitKind.BATTLESHIP: 1,
                    enums.UnitKind.CARRIER: 1,
                    enums.UnitKind.CRUISER: 1,
                    enums.UnitKind.SUBMARINE: 1,
                },
                region=map.P1,
            ),
            Command(
                country=enums.Country.JAPAN, tag=2, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=3,
                troop_type=enums.TroopType.NAVAL,
                units={
                    enums.UnitKind.BATTLESHIP: 1,
                    enums.UnitKind.CARRIER: 1,
                    enums.UnitKind.CRUISER: 1,
                    enums.UnitKind.SUBMARINE: 1,
                },
                region=map.P13,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=4,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.CRUISER: 2, enums.UnitKind.SUBMARINE: 1},
                region=map.P14,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=5,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.BATTLESHIP: 1, enums.UnitKind.CRUISER: 1},
                region=map.P15,
            ),
            Command(
                country=enums.Country.JAPAN, tag=6, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.JAPAN, tag=7, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.JAPAN, tag=8, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=9,
                troop_type=enums.TroopType.NAVAL,
                units={enums.UnitKind.CARRIER: 1, enums.UnitKind.CRUISER: 1},
                region=map.I9,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=11,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.J1,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=12,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 1},
                region=map.J22,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=13,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 2},
                region=map.J3,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=14,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 1},
                region=map.J14,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=15,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.J5,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=16,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 1},
                region=map.J16,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=17,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.J7,
            ),
            Command(
                country=enums.Country.JAPAN, tag=18, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.JAPAN, tag=19, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=24,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.J4,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=25,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.INFANTRY: 1},
                region=map.J12,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=30,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 2},
                region=map.J8,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=39,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.J22,
            ),
            Command(
                country=enums.Country.JAPAN, tag=41, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=44,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 2,
                    enums.UnitKind.ARTILLERY: 2,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.J1,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=46,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.J6,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=52,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.J20,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=54,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.INFANTRY: 1},
                region=map.J11,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=62,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.INFANTRY: 1},
                region=map.J2,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=65,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.J3,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=76,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.J24,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=77,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 2},
                region=map.J14,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=78,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.INFANTRY: 1},
                region=map.J10,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=81,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.J5,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=85,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.J9,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=87,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.INFANTRY: 1},
                region=map.J23,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=89,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.J17,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=92,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.J25,
            ),
            Command(
                country=enums.Country.JAPAN,
                tag=95,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 1},
                region=map.J7,
            ),
            Command(
                country=enums.Country.JAPAN, tag=97, troop_type=enums.TroopType.LAND
            ),
        },
    ),
    enums.Country.ITALY.name: CountryState(
        territories={
            map.T1,
            map.T2,
            map.T3,
            map.T4,
            map.T5,
        },
        commands={
            Command(
                country=enums.Country.ITALY,
                tag=1,
                troop_type=enums.TroopType.NAVAL,
                units={
                    enums.UnitKind.BATTLESHIP: 1,
                    enums.UnitKind.CRUISER: 1,
                    enums.UnitKind.SUBMARINE: 1,
                },
                region=map.M2,
            ),
            Command(
                country=enums.Country.ITALY, tag=2, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.ITALY, tag=3, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.ITALY, tag=4, troop_type=enums.TroopType.NAVAL
            ),
            Command(
                country=enums.Country.ITALY,
                tag=11,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.BOMBER: 1, enums.UnitKind.FIGHTER: 1},
                region=map.T1,
            ),
            Command(
                country=enums.Country.ITALY,
                tag=12,
                troop_type=enums.TroopType.AIR,
                units={enums.UnitKind.FIGHTER: 2},
                region=map.T2,
            ),
            Command(
                country=enums.Country.ITALY, tag=13, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.ITALY, tag=14, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.ITALY, tag=15, troop_type=enums.TroopType.AIR
            ),
            Command(
                country=enums.Country.ITALY, tag=108, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.ITALY, tag=109, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.ITALY, tag=110, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.ITALY, tag=111, troop_type=enums.TroopType.LAND
            ),
            Command(
                country=enums.Country.ITALY,
                tag=112,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.INFANTRY: 1},
                region=map.T4,
            ),
            Command(
                country=enums.Country.ITALY,
                tag=113,
                troop_type=enums.TroopType.LAND,
                units={enums.UnitKind.ARTILLERY: 1, enums.UnitKind.INFANTRY: 2},
                region=map.T5,
            ),
            Command(
                country=enums.Country.ITALY,
                tag=114,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 3,
                },
                region=map.T1,
            ),
            Command(
                country=enums.Country.ITALY,
                tag=115,
                troop_type=enums.TroopType.LAND,
                units={
                    enums.UnitKind.ARMOR: 1,
                    enums.UnitKind.ARTILLERY: 1,
                    enums.UnitKind.INFANTRY: 2,
                },
                region=map.T2,
            ),
        },
    ),
}


# TODO: check missing land commands 70, 83, 99


class GameState(pydantic.BaseModel):
    country_states: dict[enums.Country : CountryState] = INITIAL_COUNTRY_STATE
    neutral: set[map.Territory] = {
        map.N1,
        map.N2,
        map.N3,
        map.N4,
        map.N5,
        map.N6,
        map.N7,
        map.N8,
        map.N9,
        map.N10,
        map.N11,
        map.N12,
        map.N13,
        map.N14,
        map.N15,
        map.N16,
        map.N17,
        map.N18,
        map.N19,
    }
