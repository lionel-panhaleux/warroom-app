<script lang="ts">
  import { appState, setState } from '../../lib/state.svelte'
  import { NATION_IDS, NATIONS } from '../../lib/data'
  import { totalIncome, computeTurnOrder, validateBids, type OilBid } from '../../lib/economy'
  import { icon } from '../../lib/icons'
  import type { NationId } from '../../lib/types'
  import Counter from '../shared/Counter.svelte'

  let { showToast }: { showToast: (msg: string) => void } = $props()

  let phase = $derived(appState.game.roundPhase)

  let incomes = $derived(
    NATION_IDS.map(id => ({ id, income: totalIncome(id, appState.game) }))
  )

  // Oil bids (transient — reset each round)
  let bids: Record<NationId, number> = $state(
    Object.fromEntries(NATION_IDS.map(id => [id, 0])) as Record<NationId, number>
  )
  let bidError: string | null = $state(null)

  // U8: Round label
  let roundLabel = $derived(appState.game.round === 0 ? 'Setup' : `Round ${appState.game.round}`)

  function collectIncome() {
    const game = structuredClone($state.snapshot(appState.game))
    const isRedZone = (id: NationId) => game.nations[id].zone === 'Red' || game.nations[id].zone === 'Gray'
    for (const id of NATION_IDS) {
      game.nations[id].casualtyPoints = 0
      if (isRedZone(id)) continue
      const inc = totalIncome(id, game)
      game.nations[id].oil += inc.oil
      game.nations[id].iron += inc.iron
      game.nations[id].osr += inc.osr
    }
    game.neutralInvasionsThisRound = {}
    game.turnOrder = null
    game.battleLog = []
    game.round += 1
    game.roundPhase = 'bidding'
    setState(game)
    showToast('Income collected — proceed to Oil Bidding')
  }

  function confirmBids() {
    const bidList: OilBid[] = NATION_IDS.map(id => ({ nationId: id, amount: bids[id] }))
    const err = validateBids(bidList, appState.game.nations)
    if (err) { bidError = err; return }
    bidError = null

    const game = structuredClone($state.snapshot(appState.game))
    for (const b of bidList) {
      game.nations[b.nationId].oil -= b.amount
    }
    game.turnOrder = computeTurnOrder(bidList)
    game.roundPhase = 'morale'
    setState(game)
    bids = Object.fromEntries(NATION_IDS.map(id => [id, 0])) as Record<NationId, number>
    showToast('Bids confirmed — check choice order below')
  }

</script>

<div class="space-y-4">
  <!-- Income Preview -->
  <section>
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide mb-2">
      Income Preview — {roundLabel}
    </h2>
    <div class="bg-bg-surface rounded-lg overflow-hidden">
      <table class="w-full text-xs">
        <thead>
          <tr class="text-text-muted border-b border-bg-surface-alt">
            <th class="text-left py-1.5 px-2">Nation</th>
            <th class="text-right py-1.5 px-1">{@html icon('resources', 'oil', 'icon-xs')}</th>
            <th class="text-right py-1.5 px-1">{@html icon('resources', 'iron', 'icon-xs')}</th>
            <th class="text-right py-1.5 px-1">{@html icon('resources', 'osr', 'icon-xs')}</th>
          </tr>
        </thead>
        <tbody>
          {#each incomes as { id, income }}
            {@const ns = appState.game.nations[id]}
            {@const redZone = ns.zone === 'Red' || ns.zone === 'Gray'}
            <tr class="border-b border-bg-surface-alt/50 {redZone ? 'opacity-40' : ''}">
              <td class="py-1.5 px-2 flex items-center gap-1.5">
                {@html icon('nations', id, 'icon-xs')}
                <span class="font-medium">{NATIONS[id].name}</span>
                {#if redZone}<span class="text-danger text-[10px] ml-1">NO INCOME</span>{/if}
              </td>
              <td class="text-right px-1 tabular-nums">{redZone ? 0 : income.oil}</td>
              <td class="text-right px-1 tabular-nums">{redZone ? 0 : income.iron}</td>
              <td class="text-right px-1 tabular-nums">{redZone ? 0 : income.osr}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    <button
      class="w-full mt-2 py-3 rounded-lg font-semibold text-sm transition-colors
             {phase !== 'income' ? 'bg-bg-surface-alt text-text-muted' : 'bg-accent text-bg-primary active:bg-accent-dim'}"
      disabled={phase !== 'income'}
      onclick={collectIncome}
    >{phase === 'income' ? 'Collect Income' : 'Income Collected \u2713'}</button>
  </section>

  <!-- Oil Bidding -->
  <section>
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide mb-2">Oil Bidding</h2>
    <!-- U4: Clearer disabled state with label -->
    {#if phase !== 'bidding' && phase !== 'income'}
      <div class="text-center py-3 text-sm text-accent/70 font-medium">Bids Confirmed \u2713</div>
    {/if}
    <div class="space-y-2 {phase !== 'bidding' ? 'opacity-30 pointer-events-none' : ''}">
      {#each NATION_IDS as id}
        {@const ns = appState.game.nations[id]}
        <div class="flex items-center justify-between bg-bg-surface rounded-lg px-3 py-2">
          <div class="flex items-center gap-1.5 min-w-0">
            {@html icon('nations', id, 'icon-xs')}
            <span class="text-xs font-medium truncate">{NATIONS[id].name}</span>
            <span class="text-[10px] text-text-muted ml-1">({ns.oil} {@html icon('resources', 'oil', 'icon-xs')})</span>
          </div>
          {#if id === 'CHN'}
            <span class="text-xs text-text-muted">0 (no Oil)</span>
          {:else}
            <Counter bind:value={bids[id]} min={0} max={ns.oil} />
          {/if}
        </div>
      {/each}
    </div>

    {#if bidError}
      <p class="text-danger text-xs mt-2">{bidError}</p>
    {/if}

    {#if (phase === 'morale' || phase === 'production') && appState.game.turnOrder}
      <div class="mt-3 bg-bg-surface rounded-lg p-3">
        <h3 class="text-xs font-semibold text-accent mb-1.5">Choice Order</h3>
        <ol class="space-y-1">
          {#each appState.game.turnOrder as entry, i}
            <li class="flex items-center gap-2 text-xs">
              <span class="text-text-muted w-4">{i + 1}.</span>
              {@html icon('nations', entry.nationId, 'icon-xs')}
              <span class="font-medium">{NATIONS[entry.nationId].name}</span>
              <span class="text-text-muted">({entry.amount} Oil)</span>
              {#if entry.tied}<span class="text-warning text-[10px]">TIE</span>{/if}
            </li>
          {/each}
        </ol>
        <p class="text-[10px] text-text-muted mt-2">Ties shuffled randomly.</p>
      </div>
    {:else if phase === 'bidding'}
      <button
        class="w-full mt-2 py-3 rounded-lg font-semibold text-sm bg-accent text-bg-primary active:bg-accent-dim"
        onclick={confirmBids}
      >Confirm Bids</button>
    {/if}
  </section>
</div>
