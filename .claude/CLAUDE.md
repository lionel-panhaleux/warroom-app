# CLAUDE.md — keep this file short and token-efficient

## What
PWA assistant for War Room board game (Larry Harris, 2nd Ed). Single shared device, Global War scenario, offline-first.

## MVP
1. Resource tracking (Oil/Iron/OSR per nation)
2. Morale & stress tracking (casualties → stress → homeland zones)
3. Phase assistance (Phase 1: Economy, Phase 6: Morale, Phase 7: Production)
4. Battle loss recording (feeds morale)

## Stack
Svelte 5 + Vite + TypeScript + Tailwind CSS v4 + vite-plugin-pwa. No SvelteKit.

## Structure
```
vite.config.ts               Svelte + Tailwind v4 + PWA plugins
src/
  main.ts                    Svelte 5 mount
  App.svelte                 Tab routing + auto-persist
  lib/types.ts               All TypeScript interfaces
  lib/data.ts                Static game data (nations, units, brackets)
  lib/state.svelte.ts        Reactive state ($state), localStorage, undo
  components/TabBar.svelte   Fixed bottom nav
  components/Dashboard.svelte
  components/Economy.svelte
  components/Battle.svelte
  components/Morale.svelte
  styles/app.css             Tailwind v4 + theme tokens
public/icons/                PWA icons
references/                  Rules PDFs + parsed markdown refs
```

## Conventions
- Svelte 5 runes ($state, $derived, $effect, $props, $bindable)
- Only `.svelte.ts` files use runes; pure data uses `.ts`
- Tailwind v4 `@theme` block for custom properties (no tailwind.config.js)
- Central `setState()`/`persist()` pattern with undo stack
- Small pure functions, comments only where non-obvious
- Always use context7 MCP for technical documentation lookups

## Key refs
- `PLAN.md` — development roadmap & progress tracker
- `references/game-overview.md` — condensed mechanics
- `references/game-data.md` — nations, unit costs, zones, thresholds
- `references/complete_rules.md` — full rules (parsed from PDF)
- `references/*.pdf` — official rulebook + FAQ
