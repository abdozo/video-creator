---
name: whiteboard-template
description: Apply the code-native modern editorial-sketchbook whiteboard template to a Remotion Short or regular video. Use for whiteboard animation, animated ink, hand-drawn explanation, book summaries, self-help summaries, concept maps, or sketch-style educational videos. Produces SVG/TSX path animation without a stock drawing hand or generated raster doodles.
---

# Modern Whiteboard Template

Use with `$make-short` or `$make-video`. Read `remotion/src/lib/whiteboard.tsx` before authoring.

## Visual contract

- Cool paper `#F3F6F4`, graphite `#1E2926`, muted ink `#74817D`, indigo `#6366F1`, teal
  `#4DB8A8`, and restrained amber `#D89043`.
- Space Grotesk for statements, Inter for explanation, Source Serif 4 only for verified quotations.
- Use the indigo `IdeaThread` as the signature: it becomes an underline, connector, path, divider,
  or synthesis mark across scenes.
- Draw with `InkPath`/`evolvePath()`. Use an occasional pen-tip cursor, never a stock human hand.
- Prefer custom diagrams and character glyphs. Do not fill space with generic icon doodles.
- Use seeded or fixed variation only; every frame must be deterministic.

## Format behavior

- Shorts: one dominant concept at a time, large strokes, very little simultaneous detail.
- Videos: chaptered board regions, persistent diagrams, camera travel, and deliberate clean-board
  resets. Maintain a visual thread across chapters.
- Raster assets are optional. Follow `$imagegen` only when a real image is required; code-native
  diagrams must remain SVG/TSX.

## Sound

Sparse only: occasional pencil stroke, paper movement, soft tap, or chapter cue. Reuse the catalog;
import a missing licensed asset with `tools/import_audio.py` and record its provenance.

## QA

Inspect each important path at 0%, midpoint, and completion; verify erase masks, text wrapping,
camera framing, attribution, and that the canvas never becomes an unstructured doodle wall.
