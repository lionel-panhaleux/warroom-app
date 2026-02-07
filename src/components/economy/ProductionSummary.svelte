<script lang="ts">
  import { appState } from '../../lib/state.svelte'
  import { icon, uiIcons } from '../../lib/icons'
  import { canAfford, totalResources, type ResourceBundle } from '../../lib/economy'
  import type { NationId } from '../../lib/types'

  let { available, spent, remaining, civilianGoods = $bindable(0), civGoodsPay = $bindable({ oil: 0, iron: 0, osr: 0 }), bombRepair = $bindable(0), unrestPay = $bindable({ oil: 0, iron: 0, osr: 0 }), onDone, allValid, nationId }: {
    available: ResourceBundle
    spent: ResourceBundle
    remaining: ResourceBundle
    civilianGoods: number
    civGoodsPay: ResourceBundle
    bombRepair: number
    unrestPay: ResourceBundle
    onDone: () => void
    allValid: boolean
    nationId: NationId
  } = $props()

  let affordable = $derived(canAfford(remaining))
  let isChinaNoBomb = $derived(nationId === 'CHN')
  let hasUnrest = $derived(appState.game.nations[nationId]?.zone !== 'White')
  let civTotal = $derived(civilianGoods * 5)
  let civAssigned = $derived(civGoodsPay.oil + civGoodsPay.iron + civGoodsPay.osr)
  let unrestAssigned = $derived(unrestPay.oil + unrestPay.iron + unrestPay.osr)
  let currentNationOk = $derived(affordable && civAssigned === civTotal && (!hasUnrest || unrestAssigned === 0 || unrestAssigned === 3))

  function civInc(r: keyof ResourceBundle) {
    if (civAssigned >= civTotal) return
    civGoodsPay = { ...civGoodsPay, [r]: civGoodsPay[r] + 1 }
  }
  function civDec(r: keyof ResourceBundle) {
    if (civGoodsPay[r] <= 0) return
    civGoodsPay = { ...civGoodsPay, [r]: civGoodsPay[r] - 1 }
  }
  function civGoodsInc() {
    civilianGoods++
    civGoodsPay = { ...civGoodsPay, osr: civGoodsPay.osr + 5 }
  }
  function civGoodsDec() {
    if (civilianGoods <= 0) return
    civilianGoods--
    const newTotal = civilianGoods * 5
    let { oil, iron, osr } = civGoodsPay
    const excess = oil + iron + osr - newTotal
    if (excess > 0) {
      let rem = excess
      const cut = Math.min(osr, rem); osr -= cut; rem -= cut
      const cut2 = Math.min(iron, rem); iron -= cut2; rem -= cut2
      oil -= rem
    }
    civGoodsPay = { oil, iron, osr }
  }

  function unrestInc(r: keyof ResourceBundle) {
    if (unrestAssigned >= 3) return
    unrestPay = { ...unrestPay, [r]: unrestPay[r] + 1 }
  }
  function unrestDec(r: keyof ResourceBundle) {
    if (unrestPay[r] <= 0) return
    unrestPay = { ...unrestPay, [r]: unrestPay[r] - 1 }
  }
  function enableUnrest() {
    unrestPay = { oil: 0, iron: 0, osr: 3 }
  }
  function clearUnrest() {
    unrestPay = { oil: 0, iron: 0, osr: 0 }
  }
</script>

