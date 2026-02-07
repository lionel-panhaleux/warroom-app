<script lang="ts">
  import { uiIcons } from '../../lib/icons'

  let { value = $bindable(), min = 0, max = 99, label = '' }: {
    value: number; min?: number; max?: number; label?: string
  } = $props()
</script>

<div class="flex items-center gap-2">
  {#if label}<span class="text-xs text-text-muted min-w-12">{label}</span>{/if}
  <button
    class="w-10 h-10 flex items-center justify-center rounded-lg bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
    aria-label="Decrease{label ? ` ${label}` : ''}"
    disabled={value <= min}
    onclick={() => value = Math.max(min, value - 1)}
  >{@html uiIcons.minus}</button>
  <span class="w-8 text-center font-bold tabular-nums">{value}</span>
  <button
    class="w-10 h-10 flex items-center justify-center rounded-lg bg-bg-surface-alt text-text-primary active:bg-accent/30 disabled:opacity-30"
    aria-label="Increase{label ? ` ${label}` : ''}"
    disabled={value >= max}
    onclick={() => value = Math.max(min, Math.min(max, value + 1))}
  >{@html uiIcons.plus}</button>
</div>
