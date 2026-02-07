<script lang="ts">
  import { appState, resetGame } from '../lib/state.svelte'
  import { NATIONS, ALLIED_IDS, AXIS_IDS, HOMELAND_ZONES, ZONE_INFO } from '../lib/data'
  import { totalIncome } from '../lib/economy'
  import { icon } from '../lib/icons'
  import type { NationId } from '../lib/types'
  import Territories from './economy/Territories.svelte'

  let showResetModal = $state(false)
  let showTerritories = $state(false)

  function zoneIndex(nationId: NationId): number {
    return HOMELAND_ZONES.indexOf(appState.game.nations[nationId].zone)
  }

  function territoryCount(nationId: NationId): number {
    return Object.values(appState.game.territories).filter(t => t.owner === nationId).length
  }

  function confirmReset() {
    resetGame()
    showResetModal = false
  }
</script>

<div>
  <div class="flex items-center justify-between mb-4">
    <h1 class="text-xl font-bold text-accent">War Room</h1>
    <span class="text-text-muted text-sm">Round {appState.game.round}</span>
  </div>

  {#each [{ label: 'Allies', ids: ALLIED_IDS }, { label: 'Axis', ids: AXIS_IDS }] as group}
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide mb-2 mt-4">{group.label}</h2>
    <div class="grid gap-2">
      {#each group.ids as id}
        {@const nation = NATIONS[id]}
        {@const ns = appState.game.nations[id]}
        {@const zi = ZONE_INFO[ns.zone]}
        <div class="rounded-lg px-3 py-2 bg-bg-surface">
          <div class="flex items-center gap-3">
            <div class="w-2 h-8 rounded-full" style="background: var(--color-nation-{id})"></div>
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm truncate">{nation.name}</div>
              <div class="flex items-center gap-3 text-xs text-text-muted mt-0.5">
                <span class="inline-flex items-center gap-0.5">{@html icon('resources','oil','icon-xs')} {ns.oil}</span>
                <span class="inline-flex items-center gap-0.5">{@html icon('resources','iron','icon-xs')} {ns.iron}</span>
                <span class="inline-flex items-center gap-0.5">{@html icon('resources','osr','icon-xs')} {ns.osr}</span>
                <span class="inline-flex items-center gap-0.5">{@html icon('ui','territory','icon-xs')} {territoryCount(id)}</span>
                <span class="inline-flex items-center gap-0.5">{@html icon('markers','medal','icon-xs')} {ns.medals}</span>
                <span class="inline-flex items-center gap-0.5">{@html icon('markers','civilian-goods','icon-xs')} {ns.civilianGoods}</span>
              </div>
            </div>
            <div class="text-xs px-2 py-0.5 rounded font-medium"
                 style="background: color-mix(in srgb, var(--color-zone-{ns.zone}) 25%, transparent);
                        color: var(--color-zone-{ns.zone})">
              {zi.name}
            </div>
          </div>
          {#if ns.zone !== 'White'}
            <div class="text-[10px] text-text-muted mt-1 ml-5 italic">{zi.effect}</div>
          {/if}
        </div>
      {/each}
    </div>
  {/each}

  <!-- Territories -->
  <div class="mt-6">
    <button
      class="w-full flex items-center justify-between py-2 text-sm font-semibold text-text-muted uppercase tracking-wide"
      onclick={() => showTerritories = !showTerritories}
    >
      Territories
      <span class="text-xs">{showTerritories ? '▲' : '▼'}</span>
    </button>
    {#if showTerritories}
      <Territories />
    {/if}
  </div>

  <!-- New Game -->
  <div class="mt-8 mb-4">
    <button
      class="w-full py-2.5 rounded-lg font-semibold text-sm bg-red-900/40 text-red-300 active:bg-red-900/60"
      onclick={() => showResetModal = true}
    >New Game</button>
  </div>
</div>

<!-- Reset confirmation modal -->
{#if showResetModal}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
    role="dialog" aria-modal="true" tabindex="-1"
    onclick={() => showResetModal = false}
    onkeydown={(e) => { if (e.key === 'Escape') showResetModal = false }}
  >
    <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
    <div class="bg-bg-surface rounded-xl p-5 mx-4 max-w-sm w-full shadow-xl" onclick={(e) => e.stopPropagation()}>
      <h3 class="text-lg font-bold text-red-400 mb-2">Start New Game?</h3>
      <p class="text-sm text-text-muted mb-4">This will erase all current game data including resources, territories, and undo history. This cannot be undone.</p>
      <div class="flex gap-3">
        <button
          class="flex-1 py-2.5 rounded-lg font-semibold text-sm bg-bg-surface-alt text-text-primary active:bg-bg-surface"
          onclick={() => showResetModal = false}
        >Cancel</button>
        <button
          class="flex-1 py-2.5 rounded-lg font-semibold text-sm bg-red-600 text-white active:bg-red-700"
          onclick={confirmReset}
        >Reset</button>
      </div>
    </div>
  </div>
{/if}
