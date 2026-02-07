<script lang="ts">
  import { appState, persist } from './lib/state.svelte'
  import TabBar from './components/TabBar.svelte'
  import Dashboard from './components/Dashboard.svelte'
  import Economy from './components/Economy.svelte'
  import Battle from './components/Battle.svelte'
  import Morale from './components/Morale.svelte'

  let activeTab: 'dashboard' | 'economy' | 'battle' | 'morale' = $state('dashboard')

  // Auto-persist on any state change
  $effect(() => {
    // Touch reactive state to track it
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
{/if}

<TabBar bind:activeTab />
