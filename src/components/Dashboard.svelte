<script lang="ts">
  import { appState, setState, resetGame, undo } from '../lib/state.svelte'
  import { NATIONS, ALLIED_IDS, AXIS_IDS, HOMELAND_ZONES, ZONE_INFO } from '../lib/data'
  import { totalIncome } from '../lib/economy'
  import { icon } from '../lib/icons'
  import { uiIcons } from '../lib/icons'
  import type { NationId, HomelandZone, NationState } from '../lib/types'
  import Territories from './economy/Territories.svelte'

  let showResetModal = $state(false)
  let showTerritories = $state(false)
  let fixMode = $state(false)

  // U8: Round label
  let roundLabel = $derived(appState.game.round === 0 ? 'Setup' : `Round ${appState.game.round}`)

  function zoneIndex(nationId: NationId): number {
    return HOMELAND_ZONES.indexOf(appState.game.nations[nationId].zone)
  }

  function territoryCount(nationId: NationId): number {
    return Object.values(appState.game.territories).filter(t => t.owner === nationId).length
  }

  // F10: Embattled territory count
  function embattledCount(nationId: NationId): number {
    return Object.values(appState.game.territories).filter(t => t.owner === nationId && t.embattled).length
  }

  // F3: Track previous resource values for flash animation
  // prevResources is intentionally NOT $state — must not be tracked by $effect
  let prevResources: Record<string, { oil: number; iron: number; osr: number }> =
    Object.fromEntries(Object.entries(appState.game.nations).map(([id, ns]) => [id, { oil: ns.oil, iron: ns.iron, osr: ns.osr }]))
  let flashClasses: Record<string, string> = $state({})

  $effect(() => {
    const nations = appState.game.nations
    const newFlash: Record<string, string> = {}
    for (const id of [...ALLIED_IDS, ...AXIS_IDS]) {
      for (const r of ['oil', 'iron', 'osr'] as const) {
        const key = `${id}-${r}`
        const cur = nations[id][r]
        const prev = prevResources[id]?.[r]
        if (prev !== undefined && cur !== prev) {
          newFlash[key] = cur > prev ? 'flash-up' : 'flash-down'
        }
      }
    }
    // Update prev snapshot outside reactive read
    for (const id of [...ALLIED_IDS, ...AXIS_IDS]) {
      prevResources[id] = { oil: nations[id].oil, iron: nations[id].iron, osr: nations[id].osr }
    }
    if (Object.keys(newFlash).length > 0) {
      flashClasses = { ...newFlash }
      setTimeout(() => flashClasses = {}, 700)
    }
  })

  function confirmReset() {
    resetGame()
    showResetModal = false
  }

  function fixNation(id: NationId, field: keyof NationState, value: number | HomelandZone) {
    const game = structuredClone($state.snapshot(appState.game))
    ;(game.nations[id] as any)[field] = value
    setState(game)
  }

  function stressMax(id: NationId): number {
    return appState.game.nations[id].zone === 'Gray' ? 99 : NATIONS[id].stressThreshold - 1
  }

  function fixDelta(id: NationId, field: keyof NationState, delta: number, min: number, max: number) {
    const cur = appState.game.nations[id][field] as number
    const next = Math.max(min, Math.min(max, cur + delta))
    if (next !== cur) fixNation(id, field, next)
  }
</script>