<div class="fixed bottom-[4.5rem] left-0 right-0 z-40 bg-bg-surface border-t border-bg-surface-alt"
     style="padding-bottom: 0;">
  <div class="max-w-[480px] mx-auto px-3 py-2 space-y-1.5">
    <!-- Resource summary -->
    <div class="flex justify-between text-[10px]">
      <div class="flex gap-2">
        <span class="text-text-muted">Avail:</span>
        <span style="color:var(--color-res-oil)">{available.oil}</span>
        <span style="color:var(--color-res-iron)">{available.iron}</span>
        <span style="color:var(--color-res-osr)">{available.osr}</span>
      </div>
      <div class="flex gap-2">
        <span class="text-text-muted">Left:</span>
        <span class="{remaining.oil < 0 ? 'text-red-400' : ''}" style="color:{remaining.oil >= 0 ? 'var(--color-res-oil)' : ''}">{remaining.oil}</span>
        <span class="{remaining.iron < 0 ? 'text-red-400' : ''}" style="color:{remaining.iron >= 0 ? 'var(--color-res-iron)' : ''}">{remaining.iron}</span>
        <span class="{remaining.osr < 0 ? 'text-red-400' : ''}" style="color:{remaining.osr >= 0 ? 'var(--color-res-osr)' : ''}">{remaining.osr}</span>
      </div>
    </div>

    <!-- Civ goods + bomb repair -->
    <div class="flex gap-3 text-xs items-center flex-wrap">
      <span class="flex items-center gap-1">
        {@html icon('markers', 'civilian-goods', 'icon-xs')} Civ.
        <button class="w-6 h-6 flex items-center justify-center rounded bg-bg-surface-alt disabled:opacity-30"
          disabled={civilianGoods <= 0}
          onclick={civGoodsDec}>{@html uiIcons.minus}</button>
        <span class="w-4 text-center tabular-nums font-bold">{civilianGoods}</span>
        <button class="w-6 h-6 flex items-center justify-center rounded bg-bg-surface-alt disabled:opacity-30"
          disabled={totalResources(remaining) < 5}
          onclick={civGoodsInc}>{@html uiIcons.plus}</button>
      </span>
      {#if !isChinaNoBomb}
        <span class="flex items-center gap-1">
          {@html icon('markers', 'wrench', 'icon-xs')} Bomb
          <button class="w-6 h-6 flex items-center justify-center rounded bg-bg-surface-alt disabled:opacity-30"
            disabled={bombRepair <= 0}
            onclick={() => bombRepair--}>{@html uiIcons.minus}</button>
          <span class="w-4 text-center tabular-nums font-bold">{bombRepair}</span>
          <button class="w-6 h-6 flex items-center justify-center rounded bg-bg-surface-alt disabled:opacity-30"
            disabled={remaining.iron < 9}
            onclick={() => bombRepair++}>{@html uiIcons.plus}</button>
          <span class="text-text-muted text-[10px]">({bombRepair * 9}{@html icon('resources', 'iron', 'icon-xs')})</span>
        </span>
      {/if}
    </div>

    <!-- Civ goods resource split -->
    {#if civilianGoods > 0}
      <div class="flex items-center gap-2 text-[10px]">
        <span class="text-text-muted">Pay {civTotal}:</span>
        {#each (['oil', 'iron', 'osr'] as const) as r}
          {@const color = r === 'oil' ? 'var(--color-res-oil)' : r === 'iron' ? 'var(--color-res-iron)' : 'var(--color-res-osr)'}
          <span class="flex items-center gap-0.5">
            {@html icon('resources', r, 'icon-xs')}
            <button class="w-5 h-5 flex items-center justify-center rounded bg-bg-surface-alt disabled:opacity-30 text-[8px]"
              disabled={civGoodsPay[r] <= 0}
              onclick={() => civDec(r)}>-</button>
            <span class="w-4 text-center tabular-nums font-bold" style="color:{color}">{civGoodsPay[r]}</span>
            <button class="w-5 h-5 flex items-center justify-center rounded bg-bg-surface-alt disabled:opacity-30 text-[8px]"
              disabled={civAssigned >= civTotal}
              onclick={() => civInc(r)}>+</button>
          </span>
        {/each}
        {#if civAssigned < civTotal}
          <span class="text-red-400">({civTotal - civAssigned} unassigned)</span>
        {/if}
      </div>
    {/if}

    <!-- Blue zone unrest payment -->
    {#if hasUnrest}
      <div class="flex items-center gap-2 text-[10px]">
        <span class="text-blue-400 font-semibold">Unrest (3):</span>
        {#if unrestAssigned === 0}
          <button class="text-[10px] px-2 py-0.5 rounded bg-blue-900/50 text-blue-300"
            onclick={enableUnrest}>Pay 3</button>
          <span class="text-text-muted">(optional if unable)</span>
        {:else}
          {#each (['oil', 'iron', 'osr'] as const) as r}
            {@const color = r === 'oil' ? 'var(--color-res-oil)' : r === 'iron' ? 'var(--color-res-iron)' : 'var(--color-res-osr)'}
            <span class="flex items-center gap-0.5">
              {@html icon('resources', r, 'icon-xs')}
              <button class="w-5 h-5 flex items-center justify-center rounded bg-bg-surface-alt disabled:opacity-30 text-[8px]"
                disabled={unrestPay[r] <= 0}
                onclick={() => unrestDec(r)}>-</button>
              <span class="w-4 text-center tabular-nums font-bold" style="color:{color}">{unrestPay[r]}</span>
              <button class="w-5 h-5 flex items-center justify-center rounded bg-bg-surface-alt disabled:opacity-30 text-[8px]"
                disabled={unrestAssigned >= 3}
                onclick={() => unrestInc(r)}>+</button>
            </span>
          {/each}
          {#if unrestAssigned < 3}
            <span class="text-red-400">({3 - unrestAssigned} unassigned)</span>
          {/if}
          <button class="text-[10px] text-text-muted underline" onclick={clearUnrest}>clear</button>
        {/if}
      </div>
    {/if}

    <!-- Done with Production -->
    <button
      class="w-full py-2 rounded-lg font-semibold text-sm transition-colors
             {currentNationOk && allValid ? 'bg-accent text-bg-primary active:bg-accent-dim' : 'bg-red-900/50 text-red-300'}"
      disabled={!currentNationOk || !allValid}
      onclick={onDone}
    >{!affordable ? 'Overspent!' : civAssigned !== civTotal ? 'Assign Civ. Goods Cost' : (hasUnrest && unrestAssigned > 0 && unrestAssigned < 3) ? 'Assign Unrest Cost' : !allValid ? 'Fix All Nations First' : 'Done with Production'}</button>
  </div>
</div>
