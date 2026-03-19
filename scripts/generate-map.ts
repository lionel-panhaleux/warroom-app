#!/usr/bin/env npx tsx
/**
 * Build script: generates src/lib/map-paths.ts from Natural Earth geodata.
 * Run: npx tsx scripts/generate-map.ts
 */
import { readFileSync, writeFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
import * as d3Geo from 'd3-geo'
import * as topojsonServer from 'topojson-server'
import * as topojsonClient from 'topojson-client'
import * as topojsonSimplify from 'topojson-simplify'
import * as turf from '@turf/turf'
import { Delaunay } from 'd3-delaunay'
import { TERRITORY_GEO, IMPASSABLE_TERRAIN, type GeoMapping, type Bbox } from './territory-geo-mapping'

const __dirname = dirname(fileURLToPath(import.meta.url))
const GEODATA_DIR = join(__dirname, 'geodata')

// ─── Load GeoJSON ────────────────────────────────────────────────────
type GeoFeature = GeoJSON.Feature<GeoJSON.Geometry, Record<string, unknown>>
type GeoFC = GeoJSON.FeatureCollection<GeoJSON.Geometry, Record<string, unknown>>

function loadJSON(path: string): GeoFC {
  return JSON.parse(readFileSync(path, 'utf8'))
}

const admin0 = loadJSON(join(GEODATA_DIR, 'admin0.geojson'))
const admin1 = loadJSON(join(GEODATA_DIR, 'admin1.geojson'))

// ─── Pre-simplify ────────────────────────────────────────────────────
function simplifyFC(fc: GeoFC, weight: number): GeoFC {
  const topo = topojsonServer.topology({ data: fc })
  const simplified = topojsonSimplify.presimplify(topo)
  const minWeight = topojsonSimplify.quantile(simplified, weight)
  const result = topojsonSimplify.simplify(simplified, minWeight)
  return topojsonClient.feature(result, result.objects.data) as GeoFC
}

console.log('Simplifying geodata...')
const admin0s = simplifyFC(admin0, 0.08)
const admin1s = simplifyFC(admin1, 0.08)

// Build lookup maps
const admin0ByCode = new Map<string, GeoFeature>()
for (const f of admin0s.features) {
  const code = (f.properties.ADM0_A3 || f.properties.ISO_A3) as string
  if (code && code !== '-99') admin0ByCode.set(code, f)
  const iso = f.properties.ISO_A3 as string
  if (iso && iso !== '-99' && iso !== code) admin0ByCode.set(iso, f)
}

const admin1ByCode = new Map<string, GeoFeature>()
for (const f of admin1s.features) {
  const code = f.properties.iso_3166_2 as string
  if (code) admin1ByCode.set(code, f)
}

// ─── Projection ──────────────────────────────────────────────────────
const SIZE = 800
const projection = d3Geo.geoAzimuthalEquidistant()
  .rotate([0, -90, 0])
  .clipAngle(165)
  .translate([SIZE / 2, SIZE / 2])
  .scale(SIZE / 4.2)

const pathGen = d3Geo.geoPath(projection)

// ─── Helpers ─────────────────────────────────────────────────────────

/** Reverse all ring coordinate arrays to fix winding for d3-geo */
function reverseRings(geom: GeoJSON.Geometry): GeoJSON.Geometry {
  if (geom.type === 'Polygon') {
    return { ...geom, coordinates: geom.coordinates.map(ring => [...ring].reverse()) }
  }
  if (geom.type === 'MultiPolygon') {
    return { ...geom, coordinates: geom.coordinates.map(poly => poly.map(ring => [...ring].reverse())) }
  }
  return geom
}

/** Ensure geometry has correct winding for d3-geo (exterior CCW on sphere, area < 2π) */
function fixWinding(geom: GeoJSON.Geometry): GeoJSON.Geometry {
  const area = d3Geo.geoArea(geom)
  if (area > 2 * Math.PI) {
    // Inverted — covers more than half the sphere, reverse rings
    return reverseRings(geom)
  }
  return geom
}

function mergeFeatures(features: GeoFeature[]): GeoJSON.Geometry | null {
  if (features.length === 0) return null
  if (features.length === 1) {
    return fixWinding(features[0].geometry)
  }
  const fc: GeoFC = { type: 'FeatureCollection', features }
  const topo = topojsonServer.topology({ merged: fc })
  const merged = topojsonClient.merge(
    topo,
    topo.objects.merged.type === 'GeometryCollection'
      ? topo.objects.merged.geometries
      : [topo.objects.merged]
  )
  if (!merged) return null
  return fixWinding(merged)
}

function clipGeomToBbox(geom: GeoJSON.Geometry, bbox: Bbox): GeoJSON.Geometry | null {
  const [minLon, minLat, maxLon, maxLat] = bbox
  const bboxPoly = turf.bboxPolygon([minLon, minLat, maxLon, maxLat])
  try {
    const feature = turf.feature(geom)
    const clipped = turf.intersect(turf.featureCollection([feature as any, bboxPoly]))
    if (!clipped) return null
    return fixWinding(clipped.geometry)
  } catch {
    return geom // fallback if intersection fails
  }
}

function lookupAdmin0(codes: string[]): GeoFeature[] {
  return codes.map(c => admin0ByCode.get(c)).filter((f): f is GeoFeature => f != null)
}

function lookupAdmin1(codes: string[]): GeoFeature[] {
  return codes.map(c => admin1ByCode.get(c)).filter((f): f is GeoFeature => f != null)
}

// ─── Resolve territory mapping to geometry ───────────────────────────
function resolveMapping(code: string, mapping: GeoMapping): GeoJSON.Geometry | null {
  switch (mapping.type) {
    case 'countries': {
      const feats = lookupAdmin0(mapping.codes)
      if (!feats.length) { console.warn(`  [${code}] No admin0 features for: ${mapping.codes}`); return null }
      return mergeFeatures(feats)
    }
    case 'countriesClip': {
      const feats = lookupAdmin0(mapping.codes)
      if (!feats.length) { console.warn(`  [${code}] No admin0 features for: ${mapping.codes}`); return null }
      const merged = mergeFeatures(feats)
      return merged ? clipGeomToBbox(merged, mapping.bbox) : null
    }
    case 'admin1': {
      const feats = lookupAdmin1(mapping.codes)
      if (!feats.length) { console.warn(`  [${code}] No admin1 features for: ${mapping.codes}`); return null }
      return mergeFeatures(feats)
    }
    case 'admin1Clip': {
      const feats = lookupAdmin1(mapping.codes)
      if (!feats.length) { console.warn(`  [${code}] No admin1 features for: ${mapping.codes}`); return null }
      const merged = mergeFeatures(feats)
      return merged ? clipGeomToBbox(merged, mapping.bbox) : null
    }
    case 'admin1+countries': {
      const a1 = lookupAdmin1(mapping.admin1.codes)
      const a0 = lookupAdmin0(mapping.countries)
      const all = [...a1, ...a0]
      if (!all.length) { console.warn(`  [${code}] No features for admin1+countries`); return null }
      return mergeFeatures(all)
    }
    case 'admin1+countriesClip': {
      const a1 = lookupAdmin1(mapping.admin1.codes)
      const a0 = lookupAdmin0(mapping.countries)
      const all = [...a1, ...a0]
      if (!all.length) { console.warn(`  [${code}] No features`); return null }
      const merged = mergeFeatures(all)
      return merged ? clipGeomToBbox(merged, mapping.bbox) : null
    }
    case 'point': {
      const r = mapping.r || 1.5
      return d3Geo.geoCircle().center([mapping.lon, mapping.lat]).radius(r)()
    }
  }
}

// ─── Small island threshold: if projected area < N px², render as circle ─
const MIN_AREA_FOR_SHAPE = 80 // px² — below this, use a circle marker

// ─── Process all territories ─────────────────────────────────────────
console.log('Generating territory paths...')

const paths: Record<string, string> = {}
const centers: Record<string, [number, number]> = {}
const isIsland: Record<string, boolean> = {}
let missing = 0

for (const [code, mapping] of Object.entries(TERRITORY_GEO)) {
  const geom = resolveMapping(code, mapping)
  if (!geom) { missing++; continue }

  // Check if it's a small feature that should be a circle
  const area = pathGen.area(geom)
  const isSmall = area < MIN_AREA_FOR_SHAPE && mapping.type !== 'point'

  if (mapping.type !== 'point' && area < 500) {
    console.log(`  [${code}] Small area: ${area.toFixed(1)} px²`)
  }
  if (isSmall || mapping.type === 'point') {
    // Render as clean circle
    const centroid = pathGen.centroid(geom)
    if (!centroid || !isFinite(centroid[0])) { missing++; continue }
    const r = mapping.type === 'point' ? (mapping.r || 1.5) : 1.5
    // Project a circle at this point
    const projCenter = centroid
    const svgR = Math.max(4, Math.sqrt(area / Math.PI) || 4) // at least 4px radius
    // Create SVG circle path
    paths[code] = `M${Math.round(projCenter[0])},${Math.round(projCenter[1])}m-${Math.round(svgR)},0a${Math.round(svgR)},${Math.round(svgR)},0,1,0,${Math.round(svgR * 2)},0a${Math.round(svgR)},${Math.round(svgR)},0,1,0,-${Math.round(svgR * 2)},0`
    centers[code] = [Math.round(projCenter[0]), Math.round(projCenter[1])]
    isIsland[code] = true
  } else {
    const d = pathGen(geom)
    if (!d) { console.warn(`  [${code}] Path generation returned null`); missing++; continue }
    paths[code] = d
    const centroid = pathGen.centroid(geom)
    if (centroid && isFinite(centroid[0])) {
      centers[code] = [Math.round(centroid[0]), Math.round(centroid[1])]
    }
  }
}

// ─── Impassable terrain paths ────────────────────────────────────────
console.log('Generating impassable terrain...')
const terrainPaths: Record<string, string> = {}
for (const [name, points] of Object.entries(IMPASSABLE_TERRAIN)) {
  const projected = points.map(([lon, lat]) => projection([lon, lat]))
  if (projected.some(p => !p)) continue
  const d = projected.map((p, i) => {
    const [x, y] = p!
    return (i === 0 ? 'M' : 'L') + Math.round(x) + ',' + Math.round(y)
  }).join('')
  terrainPaths[name] = d
}

// ─── Sea zone Voronoi ────────────────────────────────────────────────
console.log('Generating sea zones...')

// Approximate geographic centers [lon, lat] for each sea zone
const SEA_ZONE_CENTERS: Record<string, [number, number]> = {
  // Atlantic
  A1:  [-55, 48],  A2:  [-42, 60],  A3:  [10, 72],   A4:  [80, 80],
  A5:  [22, 58],   A6:  [3, 56],    A7:  [-15, 45],  A8:  [-28, 55],
  A9:  [-52, 40],  A10: [-88, 24],  A11: [-72, 18],  A12: [-58, 5],
  A13: [-28, 0],   A14: [-22, 18],  A15: [-8, 34],   A16: [-12, 2],
  A17: [4, -8],    A18: [8, -25],   A19: [42, -18],
  // Mediterranean
  M1:  [2, 38],    M2:  [16, 36],   M3:  [30, 34],   M4:  [35, 44],
  M5:  [38, 18],   M6:  [58, 25],
  // Indian Ocean
  I1:  [63, 12],   I2:  [86, 8],    I3:  [55, -8],   I4:  [44, -26],
  I5:  [65, -20],  I6:  [88, -15],  I7:  [80, 3],    I8:  [95, -28],
  I9:  [100, 2],   I10: [93, 13],
  // Pacific
  P0:  [132, 38],  P1:  [152, 52],  P2:  [175, 38],  P3:  [-162, 42],
  P4:  [-145, 55], P5:  [-125, 30], P6:  [-108, 16], P7:  [-95, 6],
  P8:  [-115, -8], P9:  [-155, 22], P10: [-178, 25], P11: [172, 12],
  P12: [153, 5],   P13: [143, 10],  P14: [128, 18],  P15: [112, 4],
  P16: [120, -5],  P17: [135, -12], P18: [158, -18], P19: [172, -25],
  P20: [-178, -35],
}

// Project sea zone centers to pixel coordinates
const seaCentersPixel: Record<string, [number, number]> = {}
for (const [code, [lon, lat]] of Object.entries(SEA_ZONE_CENTERS)) {
  const p = projection([lon, lat])
  if (p) seaCentersPixel[code] = [Math.round(p[0]), Math.round(p[1])]
}

// Build Voronoi from sea zone + land territory centers
// Land centers are "phantom" — their cells get discarded, but they push sea zones away
const seaCodes = Object.keys(seaCentersPixel).sort()
const landCodes = Object.keys(centers).sort()
const allPoints: [number, number][] = []
const pointLabels: string[] = []
for (const c of seaCodes) { allPoints.push(seaCentersPixel[c]); pointLabels.push(c) }
for (const c of landCodes) { allPoints.push(centers[c]); pointLabels.push(c) }

const delaunay = Delaunay.from(allPoints)
const voronoi = delaunay.voronoi([0, 0, SIZE, SIZE])

// Circular clip polygon (map boundary, 128 segments)
const mapCenter: [number, number] = [SIZE / 2, SIZE / 2]
const edgePoint = projection([0, -75])
const mapRadius = edgePoint
  ? Math.sqrt((edgePoint[0] - mapCenter[0]) ** 2 + (edgePoint[1] - mapCenter[1]) ** 2)
  : SIZE / 2 - 10
const circleRing: [number, number][] = []
for (let i = 0; i < 128; i++) {
  const a = (2 * Math.PI * i) / 128
  circleRing.push([mapCenter[0] + mapRadius * Math.cos(a), mapCenter[1] + mapRadius * Math.sin(a)])
}
const circleGeoJSON = turf.polygon([[...circleRing, circleRing[0]]])

// Generate sea zone paths by clipping Voronoi cells to map circle
const seaPaths: Record<string, string> = {}
const seaCentersFinal: Record<string, [number, number]> = {}
for (let i = 0; i < seaCodes.length; i++) {
  const code = seaCodes[i]
  const cell = voronoi.cellPolygon(i)
  if (!cell) continue
  const cellPoly = turf.polygon([cell])
  try {
    const clipped = turf.intersect(turf.featureCollection([cellPoly, circleGeoJSON]))
    if (!clipped) continue
    const coords = clipped.geometry.type === 'MultiPolygon'
      ? clipped.geometry.coordinates : [clipped.geometry.coordinates]
    let d = ''
    for (const poly of coords) {
      for (const ring of poly) {
        d += ring.map((pt, j) =>
          (j === 0 ? 'M' : 'L') + Math.round(pt[0]) + ',' + Math.round(pt[1])
        ).join('') + 'Z'
      }
    }
    seaPaths[code] = d
    seaCentersFinal[code] = seaCentersPixel[code]
  } catch { console.warn(`  [${code}] Voronoi clip failed`) }
}
console.log(`  Generated ${Object.keys(seaPaths).length} sea zone paths.`)

// ─── Generate map outline ────────────────────────────────────────────
const outline = pathGen(d3Geo.geoCircle().center([0, 90]).radius(165)()) || ''

// ─── Round path coordinates ──────────────────────────────────────────
function roundPath(d: string): string {
  return d.replace(/(\d+)\.\d+/g, '$1')
}

for (const code of Object.keys(paths)) {
  if (!isIsland[code]) paths[code] = roundPath(paths[code])
}
const roundedOutline = roundPath(outline)

// ─── Write TypeScript output ─────────────────────────────────────────
const outPath = join(__dirname, '..', 'src', 'lib', 'map-paths.ts')
const lines: string[] = [
  '// Auto-generated by scripts/generate-map.ts — DO NOT EDIT',
  '',
  `export const MAP_VIEWBOX = '0 0 ${SIZE} ${SIZE}'`,
  '',
  `export const MAP_OUTLINE = '${roundedOutline}'`,
  '',
  'export const TERRITORY_PATHS: Record<string, string> = {',
]
const sortedCodes = Object.keys(paths).sort()
for (const code of sortedCodes) {
  lines.push(`  ${code}: '${paths[code]}',`)
}
lines.push('}')
lines.push('')
lines.push('export const TERRITORY_CENTERS: Record<string, [number, number]> = {')
for (const code of sortedCodes) {
  if (centers[code]) lines.push(`  ${code}: [${centers[code][0]}, ${centers[code][1]}],`)
}
lines.push('}')
lines.push('')
lines.push('export const IMPASSABLE_PATHS: Record<string, string> = {')
for (const [name, d] of Object.entries(terrainPaths)) {
  lines.push(`  '${name}': '${d}',`)
}
lines.push('}')
lines.push('')
const sortedSeaCodes = Object.keys(seaPaths).sort()
lines.push('export const SEA_ZONE_PATHS: Record<string, string> = {')
for (const code of sortedSeaCodes) {
  lines.push(`  ${code}: '${seaPaths[code]}',`)
}
lines.push('}')
lines.push('')
lines.push('export const SEA_ZONE_CENTERS: Record<string, [number, number]> = {')
for (const code of sortedSeaCodes) {
  if (seaCentersFinal[code]) lines.push(`  ${code}: [${seaCentersFinal[code][0]}, ${seaCentersFinal[code][1]}],`)
}
lines.push('}')
lines.push('')

const output = lines.join('\n')
writeFileSync(outPath, output, 'utf8')

// ─── Write JSON for preview ─────────────────────────────────────────
const jsonPath = join(__dirname, 'map-paths-data.json')
writeFileSync(jsonPath, JSON.stringify({
  MAP_OUTLINE: roundedOutline,
  TERRITORY_PATHS: Object.fromEntries(sortedCodes.map(c => [c, paths[c]])),
  TERRITORY_CENTERS: Object.fromEntries(sortedCodes.filter(c => centers[c]).map(c => [c, centers[c]])),
  IMPASSABLE_PATHS: terrainPaths,
  SEA_ZONE_PATHS: seaPaths,
  SEA_ZONE_CENTERS: seaCentersFinal,
}), 'utf8')

console.log(`\nDone! Generated ${sortedCodes.length} territory paths + ${sortedSeaCodes.length} sea zones.`)
if (missing > 0) console.warn(`Warning: ${missing} territories had no geometry.`)
console.log(`Output: ${outPath} (${(output.length / 1024).toFixed(1)} KB)`)
