# Codex Video Factory

A Remotion-based factory for vertical Shorts, regular YouTube videos, code-native motion
graphics, classic whiteboard animation, collage stories, and generative-video clips. It works
with Codex and remains compatible with Claude Code through the same shared instructions.

## What it can make

| Request | Skill | Format | Default visuals |
|---|---|---|---|
| “Make a short about the ×11 trick” | `$make-short` | 1080×1920 | Motion graphics |
| “Make a ten-minute whiteboard book summary” | `$make-video` | 1920×1080 | Classic whiteboard |
| “Make a Vox-style short about coffee” | `$make-vox` | 1080×1920 | Layered collage |
| “Make an AI video short with blue-man” | `$make-ai-short` | 1080×1920 | fal video clips |

Motion and whiteboard projects start with code-native React and SVG. The whiteboard template
uses a pure white board, bold marker lettering, and drawings staggered across the canvas.
Each element draws in on its own cue. See the [approved style reference](media/templates/classic-whiteboard/reference.png).

## Available templates

| Template | Name | Visual approach |
| --- | --- | --- |
| `motion` | Motion graphics | Code-native text, shapes, diagrams, and animation. |
| `whiteboard` | Classic whiteboard | Bold marker lettering and independently drawn elements on white. |
| `company-analysis` | [Company analysis](media/templates/company-analysis/README.md) | Research terminal, news, fundamentals, multi-timeframe charts and drawn analysis tools. |
| `lines-anime` | [Lines Anime](media/templates/lines-anime/README.md) | Turn a supplied illustration into a story with movable SVG characters and diagrams. |
| `motion-comic-static` | [Motion Comic Static](#motion-comic-static) | Still artwork in fixed comic panels with reveals, camera moves, and layered effects. |
| `motion-graphic-animated` | [Motion Graphic Animated](#motion-graphic-animated) | Comic scenes with selected character or prop movement animated in Rigby2D. |

`lines-anime` is the Lines Anime template's directory name. To create it, scaffold
with `--template motion`, then follow its linked guide and runnable starter. It currently
shares the `motion` scaffold rather than having a separate CLI option.

Vox-style layered collage (`$make-vox`) and generative-video Shorts (`$make-ai-short`) are
additional workflows.

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
  --template motion|whiteboard|company-analysis|motion-comic-static|motion-graphic-animated \
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

### Motion Comic Static

Open the [motion comic layout references](media/templates/motion-comic/README.md) before planning
the page. Choose among the two-panel and three-panel diagonals and the two tall-panel layouts
with stacked close-ups. Use the chosen image to guide geometry, gutters and balloon placement.

**Give each page its final layout from the first frame.** Place every panel in its permanent
slot and leave the slots for later panels as blank paper with hidden frames. Reveal each panel
inside its own mask. Keep earlier panels and their crops in place until the page turns. Move
the artwork inside the mask. Use a separate one-panel page for a full-screen shot.

**Remotion only.** Direct the viewer's eye with camera framing, cuts, masks and restrained
motion between layers. Stage each character pose with its feet, seat, props and contact
shadows registered to the same ground. Show a new action with a cut to an authored pose.
Keep foreground masks registered to the architecture. Give light, atmosphere and details
such as water independent motion. Let reactions hold where the reader needs time.
Rigby2D is reserved for Motion Graphic Animated. The old CLI name `motion-comic` is an alias
for `motion-comic-static`.

Keep page numbers, slide counters, AI annotations, production notes, and storyboard labels in
the project files. On screen, use the illustration and in-panel speech balloons. Ask for clean
art when generating panels, then check both the source art and rendered frames for baked-in text
or watermarks. Add subtitles only when requested.

```bash
python tools/create_project.py --format video --template motion-comic-static \
  --language en --narration none --slug comic-story --duration 10 --comic-image /path/to/page.png
```

1. Separate character dialogue from documentary narration in the script. Give the narrator the
   opening context, the action between spoken turns that needs explaining, and the closing outcome.
   For Arabic, fully vowel the speech and narration, including names and grammatical endings.
   Review the pronunciation in a voiced sample before generating the full cast. Keep one
   voice per role and listen to the generated joins before locking the timing.
   For a single voice that reads the acting directions aloud, generate from the vowelled text
   with `tools/prepare_narration.py --transcript-only`.
   For a voiced comic, align both performances before locking the speaker, action, and reveal cues.
2. Plan the visual edit before assembling it. For each page, specify the final panel masks,
   the subject each crop must preserve, and the camera move and its cue. Vary single
   images, vertical splits, horizontal stacks, and diagonals where they serve the action.
   Use three panels only when each has enough room to read. Give faces, dialogue and action
   adequate height. Reserve shallow strips for short detail inserts that fit the crop.
3. Inventory the available art before assigning shots. Match the same character design across
   angles. Use distinct views for recurring speakers and reactions, and reuse an exact shot when
   the return has a purpose. Plan image dimensions and camera movement for each panel before
   generating art.
4. Author one `PAGES` entry per page, with all the final crops and a separate `at` cue for each
   panel. Start the first panel on the page cue with `reveal: 'cut'`. Use `'cut'` or `'fade'`
   for later panels and leave `showPanelFrames` off. At delivery resolution, check frames
   before, during, and after the second and third reveals, plus the tightest zoom. Check that
   the open panels keep the same boundaries and that faces and balloons are readable.
5. Frame the art first, then put each balloon in clear space. Vary top, bottom, and side placement
   according to the image. Check the speaker's face and the key gesture at both ends of the camera
   move, and keep the balloon and its tail inside the panel. Reframe art or split long dialogue
   across successive balloons when space runs out. Review representative frames across the full
   sequence to catch repeated art, abrupt crops, covered faces, and early reveals.

#### Artwork and sheet handoff for both comic templates

1. For a new cast, generate one character reference sheet from the written brief. Show every
   recurring character in their wardrobe from the front, back, left, and right. Include the props
   and expressions needed for continuity. Share a preview and wait for the user's approval
   before generating production art. Use the approved sheet as the visual reference for each batch.
2. Set the language on either comic template with `--language ar` for Arabic or
   `--language en` for English. New projects default to English. Arrange panels across each
   sheet row from right to left in Arabic and left to right in English, with rows ordered from
   top to bottom in both. Spell out the physical cell positions in each generation prompt.
   Preserve the physical order of any previously approved sheet when cutting it.
   Map every production cell to a panel in the storyboard. Generate even `2x2` or `3x3` contact
   sheets with straight seams, no gutters, and no marks across the seams. Use 16:9 cells for
   widescreen production. Give close-ups and heavy crops more pixels. Fill each cell with
   clean art and leave room for later lettering. Keep all speech balloons, including blank
   ones, text, and identifiers out of the generated artwork. Add editable balloons in Remotion.
3. Share the first production sheet for review. Hand off the approved sheets for the user's
   local upscale and WebP optimization. Keep the full canvas, aspect ratio, and cell order
   through that step. Continue cutting and building with the returned WebP files. Use one small
   preview or local file links for review.
4. Verify the approved source filename, pixel dimensions and cell map before cutting. Split each
   sheet into equal-size cells within that sheet, allowing a small consistent trim at seams.
   Use the supplied optimized WebPs as the source when available. Confirm the composition
   resolves to those crops and inspect the actual export at 100%, including the tightest zoom.
   Pass `--direction rtl` for a sheet arranged right to left
   or `--direction ltr` for a sheet arranged left to right. List the names in that reading
   order within each row, starting at the top. Pass `-` to skip an interior cell or omit unused cells at the end.
   It writes lossless WebP crops and reports their dimensions. Inspect the crops at the tightest
   zoom. A regular grid assumes the artwork follows the specified seams.

Install Pillow with `python3 -m pip install Pillow` and run the adapter from the repo root.

```bash
python3 tools/split_comic_sheet.py /path/to/approved-sheet.webp --grid 2x2 \
  --direction rtl --out media/projects/my-comic/art --names P01 P02 P03 P04
```

Use the split WebPs as each panel's `art`. Frame them with `crop` in Remotion, then add the
balloons as text. A page designed as one shared illustration can use page-level `art` and
panel masks instead. For wide art, leave room around faces, hands, and props for the crop and
camera move. Check the original cell dimensions before upscaling.

Size the art for the tightest camera framing. The portion visible at peak zoom should have at
least the panel's output pixel dimensions. For example, a 1920×1080 panel with a 1.2× push needs
at least 2304×1296 source pixels when the source already matches the panel's aspect ratio. A
mismatched crop can require a larger source. Check the original dimensions before upscaling.

Fill every illustrated panel edge to edge. Use `artFit: 'cover'` with a crop that keeps the
subject readable. If available art needs too much enlargement, resize the panel to suit the
art, reduce the camera move, or generate a higher-resolution version with matching proportions.
`artFit: 'contain'` exposes a brown backing when the image and panel ratios differ. Reserve it
for deliberately matted inserts. At output size, check the start, tightest framing, and end
of each camera move for blank strips, exposed corners, soft detail, and cropped subjects.

The starter passes the project language to `MotionComic`. It sets the order of the default
panel positions, the direction of wipe reveals, and the direction of balloon text. List the
panels and pages in chronological order in `PAGES` for both languages. Explicit `crop`
polygons use physical page coordinates measured as percentages from the left and top. Place
those crops in the project's reading order when designing a shared page. Cues are seconds
from the start of the composition. Set `aspectRatio` for pages that differ from 16:9.

For new illustrations, set `art` on each panel to frame it independently. Add `balloons` for
editable dialogue, and `camera` for a slow push inside the panel. The lettering stays
fixed while the artwork moves. The Qadisiyyah layered example reads these settings from `beats.json`.

For a panel built from cutouts, set `art` to the clean background and use `scene.width` and
`scene.height` for its source dimensions. Set `scene.layers` in back-to-front order, with
each layer's `art`, `x`, `y`, `width` and `height` in background pixels. Use
`scene.viewport` to frame the scene within the panel. Remotion fits the viewport to cover the
panel and applies the panel camera to the background and cutouts together. A layer can add
`motion` driven by seconds since the panel reveal, a `pivot` in background pixels, and a
`clipPath` to isolate part of the art.

For existing pages with lettering drawn into the image, supply `bubble.cleanArt` and trace the
balloon's `region` on the page.

For voiced scenes, give each `DIALOGUE` entry an `id`, `speaker`, and timing. A panel or balloon
cue such as `{line: 'rostam-question', offset: -0.3}` follows the first aligned word when `words`
is available and otherwise uses `start`. For a cast of recorded voices, use `--narration recorded`
and supply `audio` on every spoken line. Trim each clip to begin with its first spoken word.
For a shared narration track, leave the per-line clip paths empty and play the master once across
the composition. Use aligned words for visual cues. When assembling turns from saved performances,
use one source boundary between adjacent turns so no spoken samples repeat. Review the waveform
and listen across joins for repeated or clipped syllables, then align the assembled track before
locking panel and balloon cues.

If a comic has an existing dialogue master, prepare the documentary voice separately in
`narrator.json` with the same composition duration, an independent output path, and all narrator
passages in `vo`. Generate them together with `tools/prepare_narration.py` using a single voice
distinct from the cast. For Arabic history, direct a measured, resonant performance in clear
Modern Standard Arabic. Give each passage its own window between dialogue turns and play the
narrator master alongside the cast. Use the narrator's aligned words to cue any illustrated
action it describes. Leave narration off the artwork.

Choose music that fits the scene. For a tense negotiation before a battle, try a restrained
pulse or low strings. Set one low music level for the full cue. Check it against the quietest
dialogue or narration, then keep that level through the pauses as well. In Remotion, use a
fixed `<Audio volume={...}>` value. If the cue needs a fade, put it at the cue's start or end.
If the local catalog lacks a suitable cue, check a licensed source and import the track with
`tools/import_audio.py --kind music`, recording its source and license. Keep required music
credit in the publication description.

### Motion Graphic Animated

Start with one complete exchange as a template pilot. [The Rubai tent pilot](remotion/src/shots/video-18/Video18RubaiTentPilot.tsx)
uses five existing images and an aligned dialogue mix. Set the composition's `animate` prop to
`false` to review the same cuts and audio as an animatic.

1. Set the cuts and listen through the scene using the available art and a temporary or final voice track.
2. Choose the movement for each shot. A still can carry the whole shot. For motion inside the
   silhouette, try a local mesh. When motion reveals what was behind a part, prepare that part
   and the clean area behind it as separate layers.
3. Use Rigby2D MCP to key the selected movement and export its frames. Open the `.rigby` work
   file in the desktop app and check the rest pose, the strongest pose, and the return or hold.
4. Add the registered pass to the same cut in Remotion. Check the rendered cut, camera move,
   and sound together before preparing art for the next scene.

Use [the Rubai entrance comic](remotion/src/shots/video-18/Video18RubaiEntranceComic.tsx) as the
default for dialogue scenes. Prepare fixed background plates and transparent character art, then
choose at most one local action for each panel. Open the panels in reading order with the
original dialogue and keep earlier panels visible. A blink, small hand signal, or moving prop
is enough to draw attention to the beat. Keep the rest of the panel in its authored pose.

Use the [motion comic layout references](media/templates/motion-comic/README.md) when planning
panel masks and camera moves. Follow the chosen reference's panel proportions and gutters.

**Remotion directs the shot. Rigby2D animates what happens inside it.** Use the fixed page layouts
and in-place reveals from [Motion Comic Static](#motion-comic-static). In Remotion, frame each panel,
pan, push in or pull back, and handle cuts and cinematic effects. Keep balloons anchored to the panel.

In Rigby2D, animate the selected detail against a clean, fixed background. Use local weights
inside the character silhouette, and separate any part whose motion reveals pixels behind it.
If lip motion is the selected detail, use alternate mouth drawings timed to the dialogue.
Check that the neighboring art holds its shape at the peak of the movement.
Follow the shared [artwork and sheet handoff](#artwork-and-sheet-handoff-for-both-comic-templates)
and the fully vowelled Arabic audio workflow above.

Before generating artwork, write the film from opening to closing. For each scene, record its
panel count and reading order. For each panel, specify the image asset, screen position and crop,
camera, visible action, motion cue, exact spoken line or silence, and balloon placement. Count
reference sheets, production sheets, panel images, and animation passes separately. Use the
first approved, optimized production sheet to test a face close-up and a moving prop in Remotion
before generating the rest of the panels.

List every panel and its final crop in reading order in `PAGES`. Start the first panel when the
page opens and give the other panels later `at` cues. Leave `showPanelFrames` disabled. Use aligned
dialogue cues when available. Check that the camera and Rigby2D layers stay inside the same crop
through the next reveal. Review a populated page and the next page turn in a rendered sample.

Put dialogue in `balloons` inside the speaking panel and point each tail toward its speaker.
Keep AI annotations, slide titles, page numbers, and production notes off screen. Keep the
documentary narrator on a separate track for the opening context, actions that need explaining,
and the closing outcome. Time the character balloons and key animation cues to aligned speech.
Mix music at one quiet level through speech and pauses, with fades only at cue boundaries.

Give each Rigby2D motion a cue and an end pose or loop. When a reaction carries the shot, keep
ambient motion quiet enough that the audience reads the face first.

```bash
python tools/create_project.py --format video --template motion-graphic-animated \
  --language en --narration none --slug comic-story --comic-image /path/to/page.png
```

1. Prepare a clean base image without the moving part. Keep the part and any joints or separate
   attachments on their own layers. Plan the rest pose and pivot against the base image before
   animating in Rigby2D.
2. Export one take per pass as transparent PNGs. For a character rig, use Rigby2D's
   [`export_sprite_sheet`](https://rigby2d.com/docs/mcp-tools.html#export_sprite_sheet) with
   `format: "frames"`. Use `loop: true` for a repeating take to omit its duplicate endpoint.
3. Position the export on a transparent canvas with the same dimensions as the base artwork.
   If the export is tight around the rig, pad every frame with the same offset. The base image
   and passes share the panel crop and camera, so their registration stays fixed through a push.
4. Put the numbered PNGs in `media/projects/<id>/` and list the passes on the panel in `PAGES`,
   back to front. Panels without `rigby` display still art on their cue.

```tsx
{
  at: 3,
  art: 'projects/<id>/panel-02.png',
  rigby: [
    {prefix: 'projects/<id>/flag/flag_', fps: 30, frameCount: 60, loop: true},
    {prefix: 'projects/<id>/gaze/gaze_', fps: 30, frameCount: 24, at: 4.2},
  ],
}
```

`prefix` points to the part before the number in `flag_000.png`. Numbering uses at least three
digits, as in a Rigby2D export. Set `digits` for other padding and `fps` to the export rate.
The pass holds its first pose until `at`, which defaults to the
panel reveal and accepts the same dialogue cues as balloons. A one-shot pass holds its last pose;
`loop: true` repeats it. Remotion owns the sound mix. Check the first pose, tightest camera crop,
and final pose or loop join in the assembled panel. See the
[Rigby2D integration notes](docs/rigby2d-integration-research.md) for rig and export details.

## Remotion systems

- `remotion/src/lib/video.tsx`: horizontal layouts, chapter cards, lower thirds, callouts,
  static backgrounds, and chapter progress.
- `remotion/src/lib/english.tsx`: vocabulary, grammar highlighting, correction, pronunciation,
  dialogue, exercises, quizzes, and translation layouts.
- `remotion/src/lib/classic-whiteboard.tsx` provides the whiteboard starter and drawing primitives
  for new horizontal videos and Shorts. Adapt the layout and replace the sample drawings with
  the story's own visual beats.
- `remotion/src/lib/whiteboard.tsx` supports the existing editorial-sketchbook compositions.
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

Gemini narration is generated as one continuous performance per video, then split, fitted, and
word-aligned locally into the authored scene windows. This keeps the same speaker identity across
scenes, gives captions and visual cues exact timestamps, and normally costs one API request for the
entire voiceover. A local free-tier guard waits 31 seconds between attempts and stops after 9
requests per Pacific-time day, leaving one request of the current 10-RPD limit unused. Usage is
stored in `.cache/gemini-tts-quota.json`; cached narration does not consume requests. If the same Google AI Studio project is used elsewhere, set
`GEMINI_TTS_USED_TODAY` to that outside usage before generating. The limits and reserve can be
adjusted in `.env` when AI Studio reports different quotas.

Codex video workflows are required by `AGENTS.md` and the `make-short`, `make-video`,
`make-ai-short`, and `make-vox` skills to use this shared path. They generate narration before
locking visual timing, consume `beats.json`/`vo.gen.ts` aligned timestamps for captions and cues,
reuse the cached master on ordinary reruns, and never silently revert to per-scene Gemini calls.

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
