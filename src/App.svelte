<script lang="ts">
  import { appState, persist, undo, reloadFromStorage, STORAGE_KEY_EXPORT } from './lib/state.svelte'
  import { uiIcons } from './lib/icons'
  import TabBar from './components/TabBar.svelte'
  import Dashboard from './components/Dashboard.svelte'
  import Economy from './components/Economy.svelte'
  import Battle from './components/Battle.svelte'
  import Morale from './components/Morale.svelte'
  import Production from './components/Production.svelte'

  type Tab = 'dashboard' | 'economy' | 'battle' | 'morale' | 'production'
  let activeTab: Tab = $state('dashboard')

  // Locked tabs based on round phase
  let lockedTabs = $derived.by(() => {
    const phase = appState.game.roundPhase
    const locked = new Set<Tab>()
    if (phase !== 'morale' && phase !== 'production') locked.add('morale')
    if (phase !== 'production') locked.add('production')
    return locked
  })

  // Auto-persist on any state change
  $effect(() => {
    JSON.stringify(appState.game)
    persist()
  })

  // B1: Multi-tab storage conflict detection
  let storageConflict = $state(false)
  $effect(() => {
    function onStorage(e: StorageEvent) {
      if (e.key === STORAGE_KEY_EXPORT && e.newValue) {
        storageConflict = true
      }
    }
    window.addEventListener('storage', onStorage)
    return () => window.removeEventListener('storage', onStorage)
  })

  function reloadState() {
    reloadFromStorage()
    storageConflict = false
  }

  // U3: Toast system for phase transitions
  let toast: { message: string; targetTab: Tab | null } | null = $state(null)
  let toastExiting = $state(false)
  let toastTimer: ReturnType<typeof setTimeout> | null = null

  export function showToast(message: string, targetTab?: Tab) {
    if (toastTimer) clearTimeout(toastTimer)
    toastExiting = false
    toast = { message, targetTab: targetTab ?? null }
    toastTimer = setTimeout(() => {
      toastExiting = true
      setTimeout(() => {
        if (toast?.targetTab) activeTab = toast.targetTab
        toast = null
        toastExiting = false
      }, 200)
    }, 1800)
  }

  function toastClick() {
    if (toastTimer) clearTimeout(toastTimer)
    if (toast?.targetTab) activeTab = toast.targetTab
    toast = null
    toastExiting = false
  }
</script>

<!-- B1: Storage conflict banner -->
{#if storageConflict}
  <div class="fixed top-0 left-0 right-0 z-[60] bg-warning/90 text-bg-primary text-center text-xs py-2 px-4 flex items-center justify-center gap-2"
       style="padding-top: calc(0.5rem + env(safe-area-inset-top, 0px));">
    <span>State changed in another tab</span>
    <button class="font-bold underline" onclick={reloadState}>Reload</button>
    <button class="ml-2 opacity-70" onclick={() => storageConflict = false}>Dismiss</button>
  </div>
{/if}

<!-- U3: Toast -->
{#if toast}
  <button
    class="fixed top-0 left-0 right-0 z-[55] bg-accent/90 text-bg-primary text-center text-sm font-medium py-2.5 px-4 cursor-pointer {toastExiting ? 'toast-exit' : 'toast-enter'}"
    style="padding-top: calc(0.625rem + env(safe-area-inset-top, 0px));"
    onclick={toastClick}
  >
    {toast.message}{#if toast.targetTab} →{/if}
  </button>
{/if}

<!-- U1: Undo bar for non-dashboard tabs -->
{#if activeTab !== 'dashboard' && appState.undoStack.length > 0}
  <div class="flex justify-end mb-2">
    <button
      class="w-8 h-8 flex items-center justify-center rounded-full bg-bg-surface text-text-muted active:bg-accent/30 [&>svg]:w-4 [&>svg]:h-4"
      aria-label="Undo"
      onclick={undo}
    >{@html uiIcons.undo}</button>
  </div>
{/if}

{#if activeTab === 'dashboard'}
  <Dashboard />
{:else if activeTab === 'economy'}
  <Economy {showToast} />
{:else if activeTab === 'battle'}
  <Battle />
{:else if activeTab === 'morale'}
  <Morale {showToast} />
{:else if activeTab === 'production'}
  <Production {showToast} />
{/if}

<TabBar bind:activeTab {lockedTabs} />
