# Codex Video Factory

A Remotion-based factory for vertical Shorts, regular YouTube videos, code-native motion
graphics, modern whiteboard animation, collage stories, and generative-video clips. It works
with Codex and remains compatible with Claude Code through the same shared instructions.

## What it can make

| Request | Skill | Format | Default visuals |
|---|---|---|---|
| “Make a short about the ×11 trick” | `$make-short` | 1080×1920 | Motion graphics |
| “Make a ten-minute whiteboard book summary” | `$make-video` | 1920×1080 | Editorial whiteboard |
| “Make a Vox-style short about coffee” | `$make-vox` | 1080×1920 | Layered collage |
| “Make an AI video short with blue-man” | `$make-ai-short` | 1080×1920 | fal video clips |

Motion graphics and whiteboard scenes are generated entirely in React/SVG and Remotion. They
do not need image generation. A supplied background or book cover is optional; `$imagegen` is
the default for image-based tracks when a new raster asset is genuinely useful.

## Narration modes

- `ai`: Gemini 3.1 Flash TTS Preview, `Charon` voice by default. Requires `GEMINI_API_KEY`.
- `recorded`: imports, normalizes, transcribes, and aligns the user’s recording locally.
- `none`: renders from explicit scene durations with no API, audio, alignment, or captions.

AI and recorded narration are aligned locally with `faster-whisper`. Authored-word coverage
below 90% fails unless estimated timing is explicitly allowed. Teaching text is independent
from subtitles: regular videos default to no conventional captions, while narrated Shorts
default to word-highlight captions.

## Quick start

Requirements: Node 18+, Python 3.10+, `ffmpeg`/`ffprobe`, and Codex. Claude Code can also read
the same project contract.

```bash
cp .env.example .env
cd remotion
npm install
npm run gen
cd ..
```

For AI narration:

```bash
python -m pip install -r requirements-voice.txt
```

Then ask Codex:

> Make a whiteboard short about procrastination.

> Create a ten-minute whiteboard book summary with my recorded narration.

> Build a regular motion-graphics English lesson without narration.

## Shared project scaffolder

```bash
python tools/create_project.py \
  --format short|video \
  --template motion|whiteboard \
  --narration ai|recorded|none \
  --slug <slug>
```

It creates `shorts/short-N-<slug>/` or `videos/video-N-<slug>/`, a compatible `beats.json`,
a script, media folder, and a registered Remotion composition under
`remotion/src/shots/<id>/`.

Narration preparation is explicit:

```bash
python tools/prepare_narration.py --beats videos/video-N-topic/beats.json
python tools/prepare_narration.py --beats videos/video-N-topic/beats.json \
  --emit-ts remotion/src/shots/video-N/vo.gen.ts
```

`tools/gen_voice.py` remains as a compatibility entrypoint and delegates to the same pipeline.

## Remotion systems

- `remotion/src/lib/video.tsx`: horizontal layouts, chapter cards, lower thirds, callouts,
  static backgrounds, and chapter progress.
- `remotion/src/lib/english.tsx`: vocabulary, grammar highlighting, correction, pronunciation,
  dialogue, exercises, quizzes, and translation layouts.
- `remotion/src/lib/whiteboard.tsx`: deterministic editorial-sketchbook primitives, including
  the indigo idea thread, concept maps, diagrams, quote cards, book cards, and erase/redraw.
- Existing TSX, collage, story-image, and generative compositions remain registered.

Generate the registry, inspect in Studio, render QA frames, or render video:

```bash
cd remotion
npm run gen
npm run studio
node scripts/frames.mjs <CompositionId> 0,150,300 --scale=0.5
node scripts/render-all.mjs <CompositionId> --scale=1
```

## Providers and audio policy

`.env.example` contains only optional providers:

- `GEMINI_API_KEY`: AI narration.
- `FAL_KEY`: preserved generative-video workflows.

Recorded and silent motion/whiteboard projects require no AI API key. Reuse bundled SFX/music
first. New free or user-owned audio must be imported with source and license provenance using
`tools/import_audio.py`. ElevenLabs is retained only in historical artifacts and legacy scripts;
it is not part of the active workflow.

## Repository layout

```text
AGENTS.md          canonical project instructions for Codex
CLAUDE.md          loads AGENTS.md for Claude Code compatibility
.agents/skills/    shared workflow skills
.claude/skills     symlink to the shared skill directory
tools/             scaffolding, narration, media import, rendering helpers
remotion/          rendering application and reusable component systems
shorts/            vertical projects and existing examples
videos/            horizontal projects
ai-shorts/         preserved generative-video track
vox-shorts/        preserved layered-collage track
media/             reusable licensed assets and project media
```

## License

MIT — see [LICENSE](LICENSE). Existing bundled media retains the provenance recorded in its
catalog or sidecar. Verify the license before republishing any asset.
