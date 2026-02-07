import type { NationId, NationState, GameState, AppState, TerritoryState } from './types'
import { NATION_IDS } from './data'
import { TERRITORIES } from './territories'

const STORAGE_KEY = 'warroom-app-state'
const MAX_UNDO = 20

function defaultNationState(): NationState {
  return { oil: 0, iron: 0, osr: 0, stress: 0, zone: 'White', medals: 0, civilianGoods: 0, casualtyPoints: 0 }
}

function defaultTerritoryStates(): Record<string, TerritoryState> {
  const out: Record<string, TerritoryState> = {}
  for (const t of TERRITORIES) {
    out[t.code] = {
      owner: t.startingOwner,
      embattled: t.code === 'J25', // Solomon Islands embattled at start
    }
  }
  return out
}

function defaultGameState(): GameState {
  const nations = {} as Record<NationId, NationState>
  for (const id of NATION_IDS) nations[id] = defaultNationState()
  return { round: 0, roundPhase: 'income' as const, nations, territories: defaultTerritoryStates() }
}

function migrateState(game: GameState): GameState {
  if (!game.territories) game.territories = defaultTerritoryStates()
  if (!game.roundPhase) (game as any).roundPhase = 'income'
  return game
}

function loadState(): AppState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const state: AppState = JSON.parse(raw)
      state.game = migrateState(state.game)
      return state
    }
  } catch { /* ignore corrupt data */ }
  return { game: defaultGameState(), undoStack: [] }
}

function saveState(state: AppState) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
}

// Reactive shared state — exported as object so mutations propagate
export const appState: AppState = $state(loadState())

/** Update game state, pushing current to undo stack */
export function setState(newGame: GameState) {
  appState.undoStack = [structuredClone($state.snapshot(appState.game)), ...appState.undoStack].slice(0, MAX_UNDO)
  appState.game = newGame
  saveState(appState)
}

/** Pop last undo snapshot */
export function undo() {
  if (appState.undoStack.length === 0) return
  const [prev, ...rest] = appState.undoStack
  appState.game = prev
  appState.undoStack = rest
  saveState(appState)
}

/** Reset to fresh game */
export function resetGame() {
  appState.game = defaultGameState()
  appState.undoStack = []
  saveState(appState)
}

/** Save without undo (for auto-persist from $effect) */
export function persist() {
  saveState(appState)
}
