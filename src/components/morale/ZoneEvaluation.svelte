<script lang="ts">
  import type { HomelandZone } from '../../lib/types'
  import { HOMELAND_ZONES, NATIONS } from '../../lib/data'
  import { zoneIndex } from '../../lib/morale'
  import type { NationId } from '../../lib/types'

  let { currentZone, projectedZone, stressAfterCancel, nationId }: {
    currentZone: HomelandZone
    projectedZone: HomelandZone
    stressAfterCancel: number
    nationId: NationId
  } = $props()

  const threshold = $derived(NATIONS[nationId].stressThreshold)
  const curIdx = $derived(zoneIndex(currentZone))
  const projIdx = $derived(zoneIndex(projectedZone))
  const advances = $derived(projIdx - curIdx)
</script>

<div class="space-y-3">
  <h3 class="text-sm font-semibold text-text-muted uppercase tracking-wide">Zone Evaluation</h3>

  <!-- Zone track -->
  <div class="flex items-center justify-between gap-1">
    {#each HOMELAND_ZONES as z, i}
      {@const isCurrent = i === curIdx}
      {@const isProjected = i === projIdx}
      <div class="flex flex-col items-center gap-1">
        <div
          class="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-bold
                 {isCurrent && !isProjected ? 'ring-2 ring-white' : ''}
                 {isProjected && !isCurrent ? 'ring-2 ring-accent' : ''}
                 {isCurrent && isProjected ? 'ring-2 ring-white' : ''}"
          style="background:var(--color-zone-{z}); color:{z === 'White' || z === 'Yellow' ? '#111' : '#fff'}"
        >
          {z[0]}
        </div>
        {#if isCurrent && !isProjected}
          <span class="text-[9px] text-text-muted">now</span>
        {:else if isProjected && !isCurrent}
          <span class="text-[9px] text-accent">new</span>
        {:else if isCurrent && isProjected}
          <span class="text-[9px] text-text-muted">stay</span>
        {:else}
          <span class="text-[9px] invisible">.</span>
        {/if}
      </div>
    {/each}
  </div>

  <!-- Summary -->
  <div class="text-sm space-y-0.5">
    {#if advances > 0}
      <p>
        <span class="text-red-400 font-semibold">{stressAfterCancel}</span> stress vs threshold
        <span class="font-semibold">{threshold}</span>
        → advance <span class="text-red-400 font-bold">{advances}</span> zone{advances > 1 ? 's' : ''}
      </p>
    {:else}
      <p class="text-green-400">Stress below threshold — no zone advance</p>
    {/if}
  </div>
</div>
