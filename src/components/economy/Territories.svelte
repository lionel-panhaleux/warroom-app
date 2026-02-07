<script lang="ts">
  import { appState, setState } from '../../lib/state.svelte'
  import { NATIONS, NATION_IDS } from '../../lib/data'
  import { TERRITORIES, TERRITORY_MAP } from '../../lib/territories'
  import { icon } from '../../lib/icons'
  import type { NationId, TerritoryOwner } from '../../lib/types'

  let search = $state('')
  let filterOwner: TerritoryOwner | 'all' = $state('all')
  let expandedCode: string | null = $state(null)

  function matchesSearch(t: typeof TERRITORIES[0]): boolean {
    if (!search) return true
    const q = search.toLowerCase()
    return t.code.toLowerCase().includes(q) || t.name.toLowerCase().includes(q)
  }

  let filtered = $derived(
    TERRITORIES.filter(t => {
      if (!matchesSearch(t)) return false
      if (filterOwner === 'all') return true
      const owner = appState.game.territories[t.code]?.owner ?? null
      return owner === filterOwner
    })
  )

  // Lost territories: originally owned by filterOwner but now owned by someone else
  let lost = $derived.by(() => {
    if (filterOwner === 'all' || filterOwner === null) return []
    return TERRITORIES.filter(t => {
      if (!matchesSearch(t)) return false
      if (t.startingOwner !== filterOwner) return false
      const owner = appState.game.territories[t.code]?.owner ?? null
      return owner !== filterOwner
    })
  })

  function hasChangedHands(t: typeof TERRITORIES[0]): boolean {
    const owner = appState.game.territories[t.code]?.owner ?? null
    return owner !== t.startingOwner
  }

  function setOwner(code: string, newOwner: TerritoryOwner) {
    const game = structuredClone($state.snapshot(appState.game))
    game.territories[code] = { ...game.territories[code], owner: newOwner }
    setState(game)
    expandedCode = null
  }

  function toggleEmbattled(code: string) {
    const game = structuredClone($state.snapshot(appState.game))
    game.territories[code] = { ...game.territories[code], embattled: !game.territories[code].embattled }
    setState(game)
  }

  function ownerLabel(owner: TerritoryOwner): string {
    return owner ? NATIONS[owner].name : 'Neutral'
  }
</script>

