import type { NationId, TerritoryState, GameState, BattleLogEntry, RaidLogEntry } from './types'
import { UNITS, CAPITALS, NATION_IDS } from './data'
import { TERRITORY_MAP } from './territories'

/** Sum casualty points from unit losses {unitIndex: qty} */
export function computeCasualtyPoints(losses: Record<number, number>): number {
  let total = 0
  for (const [idx, qty] of Object.entries(losses)) {
    const u = UNITS[Number(idx)]
    if (u) total += u.casualtyPoints * qty
  }
  return total
}

/** Medal count for a territory capture (3=capital, 1=normal, 0=neutral/unowned) */
export function medalCount(territoryCode: string): number {
  const def = TERRITORY_MAP[territoryCode]
  if (!def) return 0
  if (def.isNeutral) return 0
  if (CAPITALS.has(territoryCode)) return 3
  return 1
}

/** Check if territory is a neutral first-time invasion for this nation (uses history to prevent double-counting) */
export function isNeutralInvasion(code: string, nationId: NationId, history: Partial<Record<NationId, string[]>>): boolean {
  const def = TERRITORY_MAP[code]
  if (!def || !def.isNeutral) return false
  const invaded = history[nationId] ?? []
  return !invaded.includes(code)
}

/** Record a neutral invasion into game state (mutates game) */
export function recordNeutralInvasion(game: GameState, nationId: NationId, code: string) {
  if (!game.neutralInvasionHistory[nationId]) game.neutralInvasionHistory[nationId] = []
  game.neutralInvasionHistory[nationId]!.push(code)
  game.neutralInvasionsThisRound[nationId] = (game.neutralInvasionsThisRound[nationId] ?? 0) + 1
}

/** Reverse all effects of a battle entry (mutates game) */
export function reverseBattle(game: GameState, entry: BattleLogEntry) {
  // Subtract CP from each nation
  for (const id of NATION_IDS) {
    const cp = entry.nationCPs[id] ?? 0
    if (cp > 0) game.nations[id].casualtyPoints -= cp
  }

  // Restore territory state
  if (entry.locationCode && entry.locationCode !== 'sea') {
    const terr = game.territories[entry.locationCode]
    if (terr) {
      terr.owner = entry.prevOwner
      terr.embattled = entry.prevEmbattled
    }
  }

  // Subtract medals
  if (entry.typedOutcome === 'changes-hands' && entry.medalsAwarded > 0) {
    const recipient = entry.medalRecipient ?? entry.newOwner
    if (recipient) game.nations[recipient].medals -= entry.medalsAwarded
  }

  // Subtract SV stress from previous owner
  if (entry.typedOutcome === 'changes-hands' && entry.prevOwner && entry.svStress > 0) {
    game.nations[entry.prevOwner].stress -= entry.svStress
  }

  // Remove neutral invasion record
  if (entry.neutralInvasion && entry.newOwner && entry.locationCode) {
    const hist = game.neutralInvasionHistory[entry.newOwner]
    if (hist) {
      const idx = hist.lastIndexOf(entry.locationCode)
      if (idx >= 0) hist.splice(idx, 1)
    }
    const count = game.neutralInvasionsThisRound[entry.newOwner]
    if (count && count > 0) game.neutralInvasionsThisRound[entry.newOwner] = count - 1
  }

  // Add back repair resources
  for (const id of NATION_IDS) {
    const r = entry.repairs[id]
    if (r) {
      game.nations[id].oil += r.oil
      game.nations[id].iron += r.iron
      game.nations[id].osr += r.osr
    }
  }
}

/** Reverse all effects of a raid entry (mutates game) */
export function reverseRaid(game: GameState, entry: RaidLogEntry) {
  game.nations[entry.nationId].oil += entry.oil
  game.nations[entry.nationId].iron += entry.iron
  game.nations[entry.nationId].osr += entry.osr
  if (entry.convoyCP > 0) {
    game.nations[entry.nationId].casualtyPoints -= entry.convoyCP
  }
}
