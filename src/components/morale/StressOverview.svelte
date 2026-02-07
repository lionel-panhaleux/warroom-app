<script lang="ts">
  import type { NationState, NationId } from '../../lib/types'
  import type { NationMoraleDecisions } from '../../lib/morale'
  import { casualtyToStress } from '../../lib/data'
  import { icon } from '../../lib/icons'
  import Counter from '../shared/Counter.svelte'

  let { ns, nationId, decisions = $bindable() }: {
    ns: NationState
    nationId: NationId
    decisions: NationMoraleDecisions
  } = $props()

  const casualtyStress = $derived(casualtyToStress(ns.casualtyPoints))
  const totalStress = $derived(ns.stress + casualtyStress)
  const maxMedals = $derived(Math.min(ns.medals, totalStress))
  const remainingAfterMedals = $derived(Math.max(0, totalStress - decisions.medalsToSpend))
  const maxCG = $derived(Math.min(ns.civilianGoods, remainingAfterMedals))

  // Clamp if values exceed new maxes (e.g. when switching nations)
  $effect(() => {
    if (decisions.medalsToSpend > maxMedals) decisions.medalsToSpend = maxMedals
    if (decisions.cgToSpend > maxCG) decisions.cgToSpend = maxCG
  })
</script>

<div class="space-y-3">
  <h3 class="text-sm font-semibold text-text-muted uppercase tracking-wide">Stress</h3>

  <!-- Stress breakdown -->
  <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-sm">
    <span class="text-text-muted">Existing stress</span>
    <span class="text-right font-bold">{ns.stress}</span>
    <span class="text-text-muted">Casualty points</span>
    <span class="text-right">{ns.casualtyPoints} → <span class="font-bold text-red-400">+{casualtyStress}</span></span>
    <span class="text-text-muted font-semibold">Total stress</span>
    <span class="text-right font-bold text-red-400">{totalStress}</span>
  </div>

  <!-- Cancellation -->
  {#if totalStress > 0}
    <div class="space-y-2 pt-1">
      <p class="text-xs text-text-muted">Cancel stress with medals or civilian goods:</p>

      <div class="flex items-center gap-3">
        <span class="icon icon-sm">{@html icon('markers', 'medal')}</span>
        <Counter bind:value={decisions.medalsToSpend} min={0} max={maxMedals} label="Medals" />
        <span class="text-xs text-text-muted">/ {ns.medals}</span>
      </div>

      <div class="flex items-center gap-3">
        <span class="icon icon-sm">{@html icon('markers', 'civilian-goods')}</span>
        <Counter bind:value={decisions.cgToSpend} min={0} max={maxCG} label="CG" />
        <span class="text-xs text-text-muted">/ {ns.civilianGoods}</span>
      </div>

      <p class="text-sm">
        Stress after cancellation:
        <span class="font-bold {remainingAfterMedals - decisions.cgToSpend > 0 ? 'text-red-400' : 'text-green-400'}">
          {Math.max(0, remainingAfterMedals - decisions.cgToSpend)}
        </span>
      </p>
    </div>
  {:else}
    <p class="text-sm text-green-400">No stress this round</p>
  {/if}
</div>
