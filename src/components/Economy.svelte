<script lang="ts">
  let { showToast }: { showToast: (msg: string) => void } = $props()

  import RoundStart from './economy/RoundStart.svelte'
</script>

<div>
  <RoundStart {showToast} />
</div>
