/**
 * Maps each of 131 War Room territory codes to Natural Earth geographic features.
 *
 * Mapping types:
 *   countries     → merge admin-0 features by ADM0_A3/ISO_A3
 *   admin1        → merge admin-1 features by iso_3166_2 code
 *   point         → lat/lon marker for tiny islands (rendered as circle)
 *   countriesClip → like countries but clipped to a bounding box (removes overseas territories)
 *   admin1Clip    → like admin1 but clipped to a bounding box
 *   admin1+countries → merge both admin1 and admin0 features
 *   admin1+countriesClip → merge both, then clip to bbox
 */

export type Bbox = [minLon: number, minLat: number, maxLon: number, maxLat: number]

export type GeoMapping =
  | { type: 'countries'; codes: string[] }
  | { type: 'countriesClip'; codes: string[]; bbox: Bbox }
  | { type: 'admin1'; country: string; codes: string[] }
  | { type: 'admin1Clip'; country: string; codes: string[]; bbox: Bbox }
  | { type: 'point'; lat: number; lon: number; r?: number }
  | { type: 'admin1+countries'; admin1: { country: string; codes: string[] }; countries: string[] }
  | { type: 'admin1+countriesClip'; admin1: { country: string; codes: string[] }; countries: string[]; bbox: Bbox }

