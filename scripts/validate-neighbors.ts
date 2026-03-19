#!/usr/bin/env npx tsx
/**
 * Validates that generated territory paths match the expected NEIGHBORS data.
 * Checks which territories actually touch (share boundary or are within threshold).
 */
import { readFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

// Parse SVG path to extract all points
function pathToPoints(d: string): [number, number][] {
  const points: [number, number][] = []
  const commands = d.match(/[MLHVCSQTAZ][^MLHVCSQTAZ]*/gi) || []
  let cx = 0, cy = 0
  for (const cmd of commands) {
    const type = cmd[0]
    const nums = cmd.slice(1).trim().split(/[\s,]+/).map(Number)
    if (type === 'M' || type === 'L') {
      for (let i = 0; i < nums.length; i += 2) {
        cx = nums[i]; cy = nums[i + 1]
        points.push([cx, cy])
      }
    } else if (type === 'm') {
      // relative move (used in circle paths)
      for (let i = 0; i < nums.length; i += 2) {
        cx += nums[i]; cy += nums[i + 1]
        points.push([cx, cy])
      }
    } else if (type === 'l') {
      for (let i = 0; i < nums.length; i += 2) {
        cx += nums[i]; cy += nums[i + 1]
        points.push([cx, cy])
      }
    } else if (type === 'a' || type === 'A') {
      // Arc — just track endpoint
      if (nums.length >= 7) {
        if (type === 'a') { cx += nums[5]; cy += nums[6] }
        else { cx = nums[5]; cy = nums[6] }
        points.push([cx, cy])
      }
    }
    // Z closes path — no new point needed
  }
  return points
}

// Compute bounding box of a set of points
function bbox(points: [number, number][]): [number, number, number, number] {
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity
  for (const [x, y] of points) {
    if (x < minX) minX = x; if (y < minY) minY = y
    if (x > maxX) maxX = x; if (y > maxY) maxY = y
  }
  return [minX, minY, maxX, maxY]
}

// Check if two bounding boxes are close enough to potentially touch
function bboxesClose(a: [number, number, number, number], b: [number, number, number, number], threshold: number): boolean {
  return !(a[2] + threshold < b[0] || b[2] + threshold < a[0] ||
           a[3] + threshold < b[1] || b[3] + threshold < a[1])
}

// Minimum distance between two point sets (sampled)
function minDistance(a: [number, number][], b: [number, number][]): number {
  let min = Infinity
  // Sample at most 200 points from each for performance
  const sampleA = a.length > 200 ? a.filter((_, i) => i % Math.ceil(a.length / 200) === 0) : a
  const sampleB = b.length > 200 ? b.filter((_, i) => i % Math.ceil(b.length / 200) === 0) : b
  for (const [ax, ay] of sampleA) {
    for (const [bx, by] of sampleB) {
      const d = Math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
      if (d < min) min = d
    }
  }
  return min
}

// Load data
const data = JSON.parse(readFileSync(join(__dirname, 'map-paths-data.json'), 'utf8'))
const neighbors = JSON.parse(readFileSync(join(__dirname, 'neighbors.json'), 'utf8'))

const TERRITORY_PATHS: Record<string, string> = data.TERRITORY_PATHS
const TERRITORY_CENTERS: Record<string, [number, number]> = data.TERRITORY_CENTERS

// Parse all territory paths to points + bbox
const terrPoints: Record<string, [number, number][]> = {}
const terrBbox: Record<string, [number, number, number, number]> = {}
for (const [code, d] of Object.entries(TERRITORY_PATHS)) {
  const pts = pathToPoints(d)
  terrPoints[code] = pts
  terrBbox[code] = bbox(pts)
}

// Adjacency threshold (pixels) — territories "touch" if within this distance
const TOUCH_THRESHOLD = 5 // px

// Check all land-land pairs
const codes = Object.keys(TERRITORY_PATHS).sort()
const actualNeighbors = new Set<string>()

console.log('Checking territory adjacency...')
for (let i = 0; i < codes.length; i++) {
  for (let j = i + 1; j < codes.length; j++) {
    const a = codes[i], b = codes[j]
    if (!bboxesClose(terrBbox[a], terrBbox[b], TOUCH_THRESHOLD)) continue
    const dist = minDistance(terrPoints[a], terrPoints[b])
    if (dist <= TOUCH_THRESHOLD) {
      const pair = [a, b].sort().join('-')
      actualNeighbors.add(pair)
    }
  }
}

// Compare with expected
const expectedLandLand = new Set<string>(neighbors.landLandPairs as string[])

// Also need to check impassable terrain adjacency
const impassable = neighbors.impassable as Record<string, string[]>

// Territories that should NOT touch because impassable terrain separates them
// (This is complex — for now just report missing/extra neighbors)

const missing: string[] = []
const extra: string[] = []

for (const pair of expectedLandLand) {
  if (!actualNeighbors.has(pair)) missing.push(pair)
}

for (const pair of actualNeighbors) {
  if (!expectedLandLand.has(pair)) extra.push(pair)
}

console.log(`\n=== RESULTS ===`)
console.log(`Expected land-land pairs: ${expectedLandLand.size}`)
console.log(`Actual touching pairs: ${actualNeighbors.size}`)
console.log(`\nMISSING (expected but not touching): ${missing.length}`)
for (const p of missing.sort()) {
  const [a, b] = p.split('-')
  const ca = TERRITORY_CENTERS[a], cb = TERRITORY_CENTERS[b]
  const dist = ca && cb ? Math.round(Math.sqrt((ca[0] - cb[0]) ** 2 + (ca[1] - cb[1]) ** 2)) : '?'
  console.log(`  ${p}  (center dist: ${dist}px)`)
}

console.log(`\nEXTRA (touching but not expected): ${extra.length}`)
for (const p of extra.sort()) {
  // Check if this pair is separated by impassable terrain
  let reason = ''
  for (const [name, terrs] of Object.entries(impassable)) {
    const [a, b] = p.split('-')
    if (terrs.includes(a) && terrs.includes(b)) {
      reason = ` ← should be separated by ${name}`
    }
  }
  console.log(`  ${p}${reason}`)
}
