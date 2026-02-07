<script lang="ts">
  import type { NationId } from '../lib/types'
  import { NATION_IDS } from '../lib/data'
  import { appState, setState } from '../lib/state.svelte'
  import { initAllDecisions, computeMoralePreview, applyMoralePhase } from '../lib/morale'
  import type { NationMoraleDecisions } from '../lib/morale'
  import NationSelector from './economy/NationSelector.svelte'
  import StressOverview from './morale/StressOverview.svelte'
  import ZoneEvaluation from './morale/ZoneEvaluation.svelte'
  import ZoneRelief from './morale/ZoneRelief.svelte'
  import ZonePenalties from './morale/ZonePenalties.svelte'

  let selectedNation: NationId = $state('CHN')
  let allDecisions: Record<NationId, NationMoraleDecisions> = $state(initAllDecisions())

  const ns = $derived(appState.game.nations[selectedNation])
  const decisions = $derived(allDecisions[selectedNation])
  const preview = $derived(computeMoralePreview(ns, selectedNation, decisions))

  // Indicators: green dot if nation has CP or existing stress
  const indicators = $derived.by(() => {
    const out: Partial<Record<NationId, boolean>> = {}
    for (const id of NATION_IDS) {
      const n = appState.game.nations[id]
      const d = allDecisions[id]
      const unrest = d.unrestPay.oil + d.unrestPay.iron + d.unrestPay.osr
      out[id] = n.casualtyPoints > 0 || n.stress > 0 || d.medalsToSpend > 0 || d.cgToSpend > 0 || d.reliefMedals > 0 || d.reliefCG > 0 || unrest > 0
    }
    return out
  })

  // Available medals/CG after step 1 spending (for relief)
  const availMedalsForRelief = $derived(ns.medals - decisions.medalsToSpend)
  const availCGForRelief = $derived(ns.civilianGoods - decisions.cgToSpend)

  // Validation
  const validationError = $derived.by(() => {
    for (const id of NATION_IDS) {
      const d = allDecisions[id]
      const n = appState.game.nations[id]
      const totalRelief = d.reliefMedals + d.reliefCG
      if (totalRelief > 0) {
        const p = computeMoralePreview(n, id, d)
        if (totalRelief !== p.reliefCost) return `${id}: relief must total exactly ${p.reliefCost}`
      }
      if (d.medalsToSpend > n.medals) return `${id}: spending more medals than available`
      if (d.cgToSpend > n.civilianGoods) return `${id}: spending more CG than available`
      const unrestTotal = d.unrestPay.oil + d.unrestPay.iron + d.unrestPay.osr
      if (unrestTotal > 0 && unrestTotal !== 3) return `${id}: unrest payment must total 3`
      if (d.unrestPay.oil > n.oil || d.unrestPay.iron > n.iron || d.unrestPay.osr > n.osr) return `${id}: not enough resources for unrest`
    }
    return null
  })

  function handleApply() {
    if (validationError) return
    const newNations = applyMoralePhase(appState.game.nations, allDecisions)
    setState({ ...appState.game, nations: newNations, roundPhase: 'production' as const })
    allDecisions = initAllDecisions()
  }
</script>

<div class="space-y-4">
  <h1 class="text-xl font-bold text-accent">Morale</h1>
  <p class="text-xs text-text-muted">Phase 6 — Convert casualties to stress, advance/relieve homeland zones</p>

  <NationSelector bind:selected={selectedNation} {indicators} />

  <div class="space-y-5 bg-bg-surface rounded-xl p-4">
    <StressOverview {ns} nationId={selectedNation} bind:decisions={allDecisions[selectedNation]} />

    <hr class="border-bg-surface-alt" />

    <ZoneEvaluation
      currentZone={ns.zone}
      projectedZone={preview.zoneBeforeRelief}
      stressAfterCancel={preview.stressAfterCancel}
      nationId={selectedNation}
    />

    <hr class="border-bg-surface-alt" />

    <ZoneRelief
      zoneBeforeRelief={preview.zoneBeforeRelief}
      availMedals={availMedalsForRelief}
      availCG={availCGForRelief}
      nationId={selectedNation}
      bind:decisions={allDecisions[selectedNation]}
    />

    <hr class="border-bg-surface-alt" />

    <ZonePenalties zone={preview.finalZone} remainingStress={preview.remainingStress}
      bind:decisions={allDecisions[selectedNation]}
      available={{ oil: ns.oil, iron: ns.iron, osr: ns.osr }} />
  </div>

  <!-- Apply button -->
  <div class="pt-2">
    {#if validationError}
      <p class="text-xs text-red-400 mb-2">{validationError}</p>
    {/if}
    <button
      class="w-full py-3 rounded-xl font-bold text-lg transition-colors
             {validationError ? 'bg-bg-surface-alt text-text-muted cursor-not-allowed' : 'bg-accent text-bg-primary active:bg-accent-dim'}"
      disabled={!!validationError}
      onclick={handleApply}
    >
      Apply Morale Phase
    </button>
  </div>
</div>
