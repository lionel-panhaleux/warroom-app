<script lang="ts">
  import type { NationId, HomelandZone } from '../lib/types'
  import { NATION_IDS, NATIONS, HOMELAND_ZONES, ZONE_INFO } from '../lib/data'
  import { appState, setState } from '../lib/state.svelte'
  import { initAllDecisions, computeMoralePreview, applyMoralePhase, isPactBrokenInDecisions } from '../lib/morale'
  import type { NationMoraleDecisions } from '../lib/morale'
  import { icon } from '../lib/icons'
  import NationSelector from './economy/NationSelector.svelte'
  import StressOverview from './morale/StressOverview.svelte'
  import ZoneEvaluation from './morale/ZoneEvaluation.svelte'
  import ZoneRelief from './morale/ZoneRelief.svelte'
  import ZonePenalties from './morale/ZonePenalties.svelte'

  type Tab = 'dashboard' | 'economy' | 'battle' | 'morale' | 'production'
  let { showToast }: { showToast: (msg: string, tab: Tab) => void } = $props()

  let selectedNation: NationId = $state('CHN')
  let allDecisions: Record<NationId, NationMoraleDecisions> = $state(initAllDecisionsFromGame())

  // U11: Confirmation modal
  let showConfirmModal = $state(false)

  function initAllDecisionsFromGame() {
    const d = initAllDecisions()
    for (const id of NATION_IDS) {
      d[id].neutralInvasionCount = appState.game.neutralInvasionsThisRound[id] ?? 0
    }
    return d
  }

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
      out[id] = n.casualtyPoints > 0 || n.stress > 0 || d.medalsToSpend > 0 || d.cgToSpend > 0 || d.reliefMedals > 0 || d.reliefCG > 0 || unrest > 0 || d.neutralInvasionCount > 0 || d.breakPact
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
      if (unrestTotal > 0) {
        if (unrestTotal !== 3) return `${id}: unrest payment must total 3`
        if (d.unrestPay.oil > n.oil || d.unrestPay.iron > n.iron || d.unrestPay.osr > n.osr) return `${id}: not enough resources for unrest`
      }
    }
    return null
  })

  // U11: Confirmation summary per nation
  const confirmSummary = $derived.by(() => {
    const items: { id: NationId; oldZone: HomelandZone; newZone: HomelandZone; medals: number; cg: number; unrest: number; pact: boolean }[] = []
    for (const id of NATION_IDS) {
      const n = appState.game.nations[id]
      const d = allDecisions[id]
      const p = computeMoralePreview(n, id, d)
      const unrest = d.unrestPay.oil + d.unrestPay.iron + d.unrestPay.osr
      if (p.finalZone !== n.zone || d.medalsToSpend > 0 || d.cgToSpend > 0 || d.reliefMedals > 0 || d.reliefCG > 0 || unrest > 0 || d.breakPact || n.casualtyPoints > 0) {
        items.push({ id, oldZone: n.zone, newZone: p.finalZone, medals: d.medalsToSpend + d.reliefMedals, cg: d.cgToSpend + d.reliefCG, unrest, pact: d.breakPact })
      }
    }
    return items
  })

  function handleApply() {
    if (validationError) return
    showConfirmModal = true
  }

  function confirmApply() {
    const newNations = applyMoralePhase(appState.game.nations, allDecisions)
    const pactBroken = appState.game.pactBroken || isPactBrokenInDecisions(allDecisions)
    setState({ ...appState.game, nations: newNations, roundPhase: 'production' as const, pactBroken })
    allDecisions = initAllDecisionsFromGame()
    showConfirmModal = false
    showToast('Morale applied \u2014 proceed to Production', 'production')
  }
</script>

<div class="space-y-4">
  <h1 class="text-xl font-bold text-accent">Morale</h1>
  <p class="text-xs text-text-muted">Phase 6 — Convert casualties to stress, advance/relieve homeland zones</p>

  <NationSelector bind:selected={selectedNation} {indicators} />

  <div class="space-y-5 bg-bg-surface rounded-xl p-4">
    <StressOverview {ns} nationId={selectedNation} bind:decisions={allDecisions[selectedNation]} pactBroken={appState.game.pactBroken} />

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

  <!-- U13: Neutral invasion display -->
  {#if decisions.neutralInvasionCount > 0}
    <div class="text-xs text-warning bg-bg-surface rounded-lg px-3 py-2">
      {decisions.neutralInvasionCount} neutral invasion{decisions.neutralInvasionCount > 1 ? 's' : ''} recorded this round (+{decisions.neutralInvasionCount} stress)
    </div>
  {/if}

  <!-- Apply button -->
  <div class="pt-2">
    {#if validationError}
      <p class="text-xs text-danger mb-2">{validationError}</p>
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

<!-- U11: Confirmation modal -->
{#if showConfirmModal}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
    role="dialog" aria-modal="true" tabindex="-1"
    onclick={() => showConfirmModal = false}
    onkeydown={(e) => { if (e.key === 'Escape') showConfirmModal = false }}
  >
    <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
    <div class="bg-bg-surface rounded-xl p-5 mx-4 max-w-sm w-full shadow-xl max-h-[80vh] overflow-y-auto" onclick={(e) => e.stopPropagation()}>
      <h3 class="text-lg font-bold text-accent mb-3">Confirm Morale Phase</h3>

      {#if confirmSummary.length === 0}
        <p class="text-sm text-text-muted mb-4">No changes to apply.</p>
      {:else}
        <div class="space-y-2 mb-4">
          {#each confirmSummary as item}
            <div class="text-xs border-b border-bg-surface-alt pb-2 last:border-0">
              <div class="flex items-center gap-1.5 font-semibold">
                {@html icon('nations', item.id, 'icon-xs')} {NATIONS[item.id].name}
              </div>
              <div class="ml-5 text-text-muted space-y-0.5 mt-0.5">
                {#if item.oldZone !== item.newZone}
                  <div class="flex items-center gap-1">Zone:
                    <span class="inline-block w-2.5 h-2.5 rounded-full" style="background:var(--color-zone-{item.oldZone})"></span>{ZONE_INFO[item.oldZone].name}
                    →
                    <span class="inline-block w-2.5 h-2.5 rounded-full" style="background:var(--color-zone-{item.newZone})"></span>{ZONE_INFO[item.newZone].name}
                  </div>
                {/if}
                {#if item.medals > 0}<div>Medals spent: {item.medals}</div>{/if}
                {#if item.cg > 0}<div>CG spent: {item.cg}</div>{/if}
                {#if item.unrest > 0}<div>Unrest paid: {item.unrest} resources</div>{/if}
                {#if item.pact}<div class="text-danger">Pact broken!</div>{/if}
              </div>
            </div>
          {/each}
        </div>
      {/if}

      <div class="flex gap-3">
        <button
          class="flex-1 py-2.5 rounded-lg font-semibold text-sm bg-bg-surface-alt text-text-primary active:bg-bg-surface"
          onclick={() => showConfirmModal = false}
        >Cancel</button>
        <button
          class="flex-1 py-2.5 rounded-lg font-semibold text-sm bg-accent text-bg-primary active:bg-accent-dim"
          onclick={confirmApply}
        >Confirm</button>
      </div>
    </div>
  </div>
{/if}
