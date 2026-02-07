import pydantic

from .enums import Alliance, Country, Resource, UnitKind


class CrossOceanicConvoy(pydantic.BaseModel):
    country: Country
    resources: dict[Resource, int]


class SeaRegion(pydantic.BaseModel):
    code: str
    convoy: CrossOceanicConvoy | None = None


class Port(pydantic.BaseModel):
    sea: SeaRegion
    convoy: dict[Resource, int] = {}


class Territory(pydantic.BaseModel):
    code: str
    name: str
    strategic_value: int = 0
    industry: bool = False
    chinese_mobilization: bool = False
    trade: Resource | None = None
    defense: dict[UnitKind, int] = {}
    alignment: Alliance | None = None
    resources: dict[Resource, int] = {}
    ports = [Port] = []
    embattled: bool = False
    bombs: int = 0


class NarrowSeaPassage(pydantic.BaseModel):
    name: str
    regions: set[SeaRegion]
    required_control: set[Territory]


class ImpassableTerrain(pydantic.BaseModel):
    name: str
    neighbors: set[Territory]


A1 = SeaRegion(code="A1")
A2 = SeaRegion(code="A2")
A3 = SeaRegion(
    code="A3",
    convoy=CrossOceanicConvoy(
        country=Country.USA,
        resources={Resource.OIL: 1, Resource.OSR: 1},
    ),
)
A4 = SeaRegion(code="A4")
A5 = SeaRegion(code="A5")
A6 = SeaRegion(code="A6")
A7 = SeaRegion(code="A7")
A8 = SeaRegion(
    code="A8",
    convoy=CrossOceanicConvoy(
        country=Country.BRITAIN,
        resources={Resource.OIL: 1, Resource.IRON: 1, Resource.OSR: 1},
    ),
)
A9 = SeaRegion(
    code="A9",
    convoy=CrossOceanicConvoy(
        country=Country.USA,
        resources={Resource.OIL: 1, Resource.IRON: 1, Resource.OSR: 3},
    ),
)
A10 = SeaRegion(code="A10")
A11 = SeaRegion(code="A11")
A12 = SeaRegion(code="A12")
A13 = SeaRegion(code="A13")
A14 = SeaRegion(code="A14")
A15 = SeaRegion(code="A15")
A16 = SeaRegion(code="A16")
A17 = SeaRegion(code="A17")
A18 = SeaRegion(code="A18")
A19 = SeaRegion(code="A19")
M1 = SeaRegion(code="M1")
M2 = SeaRegion(code="M2")
M3 = SeaRegion(code="M3")
M4 = SeaRegion(code="M4")
M5 = SeaRegion(code="M5")
M6 = SeaRegion(code="M6")
I1 = SeaRegion(code="I1")
I2 = SeaRegion(code="I2")
I3 = SeaRegion(code="I3")
I4 = SeaRegion(code="I4")
I5 = SeaRegion(code="I5")
I6 = SeaRegion(code="I6")
I7 = SeaRegion(code="I7")
I8 = SeaRegion(code="I8")
I9 = SeaRegion(code="I9")
I10 = SeaRegion(code="I10")
P0 = SeaRegion(code="P0")
P1 = SeaRegion(code="P1")
P2 = SeaRegion(code="P2")
P3 = SeaRegion(code="P3")
P4 = SeaRegion(code="P4")
P5 = SeaRegion(code="P5")
P6 = SeaRegion(code="P6")
P7 = SeaRegion(code="P7")
P8 = SeaRegion(code="P8")
P9 = SeaRegion(code="P9")
P10 = SeaRegion(code="P10")
P11 = SeaRegion(code="P11")
P12 = SeaRegion(code="P12")
P13 = SeaRegion(code="P13")
P14 = SeaRegion(code="P14")
P15 = SeaRegion(code="P15")
P16 = SeaRegion(code="P16")
P17 = SeaRegion(code="P17")
P18 = SeaRegion(code="P18")
P19 = SeaRegion(code="P19")
P20 = SeaRegion(code="P20")

SEA_REGIONS = {
    A1,
    A2,
    A3,
    A4,
    A5,
    A6,
    A7,
    A8,
    A9,
    A10,
    A11,
    A12,
    A13,
    A14,
    A15,
    A16,
    A17,
    A18,
    A19,
    M1,
    M2,
    M3,
    M4,
    M5,
    M6,
    I1,
    I2,
    I3,
    I4,
    I5,
    I6,
    I7,
    I8,
    I9,
    I10,
    P0,
    P1,
    P2,
    P3,
    P4,
    P5,
    P6,
    P7,
    P8,
    P9,
    P10,
    P11,
    P12,
    P13,
    P14,
    P15,
    P16,
    P17,
    P18,
    P19,
    P20,
}

