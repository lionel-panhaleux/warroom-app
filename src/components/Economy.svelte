<script lang="ts">
  import { appState, setState } from '../lib/state.svelte'
  import { NATION_IDS } from '../lib/data'
  import { initAllOrders, hasOrders, validateAllProduction, applyNationProduction, type ResourceBundle } from '../lib/economy'
  import type { NationId, NationProductionOrders } from '../lib/types'
  import EconomyNav from './economy/EconomyNav.svelte'
  import type { EconomyTab } from './economy/EconomyNav.svelte'
  import RoundStart from './economy/RoundStart.svelte'
  import Production from './economy/Production.svelte'
  import Territories from './economy/Territories.svelte'

  let economyTab: EconomyTab = $state('round')

  // Transient production orders for all nations (not persisted)
  let allOrders: Record<NationId, NationProductionOrders> = $state(initAllOrders())

  // Auto-switch tab when phase changes
  let prevPhase = $state(appState.game.roundPhase)
  $effect(() => {
    const phase = appState.game.roundPhase
    if (phase !== prevPhase) {
      if (phase === 'income' || phase === 'bidding') economyTab = 'round'
      else if (phase === 'production') economyTab = 'production'
      prevPhase = phase
    }
  })

  // Order indicators for NationSelector
  let orderIndicators = $derived(
    Object.fromEntries(NATION_IDS.map(id => [id, hasOrders(allOrders[id])])) as Record<NationId, boolean>
  )

  function onProductionDone() {
    const err = validateAllProduction(allOrders, appState.game.nations)
    if (err) return // should be blocked by UI, but guard

    const game = structuredClone($state.snapshot(appState.game))
    for (const id of NATION_IDS) {
      if (hasOrders(allOrders[id])) {
        game.nations[id] = applyNationProduction(game.nations[id], allOrders[id])
      }
    }
    game.roundPhase = 'income'
    setState(game)
    allOrders = initAllOrders()
  }
</script>

<div>
  <EconomyNav bind:activeTab={economyTab} roundPhase={appState.game.roundPhase} />

  {#if economyTab === 'round'}
    <RoundStart />
  {:else if economyTab === 'production'}
    <Production bind:allOrders {orderIndicators} onDone={onProductionDone} />
  {:else if economyTab === 'territories'}
    <Territories />
  {/if}
</div>
