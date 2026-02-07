<script lang="ts">
  import type { HomelandZone } from '../../lib/types'
  import type { NationMoraleDecisions } from '../../lib/morale'
  import { HOMELAND_ZONES, ZONE_INFO } from '../../lib/data'
  import { zoneIndex } from '../../lib/morale'
  import { icon, uiIcons } from '../../lib/icons'
  import type { ResourceBundle } from '../../lib/economy'

  let { zone, remainingStress = 0, decisions = $bindable(), available }: {
    zone: HomelandZone
    remainingStress: number
    decisions: NationMoraleDecisions
    available: { oil: number; iron: number; osr: number }
  } = $props()

  const zi = $derived(zoneIndex(zone))
  const hasBlue = $derived(zi >= 1)
  const unrestAssigned = $derived(decisions.unrestPay.oil + decisions.unrestPay.iron + decisions.unrestPay.osr)

  function unrestInc(r: keyof ResourceBundle) {
    if (unrestAssigned >= 3) return
    decisions.unrestPay = { ...decisions.unrestPay, [r]: decisions.unrestPay[r] + 1 }
  }
  function unrestDec(r: keyof ResourceBundle) {
    if (decisions.unrestPay[r] <= 0) return
    decisions.unrestPay = { ...decisions.unrestPay, [r]: decisions.unrestPay[r] - 1 }
  }
  function enableUnrest() {
    decisions.unrestPay = { oil: 0, iron: 0, osr: 3 }
  }
  function clearUnrest() {
    decisions.unrestPay = { oil: 0, iron: 0, osr: 0 }
  }
</script>

<div class="space-y-2">
  <h3 class="text-sm font-semibold text-text-muted uppercase tracking-wide">Penalties</h3>

  {#if zi === 0}
    <p class="text-sm text-green-400">No penalties (White zone)</p>
  {:else}
    <div class="space-y-1">
      {#each HOMELAND_ZONES.slice(1, zi + 1) as z}
        {@const info = ZONE_INFO[z]}
        <div class="flex items-start gap-2 text-sm">
          <span class="w-3 h-3 rounded-full mt-0.5 shrink-0" style="background:var(--color-zone-{z})"></span>
          <div>
            <span class="font-medium" style="color:var(--color-zone-{z})">{info.name}</span>
            <span class="text-text-muted"> — {info.effect}</span>
          </div>
        </div>
      {/each}
    </div>

    <!-- Blue zone unrest payment -->
    {#if hasBlue}
      <div class="mt-2 p-2 rounded bg-bg-surface-alt space-y-1.5">
        <div class="flex items-center gap-2 text-xs">
          <span class="font-semibold" style="color:var(--color-zone-Blue)">Unrest (3):</span>
          {#if unrestAssigned === 0}
            <button class="text-[10px] px-2 py-0.5 rounded bg-blue-900/50 text-blue-300"
              onclick={enableUnrest}>Pay 3</button>
            <span class="text-text-muted text-[10px]">(optional if unable)</span>
          {:else}
            {#each (['oil', 'iron', 'osr'] as const) as r}
              {@const color = r === 'oil' ? 'var(--color-res-oil)' : r === 'iron' ? 'var(--color-res-iron)' : 'var(--color-res-osr)'}
              <span class="flex items-center gap-0.5">
                {@html icon('resources', r, 'icon-xs')}
                <button class="w-5 h-5 flex items-center justify-center rounded bg-bg-primary disabled:opacity-30 text-[8px]"
                  disabled={decisions.unrestPay[r] <= 0}
                  onclick={() => unrestDec(r)}>-</button>
                <span class="w-4 text-center tabular-nums font-bold" style="color:{color}">{decisions.unrestPay[r]}</span>
                <button class="w-5 h-5 flex items-center justify-center rounded bg-bg-primary disabled:opacity-30 text-[8px]"
                  disabled={unrestAssigned >= 3}
                  onclick={() => unrestInc(r)}>+</button>
              </span>
            {/each}
            {#if unrestAssigned < 3}
              <span class="text-red-400 text-[10px]">({3 - unrestAssigned} left)</span>
            {/if}
            <button class="text-[10px] text-text-muted underline" onclick={clearUnrest}>clear</button>
          {/if}
        </div>
        {#if unrestAssigned === 3}
          <p class="text-[10px] text-text-muted">
            Paying: {decisions.unrestPay.oil > 0 ? `${decisions.unrestPay.oil} Oil ` : ''}{decisions.unrestPay.iron > 0 ? `${decisions.unrestPay.iron} Iron ` : ''}{decisions.unrestPay.osr > 0 ? `${decisions.unrestPay.osr} OSR` : ''}
          </p>
        {/if}
      </div>
    {/if}

    {#if zone === 'Gray' && remainingStress > 0}
      <div class="mt-2 p-2 rounded bg-bg-surface-alt text-sm">
        <span class="text-red-400 font-semibold">Desertion:</span>
        Remove <span class="font-bold">{remainingStress}</span> unit{remainingStress > 1 ? 's' : ''} from the map
      </div>
    {/if}
  {/if}
</div>
