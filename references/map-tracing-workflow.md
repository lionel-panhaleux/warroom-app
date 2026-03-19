# Map Tracing Workflow (Inkscape)

Manual tracing of War Room board map territory borders as clean SVG paths.

## Setup

1. Photograph bare board from directly above, even lighting, no pieces
2. File > Import the reference image
3. Lock image layer (padlock icon) to prevent accidental moves
4. Create new layer "borders" above it

## Tracing

- **Bezier pen tool** (`B`) — click to place nodes, click+drag for curves
- **Enable snapping** (`%`) → "Snap to nodes" + "Snap to paths" so adjacent territories share exact border points
- Trace borders as open paths (not closed polygons) — each border segment drawn once
- Press `Enter` to finish a path, `Escape` to cancel
- **Node tool** (`N`) to adjust points after placing

## Recommended order

1. Outer circle (map edge)
2. Major continental coastlines
3. Inland borders (often straighter, faster)
4. Sea zone boundaries

## Display while tracing

- Stroke: 2px visible color (red), no fill
- Zoom 200-400% for accuracy

## Export

- Delete image layer
- Select all > Path > Combine (or keep separate per territory)
- Save as plain SVG
