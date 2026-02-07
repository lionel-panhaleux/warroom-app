# War Room PWA — Development Plan

> High-level roadmap. Each phase will be planned in detail before implementation.

## Architecture Summary

- **Stack**: Vanilla JS, no build step, no deps, single `index.html`
- **Storage**: localStorage + undo stack (current state only)
- **Navigation**: Bottom tab bar (4 tabs)
- **UI approach**: Functional first, theming added later
- **Scope**: Single active game, Global War scenario (7 nations)

### Tabs

| Tab | Purpose | Game Phases |
|-----|---------|-------------|
| **Dashboard** | Round overview, per-nation status summary | — |
| **Economy** | Resource income + unit production + trade | Phase 1 & 7 |
| **Battle** | Unit losses, repairs, territory exchanges, raids | Phase 4 |
| **Morale** | Stress track, zone management, medals | Phase 6 |

### File Structure

```
index.html / manifest.json / sw.js
css/style.css
js/app.js          → init + tab routing
js/state.js        → localStorage, getState/setState, undo
js/data.js         → nations, unit costs, thresholds, zones
js/ui.js           → shared UI helpers (render nation selectors, etc.)
js/phases/         → tab-specific modules
  dashboard.js
  economy.js
  battle.js
  morale.js
```

---

## Phase 1: Foundation

Scaffold the app shell — no game logic yet, just the skeleton.

- `index.html` with tab bar and content areas
- `manifest.json` + `sw.js` for PWA (installable, offline)
- `css/style.css` — minimal functional styles, mobile-first layout
- `js/app.js` — init, tab switching
- `js/state.js` — localStorage CRUD, `getState()`/`setState()`, undo stack
- `js/data.js` — static game data:
  - 7 nations (name, alliance, special rules, order limit)
  - Unit types (costs, casualty points)
  - Stress thresholds: China 4, Italy 4, USA 5, UK 6, USSR 6, Germany 6, Japan 7
  - Casualty→stress conversion chart
  - Homeland zones & penalties

**Deliverable**: Installable PWA with 4 empty tabs and working state persistence.

---

## Phase 2: Economy Tab

Resource tracking for Phase 1 (income) and Phase 7 (production).

### Phase 1: Income
- Per-nation resource display (Oil / Iron / OSR current stock)
- Add income: input resource gains from territory cards
- Embattled territory flag (reduced income — player enters actual values from card back)
- China restriction: no Oil income

### Phase 2: Oil Bidding
- Record oil bid per nation (deducted from stock)
- China always bids 0
- Display resulting turn order (descending bid)

### Phase 7: Production
- Unit purchase interface: pick units, auto-deduct resources
- Resource validation (can't overspend)
- Neutral trade: 1 trade per nation per round (Oil ×2, Iron ×3, OSR ×5)
- Civilian goods purchase (any 5 resources total)
- Bomb token repair: 9 Iron to remove 1 bomb token (max 1/round, optional)
- China restrictions: no Oil, no trade

**Deliverable**: Full resource lifecycle — earn, bid, trade, spend, track.

---

## Phase 3: Battle Tab

Loss recording for Phase 4 (Combat).

### Unit Losses
- Select nation, pick destroyed unit types from list
- Auto-calculate casualty points per battle
- Cumulative casualty tracking per nation per round

### Unit Repairs
- Track damaged units after battle
- Spend 1 resource each to repair (any resource type)
- Port Advantage: free repair when friendly port + friendly naval units present
  - Blocked by Yellow zone or worse, or bomb token on port

### Territory Exchanges
- Record territory gains/losses per nation
- Track SV (stress value) of lost territories → feeds morale stress
- Medal awards: +1 per territory captured, +3 per capital

### Bombardment & Raids
- Record resource losses from strategic bombing and convoy raids
- Deduct from nation's resource stock

**Deliverable**: Complete battle aftermath tracking — losses, repairs, territory, raids.

---

## Phase 4: Morale Tab

Stress and homeland zone management for Phase 6.

### Stress Sources (all feed into the stress track)
- **Casualties**: pull casualty points from battle tab → convert via chart (max 6/round)
- **Territory loss**: SV of lost territories (from battle tab)
- **Soviet-Japanese Pact breaking**: 6 stress for the breaker + no medals from opponent's territories that round
- **Neutral invasion**: 1 stress per neutral territory (first time only)

### Step 1: Sum Stress
- Auto-sum all stress sources for the round
- Add to existing stress on track

### Step 2: Cancel Stress
- Spend medals (1:1 stress reduction)
- Spend civilian goods (1:1 stress reduction)

### Step 3: Zone Evaluation
- Compare stress vs nation threshold
- Auto-advance zones when stress ≥ threshold
- Reduce stress by threshold on each advance
- Repeat if still over threshold

### Step 4: Zone Relief
- Spend medals/civilian goods = threshold to slide back 1 zone
- Max 1 zone relief per round, can't go past White

### Step 5: Zone Penalties
- Display active penalties (cumulative) per nation
- Enforce: Blue (pay 3), Yellow (no rails/ports/sea trade), Orange (−3 orders), Red (no income), Gray (desertion)

**Deliverable**: Full morale lifecycle — stress accumulation, cancellation, zone changes, penalties.

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
| 1. Foundation | Not started | |
| 2. Economy Tab | Not started | |
| 3. Battle Tab | Not started | |
| 4. Morale Tab | Not started | |
| 5. Dashboard Tab | Not started | |
| 6. Polish & Theming | Not started | |
