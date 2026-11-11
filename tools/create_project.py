#!/usr/bin/env python3
"""Create a backwards-compatible Remotion video project scaffold."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOTION_COMIC_STATIC = "motion-comic-static"
MOTION_GRAPHIC_ANIMATED = "motion-graphic-animated"
COMIC_TEMPLATES = (MOTION_COMIC_STATIC, MOTION_GRAPHIC_ANIMATED, "motion-comic")


def slug_value(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise argparse.ArgumentTypeError("slug must contain a letter or number")
    return slug


def next_number(parent: Path, prefix: str) -> int:
    numbers = []
    if parent.exists():
        for path in parent.iterdir():
            match = re.match(rf"{re.escape(prefix)}-(\d+)(?:-|$)", path.name)
            if match:
                numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def pascal(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("-"))


def tsx_source(project_id: str, component_id: str, config: dict, template: str,
               narration_audio: str | None, caption_mode: str, comic_art: str | None = None,
               language: str = "en") -> str:
    audio = f"'{narration_audio}'" if narration_audio else "undefined"
    starter_content = ""
    audio_condition = "NARRATION"
    caption_lines = "VO"
    if template == "company-analysis":
        body_import = "import {CompanyAnalysis, demoAnalysis} from '../../lib/company-analysis';"
        body = "<CompanyAnalysis data={demoAnalysis} />"
    elif template == "whiteboard":
        body_import = "import {ClassicWhiteboardStarter} from '../../lib/classic-whiteboard';"
        title = project_id.split("-", 2)[2].replace("-", " ").capitalize()
        starter_content = (
            f"const TITLE = {json.dumps(title)};\n"
            "const STEPS = ['Open it', 'Try one step', 'Keep going?'] as const;\n\n"
        )
        body = "<ClassicWhiteboardStarter title={TITLE} steps={STEPS} />"
    elif template in COMIC_TEMPLATES:
        body_import = "import {MotionComic, type ComicDialogue, type MotionComicPage} from '../../lib/motion-comic';"
        pages = []
        if comic_art:
            panels = [{"at": 0, "art": comic_art, "reveal": "cut"}]
            pages.append({"panels": panels})
        animated = template == MOTION_GRAPHIC_ANIMATED
        template_title = "Motion Graphic Animated" if animated else "Motion Comic Static"
        rigby_note = (
            "// Rigby2D handles performance: a glance, a restrained smile, a slight head turn, or a flag in the wind.\n"
            "// Rig isolated transparent layers over a fixed background. Keep mouths and jaws still during dialogue.\n"
            if animated else "// Static uses Remotion only. Hold grounded poses, cut between actions, and move accents on separate layers.\n"
        )
        starter_content = (
            f"// Follow the {template_title} section in README.md.\n"
            "// Choose a visual layout reference from media/templates/motion-comic/README.md before planning masks.\n"
            "// Set the final panel crops once per page. Keep unrevealed slots empty and reveal panels on their own cues.\n"
            "// Use cut or fade to reveal a panel in place. A separate page can hold a full-screen shot.\n"
            "// Vary splits, stacks and diagonal masks while giving faces, text and action room to read.\n"
            "// Use Remotion for framing, camera moves, cuts and cinematic effects. Cue them to story beats.\n"
            "// Check the tightest crop in a full-size preview.\n"
            "// List panels in story order and lay out sheet rows in the project's reading direction.\n"
            "// For Arabic, fully vowel dialogue and narration and check names before generating audio.\n"
            "// Get cast sheet approval before generating production sheets.\n"
            "// Split the returned WebPs with tools/split_comic_sheet.py. Add all balloons as Remotion text.\n"
            "// Keep page numbers and production labels off screen.\n"
            "// Play documentary commentary as a separate voice track when a cast track already exists.\n"
            "// Keep the score at one low level through speech and pauses. Fade at cue boundaries only.\n"
            f"{rigby_note}"
            f"const PAGES: MotionComicPage[] = {json.dumps(pages, indent=2)};\n"
            "const DIALOGUE: ComicDialogue[] = [];\n\n"
        )
        body = f'<MotionComic pages={{PAGES}} dialogue={{DIALOGUE}} language="{language}" panelPlayback="accumulate" />'
        audio_condition = "NARRATION && !DIALOGUE.some(({audio}) => audio)"
        caption_lines = "DIALOGUE.length ? DIALOGUE : VO"
    else:
        body_import = "import {ChapterCard, MotionCanvas} from '../../lib/video';"
        body = f"""<MotionCanvas format=\"{config['mode']}\">
      <ChapterCard kicker=\"INTRODUCTION\" title=\"{project_id.replace('-', ' ')}\" subtitle=\"Replace with the opening thesis\" />
    </MotionCanvas>"""

    return f"""import React from 'react';
import {{Audio, staticFile}} from 'remotion';
{body_import}
import {{CaptionTrack}} from '../../lib/video';
import type {{VoLine}} from '../../lib/shorts';