B1 = Territory(
    code="B1",
    name="Great Britain",
    strategic_value=8,
    industry=True,
    resources={Resource.IRON: 1, Resource.OSR: 2},
    ports=[Port(sea=A6), Port(sea=A7, convoy={Resource.IRON: 1, Resource.OSR: 1})],
)
B2 = Territory(
    code="B2",
    name="Azores",
)
B3 = Territory(
    code="B3",
    name="Gibralter",
    strategic_value=1,
    ports=[Port(sea=M1)],
)
B4 = Territory(
    code="B4",
    name="Malta",
    strategic_value=1,
)
B5 = Territory(
    code="B5",
    name="Egypt",
    strategic_value=3,
    resources={Resource.OIL: 1},
    ports=[Port(sea=M3, convoy={Resource.OIL: 1})],
)
B6 = Territory(
    code="B6",
    name="Sudan",
    strategic_value=1,
)
B7 = Territory(
    code="B7",
    name="Horn of Africa",
    strategic_value=1,
)
B8 = Territory(
    code="B8",
    name="British East Africa",
    strategic_value=1,
    resources={Resource.OSR: 1},
)
B9 = Territory(
    code="B9",
    name="Rhodesia",
    strategic_value=1,
    resources={Resource.OSR: 1},
)
B10 = Territory(
    code="B10",
    name="South Africa",
    strategic_value=3,
    industry=True,
    resources={Resource.IRON: 1, Resource.OSR: 1},
    ports=[Port(sea=A19, convoy={Resource.IRON: 1, Resource.OSR: 1})],
)
B11 = Territory(
    code="B11",
    name="Belgian Congo",
    strategic_value=1,
    resources={Resource.OSR: 1},
    ports=[Port(sea=A18, convoy={Resource.OSR: 1})],
)
B12 = Territory(
    code="B12",
    name="French Equatorial Africa",
)
B13 = Territory(
    code="B13",
    name="Nigeria Cameroon",
    strategic_value=1,
    resources={Resource.IRON: 1},
    ports=[Port(sea=A18, convoy={Resource.IRON: 1})],
)
B14 = Territory(
    code="B14",
    name="Gold Coast",
    strategic_value=1,
    resources={Resource.OSR: 1},
    ports=[Port(sea=A18, convoy={Resource.OSR: 1})],
)
B15 = Territory(
    code="B15",
    name="Sierra Leone",
    strategic_value=1,
)
B16 = Territory(
    code="B16",
    name="Middle East",
    strategic_value=3,
    resources={Resource.OIL: 2},
    ports=[Port(sea=I1, convoy={Resource.OIL: 1})],
)
B17 = Territory(
    code="B17",
    name="Iran",
    strategic_value=2,
    resources={Resource.OIL: 1},
    ports=[Port(sea=I1, convoy={Resource.OIL: 1})],
)
B18 = Territory(
    code="B18",
    name="India",
    strategic_value=5,
    industry=True,
    resources={Resource.OSR: 2},
    ports=[Port(sea=I1, convoy={Resource.OSR: 1})],
)
B19 = Territory(
    code="B19",
    name="Ceylon",
)
B20 = Territory(
    code="B20",
    name="Maldives",
)
B21 = Territory(
    code="B21",
    name="Western Australia",
    strategic_value=1,
    resources={Resource.OSR: 1},
)
B22 = Territory(
    code="B22",
    name="Northern Territory",
    strategic_value=1,
    resources={Resource.OSR: 1},
)
B23 = Territory(
    code="B23",
    name="South Australia",
    strategic_value=2,
    resources={Resource.IRON: 1},
)
B24 = Territory(
    code="B24",
    name="Eastern Australia",
    strategic_value=3,
    industry=True,
    resources={Resource.IRON: 1, Resource.OSR: 1},
    ports=[Port(sea=P18, convoy={Resource.IRON: 1, Resource.OSR: 1})],
)
B25 = Territory(
    code="B25",
    name="Papua",
    strategic_value=1,
)
B26 = Territory(
    code="B26",
    name="New Hebrides",
    strategic_value=0,
)
B27 = Territory(
    code="B27",
    name="New Zealand",
    strategic_value=2,
)
B28 = Territory(
    code="B28",
    name="Western Canada",
    strategic_value=3,
    resources={Resource.OIL: 1, Resource.IRON: 2, Resource.OSR: 1},
    ports=[Port(sea=P4, convoy={Resource.OIL: 1, Resource.IRON: 1, Resource.OSR: 1})],
)
B29 = Territory(
    code="B29",
    name="Eastern Canada",
    strategic_value=4,
    industry=True,
    resources={Resource.IRON: 1, Resource.OSR: 1},
    ports=[Port(sea=A9, convoy={Resource.IRON: 1})],
)
B30 = Territory(
    code="B30",
    name="The Guyanas",
)
C1 = Territory(
    code="C1",
    name="Honan",
    strategic_value=1,
    chinese_mobilization=True,
    resources={Resource.OSR: 1},
)
C2 = Territory(
    code="C2",
    name="Kwangsi",
    strategic_value=1,
    chinese_mobilization=True,
    resources={Resource.OSR: 1},
)
C3 = Territory(
    code="C3",
    name="Szechwan Yunnan",
    strategic_value=1,
    chinese_mobilization=True,
    resources={Resource.OSR: 2},
)
C4 = Territory(
    code="C4",
    name="Tsinghai Ningsia",
    strategic_value=2,
    chinese_mobilization=True,
    resources={Resource.IRON: 1, Resource.OSR: 2},
)
C5 = Territory(
    code="C5",
    name="Sinkiang",
    strategic_value=1,
    chinese_mobilization=True,
    resources={Resource.IRON: 1},
)
G1 = Territory(
    code="G1",
    name="Greater Germany",
    strategic_value=8,
    industry=True,
    resources={Resource.OIL: 1, Resource.IRON: 2, Resource.OSR: 3},
    ports=[Port(sea=A5, convoy={Resource.OIL: 1, Resource.IRON: 1, Resource.OSR: 1})],
)
G2 = Territory(
    code="G2",
    name="Denmark",
    strategic_value=1,
    resources={Resource.OSR: 1},
)
G3 = Territory(
    code="G3",
    name="France",
    strategic_value=6,
    industry=True,
    resources={Resource.IRON: 2, Resource.OSR: 3},
    ports=[Port(sea=A15, convoy={Resource.IRON: 1, Resource.OSR: 1}), Port(sea=M1)],
)
G4 = Territory(
    code="G4",
    name="Poland Slovakia Hungary",
    strategic_value=4,
    industry=True,
    resources={Resource.IRON: 2, Resource.OSR: 3},
)
G5 = Territory(
    code="G5",
    name="Bulgaria Rumania",
    strategic_value=4,
    industry=True,
    resources={Resource.OIL: 2, Resource.OSR: 2},
    ports=[Port(sea=M4)],
)
G6 = Territory(
    code="G6",
    name="Ukraine",
    strategic_value=4,
    industry=True,
    resources={Resource.OIL: 1, Resource.OSR: 3},
    ports=[Port(sea=M4)],
)
G7 = Territory(
    code="G7",
    name="Belarus",
    strategic_value=2,
    industry=True,
    resources={Resource.IRON: 2, Resource.OSR: 1},
)
G8 = Territory(
    code="G8",
    name="Baltic States",
    strategic_value=1,
    resources={Resource.OSR: 1},
)
G9 = Territory(
    code="G9",
    name="Finland",
    strategic_value=2,
    resources={Resource.IRON: 2},
    ports=[Port(sea=A5, convoy={Resource.IRON: 1})],
)
G10 = Territory(
    code="G10",
    name="Norway",
    strategic_value=2,
    resources={Resource.IRON: 1},
    ports=[Port(sea=A5, convoy={Resource.IRON: 1})],
)
G11 = Territory(
    code="G11",
    name="French Morocco",
    strategic_value=2,
    resources={Resource.OIL: 1, Resource.OSR: 1},
    ports=[Port(sea=A15, convoy={Resource.OIL: 1, Resource.OSR: 1})],
)
G12 = Territory(
    code="G12",
    name="Algeria",
    strategic_value=2,
    resources={Resource.OIL: 1},
    ports=[Port(sea=M2, convoy={Resource.OIL: 1})],
)
G13 = Territory(
    code="G13",
    name="Tunisia",
    strategic_value=1,
    resources={Resource.IRON: 1},
    ports=[Port(sea=M2, convoy={Resource.IRON: 1})],
)
G14 = Territory(
    code="G14",
    name="Crete",
    strategic_value=1,
)
G15 = Territory(
    code="G15",
    name="French West Africa",
    strategic_value=1,
    resources={Resource.OSR: 1},
    ports=[Port(sea=A17, convoy={Resource.OSR: 1})],
)
G16 = Territory(
    code="G16",
    name="Madagascar",
)
J1 = Territory(
    code="J1",
    name="Imperial Japan",
    strategic_value=8,
    industry=True,
    resources={Resource.IRON: 2, Resource.OSR: 2},
    ports=[Port(sea=P1, convoy={Resource.IRON: 1, Resource.OSR: 1})],
)
J2 = Territory(
    code="J2",
    name="Korea",
    strategic_value=2,
    resources={Resource.IRON: 1, Resource.OSR: 1},
    ports=[Port(sea=P1, convoy={Resource.IRON: 1, Resource.OSR: 1})],
)
J3 = Territory(
    code="J3",
    name="Manchuria",
    strategic_value=3,
    chinese_mobilization=True,
    resources={Resource.IRON: 3, Resource.OSR: 1},
    ports=[Port(sea=P0, convoy={Resource.IRON: 1, Resource.OSR: 1})],
)
J4 = Territory(
    code="J4",
    name="Peiping",
    strategic_value=2,
    industry=True,
    chinese_mobilization=True,
    resources={Resource.IRON: 1, Resource.OSR: 2},
    ports=[Port(sea=P0, convoy={Resource.IRON: 1, Resource.OSR: 1})],
)
J5 = Territory(
    code="J5",
    name="Chekiang Kwangtung",
    strategic_value=2,
    chinese_mobilization=True,
    resources={Resource.IRON: 2, Resource.OSR: 1},
    ports=[Port(sea=P0, convoy={Resource.IRON: 1, Resource.OSR: 1}), Port(sea=P14)],
)
J6 = Territory(
    code="J6",
    name="Indochina",
    strategic_value=1,
    resources={Resource.OSR: 1},
    ports=[Port(sea=P15, convoy={Resource.OSR: 1})],
)
J7 = Territory(
    code="J7",
    name="Thailand",
    strategic_value=1,
    resources={Resource.OSR: 2},
)
J8 = Territory(
    code="J8",
    name="Burma",
    strategic_value=1,
    resources={Resource.OSR: 1},
)
J9 = Territory(
    code="J9",
    name="Malaya",
    strategic_value=2,
    resources={Resource.OSR: 2},
    ports=[Port(sea=P15, convoy={Resource.OSR: 1})],
)
J10 = Territory(
    code="J10",
    name="Sumatra",
    strategic_value=2,
    resources={Resource.OIL: 3},
    ports=[Port(sea=P16, convoy={Resource.OIL: 1})],
)
J11 = Territory(
    code="J11",
    name="Java",
    strategic_value=2,
    resources={Resource.OIL: 2},
    ports=[Port(sea=P16, convoy={Resource.OIL: 1})],
)
J12 = Territory(
    code="J12",
    name="Borneo",
    strategic_value=2,
    resources={Resource.OIL: 2, Resource.OSR: 1},
    ports=[Port(sea=P15, convoy={Resource.OSR: 1, Resource.OIL: 1})],
)
J13 = Territory(
    code="J13",
    name="Celebes",
)
J14 = Territory(
    code="J14",
    name="Philippines",
    strategic_value=2,
    resources={Resource.IRON: 1, Resource.OSR: 2},
    ports=[Port(sea=P14, convoy={Resource.IRON: 1, Resource.OSR: 1})],
)
J15 = Territory(
    code="J15",
    name="Hainan",
)
J16 = Territory(
    code="J16",
    name="Formosa",
    strategic_value=1,
)
J17 = Territory(
    code="J17",
    name="Okinawa",
    strategic_value=1,
)
J18 = Territory(
    code="J18",
    name="Palau",
)
J19 = Territory(
    code="J19",
    name="Japanese Sakhalin Island",
)
J20 = Territory(
    code="J20",
    name="Iwo Jima",
    strategic_value=1,
)
J21 = Territory(
    code="J21",
    name="Mariana Islands",
    strategic_value=0,
)
J22 = Territory(
    code="J22",
    name="Caroline Islands",
    strategic_value=2,
    ports=[Port(sea=P13)],
)
J23 = Territory(
    code="J23",
    name="New Britain",
    strategic_value=1,
)
J24 = Territory(
    code="J24",
    name="New Guinea",
    strategic_value=1,
)
J25 = Territory(
    code="J25",
    name="Solomon Islands",
    strategic_value=1,
    embattled=True,
)
J26 = Territory(
    code="J26",
    name="Wake Island",
)
J27 = Territory(
    code="J27",
    name="Marshall Islands",
)
J28 = Territory(
    code="J28",
    name="Gilbert Islands",
)
N1 = Territory(
    code="N1",
    name="Mexico",
    strategic_value=0,
    trade=Resource.IRON,
    alignment=Alliance.ALLIES,
    defense={UnitKind.INFANTRY: 3, UnitKind.ARTILLERY: 1},
    ports=[Port(sea=P6), Port(sea=A11)],
)
N2 = Territory(
    code="N2",
    name="Central America",
    alignment=Alliance.ALLIES,
)
N3 = Territory(
    code="N3",
    name="West Indies",
    alignment=Alliance.ALLIES,
)
N4 = Territory(
    code="N4",
    name="Colombia",
    trade=Resource.OSR,
    defense={UnitKind.INFANTRY: 4},
    ports=[Port(sea=P7), Port(sea=A12)],
)
N5 = Territory(
    code="N5",
    name="Venezuela",
    trade=Resource.OIL,
    defense={UnitKind.INFANTRY: 4},
    ports=[Port(sea=A12)],
)
N6 = Territory(
    code="N6",
    name="Brazil",
    trade=Resource.IRON,
    alignment=Alliance.ALLIES,
    defense={UnitKind.INFANTRY: 4, UnitKind.ARTILLERY: 2, UnitKind.FIGHTER: 1},
)
N7 = Territory(
    code="N7",
    name="Greenland",
    alignment=Alliance.ALLIES,
)
N8 = Territory(
    code="N8",
    name="Iceland",
    alignment=Alliance.ALLIES,
)
N9 = Territory(
    code="N9",
    name="Ireland",
    defense={UnitKind.INFANTRY: 3},
)
N10 = Territory(
    code="N10",
    name="Sweden",
    defense={UnitKind.INFANTRY: 4, UnitKind.ARTILLERY: 1, UnitKind.FIGHTER: 1},
    ports=[Port(sea=A5)],
)
N11 = Territory(
    code="N11",
    name="Spain",
    defense={UnitKind.INFANTRY: 6, UnitKind.ARTILLERY: 2, UnitKind.FIGHTER: 1},
    ports=[Port(sea=M1)],
)
N12 = Territory(
    code="N12",
    name="Portugal",
    defense={UnitKind.INFANTRY: 4},
)
N13 = Territory(
    code="N13",
    name="Switzerland",
    defense={UnitKind.INFANTRY: 3},
)
N14 = Territory(
    code="N14",
    name="Turkey",
    defense={UnitKind.INFANTRY: 6, UnitKind.ARTILLERY: 2, UnitKind.FIGHTER: 1},
)
N15 = Territory(
    code="N15",
    name="Arabia",
    defense={UnitKind.INFANTRY: 3},
    ports=[Port(sea=I1)],
)
N16 = Territory(
    code="N16",
    name="Angola",
    defense={UnitKind.INFANTRY: 3},
)
N17 = Territory(
    code="N17",
    name="Mozambique",
    defense={UnitKind.INFANTRY: 3},
)
N18 = Territory(
    code="N18",
    name="Afghanistan",
    defense={UnitKind.INFANTRY: 4},
)
N19 = Territory(
    code="N19",
    name="Mongolia",
    defense={UnitKind.INFANTRY: 3},
)
R1 = Territory(
    code="R1",
    name="Moscow",
    strategic_value=5,
    industry=True,
    resources={Resource.OSR: 1},
)
R2 = Territory(
    code="R2",
    name="Arkhangelsk",
    strategic_value=3,
    industry=True,
    resources={Resource.OSR: 1},
    ports=[Port(sea=A4, convoy={Resource.OSR: 1})],
)
R3 = Territory(
    code="R3",
    name="Karelia",
    strategic_value=2,
    industry=True,
    ports=[Port(sea=A4, convoy={Resource.IRON: 1})],
)
R4 = Territory(
    code="R4",
    name="Leningrad",
    strategic_value=3,
    industry=True,
    resources={Resource.OSR: 1},
    ports=[Port(sea=A5)],
)
R5 = Territory(
    code="R5",
    name="Bryansk",
    strategic_value=2,
    industry=True,
    resources={Resource.OSR: 1},
)
R6 = Territory(
    code="R6",
    name="Caucasus",
    strategic_value=3,
    resources={Resource.OIL: 2},
)
R7 = Territory(
    code="R7",
    name="Volga",
    strategic_value=2,
    industry=True,
    resources={Resource.OSR: 1},
)
R8 = Territory(
    code="R8",
    name="Kazakh",
    strategic_value=1,
    resources={Resource.OSR: 2},
)
R9 = Territory(
    code="R9",
    name="Turkmen Uzbek",
    strategic_value=1,
)
R10 = Territory(
    code="R10",
    name="East Kazakh",
    strategic_value=1,
)
R11 = Territory(
    code="R11",
    name="Sverdlovsk",
    strategic_value=3,
    resources={Resource.OSR: 2},
)
R12 = Territory(
    code="R12",
    name="Urals",
    strategic_value=2,
    resources={Resource.OIL: 2},
)
R13 = Territory(
    code="R13",
    name="Krasnoyarsk",
    strategic_value=1,
    resources={Resource.OIL: 1},
)
R14 = Territory(
    code="R14",
    name="Amur Irkutsk",
    strategic_value=2,
    resources={Resource.OSR: 1},
)
R15 = Territory(
    code="R15",
    name="Yakut",
    strategic_value=2,
    resources={Resource.OIL: 1},
)
R16 = Territory(
    code="R16",
    name="Khabarovsky",
    strategic_value=2,
    industry=True,
    ports=[Port(sea=P1, convoy={Resource.IRON: 1})],
)
R17 = Territory(
    code="R17",
    name="Kamchatsky",
    strategic_value=1,
    resources={Resource.OSR: 1},
)
R18 = Territory(
    code="R18",
    name="Soviet Sakhalin Island",
)
T1 = Territory(
    code="T1",
    name="Italy",
    strategic_value=6,
    industry=True,
    resources={Resource.OSR: 3},
    ports=[Port(sea=M2, convoy={Resource.IRON: 1, Resource.OSR: 1})],
)
T2 = Territory(
    code="T2",
    name="Balkans",
    strategic_value=4,
    resources={Resource.OIL: 1, Resource.OSR: 3},
    ports=[Port(sea=M3, convoy={Resource.OIL: 1, Resource.IRON: 1, Resource.OSR: 1})],
)
T3 = Territory(
    code="T3",
    name="Sardinia",
    strategic_value=1,
)
T4 = Territory(
    code="T4",
    name="Sicily",
    strategic_value=1,
)
T5 = Territory(
    code="T5",
    name="Libya",
    strategic_value=3,
    resources={Resource.OIL: 2},
    ports=[Port(sea=M2, convoy={Resource.OIL: 1, Resource.IRON: 1})],
)
U1 = Territory(
    code="U1",
    name="Eastern United States",
    strategic_value=10,
    industry=True,
    resources={Resource.OIL: 2, Resource.OSR: 5},
    ports=[Port(sea=A10, convoy={Resource.OIL: 1, Resource.IRON: 1, Resource.OSR: 1})],
)
U2 = Territory(
    code="U2",
    name="Central United States",
    strategic_value=9,
    industry=True,
    resources={Resource.OIL: 3, Resource.OSR: 6},
    ports=[Port(sea=A11, convoy={Resource.OIL: 1, Resource.IRON: 1, Resource.OSR: 1})],
)
U3 = Territory(
    code="U3",
    name="Western United States",
    strategic_value=8,
    industry=True,
    resources={Resource.OIL: 2, Resource.OSR: 6},
    ports=[Port(sea=P5, convoy={Resource.OIL: 1, Resource.IRON: 1, Resource.OSR: 1})],
)
U4 = Territory(
    code="U4",
    name="Alaska",
    strategic_value=3,
    resources={Resource.OIL: 1, Resource.OSR: 1},
    ports=[Port(sea=P4, convoy={Resource.OIL: 1, Resource.IRON: 1, Resource.OSR: 1})],
)
U5 = Territory(
    code="U5",
    name="Aleutian Islands",
    strategic_value=1,
)
U6 = Territory(
    code="U6",
    name="Hawaiian Islands",
    strategic_value=2,
    ports=[Port(sea=P9)],
)
U7 = Territory(
    code="U7",
    name="Midway Islands",
)
U8 = Territory(
    code="U8",
    name="Johnston Atoll",
)
U9 = Territory(
    code="U9",
    name="Samoan Islands",
)
U10 = Territory(
    code="U10",
    name="New Caledonia",
)

