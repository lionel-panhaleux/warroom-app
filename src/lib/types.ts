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

export interface TurnOrderEntry {
  nationId: NationId
  amount: number
  tied: boolean
}

export interface BattleLogEntry {
  // Display fields
  location: string
  nationsInvolved: NationId[]
  totalCP: number
  outcome: string
  newOwner: NationId | null
  // Full input data (for edit/reversal)
  locationCode: string | null
  losses: Record<NationId, Record<number, number>>
  typedOutcome: 'changes-hands' | 'embattled' | 'no-change' | 'sea' | null
  medalRecipient: NationId | null
  repairs: Record<NationId, { oil: number; iron: number; osr: number }>
  // Reversal data
  nationCPs: Record<NationId, number>
  medalsAwarded: number
  svStress: number
  prevOwner: TerritoryOwner
  prevEmbattled: boolean
  neutralInvasion: boolean
}

export interface RaidLogEntry {
  nationId: NationId
  raidType: 'strategic' | 'convoy'
  oil: number
  iron: number
  osr: number
  convoyCP: number // 6 per resource lost in convoy raids
}

export interface GameState {
  round: number
  roundPhase: RoundPhase
  nations: Record<NationId, NationState>
  territories: Record<string, TerritoryState>
  neutralInvasionHistory: Partial<Record<NationId, string[]>> // permanent: territory codes invaded per nation
  neutralInvasionsThisRound: Partial<Record<NationId, number>> // count per nation, reset each round
  pactBroken: boolean // Soviet-Japanese Non-Aggression Pact (one-time, permanent)
  turnOrder: TurnOrderEntry[] | null // persisted from oil bidding
  battleLog: BattleLogEntry[] // battles this round, cleared on round advance
  raidLog: RaidLogEntry[] // raids this round, cleared on round advance
}

export interface AppState {
  game: GameState
  undoStack: GameState[]
}
