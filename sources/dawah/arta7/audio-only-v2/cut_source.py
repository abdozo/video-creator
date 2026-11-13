"""Audio-only experiment: trim interiors of two measured low-energy pauses."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PROJECT = "short-17-before-the-door-opens-audio-only"
media = ROOT / "media/projects" / PROJECT
source = next((ROOT / "projects_assets/Arta7").glob("*.mp4"))
keep = [(0, 52.1), (52.43333333333333, 55.4), (55.733333333333334, 96.23333333333333)]
filters = []
for i, (a, b) in enumerate(keep):
    duration = b - a
    filters.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v{i}]")
    # Five millisecond audio ramps remain inside the retained quiet margins.
    fade = (f",afade=t=in:st=0:d=0.005" if i else "") + (f",afade=t=out:st={duration-.005}:d=0.005" if i < len(keep)-1 else "")
    filters.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS{fade}[a{i}]")
filters.append("".join(f"[v{i}][a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-n", "-ss", "1537.92", "-t", "96.24", "-i", str(source),
                "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                "-c:a", "aac", "-movflags", "+faststart", str(media / "source-clip.mp4")], check=True)
duration = sum(b-a for a,b in keep)
joins = [keep[0][1], keep[0][1]+keep[1][1]-keep[1][0]]
(HERE / "edit.json").write_text(json.dumps({"source": str(source), "sourceOffset": 1537.92, "sourceDuration": 96.24,
    "keep": [{"start": a, "end": b} for a,b in keep], "duration": duration, "joins": joins,
    "removed": [{"start": 52.1, "end": 52.43333333333333}, {"start":55.4,"end":55.733333333333334}],
    "pauseEvidence": {"method": "FFmpeg silencedetect -30dB, minimum .25s; 125–160ms quiet padding retained", "detected": [[51.974063,52.5925],[55.249813,55.880313]], "listened": False},
    "transcriptPolicy": "Fresh ASR from edited source audio only. No original TXT, previous captions or forced text used.",
    "display": "contain; entire source width; no animated zoom; no sharpening/upscaling pass beyond 854-to-1080 width fit"}, ensure_ascii=False, indent=2)+"\n")
print(json.dumps({"duration":duration,"joins":joins,"removedSeconds":96.24-duration}))