TERRITORIES = {
    U1,
    U2,
    U3,
    U4,
    U5,
    U6,
    U7,
    U8,
    U9,
    U10,
    B1,
    B2,
    B3,
    B4,
    B5,
    B6,
    B7,
    B8,
    B9,
    B10,
    B11,
    B12,
    B13,
    B14,
    B15,
    B16,
    B17,
    B18,
    B19,
    B20,
    B21,
    B22,
    B23,
    B24,
    B25,
    B26,
    B27,
    B28,
    B29,
    B30,
    C1,
    C2,
    C3,
    C4,
    C5,
    G1,
    G2,
    G3,
    G4,
    G5,
    G6,
    G7,
    G8,
    G9,
    G10,
    G11,
    G12,
    G13,
    G14,
    G15,
    G16,
    T1,
    T2,
    T3,
    T4,
    T5,
    J1,
    J2,
    J3,
    J4,
    J5,
    J6,
    J7,
    J8,
    J9,
    J10,
    J11,
    J12,
    J13,
    J14,
    J15,
    J16,
    J17,
    J18,
    J19,
    J20,
    J21,
    J22,
    J23,
    J24,
    J25,
    J26,
    J27,
    J28,
    R1,
    R2,
    R3,
    R4,
    R5,
    R6,
    R7,
    R8,
    R9,
    R10,
    R11,
    R12,
    R13,
    R14,
    R15,
    R16,
    R17,
    R18,
    N1,
    N2,
    N3,
    N4,
    N5,
    N6,
    N7,
    N8,
    N9,
    N10,
    N11,
    N12,
    N13,
    N14,
    N15,
    N16,
    N17,
    N18,
    N19,
}

