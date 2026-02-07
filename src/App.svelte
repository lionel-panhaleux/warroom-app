<script lang="ts">
  import { appState, persist } from './lib/state.svelte'
  import TabBar from './components/TabBar.svelte'
  import Dashboard from './components/Dashboard.svelte'
  import Economy from './components/Economy.svelte'
  import Battle from './components/Battle.svelte'
  import Morale from './components/Morale.svelte'
  import Production from './components/Production.svelte'

  type Tab = 'dashboard' | 'economy' | 'battle' | 'morale' | 'production'
  let activeTab: Tab = $state('dashboard')

  // Locked tabs based on round phase
  let lockedTabs = $derived.by(() => {
    const phase = appState.game.roundPhase
    const locked = new Set<Tab>()
    if (phase !== 'morale' && phase !== 'production') locked.add('morale')
    if (phase !== 'production') locked.add('production')
    return locked
  })

  // Auto-persist on any state change
  $effect(() => {
    JSON.stringify(appState.game)
    persist()
  })
</script>

{#if activeTab === 'dashboard'}
  <Dashboard />
{:else if activeTab === 'economy'}
  <Economy />
{:else if activeTab === 'battle'}
  <Battle />
{:else if activeTab === 'morale'}
  <Morale />
{:else if activeTab === 'production'}
  <Production />
{/if}

<TabBar bind:activeTab {lockedTabs} />
