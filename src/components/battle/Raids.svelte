<script lang="ts">
  import { untrack } from 'svelte'
  import { appState, setState, persist } from '../../lib/state.svelte'
  import { NATION_IDS, NATIONS } from '../../lib/data'
  import { reverseRaid } from '../../lib/battle'
  import { icon } from '../../lib/icons'
  import type { NationId, GameState, RaidLogEntry } from '../../lib/types'
  import NationSelector from '../economy/NationSelector.svelte'
  import Counter from '../shared/Counter.svelte'

  // --- Raid log ---
  let showLog = $state(false)

  // --- Edit mode ---
  let editIndex: number | null = $state(null)
  let editEntry: RaidLogEntry | null = $state(null)
  let preEditGame: GameState | null = $state(null)
  let populatingForm = $state(false)
  let editMode = $derived(editIndex !== null)

  // --- Form ---
  let selected: NationId = $state('GER')
  let raidType: 'strategic' | 'convoy' = $state('convoy')
  let oilLoss = $state(0)
  let ironLoss = $state(0)
  let osrLoss = $state(0)

  let ns = $derived.by(() => {
    const base = appState.game.nations[selected]
    if (!editEntry || editEntry.nationId !== selected) return base
    // In edit mode, add back old entry's deductions so Counter max is correct
    return { ...base, oil: base.oil + editEntry.oil, iron: base.iron + editEntry.iron, osr: base.osr + editEntry.osr }
  })
  let totalLoss = $derived(oilLoss + ironLoss + osrLoss)
  let hasChanges = $derived(totalLoss > 0)
  let convoyCP = $derived(raidType === 'convoy' ? totalLoss * 6 : 0)

  function buildRaidGame(base: GameState): GameState {
    const game = structuredClone(base)
    game.nations[selected].oil = Math.max(0, game.nations[selected].oil - oilLoss)
    game.nations[selected].iron = Math.max(0, game.nations[selected].iron - ironLoss)
    game.nations[selected].osr = Math.max(0, game.nations[selected].osr - osrLoss)
    // Convoy raids: 6 CP per resource lost
    if (raidType === 'convoy' && totalLoss > 0) {
      game.nations[selected].casualtyPoints += convoyCP
    }
    game.raidLog = [...game.raidLog, {
      nationId: selected,
      raidType,
      oil: oilLoss,
      iron: ironLoss,
      osr: osrLoss,
      convoyCP,
    }]
    return game
  }

  function applyRaid() {
    if (!hasChanges) return
    setState(buildRaidGame($state.snapshot(appState.game) as GameState))
    resetForm()
  }

  // --- Edit mode: reverse-old, apply-new on each form change ---
  $effect(() => {
    if (editIndex === null || populatingForm || !hasChanges) return
    // Track form fields
    const _ = [selected, raidType, oilLoss, ironLoss, osrLoss]

    untrack(() => {
      if (!editEntry || editIndex === null) return
      const game = structuredClone($state.snapshot(appState.game)) as GameState
      // Reverse the old entry
      reverseRaid(game, editEntry!)
      game.raidLog.splice(editIndex!, 1)
      // Apply new from current form
      const result = buildRaidGame(game)
      // Move new entry back to original position
      const newEntry = result.raidLog.pop()!
      result.raidLog.splice(editIndex!, 0, newEntry)
      // Update editEntry for next cycle
      editEntry = structuredClone(newEntry) as RaidLogEntry
      appState.game = result
      persist()
    })
  })

  function editRaid(index: number) {
    const entry = appState.game.raidLog[index]
    if (!entry) return

    // Store pre-edit game for undo
    preEditGame = structuredClone($state.snapshot(appState.game)) as GameState
    editEntry = structuredClone($state.snapshot(entry)) as RaidLogEntry
    editIndex = index

    // Populate form from snapshot (reactive proxies need $state.snapshot)
    const snap = $state.snapshot(entry)
    populatingForm = true
    selected = snap.nationId
    raidType = snap.raidType
    oilLoss = snap.oil
    ironLoss = snap.iron
    osrLoss = snap.osr
    queueMicrotask(() => populatingForm = false)
  }

  function finishEdit() {
    if (preEditGame) {
      appState.undoStack = [preEditGame, ...appState.undoStack].slice(0, 20)
      persist()
    }
    editIndex = null
    editEntry = null
    preEditGame = null
    populatingForm = false
    resetForm()
  }

  function deleteRaid(index: number) {
    const entry = appState.game.raidLog[index]
    if (!entry) return
    const game = structuredClone($state.snapshot(appState.game)) as GameState
    reverseRaid(game, entry)
    game.raidLog.splice(index, 1)
    setState(game)
    if (editIndex === index) {
      editIndex = null
      editEntry = null
      preEditGame = null
      resetForm()
    }
  }

  function resetForm() {
    oilLoss = 0
    ironLoss = 0
    osrLoss = 0
  }
