<script lang="ts">
  import { appState } from '../../lib/state.svelte'
  import { computeNationSpent, subtractResources, validateAllProduction, type ResourceBundle } from '../../lib/economy'
  import type { NationId, NationProductionOrders } from '../../lib/types'
  import NationSelector from './NationSelector.svelte'
  import UnitPicker from './UnitPicker.svelte'
  import TradePicker from './TradePicker.svelte'
  import ProductionSummary from './ProductionSummary.svelte'

  let { allOrders = $bindable(), orderIndicators, onDone }: {
    allOrders: Record<NationId, NationProductionOrders>
    orderIndicators: Record<NationId, boolean>
    onDone: () => void
  } = $props()

  let selectedNation: NationId = $state('GER')

  let orders = $derived(allOrders[selectedNation])

  // Available resources for selected nation
  let available = $derived<ResourceBundle>({
    oil: appState.game.nations[selectedNation].oil,
    iron: appState.game.nations[selectedNation].iron,
    osr: appState.game.nations[selectedNation].osr,
  })

  let spent = $derived(computeNationSpent(orders))
  let remaining = $derived(subtractResources(available, spent))

  // Validate all nations for the Done button
  let allValid = $derived(validateAllProduction(allOrders, appState.game.nations) === null)
</script>

<div class="space-y-4 pb-36">
  <!-- Nation selector -->
  <NationSelector bind:selected={selectedNation} indicators={orderIndicators} />

  <!-- Unit orders -->
  <section>
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide mb-2">Units</h2>
    <UnitPicker nationId={selectedNation} bind:orders={allOrders[selectedNation].unitOrders} />
  </section>

  <!-- Trade -->
  <section>
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide mb-2">Trade</h2>
    <TradePicker nationId={selectedNation} bind:tradeGive={allOrders[selectedNation].tradeGive} bind:tradeReceive={allOrders[selectedNation].tradeReceive} />
  </section>

  <!-- Summary bar -->
  <ProductionSummary
    {available}
    {spent}
    {remaining}
    bind:civilianGoods={allOrders[selectedNation].civilianGoods}
    bind:civGoodsPay={allOrders[selectedNation].civGoodsPay}
    bind:bombRepair={allOrders[selectedNation].bombRepair}
    bind:unrestPay={allOrders[selectedNation].unrestPay}
    nationId={selectedNation}
    {onDone}
    {allValid}
  />
</div>
