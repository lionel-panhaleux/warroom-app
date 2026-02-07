# War Room — Game Overview for App Development

Condensed reference of mechanics relevant to the app. Verified against the 2nd Edition rulebook (2025 update) and FAQ v2. For full rules, see `complete_rules.md` or the official PDF.

---

## Game Structure

A round has **7 phases**, executed in order.

### Phase 1: Direct National Economy

1. **Check Territory Card facing** — Embattled territories (red/white stripes) produce reduced income. Restore cards that are no longer Embattled/Active.
   - **Exception:** A Collapsed Nation's Territory Cards are permanently Embattled regardless of controller.
2. **Tally resource income** — Each Nation sums Oil, Iron, OSR from Territory Cards and adds to existing stock on Resource Chart. Resources are cumulative and public.

**China:** Cannot gain or spend Oil. Cannot trade at all. Cannot enter sea regions. Cannot capture Air or Naval Units. Can only build Artillery if it controls an Industrial territory (e.g., Peiping).

### Phase 2: Strategic Planning

1. **Write movement orders** (secret, on O&P Charts). Max **9 orders** (6 for China/Italy). Multiple orders for the same Command in the same round are forbidden (only the first is executed).
2. **Bid Oil** for turn order. China bids 0. No upper limit on bids.
3. **Pay Oil bids** (all bids paid, win or lose). Establish turn order (descending Oil bid; ties drawn randomly). Turn Order Rank is the universal tie-breaker.

### Phase 3: Movement Operations

1. **Flip Embattled Hotspots** to Active side.
2. **Execute orders** in Turn Order. All rows read left to right, row 1 to row 3.
3. **Place Hotspot Markers** on Active regions (conflicts, Convoy Raids, Embattled carry-overs).
4. **Carrier Fighter Movement** — each Carrier may launch 1 Carrier Fighter to its sea region or an adjacent region. No orders needed. They never pin nor are pinned.

**Movement rules:**
- **Land Commands**: 1 adjacent territory, or unlimited distance via connected Friendly Rail. Rail blocked by Bomb Tokens, Enemy territories, Enemy Land Units, or Yellow Zone.
- **Troop Transports** (Land at sea): up to 2 sea regions if both moves end at sea; 1 adjacent territory when going ashore. Pinned by unmatched Enemy Naval Units (exception: may ignore pinning to enter adjacent Friendly territory).
- **Air Commands**: 1–2 land/sea regions. Can fly over Enemy territory and impassable regions. Cannot move by Rail. Cannot pin or be pinned.
- **Naval Commands**: 1–2 sea regions. May pin Enemy Naval Units and Troop Transports.

**Pinning:** a Command leaving a region with Enemy Units of the same Category must leave behind Units equal to the Enemy count. Not optional. Forced splits are limited to one split.

### Phase 4: Combat Operations

Resolve Active Hotspots in Turn Order.

**Battle resolution order:**
1. Air Battle Stage → 2. Raids (Strategic Bombing, Convoy) → 3. Surface Battle Stage → 4. Battle Debrief

**Key battle mechanics:**
- Dice rolled in batches of **10** (max **30 per Battle Stage**). Assign damage after each batch.
- Die colors match Unit Types. **Black = wild hit. White = hits only Units with white triangle marker.**
- Damage order: Yellow → Blue → Green → Red → Black → White.
- **Damaged Unit must be eliminated before another in the same row is hit.**
- **Force Advantage** (Surface Stage only): side with more Land/Naval Unit Types. Enemy's black and white results become misses.
- **Port Advantage**: +2 Dice in Surface Stage of sea battles (if Friendly Naval Units present). Free Naval repairs. Requires undamaged, non-Yellow-Zone Port.

**Battle Debrief** (app-relevant steps):
- **Repair damaged units** — 1 Resource each (any type). Free if Port Advantage.
- **Remove eliminated units** — to Casualty List on Morale Board.
- **Check lost Troop Transports** — unguarded at sea = eliminated.
- **Update territory control** — Land Units required; Air Units alone cannot capture.
- **Assign stress** — losing a territory = stress equal to its **SV**. Breaking Soviet-Japanese Pact = 6 stress. Invading a Neutral = 1 stress.
- **Award medals** — 1 Medal per non-capital territory captured, **3 for capitals** (regardless of SV or victory requirement). Never for Neutrals.

### Phase 5: Refit & Deploy

