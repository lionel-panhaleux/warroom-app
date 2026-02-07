import type { NationId, TerritoryState } from './types'
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

/** Check if territory is neutral and currently unowned (first-time invasion = +1 stress) */
export function isNeutralInvasion(code: string, territories: Record<string, TerritoryState>): boolean {
  const def = TERRITORY_MAP[code]
  if (!def || !def.isNeutral) return false
  const state = territories[code]
  return !state || state.owner === null
}
