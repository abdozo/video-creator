import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.prepare_narration import delivery_and_transcript, estimate_words, main, map_words


class NarrationTests(unittest.TestCase):
    def test_delivery_tags_are_not_spoken(self):
        delivery, transcript = delivery_and_transcript({
            "text": "This is Pip. Welcome home.",
            "tts": "[warmly] This is Pip. [whispers] Welcome home.",
        })
        self.assertEqual(delivery, "warmly, whispers")
        self.assertEqual(transcript, "This is Pip. Welcome home.")

    def test_exact_alignment(self):
        recognized = [
            {"word": "Hello", "start": 0.1, "end": 0.4},
            {"word": "world", "start": 0.5, "end": 0.9},
        ]
        words, coverage = map_words("Hello, world!", recognized)
        self.assertEqual(coverage, 1)
        self.assertEqual([word["w"] for word in words], ["Hello,", "world!"])

    def test_estimates_cover_window(self):
        words = estimate_words("one longer-word three", 2, 5)
        self.assertEqual(words[0]["start"], 2)
        self.assertAlmostEqual(words[-1]["end"], 5, places=3)

    def test_none_mode_invokes_no_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            beats = Path(tmp) / "beats.json"
            beats.write_text(json.dumps({
                "id": "silent-test",
                "format": {"durationSec": 5},
                "narration": {"mode": "none", "audio": None},
                "vo": [],
            }))
            with patch("tools.prepare_narration.prepare_ai", side_effect=AssertionError("AI called")), patch("tools.prepare_narration.prepare_recorded", side_effect=AssertionError("recorded called")):
                main(["--beats", str(beats)])
            updated = json.loads(beats.read_text())
            self.assertEqual(updated["voiceStatus"], "none")


if __name__ == "__main__":
    unittest.main()
