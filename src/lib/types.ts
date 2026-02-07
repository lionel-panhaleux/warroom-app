export type NationId = 'CHN' | 'UK' | 'USSR' | 'USA' | 'GER' | 'ITA' | 'JAP'
export type Alliance = 'Allied' | 'Axis'
export type ResourceType = 'oil' | 'iron' | 'osr'
export type HomelandZone = 'White' | 'Blue' | 'Yellow' | 'Orange' | 'Red' | 'Gray'
export type UnitCategory = 'Land' | 'Air' | 'Naval'

export interface NationDef {
  id: NationId
  name: string
  alliance: Alliance
  maxOrders: number
  stressThreshold: number // Global War scenario
}

export interface UnitDef {
  name: string
  cost: [oil: number, iron: number, osr: number]
  casualtyPoints: number
  category: UnitCategory
}

export interface CasualtyBracket {
  min: number
  max: number // Infinity for last bracket
  stress: number
}

export interface NationState {
  oil: number
  iron: number
  osr: number
  stress: number
  zone: HomelandZone
  medals: number
  civilianGoods: number
  casualtyPoints: number
}

export interface GameState {
  round: number
  nations: Record<NationId, NationState>
}

export interface AppState {
  game: GameState
  undoStack: GameState[]
}
