import type { NationId, ResourceType, GameState, TerritoryState, NationState, NationProductionOrders, TurnOrderEntry } from './types'
import { TERRITORY_MAP } from './territories'
import { UNITS, RESOURCES, NATION_IDS } from './data'

export interface ResourceBundle { oil: number; iron: number; osr: number }

/** Compute territory income for a nation (embattled = -1 each resource, min 0; China gets no Oil) */
export function territoryIncome(nationId: NationId, territories: Record<string, TerritoryState>): ResourceBundle {
  let oil = 0, iron = 0, osr = 0
  for (const [code, state] of Object.entries(territories)) {
    if (state.owner !== nationId) continue
    const def = TERRITORY_MAP[code]
    if (!def) continue
    const e = state.embattled ? 1 : 0
    oil += Math.max(0, def.oil - e)
    iron += Math.max(0, def.iron - e)
    osr += Math.max(0, def.osr - e)
  }
  if (nationId === 'CHN') oil = 0 // China never gets Oil
  return { oil, iron, osr }
}

/** Total income = territory income (no convoys — they're raid targets, not income) */
export function totalIncome(nationId: NationId, game: GameState): ResourceBundle {
  return territoryIncome(nationId, game.territories)
}

/** Oil bid entry per nation */
export interface OilBid { nationId: NationId; amount: number }

/** Fisher-Yates shuffle (in-place) */
function shuffle<T>(arr: T[]): T[] {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]]
  }
  return arr
}

/** Compute turn order from bids: descending by amount, ties shuffled randomly */
export function computeTurnOrder(bids: OilBid[]): TurnOrderEntry[] {
  const groups = new Map<number, OilBid[]>()
  for (const b of bids) {
    const g = groups.get(b.amount) ?? []
    g.push(b)
    groups.set(b.amount, g)
  }
  const amounts = [...groups.keys()].sort((a, b) => b - a)
  const result: TurnOrderEntry[] = []
  for (const amt of amounts) {
    const g = groups.get(amt)!
    const isTied = g.length > 1
    shuffle(g)
    for (const b of g) result.push({ ...b, tied: isTied })
  }
  return result
}

/** Check all bids are non-negative and within oil stock */
export function validateBids(bids: OilBid[], nations: GameState['nations']): string | null {
  for (const b of bids) {
    if (b.amount < 0) return `${b.nationId}: bid cannot be negative`
    if (b.amount > nations[b.nationId].oil) return `${b.nationId}: not enough Oil (has ${nations[b.nationId].oil}, bid ${b.amount})`
  }
  return null
}

/** Sum cost of unit orders */
export interface UnitOrder { unitIndex: number; qty: number }
export function unitOrderCost(orders: UnitOrder[]): ResourceBundle {
  let oil = 0, iron = 0, osr = 0
  for (const o of orders) {
    const u = UNITS[o.unitIndex]
    oil += u.cost[0] * o.qty
    iron += u.cost[1] * o.qty
    osr += u.cost[2] * o.qty
  }
  return { oil, iron, osr }
}

/** Compute trade: receive 1 block of `receive`, give 1 block of `give` */
export function tradeResult(receive: ResourceType, give: ResourceType): { receiveAmt: number; giveAmt: number } {
  return {
    receiveAmt: RESOURCES[receive].tradeRate,
    giveAmt: RESOURCES[give].tradeRate,
  }
}

/** Units available for a nation (China: land only, no Oil-costing units) */
export function availableUnits(nationId: NationId): number[] {
  return UNITS.map((u, i) => i).filter(i => {
    const u = UNITS[i]
    if (nationId === 'CHN') {
      return u.category === 'Land' && u.cost[0] === 0 // no Oil, land only
    }
    return true
  })
}

/** Total resources of a resource bundle */
export function totalResources(b: ResourceBundle): number {
  return b.oil + b.iron + b.osr
}

/** Subtract bundle b from bundle a, returning remaining (can go negative = overspent) */
export function subtractResources(a: ResourceBundle, b: ResourceBundle): ResourceBundle {
  return { oil: a.oil - b.oil, iron: a.iron - b.iron, osr: a.osr - b.osr }
}

/** Check if resources are all >= 0 */
export function canAfford(resources: ResourceBundle): boolean {
  return resources.oil >= 0 && resources.iron >= 0 && resources.osr >= 0
}