</script>

<div class="space-y-4">
  <!-- Raid log -->
  {#if appState.game.raidLog.length > 0}
    <section class="bg-bg-surface rounded-lg p-3">
      <button class="w-full flex items-center justify-between text-xs font-semibold text-accent uppercase tracking-wide" onclick={() => showLog = !showLog}>
        Raids this round ({appState.game.raidLog.length})
        <span>{showLog ? '\u25B2' : '\u25BC'}</span>
      </button>
      {#if showLog}
        <div class="mt-2 space-y-1">
          {#each appState.game.raidLog as entry, i}
            <div class="flex items-center justify-between text-xs border-b border-bg-surface-alt/50 py-1 last:border-0">
              <div class="flex items-center gap-1.5">
                <span class="text-text-muted">{i + 1}.</span>
                {@html icon('nations', entry.nationId, 'icon-xs')}
                <span class="font-medium">{entry.raidType === 'convoy' ? 'Convoy' : 'Bombing'}</span>
              </div>
              <div class="flex items-center gap-1.5">
                {#if entry.oil > 0}<span style="color:var(--color-res-oil)">{entry.oil}</span>{/if}
                {#if entry.iron > 0}<span style="color:var(--color-res-iron)">{entry.iron}</span>{/if}
                {#if entry.osr > 0}<span style="color:var(--color-res-osr)">{entry.osr}</span>{/if}
                {#if entry.convoyCP > 0}<span class="text-text-muted">({entry.convoyCP} CP)</span>{/if}
                <button class="p-2.5 rounded-md text-text-muted hover:text-accent active:bg-accent/10 transition-colors" onclick={() => editRaid(i)}>
                  {@html icon('ui', 'edit', 'icon-xs')}
                </button>
                <button class="p-2.5 rounded-md text-text-muted hover:text-danger active:bg-danger/10 transition-colors" onclick={() => deleteRaid(i)}>
                  {@html icon('ui', 'trash', 'icon-xs')}
                </button>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </section>
  {/if}

  <NationSelector bind:selected />

  <!-- Raid type -->
  <section class="bg-bg-surface rounded-lg p-3 space-y-3">
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide">
      {editMode ? 'Editing Raid' : 'Raid Type'}
    </h2>
    <div class="flex gap-1.5">
      {#each [['convoy', 'Convoy Raid'], ['strategic', 'Strategic Bombing']] as [val, label]}
        <button
          class="flex-1 text-xs py-2.5 rounded-lg transition-colors
                 {raidType === val ? 'bg-accent text-bg-primary' : 'bg-bg-surface-alt text-text-muted'}"
          onclick={() => raidType = val as 'strategic' | 'convoy'}
        >{label}</button>
      {/each}
    </div>
    {#if raidType === 'convoy'}
      <p class="text-[10px] text-text-muted">Each resource lost = 6 Casualty Points (Convoy Casualty Tokens)</p>
    {:else}
      <p class="text-[10px] text-text-muted">Depletes resources and destroys infrastructure. No casualty points.</p>
    {/if}
  </section>

  <!-- Resource losses -->
  <section class="bg-bg-surface rounded-lg p-3 space-y-3">
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide">
      Resource Losses — {NATIONS[selected].name}
    </h2>

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

    {#if convoyCP > 0}
      <div class="border-t border-bg-surface-alt pt-2 text-xs text-danger font-medium">
        +{convoyCP} Casualty Points from convoy losses
      </div>
    {/if}
  </section>

  <!-- Apply / Done -->
  {#if editMode}
    <button
      class="w-full py-3 rounded-lg font-semibold text-sm bg-accent text-bg-primary active:bg-accent-dim"
      onclick={finishEdit}
    >Done Editing</button>
  {:else}
    <button
      class="w-full py-3 rounded-lg font-semibold text-sm transition-colors
             {hasChanges ? 'bg-accent text-bg-primary active:bg-accent-dim' : 'bg-bg-surface-alt text-text-muted'}"
      disabled={!hasChanges}
      onclick={applyRaid}
    >Apply Raid</button>
  {/if}
</div>
