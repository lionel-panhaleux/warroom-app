<script lang="ts">
  import { RESOURCES } from '../../lib/data'
  import { tradeResult, type ResourceBundle } from '../../lib/economy'
  import { icon } from '../../lib/icons'
  import type { NationId, ResourceType } from '../../lib/types'

  let { nationId, tradeGive = $bindable(), tradeReceive = $bindable() }: {
    nationId: NationId
    tradeGive: ResourceType | null
    tradeReceive: ResourceType | null
  } = $props()

  const RES_KEYS: ResourceType[] = ['oil', 'iron', 'osr']

  let result = $derived(
    tradeReceive && tradeGive && tradeReceive !== tradeGive
      ? tradeResult(tradeReceive, tradeGive)
      : null
  )

  // China cannot trade
  let isChinaHidden = $derived(nationId === 'CHN')
</script>

{#if isChinaHidden}
  <div class="bg-bg-surface rounded-lg p-3 text-xs text-text-muted">China cannot trade.</div>
{:else}
  <div class="bg-bg-surface rounded-lg p-3 space-y-3">
    <p class="text-[10px] text-text-muted">Max 1 trade per nation per round. Ensure trade access on the board.</p>

    <div>
      <span class="text-xs text-text-muted">Receive:</span>
      <div class="flex gap-2 mt-1">
        {#each RES_KEYS as r}
          <button
            class="flex items-center gap-1 text-xs px-2.5 py-1.5 rounded-md
                   {tradeReceive === r ? 'bg-accent/20 ring-1 ring-accent' : 'bg-bg-surface-alt text-text-muted'}"
            onclick={() => { tradeReceive = tradeReceive === r ? null : r; if (tradeGive === r) tradeGive = null }}
          >
            {@html icon('resources', r, 'icon-xs')}
            {RESOURCES[r].label}
          </button>
        {/each}
      </div>
    </div>

    {#if tradeReceive}
      <div>
        <span class="text-xs text-text-muted">Pay with:</span>
        <div class="flex gap-2 mt-1">
          {#each RES_KEYS.filter(r => r !== tradeReceive) as r}
            <button
              class="flex items-center gap-1 text-xs px-2.5 py-1.5 rounded-md
                     {tradeGive === r ? 'bg-accent/20 ring-1 ring-accent' : 'bg-bg-surface-alt text-text-muted'}"
              onclick={() => tradeGive = tradeGive === r ? null : r}
            >
              {@html icon('resources', r, 'icon-xs')}
              {RESOURCES[r].label}
            </button>
          {/each}
        </div>
      </div>
    {/if}

    {#if result && tradeReceive && tradeGive}
      <div class="text-xs pt-1 border-t border-bg-surface-alt">
        Receive <strong>{result.receiveAmt} {RESOURCES[tradeReceive].label}</strong>,
        pay <strong>{result.giveAmt} {RESOURCES[tradeGive].label}</strong>
      </div>
    {/if}
  </div>
{/if}
