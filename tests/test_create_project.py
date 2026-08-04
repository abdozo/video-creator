import json
import tempfile
import unittest
from pathlib import Path

from tools.create_project import create, parser


class CreateProjectTests(unittest.TestCase):
    def run_create(self, *args):
        with tempfile.TemporaryDirectory() as tmp:
            ns = parser().parse_args([*args, "--root", tmp])
            result = create(ns)
            root = Path(tmp)
            beats = json.loads((root / result["project"] / "beats.json").read_text())
            tsx = next((root / result["composition"]).glob("*.tsx")).read_text()
            return result, beats, tsx

    def test_short_defaults(self):
        _, beats, tsx = self.run_create("--format", "short", "--slug", "Daily Words")
        self.assertEqual(beats["format"]["mode"], "short")
        self.assertEqual((beats["format"]["width"], beats["format"]["height"]), (1080, 1920))
        self.assertEqual(beats["narration"]["mode"], "none")
        self.assertEqual(beats["captions"]["mode"], "none")
        self.assertIn("MotionCanvas", tsx)

    def test_video_whiteboard_recorded(self):
        _, beats, tsx = self.run_create(
            "--format", "video", "--template", "whiteboard", "--narration", "recorded",
            "--slug", "Atomic Habits", "--duration", "480",
        )
        self.assertEqual(beats["format"]["durationSec"], 480)
        self.assertEqual((beats["format"]["width"], beats["format"]["height"]), (1920, 1080))
        self.assertTrue(beats["narration"]["audio"].endswith("narration.m4a"))
        self.assertIn("WhiteboardCanvas", tsx)

    def test_ai_short_defaults_to_word_highlight(self):
        _, beats, _ = self.run_create(
            "--format", "short", "--narration", "ai", "--slug", "One Rule"
        )
        self.assertEqual(beats["captions"]["mode"], "word-highlight")

    def test_every_format_template_narration_combination(self):
        for video_format in ("short", "video"):
            for template in ("motion", "whiteboard"):
                for narration in ("ai", "recorded", "none"):
                    with self.subTest(format=video_format, template=template, narration=narration):
                        _, beats, tsx = self.run_create(
                            "--format", video_format, "--template", template,
                            "--narration", narration, "--slug", "Matrix Case",
                        )
                        self.assertEqual(beats["format"]["mode"], video_format)
                        self.assertEqual(beats["template"], template)
                        self.assertEqual(beats["narration"]["mode"], narration)
                        self.assertIn("CaptionTrack", tsx)


if __name__ == "__main__":
    unittest.main()