export const TERRITORY_GEO: Record<string, GeoMapping> = {
  // ─── United States (10) ────────────────────────────────────────────
  // 3-way split by state groupings
  U1: { type: 'admin1', country: 'US', codes: [
    'US-ME','US-NH','US-VT','US-MA','US-RI','US-CT','US-NY','US-NJ','US-PA','US-DE','US-MD','US-DC',
    'US-VA','US-WV','US-NC','US-SC','US-GA','US-FL','US-OH','US-IN','US-MI','US-KY','US-TN','US-AL','US-MS',
  ]},
  U2: { type: 'admin1', country: 'US', codes: [
    'US-WI','US-IL','US-MN','US-IA','US-MO','US-AR','US-LA','US-TX','US-OK','US-KS','US-NE',
    'US-SD','US-ND',
  ]},
  U3: { type: 'admin1', country: 'US', codes: [
    'US-MT','US-WY','US-CO','US-NM','US-AZ','US-UT','US-NV','US-ID','US-WA','US-OR','US-CA',
  ]},
  U4: { type: 'admin1', country: 'US', codes: ['US-AK'] },
  U5: { type: 'point', lat: 52.5, lon: 174.0 },       // Aleutian Islands
  U6: { type: 'point', lat: 21.3, lon: -157.8 },       // Hawaiian Islands
  U7: { type: 'point', lat: 28.2, lon: -177.4 },       // Midway Islands
  U8: { type: 'point', lat: 16.7, lon: -169.5 },       // Johnston Atoll
  U9: { type: 'point', lat: -14.3, lon: -170.7 },      // Samoan Islands
  U10: { type: 'point', lat: -22.3, lon: 166.5 },      // New Caledonia

  // ─── British Commonwealth (30) ────────────────────────────────────
  B1: { type: 'countries', codes: ['GBR'] },
  B2: { type: 'point', lat: 38.7, lon: -27.2 },        // Azores
  B3: { type: 'point', lat: 36.1, lon: -5.35 },         // Gibraltar
  B4: { type: 'point', lat: 35.9, lon: 14.5 },          // Malta
  B5: { type: 'countries', codes: ['EGY'] },
  B6: { type: 'countries', codes: ['SDN','SSD'] },
  B7: { type: 'countries', codes: ['ETH','ERI','DJI','SOM'] },
  B8: { type: 'countries', codes: ['KEN','TZA','UGA'] },
  B9: { type: 'countries', codes: ['ZMB','ZWE','MWI'] },
  B10: { type: 'countries', codes: ['ZAF','SWZ','LSO','BWA','NAM'] },
  B11: { type: 'countries', codes: ['COD'] },
  B12: { type: 'countries', codes: ['COG','GAB','CAF'] },
  B13: { type: 'countries', codes: ['NGA','CMR'] },
  // B14 Gold Coast: Ghana + Togo + Benin (coastal strip, surrounded by G15)
  B14: { type: 'countries', codes: ['GHA','TGO','BEN'] },
  // B15 Sierra Leone: small coastal strip in West Africa
  B15: { type: 'countries', codes: ['SLE','LBR','GIN','GNB'] },
  B16: { type: 'countries', codes: ['IRQ','SYR','JOR','LBN','ISR','PSX'] },
  B17: { type: 'countries', codes: ['IRN'] },
  // India: clip to south-of-Himalayas (exclude regions north of ~36°N)
  B18: { type: 'countriesClip', codes: ['IND','BGD','PAK','NPL','BTN'], bbox: [60, 5, 100, 36] },
  B19: { type: 'point', lat: 7.0, lon: 80.0 },          // Ceylon (Sri Lanka)
  B20: { type: 'point', lat: 3.2, lon: 73.2 },          // Maldives
  // Australia 4-way split
  B21: { type: 'admin1', country: 'AU', codes: ['AU-WA'] },
  B22: { type: 'admin1', country: 'AU', codes: ['AU-NT'] },
  B23: { type: 'admin1', country: 'AU', codes: ['AU-SA'] },
  B24: { type: 'admin1', country: 'AU', codes: ['AU-NSW','AU-VIC','AU-QLD','AU-TAS','AU-ACT'] },
  // Papua: clip to main island only (remove offshore islands spreading at sea)
  B25: { type: 'countriesClip', codes: ['PNG'], bbox: [140, -12, 155, 0] },
  B26: { type: 'point', lat: -17.7, lon: 168.3 },       // New Hebrides = Vanuatu
  B27: { type: 'countries', codes: ['NZL'] },
  // Canada 2-way split
  B28: { type: 'admin1', country: 'CA', codes: ['CA-BC','CA-AB','CA-SK','CA-MB','CA-YT','CA-NT','CA-NU'] },
  B29: { type: 'admin1', country: 'CA', codes: ['CA-ON','CA-QC','CA-NB','CA-NS','CA-PE','CA-NL'] },
  B30: { type: 'countries', codes: ['GUY','SUR'] },

  // ─── Soviet Union (18) ─────────────────────────────────────────────
  R1: { type: 'admin1', country: 'RU', codes: [
    'RU-MOS','RU-MOW','RU-TUL','RU-RYA','RU-VLA','RU-IVA','RU-KOS','RU-YAR','RU-TVE',
    'RU-SMO','RU-KLU',
  ]},
  R2: { type: 'admin1', country: 'RU', codes: [
    'RU-ARK','RU-VLG','RU-NEN','RU-KO','RU-MUR',
  ]},
  R3: { type: 'point', lat: 63.5, lon: 33.0, r: 2 },    // Karelia
  // R4 Leningrad: clip to main area, exclude Kaliningrad exclave
  R4: { type: 'admin1Clip', country: 'RU', codes: [
    'RU-LEN','RU-SPE','RU-NGR','RU-PSK','RU-KGD',
  ], bbox: [26, 55, 42, 62] },
  R5: { type: 'admin1', country: 'RU', codes: [
    'RU-BRY','RU-ORL','RU-KRS','RU-BEL','RU-LIP','RU-VOR','RU-TAM','RU-PNZ',
  ]},
  R6: { type: 'admin1+countries', admin1: { country: 'RU', codes: [
    'RU-KDA','RU-STA','RU-AD','RU-KL','RU-ROS','RU-VGG','RU-AST',
    'RU-CE','RU-DA','RU-IN','RU-KB','RU-KC','RU-SE',
  ]}, countries: ['GEO','ARM','AZE'] },
  R7: { type: 'admin1', country: 'RU', codes: [
    'RU-SAM','RU-SAR','RU-ULY','RU-PER','RU-NIZ','RU-ME','RU-CU','RU-MO',
    'RU-TA','RU-ORE','RU-BA','RU-UD','RU-KIR',
  ]},
  R8: { type: 'countries', codes: ['KAZ'] },
  R9: { type: 'countries', codes: ['TKM','UZB'] },
  R10: { type: 'countries', codes: ['KGZ','TJK'] },
  R11: { type: 'admin1', country: 'RU', codes: [
    'RU-SVE','RU-CHE','RU-KGN','RU-TYU','RU-KHM','RU-YAN','RU-OMS','RU-NVS',
  ]},
  R12: { type: 'admin1', country: 'RU', codes: [
    'RU-KEM','RU-ALT','RU-AL','RU-TY','RU-KK','RU-TOM',
  ]},
  R13: { type: 'admin1', country: 'RU', codes: ['RU-KYA'] },
  R14: { type: 'admin1', country: 'RU', codes: ['RU-IRK','RU-BU','RU-AMU','RU-ZAB'] },
  R15: { type: 'admin1', country: 'RU', codes: ['RU-SA'] },
  R16: { type: 'admin1', country: 'RU', codes: ['RU-KHA','RU-YEV','RU-PRI','RU-MAG'] },
  R17: { type: 'admin1', country: 'RU', codes: ['RU-KAM','RU-CHU'] },
  R18: { type: 'point', lat: 51.0, lon: 143.0 },        // Soviet Sakhalin (north half)

  // ─── Germany (16) ──────────────────────────────────────────────────
  G1: { type: 'countries', codes: ['DEU','AUT','CZE'] },
  G2: { type: 'countries', codes: ['DNK'] },
  // G3 France: clip to Europe only (remove French Guiana, Pacific islands, etc.)
  G3: { type: 'countriesClip', codes: ['FRA','BEL','NLD','LUX'], bbox: [-6, 42, 10, 55] },
  G4: { type: 'countries', codes: ['POL','SVK','HUN'] },
  G5: { type: 'countries', codes: ['BGR','ROU'] },
  G6: { type: 'countries', codes: ['UKR'] },
  G7: { type: 'countries', codes: ['BLR'] },
  G8: { type: 'countries', codes: ['EST','LVA','LTU'] },
  G9: { type: 'countries', codes: ['FIN'] },
  // G10 Norway: clip to mainland only (remove Svalbard, Jan Mayen, Bouvet)
  G10: { type: 'countriesClip', codes: ['NOR'], bbox: [3, 57, 32, 72] },
  G11: { type: 'countriesClip', codes: ['MAR','SAH'], bbox: [-18, 20, 0, 37] },
  G12: { type: 'countriesClip', codes: ['DZA'], bbox: [-3, 25, 12, 38] },
  G13: { type: 'countriesClip', codes: ['TUN'], bbox: [7, 30, 12, 38] },
  G14: { type: 'point', lat: 35.2, lon: 24.9 },         // Crete
  // G15 French West Africa: large interior + coast (Mauritania, Niger, Chad, Senegal, Gambia, Mali, Ivory Coast, Burkina Faso)
  G15: { type: 'countries', codes: ['MRT','NER','TCD','SEN','GMB','MLI','BFA','CIV'] },
  G16: { type: 'countries', codes: ['MDG'] },

  // ─── Imperial Japan (28) ──────────────────────────────────────────
  J1: { type: 'countries', codes: ['JPN'] },
  J2: { type: 'countries', codes: ['PRK','KOR'] },
  // China splits: use admin1 and clip to prevent wrong neighbors
  // J3 Manchuria: northeast China (Heilongjiang, Jilin, Liaoning) — clip south to ~40°N to not touch J4 from south
  J3: { type: 'admin1', country: 'CN', codes: ['CN-HL','CN-JL','CN-LN'] },
  // J4 Peiping: northern China (Beijing, Tianjin, Hebei, Shandong, Shanxi)
  J4: { type: 'admin1', country: 'CN', codes: ['CN-BJ','CN-TJ','CN-HE','CN-SD','CN-SX'] },
  // J5 Chekiang Kwangtung: coastal China
  J5: { type: 'admin1', country: 'CN', codes: ['CN-ZJ','CN-GD','CN-FJ','CN-JX','CN-SH','CN-JS','CN-AH'] },
  J6: { type: 'countries', codes: ['VNM','KHM','LAO'] },
  J7: { type: 'countries', codes: ['THA'] },
  J8: { type: 'countries', codes: ['MMR'] },
  J9: { type: 'countriesClip', codes: ['MYS','SGP'], bbox: [99, 0, 106, 8] }, // Malaya peninsula only
  // Indonesia splits
  J10: { type: 'admin1', country: 'ID', codes: [
    'ID-AC','ID-SU','ID-SB','ID-RI','ID-KR','ID-JA','ID-SS','ID-BE','ID-LA','ID-BB',
  ]},
  J11: { type: 'admin1', country: 'ID', codes: [
    'ID-BT','ID-JK','ID-JB','ID-JT','ID-YO','ID-JI','ID-BA','ID-NB','ID-NT',
  ]},
  J12: { type: 'admin1+countries', admin1: { country: 'ID', codes: [
    'ID-KB','ID-KT','ID-KS','ID-KI',
  ]}, countries: ['BRN'] },
  J13: { type: 'admin1', country: 'ID', codes: [
    'ID-SA','ID-GO','ID-ST','ID-SG','ID-SN','ID-SR','ID-MA','ID-MU',
  ]},
  J14: { type: 'countries', codes: ['PHL'] },
  J15: { type: 'admin1', country: 'CN', codes: ['CN-HI'] },   // Hainan
  J16: { type: 'countries', codes: ['TWN'] },
  J17: { type: 'point', lat: 26.3, lon: 127.8 },              // Okinawa
  J18: { type: 'point', lat: 7.5, lon: 134.6 },               // Palau
  J19: { type: 'point', lat: 50.0, lon: 143.0 },              // Japanese Sakhalin (south)
  J20: { type: 'point', lat: 24.78, lon: 141.32 },            // Iwo Jima
  J21: { type: 'point', lat: 15.2, lon: 145.7 },              // Mariana Islands
  J22: { type: 'point', lat: 7.4, lon: 151.8 },               // Caroline Islands
  J23: { type: 'point', lat: -5.5, lon: 150.5 },              // New Britain
  J24: { type: 'admin1Clip', country: 'ID', codes: ['ID-PA','ID-PB'], bbox: [130, -10, 145, 0] },
  J25: { type: 'point', lat: -9.4, lon: 160.0 },              // Solomon Islands
  J26: { type: 'point', lat: 19.28, lon: 166.63 },            // Wake Island
  J27: { type: 'point', lat: 7.1, lon: 171.2 },               // Marshall Islands
  J28: { type: 'point', lat: 1.4, lon: 173.0 },               // Gilbert Islands

  // ─── Italy (5) ────────────────────────────────────────────────────
  // T1 Italy: clip to mainland + islands, exclude the Dodecanese
  T1: { type: 'countriesClip', codes: ['ITA'], bbox: [6, 36, 19, 48] },
  // T2 Balkans: clip to exclude Crete (that's G14)
  T2: { type: 'countriesClip', codes: ['GRC','ALB','SRB','HRV','BIH','MNE','MKD','SVN','KOS','CYP'], bbox: [13, 35, 35, 47] },
  T3: { type: 'point', lat: 40.0, lon: 9.0 },                 // Sardinia
  T4: { type: 'point', lat: 37.5, lon: 14.0 },                // Sicily
  T5: { type: 'countriesClip', codes: ['LBY'], bbox: [9, 25, 26, 34] },

  // ─── China (5) ────────────────────────────────────────────────────
  C1: { type: 'admin1', country: 'CN', codes: ['CN-HA','CN-HB','CN-HN'] },
  C2: { type: 'admin1', country: 'CN', codes: ['CN-GX','CN-GZ'] },
  // C3 Szechwan Yunnan: clip north to prevent touching C5 through Tibet
  C3: { type: 'admin1Clip', country: 'CN', codes: ['CN-SC','CN-CQ','CN-YN'], bbox: [95, 20, 110, 34] },
  C4: { type: 'admin1', country: 'CN', codes: ['CN-QH','CN-NX','CN-GS','CN-SN'] },
  // C5 Sinkiang: Xinjiang only (not Tibet/Inner Mongolia — those create wrong neighbors)
  C5: { type: 'admin1Clip', country: 'CN', codes: ['CN-XJ'], bbox: [73, 34, 97, 50] },

  // ─── Neutrals (19) ───────────────────────────────────────────────
  N1: { type: 'countries', codes: ['MEX'] },
  N2: { type: 'countries', codes: ['GTM','BLZ','HND','SLV','NIC','CRI','PAN'] },
  N3: { type: 'countries', codes: ['CUB','HTI','DOM','PRI','JAM'] },
  N4: { type: 'countries', codes: ['COL','ECU','PER'] },
  N5: { type: 'countries', codes: ['VEN'] },
  N6: { type: 'countries', codes: ['BRA','BOL','PRY','URY','ARG','CHL'] },
  N7: { type: 'countries', codes: ['GRL'] },
  N8: { type: 'countries', codes: ['ISL'] },
  N9: { type: 'countries', codes: ['IRL'] },
  N10: { type: 'countries', codes: ['SWE'] },
  N11: { type: 'countriesClip', codes: ['ESP'], bbox: [-10, 35, 5, 44] }, // Iberian Spain only
  N12: { type: 'countries', codes: ['PRT'] },
  N13: { type: 'countries', codes: ['CHE'] },
  N14: { type: 'countries', codes: ['TUR'] },
  N15: { type: 'countries', codes: ['SAU','YEM','OMN'] },
  N16: { type: 'countries', codes: ['AGO'] },
  N17: { type: 'countries', codes: ['MOZ'] },
  N18: { type: 'countries', codes: ['AFG'] },
  N19: { type: 'countriesClip', codes: ['MNG'], bbox: [87, 41, 120, 52] },
}

/**
 * Impassable terrain: visual barriers drawn on the map.
 * Each is defined by a polyline (series of lat/lon points) that separates territories.
 */
export const IMPASSABLE_TERRAIN: Record<string, [number, number][]> = {
  // Himalaya: separates B18/J8 from C3/C4/C5/N18/R9
  // Runs roughly from Afghanistan-Pakistan border east to Burma-China border
  'Himalaya': [
    [66, 36], [70, 36], [74, 35], [78, 33], [82, 29], [86, 28], [90, 28], [94, 27], [97, 26], [98, 24],
  ],
  // Western Sahara: between G11, G12 (north) and G15 (south)
  'Western Sahara': [
    [-17, 25], [-12, 23], [-6, 22], [0, 23], [3, 24],
  ],
  // Central Sahara: between G12, G13, T5 (north) and G15, B13, B14 (south)
  'Central Sahara': [
    [3, 24], [8, 22], [12, 20], [15, 16], [17, 14],
  ],
  // Eastern Sahara: between T5, B5 (north) and B6, B12, B13 (south)
  'Eastern Sahara': [
    [17, 14], [22, 14], [25, 15], [28, 17], [32, 20], [35, 22],
  ],
}
