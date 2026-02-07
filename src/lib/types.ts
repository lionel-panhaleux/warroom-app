export type NationId = 'CHN' | 'UK' | 'USSR' | 'USA' | 'GER' | 'ITA' | 'JAP'
export type Alliance = 'Allied' | 'Axis'
export type ResourceType = 'oil' | 'iron' | 'osr'
export type HomelandZone = 'White' | 'Blue' | 'Yellow' | 'Orange' | 'Red' | 'Gray'
export type UnitCategory = 'Land' | 'Air' | 'Naval'
export type RoundPhase = 'income' | 'bidding' | 'morale' | 'production'

export type TerritoryOwner = NationId | null
export type IndustryType = 'Y' | 'C' | 'YC' | null

export interface NationProductionOrders {
  unitOrders: Record<number, number>
  tradeReceive: ResourceType | null
  tradeGive: ResourceType | null
  civilianGoods: number
  civGoodsPay: { oil: number; iron: number; osr: number }
  bombRepair: number
}

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

export interface TerritoryDef {
  code: string
  name: string
  startingOwner: TerritoryOwner
  sv: number
  oil: number
  iron: number
  osr: number
  industry: IndustryType
  isNeutral: boolean
  notes?: string
}

export interface TerritoryState {
  owner: TerritoryOwner
  embattled: boolean
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
  roundPhase: RoundPhase
  nations: Record<NationId, NationState>
  territories: Record<string, TerritoryState>
}

export interface AppState {
  game: GameState
  undoStack: GameState[]
}
