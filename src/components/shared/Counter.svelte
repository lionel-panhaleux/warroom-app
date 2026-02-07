<script lang="ts">
  import { uiIcons } from '../../lib/icons'

  let { value = $bindable(), min = 0, max = 99, label = '' }: {
    value: number; min?: number; max?: number; label?: string
  } = $props()

  let editing = $state(false)
  let editValue = $state('')

  function startEdit() {
    editValue = String(value)
    editing = true
  }

  function commitEdit() {
    const parsed = parseInt(editValue, 10)
    if (!isNaN(parsed)) value = Math.max(min, Math.min(max, parsed))
    editing = false
  }

  function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter') commitEdit()
    else if (e.key === 'Escape') editing = false
  }
</script>

<div class="flex items-center gap-2">
  {#if label}<span class="text-xs text-text-muted min-w-12">{label}</span>{/if}
  <button
    class="w-10 h-10 flex items-center justify-center rounded-lg bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
    aria-label="Decrease{label ? ` ${label}` : ''}"
    disabled={value <= min}
    onclick={() => value = Math.max(min, value - 1)}
  >{@html uiIcons.minus}</button>
  {#if editing}
    <!-- svelte-ignore a11y_autofocus -->
    <input
      type="number"
      class="w-12 text-center font-bold tabular-nums bg-bg-surface-alt rounded text-sm py-0.5 outline-none ring-1 ring-accent [appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
      bind:value={editValue}
      onblur={commitEdit}
      onkeydown={onKeydown}
      autofocus
    />
  {:else}
    <button
      class="w-8 text-center font-bold tabular-nums cursor-text hover:text-accent transition-colors"
      onclick={startEdit}
      aria-label="Edit value"
    >{value}</button>
  {/if}
  <button
    class="w-10 h-10 flex items-center justify-center rounded-lg bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
    aria-label="Increase{label ? ` ${label}` : ''}"
    disabled={value >= max}
    onclick={() => value = Math.max(min, Math.min(max, value + 1))}
  >{@html uiIcons.plus}</button>
</div>
