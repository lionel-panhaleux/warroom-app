<script lang="ts">
  import { UNITS } from '../../lib/data'
  import { availableUnits, unitOrderCost, type UnitOrder } from '../../lib/economy'
  import { icon } from '../../lib/icons'
  import type { NationId } from '../../lib/types'
  import Counter from '../shared/Counter.svelte'

  let { nationId, orders = $bindable() }: {
    nationId: NationId
    orders: Record<number, number>
  } = $props()

  const unitIconNames = ['infantry', 'artillery', 'armor', 'fighter', 'bomber', 'submarine', 'cruiser', 'carrier', 'battleship']

  let allowed = $derived(availableUnits(nationId))

  let orderList = $derived<UnitOrder[]>(
    Object.entries(orders)
      .filter(([, qty]) => qty > 0)
      .map(([i, qty]) => ({ unitIndex: Number(i), qty }))
  )

  let cost = $derived(unitOrderCost(orderList))
</script>

<div class="space-y-1.5">
  {#each allowed as idx}
    {@const u = UNITS[idx]}
    <div class="flex items-center gap-2 bg-bg-surface rounded-lg px-3 py-1.5">
      {@html icon('units', unitIconNames[idx], 'icon-sm')}
      <div class="flex-1 min-w-0">
        <div class="text-xs font-medium">{u.name}</div>
        <div class="flex gap-1.5 text-[10px] text-text-muted">
          {#if u.cost[0]}<span style="color:var(--color-res-oil)">{u.cost[0]}</span>{/if}
          {#if u.cost[1]}<span style="color:var(--color-res-iron)">{u.cost[1]}</span>{/if}
          {#if u.cost[2]}<span style="color:var(--color-res-osr)">{u.cost[2]}</span>{/if}
        </div>
      </div>
      <Counter bind:value={orders[idx]} min={0} max={20} />
    </div>
  {/each}

  {#if orderList.length > 0}
    <div class="text-xs text-text-muted pt-1 flex gap-3">
      <span>Cost:</span>
      {#if cost.oil}<span style="color:var(--color-res-oil)">{cost.oil} Oil</span>{/if}
      {#if cost.iron}<span style="color:var(--color-res-iron)">{cost.iron} Iron</span>{/if}
      {#if cost.osr}<span style="color:var(--color-res-osr)">{cost.osr} OSR</span>{/if}
    </div>
  {/if}
</div>
