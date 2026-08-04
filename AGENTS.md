# Codex Video Factory

This repository is a Remotion video factory driven primarily by Codex. Run commands from the
repository root. Preserve existing examples and their historical provider metadata.

## Workflow routing

- `$make-short`: vertical 1080x1920 Shorts. Templates: `motion` or `whiteboard`.
- `$make-video`: horizontal 1920x1080 regular YouTube videos. Templates: `motion` or `whiteboard`.
- `$make-ai-short`: optional fal.ai video-model pixels.
- `$make-vox`: optional layered collage.
- `$suggest-sfx`: library-first sound design and mixing.
- `$vidtsx-2d-generator`: Remotion correctness rules for every TSX composition.

Natural-language equivalents such as "make a regular video", "make a whiteboard short", and
"build a video using my narration" should route to the matching skill.

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

## Remotion rules

- Animation is deterministic and driven by `useCurrentFrame()`.
- Never use CSS animation, CSS transition, timers, `useState`, or `useEffect` for video motion.
- `interpolate()` input ranges must increase strictly and normally clamp on both sides.
- Frames inside `Sequence` are local; explicitly convert global cue times.
- Use `Easing.bezier()`, Remotion `<Img>`/`<Audio>`, and `staticFile()` for public media.
- Run `cd remotion && npm run gen` after adding or renaming a composition.
- Render representative frames and inspect them before a full render.

## Verification

- Python: `python -m unittest discover -s tests -v`
- Registry/typecheck: `cd remotion && npm run gen && npx tsc --noEmit`
- QA frames: `cd remotion && node scripts/frames.mjs <CompositionId> <frames> --scale=0.5`
- Full render: `cd remotion && node scripts/render-all.mjs <CompositionId> --scale=1`

Read `brand.md` before visual work. Whiteboard work also follows
`remotion/src/lib/whiteboard.tsx`; English lessons use `remotion/src/lib/english.tsx`.
