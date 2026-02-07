# War Room PWA — Development Plan

> High-level roadmap. Each phase will be planned in detail before implementation.

## Architecture Summary

- **Stack**: Svelte 5 + Vite + TypeScript + Tailwind CSS v4 + vite-plugin-pwa
- **Storage**: localStorage + undo stack (current state only)
- **Navigation**: Bottom tab bar (5 tabs, phase-gated)
- **UI**: Dark theme, mobile-first, touch-friendly, nation/resource/zone color tokens
- **Scope**: Single active game, Global War scenario (7 nations)

### Tabs

| Tab | Purpose | Game Phases | Gating |
|-----|---------|-------------|--------|
| **Dashboard** | Round overview, per-nation status, territories | — | Always |
| **Economy** | Income collection, oil bidding | Phase 1 | Always |
| **Battle** | Unit losses, repairs, territory exchanges, raids | Phase 4 | Always |
| **Morale** | Stress track, zone management, medals | Phase 6 | Locked until morale/production phase |
| **Production** | Unit orders, trade, civilian goods, bomb repair | Phase 7 | Locked until production phase |

### File Structure

```
src/
  main.ts                    Svelte 5 mount
  App.svelte                 Tab routing + auto-persist
  lib/types.ts               All TypeScript interfaces
  lib/data.ts                Static game data (nations, units, brackets, zones)
  lib/territories.ts         131 territory definitions
  lib/economy.ts             Income, trade, production helpers
  lib/battle.ts              Battle CP calculation, medal count, neutral invasion
  lib/morale.ts              Morale phase: stress, zone evaluation, relief, penalties
  lib/state.svelte.ts        Reactive state ($state), localStorage, undo
  lib/icons.ts               SVG icon strings + icon() helper
  components/TabBar.svelte   Fixed bottom nav (5 tabs, phase-gated)
  components/Dashboard.svelte  Nation overview + expandable territories
  components/Economy.svelte    Income + oil bidding (RoundStart)
  components/Battle.svelte     Battle + raids
  components/Morale.svelte     Stress/zone phase
  components/Production.svelte Unit orders, trade, civ goods, bomb repair
  components/economy/        RoundStart, Territories, NationSelector, etc.
  components/battle/         BattleNav, BattleMain, Raids
  components/morale/         StressOverview, ZoneEvaluation, ZoneRelief, ZonePenalties
  components/shared/         Counter
  styles/app.css             Tailwind v4 + @theme tokens + icon sizing
assets/icons/                Nation flags, unit silhouettes, resource/marker/UI SVGs
assets/favicon/              PWA icon sources
public/icons/                PWA icons (192, 512)
references/                  Rules PDFs + parsed markdown refs
```

---

## Phase 1: Foundation ✅

Svelte 5 + Vite + TS + Tailwind v4 + PWA scaffold. 4-tab shell, reactive state with localStorage + undo, all static game data typed, dark theme with nation/resource/zone color tokens, game asset SVGs (nation flags, unit silhouettes, resource/marker/UI icons), PWA icons.

---

## Phase 2: Economy Tab ✅

Economy tab with 3 sub-tabs: Round Start (income collection from territories, oil bidding, turn order), Production (unit orders, trades, civilian goods, bomb repair), Territories (searchable/filterable list, owner change, embattled toggle). 131 territory definitions. Dashboard enhanced with resource/territory/medal/civilian-goods icons and zone names with effect descriptions.

---

## Phase 3: Battle Tab ✅

Battle tab with 2 sub-tabs: Battle (territory-centric combat recording with 5-step workflow: location, losses, territory outcome, repairs, apply) and Raids (strategic bombing + convoy raid resource deduction). Casualty points auto-computed from unit losses. Territory captures award medals (1 normal, 3 capital, 0 neutral) and apply SV stress to former owner. Neutral invasion adds +1 stress to attacker. CasualtyPoints reset to 0 at round start.

---

## Phase 4: Morale Tab + Navigation Restructure ✅

Morale tab with full stress/zone lifecycle. Navigation restructured from 4 tabs to 5 phase-gated tabs.

- **Morale phase**: StressOverview (casualty→stress conversion, medal/CG cancel), ZoneEvaluation (auto-advance when stress ≥ threshold), ZoneRelief (spend medals/CG to slide back 1 zone), ZonePenalties (Blue unrest payment, zone effect display)
- **Phase gating**: income → bidding → morale → production → income. Morale and Production tabs locked until their phase. Battle always accessible.
- **Navigation restructure**: Economy simplified to income+bidding only. Production promoted to top-level tab. Territories moved to expandable Dashboard section. EconomyNav sub-tabs removed.
- **Unrest moved**: Blue zone unrest payment moved from Production to Morale (ZonePenalties).

---

## Phase 5: Dashboard Tab

Overview and round management.

- Round counter (advance/track current round)
- Per-nation summary cards:
  - Resources (Oil / Iron / OSR)
  - Homeland zone (color-coded)
  - Current stress level
  - Medals in hand
- Alliance grouping (Allied vs Axis)
- Quick access to begin Phase 1/4/6/7 workflows

**Deliverable**: At-a-glance game state for all 7 nations.

---

## Phase 6: Polish & Theming

Visual refinement pass.

- Nation color scheme (CSS custom properties)
- War Room / military aesthetic
- Touch-friendly controls (large tap targets, swipe?)
- Mobile Safari + Chrome testing
- Accessibility basics (contrast, focus states)
- PWA icon and splash screen

**Deliverable**: Polished, themed, production-ready PWA.

---

## Game Data Reference

### Stress Thresholds (Global War)

| Nation | Threshold |
|--------|-----------|
| China | 4 |
| Italy | 4 |
| United States | 5 |
| British Commonwealth | 6 |
| Soviet Union | 6 |
| Germany | 6 |
| Imperial Japan | 7 |

### Casualty → Stress Conversion

| Casualty Pts | Stress |
|-------------|--------|
| 0–19 | 0 |
| 20–35 | 1 |
| 36–51 | 2 |
| 52–69 | 3 |
| 70–89 | 4 |
| 90–109 | 5 |
| 110+ | 6 (max) |

### All Stress Sources

| Source | Amount | When |
|--------|--------|------|
| Casualty points | 0–6 (via chart) | Phase 6 |
| Territory loss | SV of territory | Phase 4 debrief |
| Soviet-Japanese Pact break | 6 | Phase 6/7 |
| Neutral invasion | 1 per neutral | Phase 6 |

### All Resource Drains (beyond production)

| Drain | Amount | When |
|-------|--------|------|
| Oil bidding | Variable | Phase 2 |
| Unit repair | 1 per unit (free w/ Port Advantage) | Phase 4 debrief |
| Strategic bombing | 1 Oil/Iron/OSR per die hit | Phase 4 |
| Convoy raids | 1 per ship per type | Phase 4 |
| Blue zone penalty | 3 resources (any mix) | Phase 6 |
| Bomb token repair | 9 Iron (max 1/round) | Phase 7 |

---

## Progress

| Phase | Status | Notes |
|-------|--------|-------|
| 1. Foundation | ✅ Done | commit f3e7e32 |
| 2. Economy Tab | ✅ Done | commit de62861 |
| 3. Battle Tab | ✅ Done | commit ce6dd01 |
| 4. Morale + Nav Restructure | ✅ Done | commit f8b6567 |
| 5. Dashboard Tab | ✅ Done | Enhanced alongside other phases |
| 6. Polish & Theming | Ongoing | Dark theme, icons, PWA done |
