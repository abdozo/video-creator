#!/usr/bin/env python3
"""Create a backwards-compatible Remotion video project scaffold."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
               narration_audio: str | None, caption_mode: str) -> str:
    audio = f"'{narration_audio}'" if narration_audio else "undefined"
    if template == "whiteboard":
        body_import = "import {BookCard, IdeaThread, WhiteboardCanvas} from '../../lib/whiteboard';"
        body = f"""<WhiteboardCanvas format=\"{config['mode']}\">
      <BookCard title=\"{project_id.replace('-', ' ')}\" subtitle=\"Replace with the opening thesis\" />
      <IdeaThread d=\"M 180 760 C 520 650, 910 850, 1500 670\" at={{18}} duration={{70}} />
    </WhiteboardCanvas>"""
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

const VO: VoLine[] = [];
const NARRATION = {audio};
const CAPTION_MODE = '{caption_mode}';

const {component_id}: React.FC = () => (
  <>
    {body}
    {{NARRATION ? <Audio src={{staticFile(NARRATION)}} /> : null}}
    <CaptionTrack lines={{VO}} mode={{CAPTION_MODE}} format="{config['mode']}" />
  </>
);

export default {component_id};
"""


def create(args: argparse.Namespace) -> dict:
    root = Path(args.root).resolve()
    is_short = args.format == "short"
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

    duration = args.duration if args.duration is not None else (42 if is_short else 300)
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
        "template": args.template,
        "narration": {"mode": args.narration, "audio": narration_audio},
        "captions": {"mode": caption_mode},
        "vo": [],
        "beats": [],
    }

    project_dir.mkdir(parents=True)
    shot_dir.mkdir(parents=True)
    media_dir.mkdir(parents=True)
    (project_dir / "beats.json").write_text(json.dumps(beats, indent=2) + "\n", encoding="utf-8")
    (project_dir / "script.md").write_text(
        f"# {beats['title']}\n\n"
        f"Format: {args.format} · Template: {args.template} · Narration: {args.narration}\n\n"
        "## Outline\n\n- Hook / thesis\n- Development\n- Synthesis / payoff\n",
        encoding="utf-8",
    )
    component_id = beats["composition"]
    (shot_dir / f"{component_id}.tsx").write_text(
        tsx_source(project_id, component_id, config, args.template, narration_audio, caption_mode),
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
    ap.add_argument("--template", choices=("motion", "whiteboard"), default="motion")
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
