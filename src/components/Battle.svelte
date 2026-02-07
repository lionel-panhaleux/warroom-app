<script lang="ts">
  import BattleNav from './battle/BattleNav.svelte'
  import type { BattleTab } from './battle/BattleNav.svelte'
  import BattleMain from './battle/BattleMain.svelte'
  import Raids from './battle/Raids.svelte'

  let battleTab: BattleTab = $state('battle')
</script>

<div>
  <BattleNav bind:activeTab={battleTab} />

  {#if battleTab === 'battle'}
    <BattleMain />
  {:else if battleTab === 'raids'}
    <Raids />
  {/if}
</div>
