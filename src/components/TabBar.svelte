<script lang="ts">
  import { navIcons } from '../lib/icons'

  type Tab = 'dashboard' | 'economy' | 'battle' | 'morale' | 'production'

  let { activeTab = $bindable<Tab>(), lockedTabs = new Set<Tab>() }: {
    activeTab: Tab
    lockedTabs?: Set<Tab>
  } = $props()

  const tabs: { id: Tab; label: string; svg: string }[] = [
    { id: 'dashboard',  label: 'Dashboard',  svg: navIcons.dashboard },
    { id: 'economy',    label: 'Economy',     svg: navIcons.economy },
    { id: 'battle',     label: 'Battle',      svg: navIcons.battle },
    { id: 'morale',     label: 'Morale',      svg: navIcons.morale },
    { id: 'production', label: 'Produce',     svg: navIcons.production },
  ]
</script>

<nav class="fixed bottom-0 left-0 right-0 z-50 bg-bg-surface border-t border-bg-surface-alt"
     style="padding-bottom: env(safe-area-inset-bottom, 0px);">
  <div class="flex" role="tablist">
  {#each tabs as tab}
    {@const locked = lockedTabs.has(tab.id)}
    <button
      role="tab"
      aria-current={activeTab === tab.id ? 'page' : undefined}
      class="flex-1 flex flex-col items-center py-1.5 text-xs transition-colors
             {locked ? 'text-text-muted/30 cursor-not-allowed' : activeTab === tab.id ? 'text-accent' : 'text-text-muted'}"
      disabled={locked}
      onclick={() => activeTab = tab.id}
    >
      <span class="mb-0.5 [&>svg]:w-5 [&>svg]:h-5">{@html tab.svg}</span>
      {tab.label}
    </button>
  {/each}
  </div>
</nav>