1. **Land Air Commands** — move up to 2 regions, must land in Friendly territory (including Embattled or newly captured). Remove Arrow Tags. Remove all Carrier Fighters to storage.
2. **Deploy new units** — from Industry Tokens placed in Phase 7 of the previous round. Naval Units deploy to Port-connected sea regions.
3. **Reorganize Commands** — merge/split within regions. Max 8 Units per stack.

### Phase 6: Morale

**Convert casualties into stress:**
1. For each Unit Type: count eliminated × casualty point multiplier.
2. Sum all casualty points.
3. Convert to stress via Conversion Chart (max **6 stress from casualties per round**).
4. Add to existing stress on Stress Track.

**Resolve medals and stress points (each step for ALL Nations before next step, in Turn Order):**

**Step 1:** Submit Medals/Civilian Goods to cancel stress (1:1).

**Step 2:** Evaluate stress levels — if stress ≥ threshold, advance 1 Zone, subtract threshold from stress. Repeat if still ≥ threshold. A Nation with no Units and no Territories also advances 1 Zone. Gray Zone cannot advance further.

**Step 3:** Relieve stress — spend Medals/Civilian Goods equal to threshold to slide back 1 Zone (max 1 per round, cannot go past White).

**Step 4:** Apply zone penalties (cumulative, recurring):

| Zone | Effect |
|---|---|
| White | None |
| Blue | Pay 3 Resources (any mix) |
| Yellow | Nation's Rails and Ports disabled. No sea trade. No Port Advantage. |
| Orange | 3 fewer written orders (slash last 3 O&P boxes) |
| Red | Economic collapse — no new Resource income |
| Gray | Desertion — remove Units (excl. units under construction and Carrier Fighters) from map equal to current stress. Stress is NOT reduced. |

### Phase 7: Production

**Step 1:** Mark starting Resources on O&P Chart.

**Step 2:** Purchase units (secret). Trade with Neutrals if applicable (Global War only, 1 trade per nation per round).

**Step 3:** Reveal purchases, validate, update Resource Charts.

**Step 4:** Place new Units in controlled Industrial territories under Industry Tokens. Limited by SV minus Bomb Tokens minus Deferred Units. Naval Units require a Port. Chinese Infantry deploy immediately to Mobilization/Industry territories.

---

## Morale Board Details

### Stress Thresholds (Global War)

| Nation | Threshold |
|---|---|
| China | 4 |
| British Commonwealth | 6 |
| Soviet Union | 6 |
| United States | 5 |
| Germany | 6 |
| Italy | 4 |
| Imperial Japan | 7 |

### Casualty Points Conversion Chart

| Casualty Points | Stress |
|---|---|
| 0–17 | 0 |
| 18–33 | 1 |
| 34–49 | 2 |
| 50–62 | 3 |
| 63–87 | 4 |
| 88–109 | 5 |
| 110+ | 6 (max per round) |

### Medals
- Capture non-capital territory: 1 Medal
- Capture capital territory: 3 Medals
- Medals cancel stress 1:1 or can relieve zone position (spend threshold value to go back 1 Zone)

---

## Victory Conditions (Global War)

- **Axis wins:** Control 2 of 3 Allied capitals (Eastern US, Great Britain, Moscow).
- **Allies win:** Control both Axis capitals (Greater Germany, Japan).
- A Collapsed Nation with an unoccupied Capital counts as captured.
- Victory checked at the end of any game round. If both sides meet conditions simultaneously, continue until only one does.

### Collapsed Nation
A Nation with **no Units on the World Map** AND in the **Gray Zone** at **end of round** is Collapsed. Remove Resource Chart. All its original Territory Cards permanently flip to Embattled. It is no longer Friendly to any Nation.

---

## Nations Summary

### Allied Forces
- **China** — No Oil, no trade, no sea, land-only. Max 6 orders. Special Infantry mobilization. Threshold: 4.
- **British Commonwealth** — Global presence, shared territories with US. Threshold: 6.
- **Soviet Union** — Stalin Doctrine restricts Allied entry into Soviet territories. Soviet-Japanese Non-Aggression Pact. Threshold: 6.
- **United States** — Industrial powerhouse. Threshold: 5.

### Axis Nations
- **Germany** — Central position, strong starting forces. Threshold: 6.
- **Italy** — Max 6 orders, vulnerable position. Threshold: 4.
- **Imperial Japan** — Pacific naval power. Soviet-Japanese Non-Aggression Pact. Threshold: 7.
