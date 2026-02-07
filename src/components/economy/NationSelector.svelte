<script lang="ts">
  import { appState } from '../../lib/state.svelte'
  import { NATION_IDS, NATIONS } from '../../lib/data'
  import { icon } from '../../lib/icons'
  import type { NationId } from '../../lib/types'

  let { selected = $bindable<NationId>(), indicators }: {
    selected: NationId
    indicators?: Partial<Record<NationId, boolean>>
  } = $props()
</script>

<div class="flex gap-1.5 overflow-x-auto py-1 -mx-1 px-1">
  {#each NATION_IDS as id}
    {@const ns = appState.game.nations[id]}
    {@const hasOrder = indicators?.[id]}
    <button
      class="relative flex flex-col items-center gap-0.5 px-2 py-1.5 rounded-lg min-w-[3.5rem] transition-colors
             {selected === id ? 'bg-accent/20 ring-1 ring-accent' : 'bg-bg-surface'}"
      onclick={() => selected = id}
    >
      {#if hasOrder}
        <span class="absolute top-0.5 right-0.5 w-2 h-2 rounded-full bg-green-500"></span>
      {/if}
      {@html icon('nations', id, 'icon-sm')}
      <span class="text-[10px] font-medium">{id}</span>
      <div class="flex gap-1 text-[9px] tabular-nums">
        <span style="color:var(--color-res-oil)">{ns.oil}</span>
        <span style="color:var(--color-res-iron)">{ns.iron}</span>
        <span style="color:var(--color-res-osr)">{ns.osr}</span>
      </div>
    </button>
  {/each}
</div>
