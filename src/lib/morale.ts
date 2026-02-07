import type { NationId, NationState, HomelandZone } from './types'
import { NATIONS, HOMELAND_ZONES, casualtyToStress, NATION_IDS } from './data'

export interface NationMoraleDecisions {
  medalsToSpend: number
  cgToSpend: number
  reliefMedals: number
  reliefCG: number
  unrestPay: { oil: number; iron: number; osr: number }
  neutralInvasionCount: number
  breakPact: boolean
}

export interface MoralePreview {
  casualtyStress: number
  neutralStress: number
  pactStress: number
  totalStress: number
  stressAfterCancel: number
  zoneBeforeRelief: HomelandZone
  advances: number
  remainingStress: number
  reliefEligible: boolean
  reliefCost: number
  finalZone: HomelandZone
  finalStress: number
  finalMedals: number
  finalCG: number
}

export function emptyMoraleDecisions(): NationMoraleDecisions {
  return { medalsToSpend: 0, cgToSpend: 0, reliefMedals: 0, reliefCG: 0, unrestPay: { oil: 0, iron: 0, osr: 0 }, neutralInvasionCount: 0, breakPact: false }
}

export function initAllDecisions(): Record<NationId, NationMoraleDecisions> {
  return Object.fromEntries(NATION_IDS.map(id => [id, emptyMoraleDecisions()])) as Record<NationId, NationMoraleDecisions>
}

export function zoneIndex(zone: HomelandZone): number {
  return HOMELAND_ZONES.indexOf(zone)
}

export function advanceZone(zone: HomelandZone, steps: number): HomelandZone {
  const idx = Math.min(zoneIndex(zone) + steps, HOMELAND_ZONES.length - 1)
  return HOMELAND_ZONES[idx]
}

export function retreatZone(zone: HomelandZone): HomelandZone {
  const idx = Math.max(zoneIndex(zone) - 1, 0)
  return HOMELAND_ZONES[idx]
}

/** Evaluate zone advances from stress: consume threshold repeatedly */
function evaluateZone(stress: number, zone: HomelandZone, threshold: number): { newZone: HomelandZone; remainingStress: number; advances: number } {
  let advances = 0
  let zi = zoneIndex(zone)
  let remaining = stress
  while (remaining >= threshold && zi < HOMELAND_ZONES.length - 1) {
    remaining -= threshold
    zi++
    advances++
  }
  return { newZone: HOMELAND_ZONES[zi], remainingStress: remaining, advances }
}

/** Compute full morale preview for one nation */
export function computeMoralePreview(ns: NationState, nationId: NationId, d: NationMoraleDecisions): MoralePreview {
  const threshold = NATIONS[nationId].stressThreshold
  const casualtyStress = casualtyToStress(ns.casualtyPoints)
  const neutralStress = d.neutralInvasionCount
  const pactStress = d.breakPact ? 6 : 0
  const totalStress = ns.stress + casualtyStress + neutralStress + pactStress
  const cancelledStress = d.medalsToSpend + d.cgToSpend
  const stressAfterCancel = Math.max(0, totalStress - cancelledStress)

  const { newZone, remainingStress, advances } = evaluateZone(stressAfterCancel, ns.zone, threshold)
  const zoneBeforeRelief = newZone

  const reliefEligible = zoneIndex(zoneBeforeRelief) >= 1 // Blue or worse
  const reliefCost = threshold
  const reliefTotal = d.reliefMedals + d.reliefCG

  let finalZone = zoneBeforeRelief
  if (reliefEligible && reliefTotal === reliefCost) {
    finalZone = retreatZone(zoneBeforeRelief)
  }

  const finalStress = remainingStress
  const finalMedals = ns.medals - d.medalsToSpend - d.reliefMedals
  const finalCG = ns.civilianGoods - d.cgToSpend - d.reliefCG

  return {
    casualtyStress, neutralStress, pactStress,
    totalStress, stressAfterCancel,
    zoneBeforeRelief, advances, remainingStress,
    reliefEligible, reliefCost, finalZone, finalStress,
    finalMedals, finalCG,
  }
}

/** Check if any nation is breaking the pact */
export function isPactBrokenInDecisions(decisions: Record<NationId, NationMoraleDecisions>): boolean {
  return decisions.USSR.breakPact || decisions.JAP.breakPact
}

/** Apply morale phase to all nations. Returns new nations record. */
export function applyMoralePhase(
  nations: Record<NationId, NationState>,
  decisions: Record<NationId, NationMoraleDecisions>,
): Record<NationId, NationState> {
  const out = { ...nations }
  for (const id of NATION_IDS) {
    const ns = nations[id]
    const d = decisions[id]
    const preview = computeMoralePreview(ns, id, d)
    out[id] = {
      ...ns,
      oil: ns.oil - d.unrestPay.oil,
      iron: ns.iron - d.unrestPay.iron,
      osr: ns.osr - d.unrestPay.osr,
      stress: preview.finalStress,
      zone: preview.finalZone,
      medals: preview.finalMedals,
      civilianGoods: preview.finalCG,
      casualtyPoints: 0,
    }
  }
  return out
}
