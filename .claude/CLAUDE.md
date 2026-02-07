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
js/app.js          init + routing
js/state.js        localStorage state
js/data.js         static game data (nations, costs, thresholds)
js/phases/         phase-specific modules
references/        rules PDFs + game-overview.md + game-data.md
```

## Conventions
- `data-` attributes for DOM binding, no virtual DOM
- CSS custom properties for nation colors
- Central `setState()`/`getState()` pattern
- Small pure functions, comments only where non-obvious
- No external deps, test on mobile Safari + Chrome

## Key rules refs
- `references/game-overview.md` — condensed mechanics
- `references/game-data.md` — nations, unit costs, zones, thresholds
- `references/*.pdf` — official rulebook + FAQ
