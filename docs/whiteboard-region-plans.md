# Region plans for whiteboard slides

## What the upstream tool provides

A region plan describes the drawing order for one finished image. Each region names an object, its role, its order, and a bounding box. An annotation associates it with narration, and a reveal hint can be `stroke`, `fill`, or `fade`. The named box fields are integers from 0 to 1000, measured from the top-left of the source image. Convert horizontal edges with the source width and vertical edges with the source height. A box provides a location for assigning components to a drawing beat. Component analysis supplies the masks and stroke order. [Region schema and coordinate conversion](https://github.com/masihsultani/whiteboard-animator/blob/main/whiteboard_animator/regions.py), [component scheduling](https://github.com/masihsultani/whiteboard-animator/blob/main/whiteboard_animator/animator.py#L205-L295).

The standard renderer reserves 75% of the scene for drawing when it has a region plan. It divides that time by annotation length and box area, weighted 70% and 30% when annotations exist. The resulting entries carry boxes and start and end times. The reveal hint stays in the source plan while the animator chooses how to reveal detected pixels. The lower-level renderer accepts explicit windows through `element_plan`. The optional Gemini detector sends the image and transcript text to produce region suggestions. [Timing implementation](https://github.com/masihsultani/whiteboard-animator/blob/main/whiteboard_animator/regions.py#L155-L202), [standard renderer](https://github.com/masihsultani/whiteboard-animator/blob/main/whiteboard_animator/render.py#L45-L89), [detector implementation](https://github.com/masihsultani/whiteboard-animator/blob/main/whiteboard_animator/detect_regions.py#L138-L189).

## How it fits Video Factory

Add an optional, editable `regions.json` for raster whiteboard slides. Accept upstream-shaped plans and resolve each region to an explicit cue in `vo[].words` or `vo.gen.ts`. Store the approved cue separately from the annotation so repeated words, paraphrases, and silent slides have a clear manual override. Report unmatched cues for review. Narration preparation stays in `tools/prepare_narration.py`, and initial plans can be imported or authored without a new provider call. [Project contract](../AGENTS.md), [narration preparation](../tools/prepare_narration.py).

Keep Remotion responsible for timing, camera, and compositing. The local `video-11` slide already reveals separate ink and pigment masks using SVG paths in `DrawnSlide.tsx`. Start with a clipped sweep for a simple region and allow a custom mask or path for overlapping art and precise marker motion. Validate box bounds, unique region IDs and order, and cue windows, then render a labeled overlay before animation. A crop around a laptop can also contain a neighboring caption or connector. Reviewing the overlay catches those ownership mistakes early. [Approved style reference](../media/templates/classic-whiteboard/reference.png).

For a pilot, use the existing 1672×941 slide and narration from *Make the First Step Smaller*. The laptop is approximately `{"ymin":568,"xmin":382,"ymax":790,"xmax":530}`. Tie it to the aligned word “Open” at 16.36 seconds. Check the pen at 27.14, the checkmark at 29.66, and the fork branches at 36.92 and 40.76. Compare preview frames immediately before each cue and during its reveal with the current export. The pilot uses the locally rendered video and its existing aligned narration.

## Where upstream rendering could help

Try the offline Python engine on the same slide if automatic pixel tracing would save enough manual path work. Its high-level output is a baked MP4, its standard presets top out at 24 fps, and it downsizes images to a longest side of 1280 px. It also adds scientific Python dependencies and a bundled text detector. An isolated comparison can show whether the gain in automatic tracing is worth those tradeoffs. Keep optional network detection a separate decision because this project reserves `GEMINI_API_KEY` for TTS. Upstream is MIT licensed. [Usage](https://github.com/masihsultani/whiteboard-animator#usage), [license](https://github.com/masihsultani/whiteboard-animator/blob/main/LICENSE), [package dependencies](https://github.com/masihsultani/whiteboard-animator/blob/main/pyproject.toml), [resolution cap](https://github.com/masihsultani/whiteboard-animator/blob/main/whiteboard_animator/animator.py#L182-L189).

## Local render test

Installed `whiteboard-animator[gemini]==0.1.1` under
`.cache/whiteboard-animator/venv`. The test exports are in
`remotion/out/whiteboard-animator-test/`, alongside the authored region and cue JSON.

| Test | Result |
| --- | --- |
| Automatic, approved slide | Recognizable handwriting, contour strokes, and an ochre brush fill. The order followed the page layout, beginning with the headline and revealing the fork before the laptop. |
| Region JSON with existing narration | Better grouping. The laptop started around 12.75s, about 3.6s before “Open.” The headline started at 34.83s, about 20s ahead of the final line. |
| Explicit API cues | The 60s render took 5.9s locally and produced 1280×720 at 30 fps. The laptop and checkmark showed ink at about 16.40s and 29.73s, close to their 16.36s and 29.66s cues. |
| Explicit cues with a separate teal pass | The connected fork was assigned to the earlier cue in the single pass. Separating and compositing the teal branch moved its first visible ink from about 36.93s to 40.80s, close to its 40.76s cue. Both exact-cue exports copied the original AAC packets. |
| Dense illustration and two-scene CLI | The two scenes concatenated successfully. Automatic mode on the dense illustration stayed almost blank through 6s of a 12s test and then drew most of the image quickly. Seven region boxes made it start promptly, but connected artwork still appeared as a large early block. |

The offline text detector ran on both slides. The optional Gemini region detector requires a
separate `GOOGLE_API_KEY` and was unavailable in this test. The tested engine is useful for
quick raster draw-ons on sparse boards. An optional tracing pass with explicit cues and
manual splits for connected objects fits the project better than using the default CLI as
the main renderer.
