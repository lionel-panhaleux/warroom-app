<script lang="ts">
  import { appState, setState } from '../../lib/state.svelte'
  import { NATION_IDS, NATIONS, UNITS } from '../../lib/data'
  import { TERRITORIES, TERRITORY_MAP } from '../../lib/territories'
  import { computeCasualtyPoints, medalCount, isNeutralInvasion, recordNeutralInvasion } from '../../lib/battle'
  import { icon } from '../../lib/icons'
  import type { NationId, TerritoryDef } from '../../lib/types'
  import NationSelector from '../economy/NationSelector.svelte'
  import Counter from '../shared/Counter.svelte'

  // --- U5: Battle history log ---
  interface BattleLogEntry {
    location: string
    nationsInvolved: NationId[]
    totalCP: number
    outcome: string
    newOwner: NationId | null
  }
  let battleLog: BattleLogEntry[] = $state([])
  let showLog = $state(false)
  let currentRound = $state(appState.game.round)

  // Clear log on round change
  $effect(() => {
    if (appState.game.round !== currentRound) {
      battleLog = []
      currentRound = appState.game.round
    }
  })

  // --- Step 1: Location ---
  let locationSearch = $state('')
  let location: string | null = $state(null) // territory code or 'sea'
  let isSeaBattle = $derived(location === 'sea')

  let searchResults = $derived.by(() => {
    const q = locationSearch.trim().toLowerCase()
    if (!q) return []
    return TERRITORIES.filter(t =>
      t.name.toLowerCase().includes(q) || t.code.toLowerCase().includes(q)
    ).slice(0, 8)
  })

  let locationDef = $derived(location && location !== 'sea' ? TERRITORY_MAP[location] : null)
  let locationState = $derived(location && location !== 'sea' ? appState.game.territories[location] : null)

  // --- Step 2: Losses ---
  let lossNation: NationId = $state('GER')
  let losses: Record<NationId, Record<number, number>> = $state(initLosses())

  function initLosses(): Record<NationId, Record<number, number>> {
    const out = {} as Record<NationId, Record<number, number>>
    for (const id of NATION_IDS) {
      out[id] = {}
      for (let i = 0; i < UNITS.length; i++) out[id][i] = 0
    }
    return out
  }

  let nationCPs = $derived.by(() => {
    const out = {} as Record<NationId, number>
    for (const id of NATION_IDS) out[id] = computeCasualtyPoints(losses[id])
    return out
  })

  let totalCP = $derived(Object.values(nationCPs).reduce((s, v) => s + v, 0))
  let nationsWithLosses = $derived(NATION_IDS.filter(id => nationCPs[id] > 0))

  // --- Step 3: Territory Outcome ---
  type Outcome = 'changes-hands' | 'embattled' | 'no-change'
  let outcome: Outcome | null = $state(null)
  let newOwner: NationId | null = $state(null)
  let medalRecipient: NationId | null = $state(null)

  let medalsAwarded = $derived(location && location !== 'sea' && outcome === 'changes-hands' ? medalCount(location) : 0)
  let svStress = $derived(locationDef?.sv ?? 0)
  let neutralInvasion = $derived(
    location !== null && location !== 'sea' && outcome === 'changes-hands' && newOwner
      ? isNeutralInvasion(location, newOwner, appState.game.neutralInvasionHistory)
      : false
  )

  // --- Step 4: Repairs ---
  // U12: Default to first nation with losses, fallback to first allied
  let repairNation: NationId = $state('CHN')
  let repairNationState = $derived(appState.game.nations[repairNation])
  let repairs: Record<NationId, { oil: number; iron: number; osr: number }> = $state(initRepairs())

  // U12: Auto-select repair nation when losses change
  $effect(() => {
    if (nationsWithLosses.length > 0 && !nationsWithLosses.includes(repairNation)) {
      repairNation = nationsWithLosses[0]
    }
  })

  function initRepairs() {
    const out = {} as Record<NationId, { oil: number; iron: number; osr: number }>
    for (const id of NATION_IDS) out[id] = { oil: 0, iron: 0, osr: 0 }
    return out
  }

  let repairTotal = $derived.by(() => {
    let t = 0
    for (const id of NATION_IDS) {
      t += repairs[id].oil + repairs[id].iron + repairs[id].osr
    }
    return t
  })

  // --- Validation ---
  let canApply = $derived.by(() => {
    if (!location) return false
    if (totalCP === 0 && repairTotal === 0) return false
    if (!isSeaBattle && totalCP > 0 && !outcome) return false
    if (outcome === 'changes-hands' && !newOwner) return false
    return true
  })

  // --- Apply ---
  function applyBattle() {
    if (!canApply) return
    const game = structuredClone($state.snapshot(appState.game))

    // Add CP to nations
    for (const id of NATION_IDS) {
      const cp = computeCasualtyPoints(losses[id])
      if (cp > 0) game.nations[id].casualtyPoints += cp
    }

    // Territory outcome
    if (!isSeaBattle && outcome === 'changes-hands' && location && newOwner) {
      const prevOwner = game.territories[location]?.owner
      game.territories[location].owner = newOwner
      game.territories[location].embattled = false

      // Medals
      const recipient = medalRecipient ?? newOwner
      game.nations[recipient].medals += medalsAwarded

      // SV stress to former owner
      if (prevOwner && svStress > 0) {
        game.nations[prevOwner].stress += svStress
      }

      // Record neutral invasion (stress applied in morale phase)
      if (neutralInvasion) {
        recordNeutralInvasion(game, newOwner, location)
      }
    } else if (!isSeaBattle && outcome === 'embattled' && location) {
      game.territories[location].embattled = true
    } else if (!isSeaBattle && outcome === 'no-change' && location) {
      game.territories[location].embattled = false
    }

    // Repairs — deduct resources
    for (const id of NATION_IDS) {
      const r = repairs[id]
      game.nations[id].oil = Math.max(0, game.nations[id].oil - r.oil)
      game.nations[id].iron = Math.max(0, game.nations[id].iron - r.iron)
      game.nations[id].osr = Math.max(0, game.nations[id].osr - r.osr)
    }

    setState(game)

    // U5: Log entry
    const locName = isSeaBattle ? 'Sea Battle' : (locationDef?.name ?? location ?? '?')
    const outcomeLabel = isSeaBattle ? 'Sea' : outcome === 'changes-hands' ? `→ ${newOwner}` : outcome === 'embattled' ? 'Embattled' : 'No Change'
    battleLog = [...battleLog, {
      location: locName,
      nationsInvolved: nationsWithLosses,
      totalCP,
      outcome: outcomeLabel,
      newOwner: outcome === 'changes-hands' ? newOwner : null,
    }]

    resetAll()
  }

  function resetAll() {
    location = null
    locationSearch = ''
    losses = initLosses()
    lossNation = 'GER'
    outcome = null
    newOwner = null
    medalRecipient = null
    repairs = initRepairs()
    repairNation = 'CHN'
  }

  function selectLocation(code: string) {
    location = code
    locationSearch = ''
  }