REGIONS = SEA_REGIONS | TERRITORIES
REGIONS_BY_CODE = {r.code: r for r in REGIONS}

NARROW_SEA_PASSAGES = [
    NarrowSeaPassage(name="Panama Canal", regions={A12, P7}, required_control={N2}),
    NarrowSeaPassage(name="Suez Canal", regions={M3, M5}, required_control={B5}),
    NarrowSeaPassage(
        name="Danish Straits", regions={A5, A6}, required_control={G2, G10}
    ),
    NarrowSeaPassage(
        name="Strait of Gibraltar", regions={A15, M1}, required_control={B3}
    ),
    NarrowSeaPassage(
        name="Strait of Malacca", regions={I9, P15}, required_control={J9}
    ),
    NarrowSeaPassage(name="Turkish Straits", regions={M3, M4}, required_control={N14}),
]

IMPASSABLE_TERRAINS = [
    ImpassableTerrain(
        name="Western Sahara",
        neighbors={G11, G12, G15, A16, A17},
    ),
    ImpassableTerrain(
        name="Central Sahara",
        neighbors={G12, G13, T5, B13, B14, G15},
    ),
    ImpassableTerrain(
        name="Eastern Sahara",
        neighbors={T5, B5, B6, B12, B13},
    ),
    ImpassableTerrain(
        name="Himalaya",
        neighbors={B18, N18, R9, C3, C4, C5, J8},
    ),
]