/** Empty production orders for one nation */
export function emptyProductionOrders(): NationProductionOrders {
  const unitOrders: Record<number, number> = {}
  for (let i = 0; i < UNITS.length; i++) unitOrders[i] = 0
  return { unitOrders, tradeReceive: null, tradeGive: null, civilianGoods: 0, civGoodsPay: { oil: 0, iron: 0, osr: 0 }, bombRepair: 0 }
}

/** Empty orders for all 7 nations */
export function initAllOrders(): Record<NationId, NationProductionOrders> {
  return Object.fromEntries(NATION_IDS.map(id => [id, emptyProductionOrders()])) as Record<NationId, NationProductionOrders>
}

/** Check if a nation has any non-empty orders */
export function hasOrders(o: NationProductionOrders): boolean {
  if (o.tradeReceive || o.tradeGive) return true
  if (o.civilianGoods > 0) return true
  if (o.bombRepair > 0) return true
  return Object.values(o.unitOrders).some(q => q > 0)
}

/** Compute total spent for one nation's orders */
export function computeNationSpent(orders: NationProductionOrders): ResourceBundle {
  const ol: UnitOrder[] = Object.entries(orders.unitOrders)
    .filter(([, qty]) => qty > 0)
    .map(([i, qty]) => ({ unitIndex: Number(i), qty }))
  const uc = unitOrderCost(ol)
  let oil = uc.oil, iron = uc.iron, osr = uc.osr

  if (orders.tradeReceive && orders.tradeGive && orders.tradeReceive !== orders.tradeGive) {
    const tr = tradeResult(orders.tradeReceive, orders.tradeGive)
    const recv: ResourceBundle = { oil: 0, iron: 0, osr: 0 }
    recv[orders.tradeReceive] = tr.receiveAmt
    const give: ResourceBundle = { oil: 0, iron: 0, osr: 0 }
    give[orders.tradeGive] = tr.giveAmt
    oil -= recv.oil - give.oil
    iron -= recv.iron - give.iron
    osr -= recv.osr - give.osr
  }

  oil += orders.civGoodsPay.oil
  iron += orders.civGoodsPay.iron
  osr += orders.civGoodsPay.osr
  if (orders.bombRepair > 0) iron += orders.bombRepair * 9

  return { oil, iron, osr }
}

/** Apply one nation's production orders to its state (pure — returns new NationState) */
export function applyNationProduction(ns: NationState, orders: NationProductionOrders): NationState {
  const out = { ...ns }

  // Trade
  if (orders.tradeReceive && orders.tradeGive && orders.tradeReceive !== orders.tradeGive) {
    const tr = tradeResult(orders.tradeReceive, orders.tradeGive)
    out[orders.tradeReceive] += tr.receiveAmt
    out[orders.tradeGive] -= tr.giveAmt
  }

  // Unit costs
  const ol: UnitOrder[] = Object.entries(orders.unitOrders)
    .filter(([, qty]) => qty > 0)
    .map(([i, qty]) => ({ unitIndex: Number(i), qty }))
  const uc = unitOrderCost(ol)
  out.oil -= uc.oil
  out.iron -= uc.iron
  out.osr -= uc.osr

  // Civilian goods
  if (orders.civilianGoods > 0) {
    out.oil -= orders.civGoodsPay.oil
    out.iron -= orders.civGoodsPay.iron
    out.osr -= orders.civGoodsPay.osr
    out.civilianGoods += orders.civilianGoods
  }

  // Bomb repair
  if (orders.bombRepair > 0) out.iron -= orders.bombRepair * 9

  return out
}

/** Validate all nations can afford their orders. Returns error string or null. */
export function validateAllProduction(
  allOrders: Record<NationId, NationProductionOrders>,
  nations: Record<NationId, NationState>,
): string | null {
  for (const id of NATION_IDS) {
    const orders = allOrders[id]
    if (!hasOrders(orders)) continue
    const avail: ResourceBundle = { oil: nations[id].oil, iron: nations[id].iron, osr: nations[id].osr }
    const spent = computeNationSpent(orders)
    const rem = subtractResources(avail, spent)
    if (!canAfford(rem)) return `${id}: cannot afford production`
    // Check civ goods assignment
    if (orders.civilianGoods > 0) {
      const civTotal = orders.civilianGoods * 5
      const civAssigned = orders.civGoodsPay.oil + orders.civGoodsPay.iron + orders.civGoodsPay.osr
      if (civAssigned !== civTotal) return `${id}: civilian goods cost not fully assigned`
    }
  }
  return null
}
