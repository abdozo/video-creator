#!/usr/bin/env python3
"""Prepare AI, recorded, or transcript-only narration for a Remotion project."""

from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-3.1-flash-tts-preview"
DEFAULT_VOICE = "Charon"
DEFAULT_ALIGN_MODEL = "base.en"


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    path = ROOT / ".env"
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip().strip('"').strip("'")
    return {**env, **os.environ}


def run(command: list[str]) -> str:
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode:
        raise RuntimeError(f"command failed: {' '.join(command)}\n{result.stdout}")
    return result.stdout


def duration(path: Path) -> float:
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)]).strip())


def delivery_and_transcript(line: dict) -> tuple[str, str]:
    source = line.get("tts") or line["text"]
    directions = [tag.strip() for tag in re.findall(r"\[([^]]+)]", source) if tag.strip()]
    clean = re.sub(r"\s*\[[^]]+]\s*", " ", source)
    clean = re.sub(r"\s+", " ", clean).strip()
    # Caption text is authoritative when old ElevenLabs tags were mixed into `tts`.
    transcript = line.get("text", clean).strip()
    return ", ".join(directions), transcript


def normalize_word(word: str) -> str:
    return re.sub(r"[^a-z0-9']+", "", word.lower().replace("’", "'"))


def estimate_words(text: str, start: float, end: float) -> list[dict]:
    words = text.split()
    if not words:
        return []
    weights = [max(2, len(normalize_word(word))) + 1.6 for word in words]
    total = sum(weights)
    cursor = start
    output = []
    for word, weight in zip(words, weights):
        word_end = cursor + (end - start) * weight / total
        output.append({"w": word, "start": round(cursor, 3), "end": round(word_end, 3)})
        cursor = word_end
    return output


def map_words(text: str, recognized: list[dict], start: float = 0.0,
              end: float | None = None) -> tuple[list[dict], float]:
    authored = text.split()
    a_norm = [normalize_word(word) for word in authored]
    r_norm = [normalize_word(word["word"]) for word in recognized]
    matcher = difflib.SequenceMatcher(a=a_norm, b=r_norm, autojunk=False)
    mapped: list[dict | None] = [None] * len(authored)
    matched = 0
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            ai, ri = block.a + offset, block.b + offset
            mapped[ai] = {
                "w": authored[ai],
                "start": round(start + float(recognized[ri]["start"]), 3),
                "end": round(start + float(recognized[ri]["end"]), 3),
            }
            matched += 1
    coverage = matched / max(1, len(authored))
    fallback_end = end if end is not None else (start + float(recognized[-1]["end"]) if recognized else start + max(1, len(authored)) * .35)
    estimated = estimate_words(text, start, fallback_end)
    # Interpolate unmatched words between their nearest aligned neighbors.
    for index, value in enumerate(mapped):
        if value is None:
            mapped[index] = estimated[index]
    return [word for word in mapped if word is not None], coverage


def whisper_words(path: Path, model_name: str, language: str | None) -> tuple[list[dict], list[dict]]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("faster-whisper is required for local alignment; install requirements-voice.txt") from exc
    model = WhisperModel(model_name, device="auto", compute_type="int8")
    segments, _ = model.transcribe(str(path), language=language, word_timestamps=True, vad_filter=True)
    words: list[dict] = []
    segment_rows: list[dict] = []
    for segment in segments:
        segment_rows.append({"text": segment.text.strip(), "start": segment.start, "end": segment.end})
        for word in segment.words or []:
            words.append({"word": word.word.strip(), "start": word.start, "end": word.end})
    return words, segment_rows