RAILROADS = [
    {B8, B9},
    {B9, B10},
    {B16, N14},
    {B16, B17},
    {B17, B18},
    {B21, B23},
    {B22, B23},
    {B23, B24},
    {B28, B29},
    {B28, U2},
    {B28, U3},
    {B29, U1},
    {B29, U2},
    {C1, C2},
    {C1, J4},
    {C1, J5},
    {G1, G2},
    {G1, G3},
    {G1, G4},
    {G1, G8},
    {G1, T1},
    {G1, T2},
    {G3, N11},
    {G3, T1},
    {G4, G5},
    {G4, G6},
    {G4, G8},
    {G5, G6},
    {G5, N14},
    {G5, T2},
    {G6, G7},
    {G6, R5},
    {G6, R6},
    {G7, G8},
    {G7, R4},
    {G7, R5},
    {G8, R4},
    {G9, N10},
    {G9, R4},
    {G10, N10},
    {G11, G12},
    {G12, G13},
    {J2, J3},
    {J3, J4},
    {J4, J5},
    {J6, J7},
    {J7, J8},
    {J7, J9},
    {N1, U2},
    {N1, U3},
    {R1, R2},
    {R1, R5},
    {R1, R11},
    {R1, R7},
    {R1, R8},
    {R2, R3},
    {R2, R5},
    {R2, R12},
    {R3, R4},
    {R4, R5},
    {R6, R7},
    {R11, R13},
    {R13, R14},
    {R14, R16},
    {T1, T2},
    {U1, U2},
    {U2, U3},
]