</script>

<div class="space-y-4">
  <!-- U5: Battle log -->
  {#if battleLog.length > 0}
    <section class="bg-bg-surface rounded-lg p-3">
      <button class="w-full flex items-center justify-between text-xs font-semibold text-accent uppercase tracking-wide" onclick={() => showLog = !showLog}>
        Battles this round ({battleLog.length})
        <span>{showLog ? '\u25B2' : '\u25BC'}</span>
      </button>
      {#if showLog}
        <div class="mt-2 space-y-1">
          {#each battleLog as entry, i}
            <div class="flex items-center justify-between text-xs border-b border-bg-surface-alt/50 py-1 last:border-0">
              <div class="flex items-center gap-1.5">
                <span class="text-text-muted">{i + 1}.</span>
                <span class="font-medium">{entry.location}</span>
                <span class="text-text-muted">({entry.totalCP} CP)</span>
              </div>
              <div class="flex items-center gap-1">
                {#each entry.nationsInvolved as nid}
                  {@html icon('nations', nid, 'icon-xs')}
                {/each}
                <span class="text-text-muted ml-1">{entry.outcome}</span>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </section>
  {/if}

  <!-- Step 1: Location -->
  <section class="bg-bg-surface rounded-lg p-3 space-y-2">
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide">1. Location</h2>

    {#if !location}
      <input
        type="text"
        class="w-full bg-bg-surface-alt rounded-lg px-3 py-2 text-sm text-text-primary placeholder-text-muted/50 outline-none focus:ring-1 focus:ring-accent"
        aria-label="Search battle location"
        placeholder="Search territory..."
        bind:value={locationSearch}
      />
      {#if searchResults.length > 0}
        <div class="space-y-1 max-h-48 overflow-y-auto">
          {#each searchResults as t}
            {@const ts = appState.game.territories[t.code]}
            <button
              class="w-full text-left px-3 py-2 rounded-md text-xs bg-bg-surface-alt/50 hover:bg-accent/10 active:bg-accent/20 flex justify-between items-center"
              onclick={() => selectLocation(t.code)}
            >
              <span>
                <span class="font-mono text-text-muted mr-1">{t.code}</span> {t.name}
                <!-- U10: Show owner and embattled in search results -->
                <span class="text-text-muted ml-1">({ts?.owner ?? 'Neutral'})</span>
                {#if ts?.embattled}<span class="text-danger ml-0.5">!</span>{/if}
              </span>
              <span class="text-text-muted">SV {t.sv}</span>
            </button>
          {/each}
        </div>
      {/if}
      <button
        class="w-full text-left px-3 py-2 rounded-lg text-xs bg-bg-surface-alt/50 text-accent active:bg-accent/20"
        onclick={() => location = 'sea'}
      >Sea Battle (no territory)</button>
    {:else}
      <div class="flex items-center justify-between">
        {#if isSeaBattle}
          <span class="text-sm font-medium">Sea Battle</span>
        {:else if locationDef}
          <div>
            <span class="font-mono text-text-muted text-xs mr-1">{locationDef.code}</span>
            <span class="text-sm font-medium">{locationDef.name}</span>
            <span class="text-xs text-text-muted ml-1">SV {locationDef.sv}</span>
            {#if locationDef.notes?.includes('Capital')}
              <span class="text-xs text-warning ml-1">{@html icon('markers', 'medal', 'icon-xs')} Capital</span>
            {/if}
          </div>
          <div class="text-[10px] text-text-muted text-right">
            {#if locationState}
              Owner: {locationState.owner ?? 'Neutral'}
              {#if locationState.embattled}
                <span class="text-danger ml-1">Embattled</span>
              {/if}
            {/if}
          </div>
        {/if}
        <button class="text-xs text-accent ml-2" onclick={resetAll}>Change</button>
      </div>
      {#if neutralInvasion && outcome === 'changes-hands'}
        <p class="text-[10px] text-warning">Neutral invasion: +1 stress to attacker</p>
      {/if}
    {/if}
  </section>

  {#if location}
    <!-- Step 2: Losses -->
    <section class="bg-bg-surface rounded-lg p-3 space-y-3">
      <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide">2. Record Losses</h2>
      <NationSelector bind:selected={lossNation} />

      <div class="space-y-1.5">
        {#each UNITS as unit, i}
          {#if losses[lossNation][i] !== undefined}
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-1.5 min-w-0">
                {@html icon('units', unit.name.toLowerCase().replace(' ', '-'), 'icon-xs')}
                <span class="text-xs truncate">{unit.name}</span>
                <span class="text-[10px] text-text-muted">{unit.casualtyPoints} CP</span>
              </div>
              <Counter bind:value={losses[lossNation][i]} min={0} max={99} />
            </div>
          {/if}
        {/each}
      </div>

      <!-- CP summary -->
      {#if totalCP > 0}
        <div class="border-t border-bg-surface-alt pt-2 space-y-1">
          {#each nationsWithLosses as id}
            <div class="flex items-center justify-between text-xs">
              <div class="flex items-center gap-1">
                {@html icon('nations', id, 'icon-xs')}
                <span>{id}</span>
              </div>
              <span class="font-bold tabular-nums">{nationCPs[id]} CP</span>
            </div>
          {/each}
          <div class="flex justify-between text-xs font-bold text-accent pt-1">
            <span>Total</span>
            <span>{totalCP} CP</span>
          </div>
        </div>
      {/if}
    </section>

    <!-- Step 3: Territory Outcome (land battles only) -->
    {#if !isSeaBattle}
      <section class="bg-bg-surface rounded-lg p-3 space-y-3">
        <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide">3. Territory Outcome</h2>

        <div class="flex gap-1.5">
          {#each [['changes-hands', 'Changes Hands'], ['embattled', 'Stays Embattled'], ['no-change', 'Attacker Withdrew']] as [val, label]}
            <button
              class="flex-1 text-xs py-2.5 rounded-lg transition-colors
                     {outcome === val ? 'bg-accent text-bg-primary' : 'bg-bg-surface-alt text-text-muted'}"
              onclick={() => outcome = val as Outcome}
            >{label}</button>
          {/each}
        </div>

        {#if outcome === 'changes-hands'}
          <div class="space-y-2">
            <div>
              <span class="text-xs text-text-muted">New Owner</span>
              <div class="flex gap-1.5 mt-1 flex-wrap">
                {#each NATION_IDS as id}
                  {@const isCurrent = locationState?.owner === id}
                  <button
                    class="px-2 py-1 rounded-md text-xs flex items-center gap-1 transition-colors
                           {newOwner === id ? 'bg-accent/20 ring-1 ring-accent' : isCurrent ? 'bg-bg-surface-alt opacity-30' : 'bg-bg-surface-alt'}"
                    disabled={isCurrent}
                    onclick={() => { newOwner = id; if (!medalRecipient) medalRecipient = id }}
                  >
                    {@html icon('nations', id, 'icon-xs')}
                    {id}
                  </button>
                {/each}
              </div>
            </div>

            {#if newOwner && medalsAwarded > 0}
              <div class="flex items-center gap-2 text-xs">
                {@html icon('markers', 'medal', 'icon-xs')}
                <span class="font-medium">+{medalsAwarded} medal{medalsAwarded > 1 ? 's' : ''}</span>
                <span class="text-text-muted">to</span>
              </div>
              <div class="flex gap-1.5 flex-wrap">
                {#each NATION_IDS as id}
                  <button
                    class="px-2 py-1 rounded-md text-xs flex items-center gap-1 transition-colors
                           {medalRecipient === id ? 'bg-accent/20 ring-1 ring-accent' : 'bg-bg-surface-alt'}"
                    onclick={() => medalRecipient = id}
                  >
                    {@html icon('nations', id, 'icon-xs')}
                    {id}
                  </button>
                {/each}
              </div>
            {/if}

            {#if locationState?.owner && svStress > 0}
              <p class="text-[10px] text-danger">
                {locationState.owner} receives +{svStress} stress (SV of {locationDef?.name})
              </p>
            {/if}
          </div>
        {/if}
      </section>
    {/if}

    <!-- Step 4: Repairs -->
    <section class="bg-bg-surface rounded-lg p-3 space-y-3">
      <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide">4. Repairs</h2>
      <p class="text-[10px] text-text-muted">Spend resources to repair damaged units. Port Advantage: naval repairs are free (informational).</p>

      <NationSelector bind:selected={repairNation} />

      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-1.5">
            {@html icon('resources', 'oil', 'icon-xs')}
            <span class="text-xs">Oil</span>
            <span class="text-[10px] text-text-muted">(has {repairNationState.oil})</span>
          </div>
          <Counter bind:value={repairs[repairNation].oil} min={0} max={repairNationState.oil} />
        </div>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-1.5">
            {@html icon('resources', 'iron', 'icon-xs')}
            <span class="text-xs">Iron</span>
            <span class="text-[10px] text-text-muted">(has {repairNationState.iron})</span>
          </div>
          <Counter bind:value={repairs[repairNation].iron} min={0} max={repairNationState.iron} />
        </div>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-1.5">
            {@html icon('resources', 'osr', 'icon-xs')}
            <span class="text-xs">OSR</span>
            <span class="text-[10px] text-text-muted">(has {repairNationState.osr})</span>
          </div>
          <Counter bind:value={repairs[repairNation].osr} min={0} max={repairNationState.osr} />
        </div>
      </div>
    </section>

    <!-- Step 5: Apply -->
    <button
      class="w-full py-3 rounded-lg font-semibold text-sm transition-colors
             {canApply ? 'bg-accent text-bg-primary active:bg-accent-dim' : 'bg-bg-surface-alt text-text-muted'}"
      disabled={!canApply}
      onclick={applyBattle}
    >Apply Battle</button>
  {/if}
</div>
