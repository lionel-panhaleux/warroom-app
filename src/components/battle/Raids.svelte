<script lang="ts">
  import { appState, setState } from '../../lib/state.svelte'
  import { NATION_IDS, NATIONS } from '../../lib/data'
  import { icon } from '../../lib/icons'
  import type { NationId } from '../../lib/types'
  import NationSelector from '../economy/NationSelector.svelte'
  import Counter from '../shared/Counter.svelte'

  let selected: NationId = $state('GER')
  let oilLoss = $state(0)
  let ironLoss = $state(0)
  let osrLoss = $state(0)

  let ns = $derived(appState.game.nations[selected])
  let hasChanges = $derived(oilLoss > 0 || ironLoss > 0 || osrLoss > 0)

  function applyRaid() {
    if (!hasChanges) return
    const game = structuredClone($state.snapshot(appState.game))
    game.nations[selected].oil = Math.max(0, game.nations[selected].oil - oilLoss)
    game.nations[selected].iron = Math.max(0, game.nations[selected].iron - ironLoss)
    game.nations[selected].osr = Math.max(0, game.nations[selected].osr - osrLoss)
    setState(game)
    resetForm()
  }

  function resetForm() {
    oilLoss = 0
    ironLoss = 0
    osrLoss = 0
  }
</script>

<div class="space-y-4">
  <NationSelector bind:selected />

  <section class="bg-bg-surface rounded-lg p-3 space-y-3">
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide">
      Resource Losses — {NATIONS[selected].name}
    </h2>
    <p class="text-[10px] text-text-muted">Strategic bombing & convoy raids: deduct resources lost.</p>

    <div class="space-y-2">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-1.5">
          {@html icon('resources', 'oil', 'icon-xs')}
          <span class="text-xs">Oil</span>
          <span class="text-[10px] text-text-muted">(has {ns.oil})</span>
        </div>
        <Counter bind:value={oilLoss} min={0} max={ns.oil} />
      </div>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-1.5">
          {@html icon('resources', 'iron', 'icon-xs')}
          <span class="text-xs">Iron</span>
          <span class="text-[10px] text-text-muted">(has {ns.iron})</span>
        </div>
        <Counter bind:value={ironLoss} min={0} max={ns.iron} />
      </div>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-1.5">
          {@html icon('resources', 'osr', 'icon-xs')}
          <span class="text-xs">OSR</span>
          <span class="text-[10px] text-text-muted">(has {ns.osr})</span>
        </div>
        <Counter bind:value={osrLoss} min={0} max={ns.osr} />
      </div>
    </div>
  </section>

  <button
    class="w-full py-3 rounded-lg font-semibold text-sm transition-colors
           {hasChanges ? 'bg-accent text-bg-primary active:bg-accent-dim' : 'bg-bg-surface-alt text-text-muted'}"
    disabled={!hasChanges}
    onclick={applyRaid}
  >Apply Raid</button>
</div>