NEIGHBORS = [
    {A1, A2},
    {A1, B28},
    {A1, B29},
    {A2, A3},
    {A2, A7},
    {A2, A8},
    {A2, A9},
    {A2, B29},
    {A2, N7},
    {A2, N8},
    {A3, A4},
    {A3, A6},
    {A3, A7},
    {A3, G9},
    {A3, G10},
    {A3, N7},
    {A3, R3},
    {A4, R2},
    {A4, R3},
    {A4, R12},
    {A5, A6},
    {A5, G1},
    {A5, G2},
    {A5, G8},
    {A5, G9},
    {A5, G10},
    {A5, N10},
    {A5, R4},
    {A6, A7},
    {A6, A15},
    {A6, B1},
    {A6, G1},
    {A6, G2},
    {A6, G3},
    {A6, G10},
    {A7, A8},
    {A7, A13},
    {A7, A14},
    {A7, B1},
    {A7, N9},
    {A8, A9},
    {A8, A13},
    {A9, A10},
    {A9, A12},
    {A9, A13},
    {A9, B29},
    {A10, A11},
    {A10, A12},
    {A10, N3},
    {A10, U1},
    {A11, A12},
    {A11, U1},
    {A11, U2},
    {A11, N1},
    {A11, N2},
    {A12, A13},
    {A12, B30},
    {A12, N2},
    {A12, N3},
    {A12, N4},
    {A12, N5},
    {A12, N6},
    {A13, A14},
    {A13, A16},
    {A13, N6},
    {A14, A15},
    {A14, A16},
    {A14, B2},
    {A15, A16},
    {A15, B2},
    {A15, B3},
    {A15, G11},
    {A15, N11},
    {A15, N12},
    {A16, A17},
    {A16, G11},
    {A17, A18},
    {A17, B15},
    {A17, G15},
    {A18, A19},
    {A18, B11},
    {A18, B12},
    {A18, B13},
    {A18, B14},
    {A19, I4},
    {A19, B10},
    {A19, N16},
    {A19, N17},
    {A8, N8},
    {A8, N8},
    {B1, N9},
    {B3, N11},
    {B4, M2},
    {B5, B6},
    {B5, B16},
    {B5, M3},
    {B5, M5},
    {B5, N15},
    {B5, T5},
    {B6, B7},
    {B6, B8},
    {B6, B11},
    {B6, B12},
    {B6, M5},
    {B7, B8},
    {B7, I2},
    {B7, I3},
    {B7, M5},
    {B8, B9},
    {B8, B11},
    {B8, I3},
    {B8, N17},
    {B9, B10},
    {B9, B11},
    {B9, N16},
    {B9, N17},
    {B10, N16},
    {B10, N17},
    {B11, B12},
    {B11, N16},
    {B12, B13},
    {B13, B14},
    {B14, G15},
    {B15, G15},
    {B16, B17},
    {B16, I1},
    {B16, M3},
    {B16, N14},
    {B16, N15},
    {B17, B18},
    {B17, I1},
    {B17, M6},
    {B17, N14},
    {B17, N18},
    {B17, R6},
    {B17, R9},
    {B18, I1},
    {B18, I2},
    {B18, I7},
    {B18, I10},
    {B18, J8},
    {B18, N18},
    {B19, I7},
    {B20, I2},
    {B20, I6},
    {B21, B22},
    {B21, B23},
    {B21, P16},
    {B21, P17},
    {B22, B23},
    {B22, B24},
    {B22, P17},
    {B23, B24},
    {B23, P18},
    {B24, P17},
    {B24, P18},
    {B25, J24},
    {B25, J24},
    {B25, P17},
    {B25, P18},
    {B26, P19},
    {B27, P19},
    {B27, P20},
    {B28, B29},
    {B28, P4},
    {B28, U2},
    {B28, U3},
    {B28, U4},
    {B29, U1},
    {B29, U2},
    {B30, N5},
    {B30, N6},
    {C1, C2},
    {C1, C3},
    {C1, C4},
    {C1, J4},
    {C1, J5},
    {C2, C3},
    {C2, J5},
    {C2, J6},
    {C3, C4},
    {C3, J6},
    {C3, J8},
    {C4, C5},
    {C4, J4},
    {C4, N19},
    {C5, N19},
    {C5, R9},
    {C5, R10},
    {G1, G2},
    {G1, G3},
    {G1, G4},
    {G1, G8},
    {G1, N13},
    {G1, T1},
    {G1, T2},
    {G3, M1},
    {G3, N11},
    {G3, N13},
    {G3, T1},
    {G4, G5},
    {G4, G6},
    {G4, G8},
    {G4, T2},
    {G5, G6},
    {G5, M4},
    {G5, N14},
    {G5, T2},
    {G6, G7},
    {G6, M4},
    {G6, R5},
    {G6, R6},
    {G7, G8},
    {G7, R4},
    {G7, R5},
    {G8, R4},
    {G9, N10},
    {G9, R3},
    {G9, R4},
    {G10, N10},
    {G11, G12},
    {G11, M1},
    {G12, G13},
    {G12, M2},
    {G13, M2},
    {G13, T5},
    {G14, M3},
    {G16, I4},
    {I1, I2},
    {I1, N15},
    {I2, I3},
    {I2, I6},
    {I2, I7},
    {I2, M5},
    {I3, I4},
    {I3, N17},
    {I4, I5},
    {I4, I6},
    {I4, N17},
    {I5, I6},
    {I5, I7},
    {I5, I8},
    {I6, I7},
    {I7, I8},
    {I7, I9},
    {I7, I10},
    {I8, I9},
    {I8, P16},
    {I9, I10},
    {I9, J7},
    {I9, J9},
    {I9, J10},
    {I9, P16},
    {I10, J7},
    {I10, J8},
    {J1, P0},
    {J1, P1},
    {J2, J3},
    {J2, P0},
    {J2, P1},
    {J3, J4},
    {J3, N19},
    {J3, P0},
    {J3, R14},
    {J3, R16},
    {J4, J5},
    {J4, N19},
    {J4, P0},
    {J5, J6},
    {J5, P0},
    {J5, P14},
    {J6, J7},
    {J6, P14},
    {J6, P15},
    {J7, J8},
    {J7, J9},
    {J7, P15},
    {J9, P15},
    {J10, P15},
    {J10, P16},
    {J11, P16},
    {J12, P15},
    {J13, P15},
    {J14, P14},
    {J15, P14},
    {J16, P0},
    {J16, P14},
    {J17, P0},
    {J17, P1},
    {J17, P13},
    {J17, P14},
    {J18, P13},
    {J18, P14},
    {J19, P1},
    {J19, R18},
    {J20, P1},
    {J21, P1},
    {J21, P12},
    {J21, P13},
    {J22, P13},
    {J23, P13},
    {J24, P13},
    {J25, P13},
    {J25, P18},
    {J25, P19},
    {J26, P2},
    {J26, P11},
    {J26, P12},
    {J27, P11},
    {J27, P12},
    {J27, P20},
    {J28, P12},
    {J28, P19},
    {J28, P20},
    {M1, M2},
    {M1, N11},
    {M2, M3},
    {M2, T1},
    {M2, T2},
    {M2, T3},
    {M2, T4},
    {M2, T5},
    {M3, N14},
    {M3, T2},
    {M3, T5},
    {M4, N14},
    {M4, R6},
    {M5, N15},
    {M6, R6},
    {M6, R7},
    {M6, R8},
    {M6, R9},
    {N1, N2},
    {N1, P5},
    {N1, P6},
    {N1, P7},
    {N1, U2},
    {N1, U3},
    {N2, N4},
    {N2, P7},
    {N4, N5},
    {N4, P7},
    {N11, N12},
    {N13, T1},
    {N14, R6},
    {N18, R9},
    {N19, R10},
    {N19, R14},
    {P0, P1},
    {P0, P14},
    {P1, R16},
    {P1, R18},
    {P1, P2},
    {P1, P12},
    {P1, P13},
    {P2, P3},
    {P2, P11},
    {P2, P12},
    {P2, R17},
    {P3, P4},
    {P3, P9},
    {P3, P10},
    {P3, P11},
    {P3, U4},
    {P3, U5},
    {P3, U7},
    {P4, P5},
    {P4, P9},
    {P4, U4},
    {P5, P6},
    {P5, P8},
    {P5, P9},
    {P5, U3},
    {P6, P7},
    {P6, P8},
    {P8, P9},
    {P9, P10},
    {P9, U6},
    {P9, U7},
    {P9, U8},
    {P10, P11},
    {P10, P20},
    {P10, U7},
    {P10, U8},
    {P10, U9},
    {P11, P12},
    {P11, P20},
    {P12, P13},
    {P12, P19},
    {P12, P20},
    {P13, P14},
    {P13, P17},
    {P13, P18},
    {P14, P15},
    {P14, P17},
    {P15, P16},
    {P15, P17},
    {P16, P17},
    {P17, P18},
    {P18, P19},
    {P19, P20},
    {P19, U10},
    {P20, U9},
    {R1, R2},
    {R1, R5},
    {R1, R7},
    {R1, R8},
    {R1, R11},
    {R1, R12},
    {R2, R3},
    {R2, R4},
    {R2, R5},
    {R2, R12},
    {R3, R4},
    {R4, R5},
    {R4, G7},
    {R4, G8},
    {R5, R6},
    {R5, R7},
    {R6, R7},
    {R7, R8},
    {R8, R9},
    {R8, R10},
    {R8, R11},
    {R9, R10},
    {R10, R11},
    {R10, R13},
    {R10, R14},
    {R11, R12},
    {R11, R13},
    {R12, R13},
    {R13, R14},
    {R13, R15},
    {R14, R15},
    {R14, R16},
    {R15, R16},
    {R16, R17},
    {T1, T2},
    {U1, U2},
    {U2, U3},
]
