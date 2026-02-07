<script lang="ts">
  export type BattleTab = 'battle' | 'raids'

  let { activeTab = $bindable<BattleTab>() }: { activeTab: BattleTab } = $props()

  const tabs: { id: BattleTab; label: string }[] = [
    { id: 'battle', label: 'Battle' },
    { id: 'raids', label: 'Raids' },
  ]
</script>

<div class="flex gap-1 mb-4 bg-bg-surface rounded-lg p-1">
  {#each tabs as tab}
    <button
      class="flex-1 text-xs font-medium py-1.5 rounded-md transition-colors
             {activeTab === tab.id ? 'bg-accent text-bg-primary' : 'text-text-muted'}"
      onclick={() => activeTab = tab.id}
    >{tab.label}</button>
  {/each}
</div>