export const compositionConfig = {{
  id: '{component_id}',
  durationInSeconds: {config['durationSec']},
  fps: {config['fps']},
  width: {config['width']},
  height: {config['height']},
}};

{starter_content}const VO: VoLine[] = [];
const NARRATION = {audio};
const CAPTION_MODE = '{caption_mode}';

const {component_id}: React.FC = () => (
  <>
    {body}
    {{{audio_condition} ? <Audio src={{staticFile(NARRATION)}} /> : null}}
    <CaptionTrack lines={{{caption_lines}}} mode={{CAPTION_MODE}} format="{config['mode']}" />
  </>
);

export default {component_id};
"""


def create(args: argparse.Namespace) -> dict:
    root = Path(args.root).resolve()
    template = MOTION_COMIC_STATIC if args.template == "motion-comic" else args.template
    is_short = args.format == "short"
    if template == "company-analysis" and is_short:
        raise SystemExit("company-analysis requires --format video (1920x1080)")
    parent = root / ("shorts" if is_short else "videos")
    prefix = "short" if is_short else "video"
    number = args.number or next_number(parent, prefix)
    project_id = f"{prefix}-{number}-{args.slug}"
    project_dir = parent / project_id
    shot_dir = root / "remotion" / "src" / "shots" / f"{prefix}-{number}"
    media_dir = root / "media" / "projects" / project_id
    for path in (project_dir, shot_dir, media_dir):
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing path: {path}")

    duration = args.duration if args.duration is not None else (42 if is_short else 120 if template == "company-analysis" else 300)
    comic_image = getattr(args, "comic_image", None)
    if comic_image and (template not in COMIC_TEMPLATES or not comic_image.is_file()):
        raise SystemExit("--comic-image must be an existing file used with a comic template")
    comic_filename = f"page-01{comic_image.suffix.lower()}" if comic_image else None
    comic_art = f"projects/{project_id}/{comic_filename}" if comic_filename else None
    language = getattr(args, "language", None) or "en"
    width, height = ((1080, 1920) if is_short else (1920, 1080))
    narration_audio = None
    if args.narration != "none":
        narration_audio = f"projects/{project_id}/narration.m4a"
    caption_mode = args.captions
    if caption_mode is None:
        caption_mode = "word-highlight" if is_short and args.narration != "none" else "none"

    config = {
        "mode": args.format,
        "width": width,
        "height": height,
        "fps": 30,
        "durationSec": duration,
    }
    beats = {
        "id": project_id,
        "title": args.slug.replace("-", " ").title(),
        "composition": f"{prefix.capitalize()}{number}{pascal(args.slug)}",
        "format": config,
        "template": template,
        "narration": {"mode": args.narration, "audio": narration_audio},
        "captions": {"mode": caption_mode},
        "vo": [],
        "beats": [],
    }
    if template in COMIC_TEMPLATES:
        beats["language"] = language

    project_dir.mkdir(parents=True)
    shot_dir.mkdir(parents=True)
    media_dir.mkdir(parents=True)
    if comic_image and comic_filename:
        shutil.copyfile(comic_image, media_dir / comic_filename)
    (project_dir / "beats.json").write_text(json.dumps(beats, indent=2) + "\n", encoding="utf-8")
    (project_dir / "script.md").write_text(
        f"# {beats['title']}\n\n"
        f"Format: {args.format} · Template: {template} · Narration: {args.narration}\n\n"
        "## Outline\n\n- Hook / thesis\n- Development\n- Synthesis / payoff\n",
        encoding="utf-8",
    )
    component_id = beats["composition"]
    (shot_dir / f"{component_id}.tsx").write_text(
        tsx_source(project_id, component_id, config, template, narration_audio, caption_mode, comic_art, language),
        encoding="utf-8",
    )
    return {
        "id": project_id,
        "project": str(project_dir.relative_to(root)),
        "composition": str(shot_dir.relative_to(root)),
        "media": str(media_dir.relative_to(root)),
    }


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--format", choices=("short", "video"), required=True)
    ap.add_argument("--template", choices=("motion", "whiteboard", "company-analysis", *COMIC_TEMPLATES), default="motion",
                    help="motion-comic is a legacy alias for motion-comic-static")
    ap.add_argument("--comic-image", type=Path, help="initial page image for either comic template")
    ap.add_argument("--language", choices=("ar", "en"), help="comic language and reading direction (default: en)")
    ap.add_argument("--narration", choices=("ai", "recorded", "none"), default="none")
    ap.add_argument("--captions", choices=("none", "subtitles", "word-highlight"))
    ap.add_argument("--slug", required=True, type=slug_value)
    ap.add_argument("--duration", type=float)
    ap.add_argument("--number", type=int)
    ap.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)
    return ap


def main() -> None:
    args = parser().parse_args()
    print(json.dumps(create(args), indent=2))


if __name__ == "__main__":
    main()