def write_pcm_wav(path: Path, pcm: bytes, rate: int = 24000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(rate)
        output.writeframes(pcm)


def gemini_tts(api_key: str, model: str, voice: str, transcript: str,
               delivery: str, output: Path) -> None:
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError("google-genai is required for AI narration; install requirements-voice.txt") from exc
    direction = delivery or "clear, natural, informative"
    prompt = (
        "Synthesize speech. Do not read the directions or labels aloud. "
        f"Delivery: {direction}. Speak the transcript exactly as written.\nTRANSCRIPT:\n{transcript}"
    )
    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
            )
        ),
    )
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(model=model, contents=prompt, config=config)
            part = response.candidates[0].content.parts[0]
            data = part.inline_data.data
            pcm = base64.b64decode(data) if isinstance(data, str) else data
            write_pcm_wav(output, pcm)
            return
        except Exception as exc:  # SDK error types vary by release.
            last_error = exc
            if attempt < 2:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"Gemini TTS failed after 3 attempts: {last_error}")


def narration_output(beats_path: Path, beats: dict) -> Path:
    audio = (beats.get("narration") or {}).get("audio")
    if audio:
        return ROOT / "media" / audio
    project_id = beats.get("id") or beats_path.parent.name
    return ROOT / "media" / "projects" / project_id / "narration.m4a"


def emit_ts(vo: list[dict], path: Path) -> None:
    lines = ["// AUTO-GENERATED by tools/prepare_narration.py — do not edit.",
             "import type { VoLine } from '../../lib/shorts';", "", "export const VO: VoLine[] = ["]
    for line in vo:
        lines.append("  " + json.dumps({key: line[key] for key in ("text", "start", "end", "words") if key in line}, ensure_ascii=False) + ",")
    lines.extend(["];", ""])
    # JSON object syntax is valid TypeScript; protect U+2028/U+2029 parsing.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"), encoding="utf-8")


def align_or_estimate(path: Path, text: str, args: argparse.Namespace,
                      offset: float = 0.0, known_end: float | None = None) -> tuple[list[dict], float]:
    try:
        recognized, _ = whisper_words(path, args.align_model, args.language)
        words, coverage = map_words(text, recognized, offset, known_end)
    except RuntimeError:
        if not args.allow_estimated_alignment:
            raise
        words = estimate_words(text, offset, known_end or offset + duration(path))
        coverage = 0.0
    if coverage < .90 and not args.allow_estimated_alignment:
        raise RuntimeError(f"alignment coverage {coverage:.0%} is below the required 90% for: {text!r}")
    return words, coverage


def prepare_ai(beats_path: Path, beats: dict, args: argparse.Namespace) -> Path:
    key = load_env().get("GEMINI_API_KEY", "").strip()
    if not key and not args.dry_run:
        raise RuntimeError("GEMINI_API_KEY is required for --mode ai")
    vo = beats.get("vo", [])
    if not vo:
        raise RuntimeError("AI narration requires at least one authored line in beats.json vo[]")
    total = float(beats["format"]["durationSec"])
    cache = beats_path.parent / "voice"
    cache.mkdir(exist_ok=True)
    fitted: list[tuple[Path, float]] = []
    for index, line in enumerate(vo):
        delivery, transcript = delivery_and_transcript(line)
        digest = hashlib.sha1(f"gemini|{args.model}|{args.voice}|{delivery}|{transcript}".encode()).hexdigest()[:10]
        raw = cache / f"line-{index:02d}-{digest}.wav"
        start = float(line["start"])
        next_start = float(vo[index + 1]["start"]) if index + 1 < len(vo) else total - .2
        window = max(.2, next_start - start - .05)
        fit = cache / f"line-{index:02d}-{digest}-fit-{round(window * 1000)}ms.wav"
        if args.dry_run:
            print(f"{index:02d} {start:7.2f}s {args.voice}: {transcript}")
            continue
        if args.force or not raw.exists():
            gemini_tts(key, args.model, args.voice, transcript, delivery, raw)
        raw_duration = duration(raw)
        tempo = min(1.3, raw_duration / window) if raw_duration > window else 1.0
        if args.force or not fit.exists():
            run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-filter:a", f"atempo={tempo:.5f}", "-ar", "44100", "-ac", "2", str(fit)])
        fitted_duration = duration(fit)
        if fitted_duration > window + .08:
            raise RuntimeError(
                f"line {index} is {fitted_duration:.2f}s after maximum safe time compression "
                f"but its scene window is {window:.2f}s; retime the scene or shorten the line"
            )
        line["end"] = round(start + fitted_duration, 3)
        raw_words, coverage = align_or_estimate(raw, transcript, args, 0.0, raw_duration)
        line["words"] = [{"w": word["w"], "start": round(start + word["start"] / tempo, 3), "end": round(start + word["end"] / tempo, 3)} for word in raw_words]
        line["alignmentCoverage"] = round(coverage, 3)
        fitted.append((fit, start))
    if args.dry_run:
        return narration_output(beats_path, beats)
    output = narration_output(beats_path, beats)
    output.parent.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    filters: list[str] = []
    labels = []
    for index, (path, start) in enumerate(fitted):
        inputs.extend(["-i", str(path)])
        delay = round(start * 1000)
        filters.append(f"[{index}:a]adelay={delay}|{delay}[a{index}]")
        labels.append(f"[a{index}]")
    filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,apad,atrim=0:{total},loudnorm=I=-16:TP=-1.5:LRA=11[out]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters), "-map", "[out]", "-c:a", "aac", "-b:a", "192k", str(output)])
    beats["voiceStatus"] = f"gemini:{args.model}:{args.voice}"
    return output


