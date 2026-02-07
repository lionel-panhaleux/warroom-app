# CLAUDE.md — keep this file short and token-efficient

## What
PWA assistant for War Room board game (Larry Harris, 2nd Ed). Single shared device, Global War scenario, offline-first.

## MVP
1. Resource tracking (Oil/Iron/OSR per nation)
2. Morale & stress tracking (casualties → stress → homeland zones)
3. Phase assistance (Phase 1: Economy, Phase 6: Morale, Phase 7: Production)
4. Battle loss recording (feeds morale)

## Stack
Vanilla JS, no build step, no deps. Single index.html, service worker, localStorage. Mobile-first CSS.

## Structure
```
index.html / manifest.json / sw.js
css/style.css
js/app.js          init + tab routing
js/state.js        localStorage, getState/setState, undo
js/data.js         static game data (nations, costs, thresholds, zones)
js/ui.js           shared UI helpers
js/phases/         tab modules (dashboard, economy, battle, morale)
references/        rules PDFs + parsed markdown refs
```

## Conventions
- `data-` attributes for DOM binding, no virtual DOM
- CSS custom properties for nation colors
- Central `setState()`/`getState()` pattern
- Small pure functions, comments only where non-obvious
- No external deps, test on mobile Safari + Chrome
- Always use context7 MCP for technical documentation lookups

## Key refs
- `PLAN.md` — development roadmap & progress tracker
- `references/game-overview.md` — condensed mechanics
- `references/game-data.md` — nations, unit costs, zones, thresholds
- `references/complete_rules.md` — full rules (parsed from PDF)
- `references/*.pdf` — official rulebook + FAQ