<div>
  <div class="flex items-center justify-between mb-4">
    <h1 class="text-xl font-bold text-accent">War Room</h1>
    <div class="flex items-center gap-3">
      <button
        class="flex items-center gap-1.5 text-sm px-3 py-2 rounded-lg {fixMode ? 'bg-accent/20 text-accent font-semibold' : 'bg-bg-surface text-text-muted'}"
        onclick={() => { fixMode = !fixMode; if (fixMode) showTerritories = true }}
        aria-pressed={fixMode}
      >
        {@html icon('markers','wrench','icon-sm')} Fix State
      </button>
      <span class="text-text-muted text-sm">{roundLabel}</span>
      {#if appState.undoStack.length > 0}
        <button
          class="w-8 h-8 flex items-center justify-center rounded-full bg-bg-surface-alt text-text-muted active:bg-accent/30 [&>svg]:w-4 [&>svg]:h-4"
          aria-label="Undo"
          onclick={undo}
        >{@html uiIcons.undo}</button>
      {/if}
    </div>
  </div>

  {#each [{ label: 'Allies', ids: ALLIED_IDS }, { label: 'Axis', ids: AXIS_IDS }] as group}
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide mb-2 mt-4">{group.label}</h2>
    <div class="grid gap-2">
      {#each group.ids as id}
        {@const nation = NATIONS[id]}
        {@const ns = appState.game.nations[id]}
        {@const zi = ZONE_INFO[ns.zone]}
        {@const emb = embattledCount(id)}
        <!-- F9: Nation color-coded left border -->
        <div class="rounded-lg px-3 py-2 bg-bg-surface border-l-4" style="border-color: var(--color-nation-{id})">
          <div class="flex items-center gap-3">
            <!-- U9: Nation flag icon instead of colored bar -->
            <span class="[&>span]:!inline-flex">{@html icon('nations', id, 'icon-sm')}</span>
            <div class="flex-1 min-w-0">
              <div class="font-medium text-sm truncate">{nation.name}</div>
              <div class="flex items-center gap-3 text-xs text-text-muted mt-0.5">
                <span class="inline-flex items-center gap-0.5 {flashClasses[`${id}-oil`] ?? ''}">{@html icon('resources','oil','icon-xs')} {ns.oil}</span>
                <span class="inline-flex items-center gap-0.5 {flashClasses[`${id}-iron`] ?? ''}">{@html icon('resources','iron','icon-xs')} {ns.iron}</span>
                <span class="inline-flex items-center gap-0.5 {flashClasses[`${id}-osr`] ?? ''}">{@html icon('resources','osr','icon-xs')} {ns.osr}</span>
                <span class="inline-flex items-center gap-0.5">{@html icon('ui','territory','icon-xs')} {territoryCount(id)}{#if emb > 0}<span class="text-danger ml-0.5" title="{emb} embattled">!{emb}</span>{/if}</span>
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
          {#if ns.zone !== 'White' && !fixMode}
            <div class="text-[10px] text-text-muted mt-1 ml-5 italic">{zi.effect}</div>
          {/if}

          <!-- Fix Mode panel -->
          {#if fixMode}
            <div class="mt-2 pt-2 border-t border-bg-surface-alt space-y-2">
              <!-- Resources -->
              {#each [
                { field: 'oil' as const, label: 'Oil', icon: 'oil' },
                { field: 'iron' as const, label: 'Iron', icon: 'iron' },
                { field: 'osr' as const, label: 'OSR', icon: 'osr' },
              ] as r}
                <div class="flex items-center gap-2">
                  <span class="inline-flex items-center gap-0.5 text-xs text-text-muted w-14">
                    {@html icon('resources', r.icon, 'icon-xs')} {r.label}
                  </span>
                  <button
                    class="w-8 h-8 flex items-center justify-center rounded bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
                    disabled={ns[r.field] <= 0}
                    onclick={() => fixDelta(id, r.field, -1, 0, 99)}
                  >{@html uiIcons.minus}</button>
                  <span class="w-8 text-center font-bold tabular-nums text-sm">{ns[r.field]}</span>
                  <button
                    class="w-8 h-8 flex items-center justify-center rounded bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
                    disabled={ns[r.field] >= 99}
                    onclick={() => fixDelta(id, r.field, 1, 0, 99)}
                  >{@html uiIcons.plus}</button>
                </div>
              {/each}

              <!-- Stress -->
              <div class="flex items-center gap-2">
                <span class="text-xs text-text-muted w-14">Stress</span>
                <button
                  class="w-8 h-8 flex items-center justify-center rounded bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
                  disabled={ns.stress <= 0}
                  onclick={() => fixDelta(id, 'stress', -1, 0, stressMax(id))}
                >{@html uiIcons.minus}</button>
                <span class="w-8 text-center font-bold tabular-nums text-sm">{ns.stress}</span>
                <button
                  class="w-8 h-8 flex items-center justify-center rounded bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
                  disabled={ns.stress >= stressMax(id)}
                  onclick={() => fixDelta(id, 'stress', 1, 0, stressMax(id))}
                >{@html uiIcons.plus}</button>
                <span class="text-[10px] text-text-muted">/ {ns.zone === 'Gray' ? '\u221E' : nation.stressThreshold - 1}</span>
              </div>

              <!-- Medals -->
              <div class="flex items-center gap-2">
                <span class="inline-flex items-center gap-0.5 text-xs text-text-muted w-14">
                  {@html icon('markers', 'medal', 'icon-xs')} Medals
                </span>
                <button
                  class="w-8 h-8 flex items-center justify-center rounded bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
                  disabled={ns.medals <= 0}
                  onclick={() => fixDelta(id, 'medals', -1, 0, 99)}
                >{@html uiIcons.minus}</button>
                <span class="w-8 text-center font-bold tabular-nums text-sm">{ns.medals}</span>
                <button
                  class="w-8 h-8 flex items-center justify-center rounded bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
                  disabled={ns.medals >= 99}
                  onclick={() => fixDelta(id, 'medals', 1, 0, 99)}
                >{@html uiIcons.plus}</button>
              </div>

              <!-- Civilian Goods -->
              <div class="flex items-center gap-2">
                <span class="inline-flex items-center gap-0.5 text-xs text-text-muted w-14">
                  {@html icon('markers', 'civilian-goods', 'icon-xs')} CG
                </span>
                <button
                  class="w-8 h-8 flex items-center justify-center rounded bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
                  disabled={ns.civilianGoods <= 0}
                  onclick={() => fixDelta(id, 'civilianGoods', -1, 0, 99)}
                >{@html uiIcons.minus}</button>
                <span class="w-8 text-center font-bold tabular-nums text-sm">{ns.civilianGoods}</span>
                <button
                  class="w-8 h-8 flex items-center justify-center rounded bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
                  disabled={ns.civilianGoods >= 99}
                  onclick={() => fixDelta(id, 'civilianGoods', 1, 0, 99)}
                >{@html uiIcons.plus}</button>
              </div>

              <!-- Homeland Zone -->
              <div class="flex items-center gap-2">
                <span class="text-xs text-text-muted w-14">Zone</span>
                <div class="flex gap-1">
                  {#each HOMELAND_ZONES as z}
                    <button
                      class="w-7 h-7 rounded text-[9px] font-bold {ns.zone === z ? 'ring-2 ring-white' : 'ring-1 ring-white/20 opacity-50'}"
                      style="background: var(--color-zone-{z}); color: {z === 'White' || z === 'Yellow' ? '#1a1a1a' : '#fff'}"
                      onclick={() => fixNation(id, 'zone', z)}
                    >{z[0]}</button>
                  {/each}
                </div>
              </div>
            </div>
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
      <span class="text-xs">{showTerritories ? '\u25B2' : '\u25BC'}</span>
    </button>
    {#if showTerritories}
      <Territories />
    {/if}
  </div>

  <!-- New Game -->
  <div class="mt-8 mb-4">
    <button
      class="w-full py-2.5 rounded-lg font-semibold text-sm bg-danger-dim/40 text-danger active:bg-danger-dim/60"
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
      <h3 class="text-lg font-bold text-danger mb-2">Start New Game?</h3>
      <p class="text-sm text-text-muted mb-4">This will erase all current game data including resources, territories, and undo history. This cannot be undone.</p>
      <div class="flex gap-3">
        <button
          class="flex-1 py-2.5 rounded-lg font-semibold text-sm bg-bg-surface-alt text-text-primary active:bg-bg-surface"
          onclick={() => showResetModal = false}
        >Cancel</button>
        <button
          class="flex-1 py-2.5 rounded-lg font-semibold text-sm bg-danger text-white active:bg-danger-dim"
          onclick={confirmReset}
        >Reset</button>
      </div>
    </div>
  </div>
{/if}