def prepare_recorded(beats_path: Path, beats: dict, args: argparse.Namespace) -> Path:
    if not args.audio:
        raise RuntimeError("--audio is required for --mode recorded")
    source = Path(args.audio).resolve()
    if not source.exists():
        raise RuntimeError(f"recording not found: {source}")
    output = narration_output(beats_path, beats)
    output.parent.mkdir(parents=True, exist_ok=True)
    if not args.dry_run:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(source), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", str(output)])
    if args.dry_run:
        return output
    recognized, segments = whisper_words(output, args.align_model, args.language)
    vo = beats.get("vo", [])
    if not vo:
        beats["vo"] = [{"beat": "narration", "text": row["text"], "start": round(row["start"], 3), "end": round(row["end"], 3), "words": []} for row in segments if row["text"]]
        vo = beats["vo"]
    authored = " ".join(line["text"] for line in vo)
    mapped, coverage = map_words(authored, recognized, 0.0, duration(output))
    if coverage < .90 and not args.allow_estimated_alignment:
        raise RuntimeError(f"recorded narration alignment coverage {coverage:.0%} is below 90%")
    cursor = 0
    for line in vo:
        count = len(line["text"].split())
        words = mapped[cursor:cursor + count]
        cursor += count
        if words:
            line["start"], line["end"], line["words"] = words[0]["start"], words[-1]["end"], words
        line["alignmentCoverage"] = round(coverage, 3)
    beats["format"]["durationSec"] = round(duration(output), 3)
    beats["voiceStatus"] = f"recorded:{source.name}"
    return output


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--beats", required=True)
    ap.add_argument("--mode", choices=("ai", "recorded", "none"), help="defaults to beats.json narration.mode, then ai for legacy projects")
    ap.add_argument("--audio", help="recorded narration file")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--align-model", default=DEFAULT_ALIGN_MODEL)
    ap.add_argument("--language", default="en")
    ap.add_argument("--emit-ts")
    ap.add_argument("--allow-estimated-alignment", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> None:
    args = parser().parse_args(argv)
    beats_path = Path(args.beats).resolve()
    beats = json.loads(beats_path.read_text(encoding="utf-8"))
    mode = args.mode or (beats.get("narration") or {}).get("mode") or "ai"
    args.mode = mode
    if mode == "ai":
        output = prepare_ai(beats_path, beats, args)
    elif mode == "recorded":
        output = prepare_recorded(beats_path, beats, args)
    else:
        beats.setdefault("narration", {})["mode"] = "none"
        beats["voiceStatus"] = "none"
        output = narration_output(beats_path, beats)
    if not args.dry_run:
        beats.setdefault("narration", {})["mode"] = mode
        beats_path.write_text(json.dumps(beats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.emit_ts:
            emit_ts(beats.get("vo", []), Path(args.emit_ts).resolve())
    print(f"narration -> {output}")


if __name__ == "__main__":
    main()
