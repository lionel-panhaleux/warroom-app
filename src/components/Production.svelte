<script lang="ts">
  import { appState, setState } from '../lib/state.svelte'
  import { NATION_IDS, NATIONS, UNITS } from '../lib/data'
  import { initAllOrders, hasOrders, validateAllProduction, applyNationProduction, computeNationSpent, subtractResources, type ResourceBundle } from '../lib/economy'
  import { icon } from '../lib/icons'
  import type { NationId, NationProductionOrders } from '../lib/types'
  import NationSelector from './economy/NationSelector.svelte'
  import UnitPicker from './economy/UnitPicker.svelte'
  import TradePicker from './economy/TradePicker.svelte'
  import ProductionSummary from './economy/ProductionSummary.svelte'

  type Tab = 'dashboard' | 'economy' | 'battle' | 'morale' | 'production'
  let { showToast }: { showToast: (msg: string, tab: Tab) => void } = $props()

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

  // F11: Confirmation modal
  let showConfirmModal = $state(false)

  // F11: Build summary for modal
  interface ProdSummaryUnit { idx: number; qty: number }
  interface ProdSummaryItem { id: NationId; units: ProdSummaryUnit[]; tradeGive: string | null; tradeReceive: string | null; cg: number; bombs: number; spent: ResourceBundle }
  const productionSummary = $derived.by(() => {
    const items: ProdSummaryItem[] = []
    for (const id of NATION_IDS) {
      if (!hasOrders(allOrders[id])) continue
      const o = allOrders[id]
      const s = computeNationSpent(o)
      const units: ProdSummaryUnit[] = []
      for (const [idx, qty] of Object.entries(o.unitOrders)) {
        if (qty > 0) units.push({ idx: Number(idx), qty })
      }
      items.push({ id, units, tradeGive: o.tradeGive, tradeReceive: o.tradeReceive, cg: o.civilianGoods, bombs: o.bombRepair, spent: s })
    }
    return items
  })

  function onProductionDone() {
    const err = validateAllProduction(allOrders, appState.game.nations)
    if (err) return
    showConfirmModal = true
  }

  function confirmProduction() {
    const game = structuredClone($state.snapshot(appState.game))
    for (const id of NATION_IDS) {
      if (hasOrders(allOrders[id])) {
        game.nations[id] = applyNationProduction(game.nations[id], allOrders[id])
      }
    }
    game.turnOrder = null
    game.roundPhase = 'income'
    setState(game)
    allOrders = initAllOrders()
    showConfirmModal = false
    showToast('Production complete \u2014 proceed to Income', 'economy')
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

<!-- F11: Production confirmation modal -->
{#if showConfirmModal}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
    role="dialog" aria-modal="true" tabindex="-1"
    onclick={() => showConfirmModal = false}
    onkeydown={(e) => { if (e.key === 'Escape') showConfirmModal = false }}
  >
    <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
    <div class="bg-bg-surface rounded-xl p-5 mx-4 max-w-sm w-full shadow-xl max-h-[80vh] overflow-y-auto" onclick={(e) => e.stopPropagation()}>
      <h3 class="text-lg font-bold text-accent mb-3">Confirm Production</h3>

      {#if productionSummary.length === 0}
        <p class="text-sm text-text-muted mb-4">No orders to apply.</p>
      {:else}
        <div class="space-y-2 mb-4">
          {#each productionSummary as item}
            <div class="text-xs border-b border-bg-surface-alt pb-2 last:border-0">
              <div class="flex items-center gap-1.5 font-semibold">
                {@html icon('nations', item.id, 'icon-xs')} {NATIONS[item.id].name}
              </div>
              <div class="ml-5 text-text-muted space-y-1 mt-1">
                {#if item.units.length > 0}
                  <div class="flex items-center gap-1.5 flex-wrap">
                    {#each item.units as u}
                      <span class="inline-flex items-center gap-0.5">{u.qty}x {@html icon('units', UNITS[u.idx].name.toLowerCase().replace(' ', '-'), 'icon-xs')}</span>
                    {/each}
                  </div>
                {/if}
                <div class="flex items-center gap-3 flex-wrap">
                  {#if item.tradeGive && item.tradeReceive}
                    <span class="inline-flex items-center gap-1">Trade: {@html icon('resources', item.tradeGive, 'icon-xs')} → {@html icon('resources', item.tradeReceive, 'icon-xs')}</span>
                  {/if}
                  {#if item.cg > 0}<span class="inline-flex items-center gap-1">{@html icon('markers', 'civilian-goods', 'icon-xs')} {item.cg}</span>{/if}
                  {#if item.bombs > 0}<span class="inline-flex items-center gap-1">{@html icon('markers', 'wrench', 'icon-xs')} {item.bombs}</span>{/if}
                  <span class="inline-flex items-center gap-1 text-text-muted/70">Cost: {@html icon('resources', 'oil', 'icon-xs')}{item.spent.oil} {@html icon('resources', 'iron', 'icon-xs')}{item.spent.iron} {@html icon('resources', 'osr', 'icon-xs')}{item.spent.osr}</span>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}

      <div class="flex gap-3">
        <button
          class="flex-1 py-2.5 rounded-lg font-semibold text-sm bg-bg-surface-alt text-text-primary active:bg-bg-surface"
          onclick={() => showConfirmModal = false}
        >Cancel</button>
        <button
          class="flex-1 py-2.5 rounded-lg font-semibold text-sm bg-accent text-bg-primary active:bg-accent-dim"
          onclick={confirmProduction}
        >Confirm</button>
      </div>
    </div>
  </div>
{/if}
