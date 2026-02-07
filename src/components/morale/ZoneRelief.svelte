<script lang="ts">
  import type { HomelandZone, NationId } from '../../lib/types'
  import type { NationMoraleDecisions } from '../../lib/morale'
  import { NATIONS } from '../../lib/data'
  import { zoneIndex, retreatZone } from '../../lib/morale'
  import { icon } from '../../lib/icons'
  import Counter from '../shared/Counter.svelte'

  let { zoneBeforeRelief, availMedals, availCG, nationId, decisions = $bindable() }: {
    zoneBeforeRelief: HomelandZone
    availMedals: number
    availCG: number
    nationId: NationId
    decisions: NationMoraleDecisions
  } = $props()

  const threshold = $derived(NATIONS[nationId].stressThreshold)
  const eligible = $derived(zoneIndex(zoneBeforeRelief) >= 1)
  const reliefTotal = $derived(decisions.reliefMedals + decisions.reliefCG)
  const isValid = $derived(reliefTotal === 0 || reliefTotal === threshold)
  const maxReliefMedals = $derived(Math.min(availMedals, threshold))
  const maxReliefCG = $derived(Math.min(availCG, threshold - decisions.reliefMedals))
  const targetZone = $derived(reliefTotal === threshold ? retreatZone(zoneBeforeRelief) : zoneBeforeRelief)

  // Clamp on changes
  $effect(() => {
    if (decisions.reliefMedals > maxReliefMedals) decisions.reliefMedals = maxReliefMedals
    if (decisions.reliefCG > maxReliefCG) decisions.reliefCG = Math.max(0, maxReliefCG)
  })
</script>

<div class="space-y-2">
  <h3 class="text-sm font-semibold text-text-muted uppercase tracking-wide">Zone Relief</h3>

  {#if !eligible}
    <p class="text-sm text-text-muted">Already in White zone — no relief needed</p>
  {:else}
    <p class="text-xs text-text-muted">
      Spend exactly <span class="font-bold text-accent">{threshold}</span> medals + civilian goods to retreat one zone.
    </p>

    <div class="space-y-2">
      <div class="flex items-center gap-3">
        <span class="icon icon-sm">{@html icon('markers', 'medal')}</span>
        <Counter bind:value={decisions.reliefMedals} min={0} max={maxReliefMedals} label="Medals" />
        <span class="text-xs text-text-muted">/ {availMedals}</span>
      </div>

      <div class="flex items-center gap-3">
        <span class="icon icon-sm">{@html icon('markers', 'civilian-goods')}</span>
        <Counter bind:value={decisions.reliefCG} min={0} max={maxReliefCG} label="CG" />
        <span class="text-xs text-text-muted">/ {availCG}</span>
      </div>
    </div>

    {#if reliefTotal > 0 && !isValid}
      <p class="text-xs text-danger">Must total exactly {threshold} (currently {reliefTotal})</p>
    {/if}

    {#if reliefTotal === threshold}
      <p class="text-sm">
        Zone retreats:
        <span class="font-bold" style="color:var(--color-zone-{zoneBeforeRelief})">{zoneBeforeRelief}</span>
        →
        <span class="font-bold" style="color:var(--color-zone-{targetZone})">{targetZone}</span>
      </p>
    {/if}
  {/if}
</div>
