# War Room Assistant

Offline-first Progressive Web App to assist players of [War Room](https://www.nightingale-games.com/) (Larry Harris, 2nd Edition) at the table.

Designed for a single shared mobile device during a game session.

## Features

- **Resource Tracking** — Oil, Iron, OSR per nation with income tallying
- **Morale Management** — Casualty conversion, stress tracking, homeland status zones, medals
- **Phase Guidance** — Step-by-step assistance for National Economy, Morale, and Production phases
- **Battle Loss Recording** — Track eliminated units for morale calculations

## Running Locally

Serve the directory with any static file server:

```sh
# Python
python3 -m http.server 8000

# Node
npx serve .
```

Open `http://localhost:8000` on your phone (same network) or desktop browser.

## Installing as PWA

On mobile, use "Add to Home Screen" from the browser menu. The app works fully offline once installed.

## Architecture

Single-page vanilla JS app. No build step, no dependencies.

```
index.html          App shell
manifest.json       PWA manifest
sw.js               Service worker (offline caching)
css/style.css       Styles (mobile-first)
js/app.js           App init and navigation
js/state.js         Game state (localStorage)
js/data.js          Static game data
js/phases/          Phase-specific modules
```

## Game Reference

- `references/game-overview.md` — Condensed mechanics relevant to the app
- `references/WR_RULES_2ND_EDITION_V27u-compressed.pdf` — Official rulebook
- `references/War_Room_FAQ_v2_2023.pdf` — Official FAQ & errata

## Scope

Currently supports the **Global War** scenario only (all 7 nations).
