import type { NationId, TerritoryState, GameState } from './types'
import { UNITS, CAPITALS } from './data'
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
