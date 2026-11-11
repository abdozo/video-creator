# Codex Video Factory

This repository is a Remotion video factory driven primarily by Codex. Run commands from the
repository root. Preserve existing examples and their historical provider metadata.

## Workflow routing

- `$make-short`: vertical 1080x1920 Shorts. Templates: `motion` or `whiteboard`.
- `$make-video`: horizontal 1920x1080 regular YouTube videos. For comic pages, follow [Motion Comic Static](README.md#motion-comic-static) for still art or [Motion Graphic Animated](README.md#motion-graphic-animated) for Rigby2D character and prop animation.
- `$make-ai-short`: optional fal.ai video-model pixels.
- `$make-vox`: optional layered collage.
- `$suggest-sfx`: library-first sound design and mixing.
- `$vidtsx-2d-generator`: Remotion correctness rules for every TSX composition.

Natural-language equivalents such as "make a regular video", "make a whiteboard short", and
"build a video using my narration" should route to the matching skill.

For template listings, use the complete [template catalog](README.md#available-templates).
For company or stock analysis videos, use `$make-video` with `--template company-analysis`
and follow [the Company Analysis guide](media/templates/company-analysis/README.md).
For `lines-anime`, "Lines Anime", or animating a supplied illustration, read
[the Lines Anime guide](media/templates/lines-anime/README.md), then use `$make-short`
or `$make-video` for the requested format with the `motion` scaffold.

## Project contract

- Shorts live in `shorts/short-N-<slug>/`; regular videos in `videos/video-N-<slug>/`.
- Remotion entrypoints live in `remotion/src/shots/<id>/` and export `compositionConfig`.
- `beats.json` carries `format`, `template`, `narration`, `captions`, `vo`, and `beats`.
- Missing new fields in old projects mean legacy Short behavior; do not migrate examples merely
  to make them look current.
- Narration modes are `ai`, `recorded`, and `none`. Caption modes are `none`, `subtitles`, and
  `word-highlight`.

## Provider policy

- `GEMINI_API_KEY` is optional and used only for Gemini TTS.
- `FAL_KEY` is optional and used only for true generative-video clips.
- Recorded and silent Remotion projects require no AI API key.
- Prefer code-native TSX, CSS, and SVG. Use Codex `$imagegen` only when a requested raster asset
  materially improves the video; copy project-bound outputs into `media/projects/<id>/`.
- ElevenLabs is not an active dependency. Reuse committed SFX/music first; import new audio only
  with source and license provenance.

## AI narration contract

- For `narration.mode: ai`, always use `tools/prepare_narration.py`; never call Gemini once per VO
  line or create a second direct-TTS path.
- The tool sends all `vo[]` passages as one continuous Gemini performance, explicitly locks one
  speaker identity, then locally splits, time-fits, and word-aligns it into authored scene windows.
  A normal video therefore costs one request, not one request per scene.
- Generate narration before final visual timing. Treat authored `vo[].start` values as scene
  anchors, then use the resulting `vo[].words` or emitted `vo.gen.ts` timestamps for captions and
  word-driven animation cues. Never keep estimated timing after aligned audio exists.
- Reuse the cached continuous master. A normal rerun costs zero requests; `--force` deliberately
  spends one fresh request and should be used only when the script, voice, or performance must
  change.
- The local free-tier guard counts attempts before network calls, waits 31 seconds between them,
  and stops at 9 requests per Pacific-time day against the current 10-RPD limit. It stores state in
  `.cache/gemini-tts-quota.json`. Set `GEMINI_TTS_USED_TODAY` for usage made outside this repository.
- Failed provider calls may retry, but every retry is paced and counted. Do not bypass the guard.
- For narration substantially longer than a few minutes, keep one continuous request when quality
  is acceptable. If chapter batching is needed, explain the voice-consistency and quota tradeoff
  and get user approval; never silently fall back to per-line generation.

## Remotion rules

- Animation is deterministic and driven by `useCurrentFrame()`.
- Never use CSS animation, CSS transition, timers, `useState`, or `useEffect` for video motion.
- `interpolate()` input ranges must increase strictly and normally clamp on both sides.
- Frames inside `Sequence` are local; explicitly convert global cue times.
- Use `Easing.bezier()`, Remotion `<Img>`/`<Audio>`, and `staticFile()` for public media.
- Run `cd remotion && npm run gen` after adding or renaming a composition.
- Render representative frames and inspect them before a full render.
- When narration exists, verify scene boundaries, captions, and important reveals against the real
  aligned word times before the full render.

## Verification

- Python: `python -m unittest discover -s tests -v`
- Registry/typecheck: `cd remotion && npm run gen && npx tsc --noEmit`
- QA frames: `cd remotion && node scripts/frames.mjs <CompositionId> <frames> --scale=0.5`
- Full render: `cd remotion && node scripts/render-all.mjs <CompositionId> --scale=1`

Read `brand.md` before visual work. For new whiteboard projects, open
`media/templates/classic-whiteboard/reference.png` and use `remotion/src/lib/classic-whiteboard.tsx`.
The approved whiteboard style uses a pure white background, bold marker lettering, and
independently drawn elements staggered at different heights. Use `remotion/src/lib/english.tsx`
for English lessons.
