<script lang="ts">
  import { appState, setState } from '../lib/state.svelte'
  import { NATION_IDS } from '../lib/data'
  import { initAllOrders, hasOrders, validateAllProduction, applyNationProduction, computeNationSpent, subtractResources, type ResourceBundle } from '../lib/economy'
  import type { NationId, NationProductionOrders } from '../lib/types'
  import NationSelector from './economy/NationSelector.svelte'
  import UnitPicker from './economy/UnitPicker.svelte'
  import TradePicker from './economy/TradePicker.svelte'
  import ProductionSummary from './economy/ProductionSummary.svelte'

  // Transient production orders for all nations (not persisted)
  let allOrders: Record<NationId, NationProductionOrders> = $state(initAllOrders())

  let selectedNation: NationId = $state('GER')

  let orders = $derived(allOrders[selectedNation])

  let orderIndicators = $derived(
    Object.fromEntries(NATION_IDS.map(id => [id, hasOrders(allOrders[id])])) as Record<NationId, boolean>
  )

  let available = $derived<ResourceBundle>({
    oil: appState.game.nations[selectedNation].oil,
    iron: appState.game.nations[selectedNation].iron,
    osr: appState.game.nations[selectedNation].osr,
  })

  let spent = $derived(computeNationSpent(orders))
  let remaining = $derived(subtractResources(available, spent))

  let allValid = $derived(validateAllProduction(allOrders, appState.game.nations) === null)

  function onProductionDone() {
    const err = validateAllProduction(allOrders, appState.game.nations)
    if (err) return

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

<div class="space-y-4 pb-36">
  <NationSelector bind:selected={selectedNation} indicators={orderIndicators} />

  <section>
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide mb-2">Units</h2>
    <UnitPicker nationId={selectedNation} bind:orders={allOrders[selectedNation].unitOrders} />
  </section>

  <section>
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide mb-2">Trade</h2>
    <TradePicker nationId={selectedNation} bind:tradeGive={allOrders[selectedNation].tradeGive} bind:tradeReceive={allOrders[selectedNation].tradeReceive} />
  </section>

  <ProductionSummary
    {available}
    {spent}
    {remaining}
    bind:civilianGoods={allOrders[selectedNation].civilianGoods}
    bind:civGoodsPay={allOrders[selectedNation].civGoodsPay}
    bind:bombRepair={allOrders[selectedNation].bombRepair}
    nationId={selectedNation}
    onDone={onProductionDone}
    {allValid}
  />
</div>
