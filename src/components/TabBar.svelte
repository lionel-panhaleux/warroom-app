<script lang="ts">
  type Tab = 'dashboard' | 'economy' | 'battle' | 'morale' | 'production'

  let { activeTab = $bindable<Tab>(), lockedTabs = new Set<Tab>() }: {
    activeTab: Tab
    lockedTabs?: Set<Tab>
  } = $props()

  const tabs: { id: Tab; label: string; icon: string }[] = [
    { id: 'dashboard',  label: 'Dashboard',  icon: '📊' },
    { id: 'economy',    label: 'Economy',     icon: '💰' },
    { id: 'battle',     label: 'Battle',      icon: '⚔️' },
    { id: 'morale',     label: 'Morale',      icon: '🏠' },
    { id: 'production', label: 'Produce',     icon: '🏭' },
  ]
</script>

<nav class="fixed bottom-0 left-0 right-0 z-50 flex bg-bg-surface border-t border-bg-surface-alt"
     style="padding-bottom: env(safe-area-inset-bottom, 0px);">
  {#each tabs as tab}
    {@const locked = lockedTabs.has(tab.id)}
    <button
      class="flex-1 flex flex-col items-center py-1.5 text-[10px] transition-colors
             {locked ? 'text-text-muted/30 cursor-not-allowed' : activeTab === tab.id ? 'text-accent' : 'text-text-muted'}"
      disabled={locked}
      onclick={() => activeTab = tab.id}
    >
      <span class="text-base leading-none mb-0.5">{tab.icon}{#if locked}<span class="text-[8px] ml-0.5">🔒</span>{/if}</span>
      {tab.label}
    </button>
  {/each}
</nav>
