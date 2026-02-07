<script lang="ts">
  import type { RoundPhase } from '../../lib/types'

  export type EconomyTab = 'round' | 'production' | 'territories'

  let { activeTab = $bindable<EconomyTab>(), roundPhase }: { activeTab: EconomyTab; roundPhase: RoundPhase } = $props()

  const tabs: { id: EconomyTab; label: string }[] = [
    { id: 'round', label: 'Round Start' },
    { id: 'production', label: 'Production' },
    { id: 'territories', label: 'Territories' },
  ]
</script>

<div class="flex gap-1 mb-4 bg-bg-surface rounded-lg p-1">
  {#each tabs as tab}
    {@const locked = tab.id === 'production' && roundPhase !== 'production'}
    <button
      class="flex-1 text-xs font-medium py-1.5 rounded-md transition-colors
             {activeTab === tab.id ? 'bg-accent text-bg-primary' : locked ? 'text-text-muted/40 cursor-not-allowed' : 'text-text-muted'}"
      disabled={locked}
      onclick={() => activeTab = tab.id}
    >{tab.label}</button>
  {/each}
</div>
