# Verification of review preview

Status: review preview, not approved for publication. Listening and final text review are incomplete.

- Compared owner transcript with independent local small/base ASR passes.
- Forced aligned 227 authored draft words against the actual source audio. No estimated word durations.
- 66 short caption phrases. The ambiguous anecdote at source 26:09.300–26:15.560 remains audible but intentionally uncaptioned.
- Read full supplied transcript. This continuous passage contains the question, doctor analogy, persistence, and payoff. Other passages at 18:12–19:32 and 23:16–24:25 discuss broader provision/openings; retaining the selected passage keeps the specific delayed-answer argument together.
- No directly quoted Quran/hadith is present in the selected draft text; the preceding quotation is excluded.
- Source bounds: 1537.920–1634.160 seconds. No internal joins or altered playback rate.
- Registry generation and TypeScript check passed.
- Inspected representative opening, narrative, blank-caption, paper-cue, payoff and closing frames at half scale. Arabic joins and caption placement look readable.
- Python suite: 26 passed, 1 failed. The failure is an existing error-message expectation in test_rejects_crossing_cues_reordered_edits_and_subframe_durations: regex ordered versus actual story order. Shared tool/test files were not modified for this preview.

Remaining: listen to source and full output; resolve uncertain anecdote words, verify all draft captions and opening/closing syllables, then set actual review flags and use approved export. ASR/forced alignment do not certify any of those checks.

Full-size review render completed: H.264 1080×1920, AAC audio, 96.32 seconds, 97,587,017 bytes. Inspected a frame extracted from the baked MP4. Final output: shorts/short-15-before-the-door-opens/output/before-the-door-opens-review.mp4.
