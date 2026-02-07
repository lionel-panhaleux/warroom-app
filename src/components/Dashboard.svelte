<script lang="ts">
  import { appState } from '../lib/state.svelte'
  import { NATIONS, ALLIED_IDS, AXIS_IDS, HOMELAND_ZONES } from '../lib/data'
  import type { NationId } from '../lib/types'

  function zoneIndex(nationId: NationId): number {
    return HOMELAND_ZONES.indexOf(appState.game.nations[nationId].zone)
  }
</script>

<div>
  <div class="flex items-center justify-between mb-4">
    <h1 class="text-xl font-bold text-accent">War Room</h1>
    <span class="text-text-muted text-sm">Round {appState.game.round}</span>
  </div>

  {#each [{ label: 'Allies', ids: ALLIED_IDS }, { label: 'Axis', ids: AXIS_IDS }] as group}
    <h2 class="text-sm font-semibold text-text-muted uppercase tracking-wide mb-2 mt-4">{group.label}</h2>
    <div class="grid gap-2">
      {#each group.ids as id}
        {@const nation = NATIONS[id]}
        {@const ns = appState.game.nations[id]}
        <div class="flex items-center gap-3 rounded-lg px-3 py-2 bg-bg-surface">
          <div class="w-2 h-8 rounded-full" style="background: var(--color-nation-{id})"></div>
          <div class="flex-1 min-w-0">
            <div class="font-medium text-sm truncate">{nation.name}</div>
            <div class="flex gap-3 text-xs text-text-muted mt-0.5">
              <span style="color: var(--color-res-oil)">Oil {ns.oil}</span>
              <span style="color: var(--color-res-iron)">Iron {ns.iron}</span>
              <span style="color: var(--color-res-osr)">OSR {ns.osr}</span>
            </div>
          </div>
          <div class="text-xs px-2 py-0.5 rounded font-medium"
               style="background: color-mix(in srgb, var(--color-zone-{ns.zone}) 25%, transparent);
                      color: var(--color-zone-{ns.zone})">
            {ns.zone}
          </div>
        </div>
      {/each}
    </div>
  {/each}
</div>
