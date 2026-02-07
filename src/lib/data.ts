import type { NationId, NationDef, UnitDef, CasualtyBracket, HomelandZone } from './types'

export const NATION_IDS: NationId[] = ['CHN', 'UK', 'USSR', 'USA', 'GER', 'ITA', 'JAP']
export const ALLIED_IDS: NationId[] = ['CHN', 'UK', 'USSR', 'USA']
export const AXIS_IDS: NationId[] = ['GER', 'ITA', 'JAP']

export const NATIONS: Record<NationId, NationDef> = {
  CHN: { id: 'CHN', name: 'China', alliance: 'Allied', maxOrders: 6, stressThreshold: 4 },
  UK:  { id: 'UK',  name: 'British Commonwealth', alliance: 'Allied', maxOrders: 9, stressThreshold: 6 },
  USSR:{ id: 'USSR',name: 'Soviet Union', alliance: 'Allied', maxOrders: 9, stressThreshold: 6 },
  USA: { id: 'USA', name: 'United States', alliance: 'Allied', maxOrders: 9, stressThreshold: 5 },
  GER: { id: 'GER', name: 'Germany', alliance: 'Axis', maxOrders: 9, stressThreshold: 6 },
  ITA: { id: 'ITA', name: 'Italy', alliance: 'Axis', maxOrders: 6, stressThreshold: 4 },
  JAP: { id: 'JAP', name: 'Imperial Japan', alliance: 'Axis', maxOrders: 9, stressThreshold: 7 },
}

export const UNITS: UnitDef[] = [
  { name: 'Infantry',   cost: [0, 0, 2], casualtyPoints: 2,  category: 'Land' },
  { name: 'Artillery',  cost: [0, 2, 1], casualtyPoints: 2,  category: 'Land' },
  { name: 'Armor',      cost: [1, 2, 1], casualtyPoints: 4,  category: 'Land' },
  { name: 'Fighter',    cost: [2, 1, 1], casualtyPoints: 4,  category: 'Air' },
  { name: 'Bomber',     cost: [2, 2, 1], casualtyPoints: 6,  category: 'Air' },
  { name: 'Submarine',  cost: [1, 2, 1], casualtyPoints: 6,  category: 'Naval' },
  { name: 'Cruiser',    cost: [2, 3, 2], casualtyPoints: 10, category: 'Naval' },
  { name: 'Carrier',    cost: [4, 3, 3], casualtyPoints: 20, category: 'Naval' },
  { name: 'Battleship', cost: [3, 4, 3], casualtyPoints: 20, category: 'Naval' },
]

export const CASUALTY_BRACKETS: CasualtyBracket[] = [
  { min: 0,   max: 19,       stress: 0 },
  { min: 20,  max: 35,       stress: 1 },
  { min: 36,  max: 51,       stress: 2 },
  { min: 52,  max: 69,       stress: 3 },
  { min: 70,  max: 89,       stress: 4 },
  { min: 90,  max: 109,      stress: 5 },
  { min: 110, max: Infinity,  stress: 6 },
]

export const HOMELAND_ZONES: HomelandZone[] = ['White', 'Blue', 'Yellow', 'Orange', 'Red', 'Gray']

export const ZONE_INFO: Record<HomelandZone, { name: string; effect: string }> = {
  White: { name: 'Acceptable', effect: 'No penalty' },
  Blue: { name: 'Unrest', effect: 'Pay 3 resources (any mix)' },
  Yellow: { name: 'Dysfunctional', effect: 'No rails, no sea trade, no port advantage' },
  Orange: { name: 'Disrupted', effect: '3 fewer written orders' },
  Red: { name: 'Collapse', effect: 'No new resource income' },
  Gray: { name: 'Desertion', effect: 'Remove units from map equal to stress' },
}

export const RESOURCES = {
  oil:  { label: 'Oil',  tradeRate: 2, color: '#e74c3c' },
  iron: { label: 'Iron', tradeRate: 3, color: '#3498db' },
  osr:  { label: 'OSR',  tradeRate: 5, color: '#f1c40f' },
} as const

// Capitals: 3 medals when captured (J4 = Peiping for Chinese capital purposes)
export const CAPITALS = new Set(['U1', 'B1', 'R1', 'G1', 'J1', 'T1', 'J4'])

export function casualtyToStress(cp: number): number {
  for (const b of CASUALTY_BRACKETS) {
    if (cp <= b.max) return b.stress
  }
  return 6
}
