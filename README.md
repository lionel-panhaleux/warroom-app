# War Room Assistant

Offline-first Progressive Web App to assist players of [War Room](https://www.nightingale-games.com/) (Larry Harris, 2nd Edition) at the table.

Designed for a single shared mobile device during a game session.

## Features

- **Resource Tracking** — Oil, Iron, OSR per nation with territory-based income
- **Economy Phase** — Income collection, oil bidding, turn order
- **Battle Recording** — Unit losses, casualty points, territory captures, medals, raids
- **Morale Management** — Casualty→stress conversion, zone evaluation, relief, penalties
- **Production** — Unit orders, trade, civilian goods, bomb repair
- **Phase Gating** — Guided round flow: income → bidding → morale → production
- **131 Territories** — Searchable/filterable, owner changes, embattled tracking
- **Offline PWA** — Works fully offline once installed

## Tech Stack

Svelte 5 + Vite + TypeScript + Tailwind CSS v4 + vite-plugin-pwa

## Running Locally

```sh
npm install
npm run dev
```

## Installing as PWA

On mobile, use "Add to Home Screen" from the browser menu. The app works fully offline once installed.

## Game Reference

- `references/game-overview.md` — Condensed mechanics relevant to the app
- `references/game-data.md` — Nations, unit costs, zones, thresholds
- `references/complete_rules.md` — Full rules (parsed from PDF)

## Development

See [`PLAN.md`](PLAN.md) for the development roadmap and progress tracker.

## Scope

Currently supports the **Global War** scenario only (all 7 nations).
