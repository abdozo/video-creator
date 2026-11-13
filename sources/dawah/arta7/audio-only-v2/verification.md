# Audio-only rebuild verification

- Input text policy: original TXT and previous captions were not read or imported for this rebuild.
- Transcription: repository tools.dawah_clips transcribe, shared faster-whisper small helper, Arabic, real word timestamps; isolated original PCM audio.
- Tool output preserved exactly: 237/237 recognized words, 76 displayed phrases. No editorial word replacements, no estimated timing, no forced transcript prompt.
- Original-audio ASR was selected. A separate ASR pass on the edited audio is retained for comparison; it made additional obvious recognition errors in the opening question.
- No caption gap between recognized words exceeds 1 second. Formerly omitted anecdote now has captions from ASR.
- Audio source and spoken order retained; no spoken sentence intentionally removed or reordered.
- Removed measured low-energy interiors at local 52.100–52.433 and 55.400–55.733 seconds, with 125–160ms quiet padding. Last boundary aligned to frame grid by 6.7ms.
- No direct listening review claimed. Quiet intervals are an audio-analysis experiment and still need listening before publication.
- Visual dips last four frames each, peak opacity .3, with five-millisecond audio ramps in quiet margins. No voice crossfade or speed change.
- Wide contain layout displays the full 854×480 source in a 1080×1920 composition. Width fit is 1.265× versus 4× height fit in the previous full-screen crop. No animated zoom or sharpen/upscale process.
- Current shared DawahPaper provides bundled Noto Naskh font, texture and paper entrances/exits.
- Registry generation and TypeScript check passed.
- Inspected opening paper, former caption gap, first edit midpoint and closing paper frames at half scale before full rendering.

This is an ASR quality test, not a corrected religious transcript. Recognizer errors remain visible by design. listened/text/approved remain false.

Full render completed and contains H.264 video at 1080×1920 with AAC embedded audio. Output stored alongside the derived SRT.
