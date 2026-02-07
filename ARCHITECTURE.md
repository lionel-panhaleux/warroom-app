# War Room PWA — Architecture

## Overview

Offline-first PWA for the War Room board game (Larry Harris, 2nd Ed, Global War scenario). A single shared device at the table tracks resources, battles, morale, and production for 7 nations across game rounds.

## Stack

- **Svelte 5** — UI framework, using runes (`$state`, `$derived`, `$effect`, `$props`, `$bindable`)
- **Vite** — Build tool + dev server
- **TypeScript** — Strict typing throughout
- **Tailwind CSS v4** — Utility-first styling via `@theme` block (no `tailwind.config.js`)
- **vite-plugin-pwa** — Service worker generation for offline use

No backend, no SvelteKit, no router — just a single-page app with tab-based navigation.

## File Structure

```
src/
  main.ts                          Svelte 5 mount point
  App.svelte                       Tab routing, auto-persist via $effect, undo binding
  lib/
    types.ts                       All TypeScript interfaces (NationId, GameState, etc.)
    data.ts                        Static game data (nations, units, casualty brackets, zones)
    territories.ts                 131 territory definitions (parsed from official PDF)
    economy.ts                     Income calculation, trade, production cost helpers
    battle.ts                      Casualty point computation, medal count, neutral invasion
    morale.ts                      Stress evaluation, zone advance/relief, penalty logic
    state.svelte.ts                Reactive game state, localStorage persistence, undo stack
    icons.ts                       SVG icon strings + icon() helper
  components/
    TabBar.svelte                  Fixed bottom nav (5 tabs, phase-gated)
    Dashboard.svelte               Per-nation overview cards + expandable territory browser
    Economy.svelte                 Wrapper for RoundStart (income + bidding)
    Battle.svelte                  Wrapper for BattleMain + Raids
    Morale.svelte                  Full morale phase: stress → zone → relief → penalties
    Production.svelte              Unit orders, trade, civ goods, bomb repair
    economy/
      RoundStart.svelte            Income collection + oil bidding + turn order
      Territories.svelte           Searchable/filterable territory list with owner management
      NationSelector.svelte        Reusable 7-nation selector with optional activity indicators
      UnitPicker.svelte            Unit order grid for production
      TradePicker.svelte           Resource trade interface
      ProductionSummary.svelte     Fixed bottom bar: resource remaining, civ goods, done button
    battle/
      BattleNav.svelte             Battle / Raids sub-tab selector
      BattleMain.svelte            5-step battle workflow
      Raids.svelte                 Strategic bombing + convoy raid resource deduction
    morale/
      StressOverview.svelte        Casualty→stress, neutral invasions, pact breaking, cancel
      ZoneEvaluation.svelte        Auto-advance when stress ≥ threshold
      ZoneRelief.svelte            Spend medals/CG to slide zone back
      ZonePenalties.svelte         Blue zone unrest, zone effects display, Gray desertion
    shared/
      Counter.svelte               Reusable +/- counter with touch-friendly 40px targets
  styles/
    app.css                        Tailwind v4 @theme tokens + icon sizing + focus-visible
assets/
  icons/                           SVG source files (nations, units, resources, markers, UI)
  favicon/                         PWA icon PNGs (512, 192, 180)
public/
  icons/                           PWA manifest icons
references/
  game-overview.md                 Condensed game mechanics
  game-data.md                     Nations, unit costs, zones, thresholds
  complete_rules.md                Full rules (parsed from PDF)
  *.pdf                            Official rulebook + FAQ
```

## State Management

All game state lives in a single `appState` object (`lib/state.svelte.ts`) using Svelte 5's `$state` rune. Changes go through `setState()` which pushes the previous state onto an undo stack before applying the new one.

Persistence happens via a `$effect` in `App.svelte` that serializes to `localStorage` on every change. State migrations handle saves from older versions (e.g. adding territories field).

**Key constraint**: Only `.svelte.ts` files can use runes. Pure data/logic files use plain `.ts`.

## Navigation & Phase Gating

Five bottom tabs with a round lifecycle: **income → bidding → morale → production → income**.

- **Dashboard** and **Economy** and **Battle** — always accessible
- **Morale** — locked until bidding phase completes
- **Production** — locked until morale phase completes

The `roundPhase` field in game state (`'income' | 'bidding' | 'morale' | 'production'`) drives the gating. Completing each phase advances to the next.

## Theming

Dark theme using Tailwind v4's `@theme` block for custom properties:

- **Nation colors** (`--color-nation-CHN`, etc.) — unique per nation
- **Resource colors** (`--color-res-oil`, `--color-res-iron`, `--color-res-osr`) — red, blue, yellow
- **Zone colors** (`--color-zone-White` through `--color-zone-Gray`) — homeland zone progression
- **Status colors** (`--color-danger`, `--color-success`, `--color-warning`) — semantic, used app-wide
- **Surface colors** (`--color-bg-primary`, `--color-bg-surface`, `--color-bg-surface-alt`) — layered dark backgrounds

All status-indicating colors (errors, warnings, success states) use theme tokens rather than hardcoded Tailwind color classes.

## Icons

All icons are inline SVG strings exported from `lib/icons.ts`. No icon font, no external requests. Categories:

- **Nation flags** — 7 circular flags (viewBox 48×48, unique clipPath IDs)
- **Unit silhouettes** — 10 units with color-coded shape badges (land=square, air=circle, naval=hexagon)
- **Resource icons** — Oil (red), Iron (blue), OSR (yellow)
- **Marker icons** — Medal, civilian goods, wrench, bomb, embattled, etc.
- **UI icons** — Plus, minus, undo, trade (currentColor)
- **Nav icons** — Lucide-derived tab icons

Sizing via CSS classes: `.icon`, `.icon-xs`, `.icon-sm`, `.icon-lg`, `.icon-xl`.

## Key Design Decisions

### Single shared device
The app is designed for 2-6 players passing one phone around the table. This means:
- No authentication or multi-user state
- Large touch targets (min 40px for counters, 48px for primary actions)
- Clear visual feedback for which nation is selected
- No complex navigation — everything 1-2 taps away

### localStorage over IndexedDB
One game at a time, state is a few KB. localStorage is synchronous, simpler, and sufficient. The undo stack is in-memory only (lost on refresh by design — prevents accidentally undoing across sessions).

### Inline SVG over icon fonts or image sprites
Needed colored, composable icons (nation flags with unique clipPaths, unit silhouettes with shape badges). Inline SVG allows per-icon coloring via CSS and avoids network requests for offline use.

### Phase gating via tab locking
Rather than a wizard/stepper, the round phases are enforced by locking tabs until their prerequisites complete. This keeps the interface explorable (you can always check Dashboard or record battles) while ensuring the economic sequence is followed.

### Territory data from PDF, not rules markdown
The parsed rules markdown (`complete_rules.md`) contained hallucinated tables from PDF image extraction. Territory resource values were verified against the official PDF territory list and the physical game board. The Python legacy codebase was correct for unit costs and casualty mechanics but wrong for territory resources.

### No SvelteKit
No server-side rendering needed, no routing needed, no API. Plain Vite + Svelte keeps the build simple and the bundle small (~130KB gzipped).

### Tailwind v4 @theme over config file
Tailwind v4 supports `@theme` blocks directly in CSS, eliminating the need for `tailwind.config.js`. All custom design tokens (colors, etc.) live in `src/styles/app.css`.
