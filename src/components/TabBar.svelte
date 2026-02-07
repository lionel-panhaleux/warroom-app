<script lang="ts">
  type Tab = 'dashboard' | 'economy' | 'battle' | 'morale'

  let { activeTab = $bindable<Tab>() }: { activeTab: Tab } = $props()

  const tabs: { id: Tab; label: string; icon: string }[] = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'economy',   label: 'Economy',   icon: '💰' },
    { id: 'battle',    label: 'Battle',    icon: '⚔️' },
    { id: 'morale',    label: 'Morale',    icon: '🏠' },
  ]
</script>

<nav class="fixed bottom-0 left-0 right-0 z-50 flex bg-bg-surface border-t border-bg-surface-alt"
     style="padding-bottom: env(safe-area-inset-bottom, 0px);">
  {#each tabs as tab}
    <button
      class="flex-1 flex flex-col items-center py-2 text-xs transition-colors
             {activeTab === tab.id ? 'text-accent' : 'text-text-muted'}"
      onclick={() => activeTab = tab.id}
    >
      <span class="text-lg leading-none mb-0.5">{tab.icon}</span>
      {tab.label}
    </button>
  {/each}
</nav>