{#snippet territoryRow(t: typeof TERRITORIES[0], dimmed: boolean)}
  {@const state = appState.game.territories[t.code]}
  {@const isExpanded = expandedCode === t.code}
  {@const changed = hasChangedHands(t)}
  <div class="bg-bg-surface rounded-lg overflow-hidden" class:opacity-50={dimmed}>
    <!-- Row -->
    <button
      class="w-full flex items-center gap-2 px-3 py-2 text-left"
      onclick={() => expandedCode = isExpanded ? null : t.code}
    >
      <span class="text-[10px] text-text-muted w-6 font-mono">{t.code}</span>
      <!-- Flag cell: ghost flag for changed territories -->
      {#if changed && t.startingOwner}
        <span class="relative inline-flex" style="width:1.4em;height:1em">
          <span class="absolute left-0 top-0 opacity-30">{@html icon('nations', t.startingOwner, 'icon-xs')}</span>
          <span class="absolute right-0 top-0">{#if state?.owner}{@html icon('nations', state.owner, 'icon-xs')}{/if}</span>
        </span>
      {:else if state?.owner}
        {@html icon('nations', state.owner, 'icon-xs')}
      {:else}
        <span class="inline-flex w-[1em] h-[1em]"></span>
      {/if}
      <span class="flex-1 text-xs font-medium truncate">{t.name}</span>
      {#if state?.embattled}
        {@html icon('markers', 'embattled', 'icon-xs')}
      {/if}
      {#if t.oil}<span class="text-[10px] tabular-nums" style="color:var(--color-res-oil)">{t.oil}</span>{/if}
      {#if t.iron}<span class="text-[10px] tabular-nums" style="color:var(--color-res-iron)">{t.iron}</span>{/if}
      {#if t.osr}<span class="text-[10px] tabular-nums" style="color:var(--color-res-osr)">{t.osr}</span>{/if}
      {#if t.sv}<span class="text-[10px] text-text-muted">SV{t.sv}</span>{/if}
    </button>

    <!-- Expanded panel -->
    {#if isExpanded}
      <div class="px-3 pb-3 border-t border-bg-surface-alt space-y-2">
        <div class="pt-2">
          <span class="text-[10px] text-text-muted">Owner: {ownerLabel(state?.owner ?? null)}</span>
          {#if t.industry}<span class="text-[10px] text-accent ml-2">Ind: {t.industry}</span>{/if}
          {#if t.notes}<span class="text-[10px] text-text-muted ml-2">{t.notes}</span>{/if}
        </div>
        {#if changed}
          <div class="flex items-center gap-1">
            <span class="text-[10px] text-text-muted">Originally:</span>
            {#if t.startingOwner}
              {@html icon('nations', t.startingOwner, 'icon-xs')}
              <span class="text-[10px] text-text-muted">{ownerLabel(t.startingOwner)}</span>
            {:else}
              <span class="text-[10px] text-text-muted">Neutral</span>
            {/if}
          </div>
        {/if}
        <!-- Change owner -->
        <div class="flex gap-1 flex-wrap">
          {#each NATION_IDS as id}
            <button
              class="text-[10px] px-2 py-1 rounded-md {state?.owner === id ? 'bg-accent text-bg-primary' : 'bg-bg-surface-alt text-text-muted'}"
              onclick={() => setOwner(t.code, id)}
            >{id}</button>
          {/each}
          <button
            class="text-[10px] px-2 py-1 rounded-md {state?.owner === null ? 'bg-accent text-bg-primary' : 'bg-bg-surface-alt text-text-muted'}"
            onclick={() => setOwner(t.code, null)}
          >Neutral</button>
        </div>
        <!-- Embattled toggle -->
        <label class="flex items-center gap-2 text-xs">
          <input type="checkbox" checked={state?.embattled ?? false} onchange={() => toggleEmbattled(t.code)} />
          Embattled
          {@html icon('markers', 'embattled', 'icon-xs')}
        </label>
      </div>
    {/if}
  </div>
{/snippet}

<div class="space-y-3">
  <!-- Search -->
  <input
    type="text"
    class="w-full bg-bg-surface rounded-lg px-3 py-2 text-sm text-text-primary placeholder-text-muted outline-none focus:ring-1 focus:ring-accent"
    placeholder="Search territories..."
    bind:value={search}
  />

  <!-- Owner filter -->
  <div class="flex gap-1 flex-wrap">
    <button
      class="text-[10px] px-2 py-1 rounded-md {filterOwner === 'all' ? 'bg-accent text-bg-primary' : 'bg-bg-surface text-text-muted'}"
      onclick={() => filterOwner = 'all'}
    >All</button>
    {#each NATION_IDS as id}
      <button
        class="text-[10px] px-2 py-1 rounded-md {filterOwner === id ? 'bg-accent text-bg-primary' : 'bg-bg-surface text-text-muted'}"
        onclick={() => filterOwner = id}
      >{id}</button>
    {/each}
    <button
      class="text-[10px] px-2 py-1 rounded-md {filterOwner === null ? 'bg-accent text-bg-primary' : 'bg-bg-surface text-text-muted'}"
      onclick={() => filterOwner = null}
    >Neutral</button>
  </div>

  <!-- Count -->
  <p class="text-[10px] text-text-muted">
    {filtered.length} territories{#if lost.length > 0} + {lost.length} lost{/if}
  </p>

  <!-- Territory list -->
  <div class="space-y-1">
    {#each filtered as t (t.code)}
      {@render territoryRow(t, false)}
    {/each}

    <!-- Lost territories section -->
    {#if lost.length > 0}
      <div class="flex items-center gap-2 pt-2 pb-1">
        <div class="flex-1 h-px bg-bg-surface-alt"></div>
        <span class="text-[10px] text-text-muted">Lost</span>
        <div class="flex-1 h-px bg-bg-surface-alt"></div>
      </div>
      {#each lost as t (t.code)}
        {@render territoryRow(t, true)}
      {/each}
    {/if}
  </div>
</div>
