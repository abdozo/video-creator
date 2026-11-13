"""Build a review-only artifact without marking the gated batch export approved."""
import json
import shutil
from pathlib import Path

from tools.dawah_clips import local_data, load_plan, write_json

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PROJECT_ID = "short-15-before-the-door-opens"
PROJECT = ROOT / "shorts" / PROJECT_ID
SHOT = ROOT / "remotion/src/shots/short-15"
MEDIA = ROOT / "media/projects" / PROJECT_ID
START, END = 1537.92, 1634.16
words = json.loads((HERE / "forced-words.draft.json").read_text())
windows = json.loads((HERE / "alignment-windows.draft.json").read_text())
segments = []
for window in windows:
    selected = [w for w in words if window["start"] <= w["start"] < window["end"]]
    group = []
    for index, word in enumerate(selected):
        group.append({"text": word["word"], "start": round(1518 + word["start"], 4), "end": round(1518 + word["end"], 4)})
        gap = index + 1 < len(selected) and selected[index + 1]["start"] - word["end"] > .25
        if len(group) == 4 or word["word"].endswith((".", "؟", "،")) or gap or index == len(selected) - 1:
            segments.append({"start": group[0]["start"], "end": group[-1]["end"], "text": " ".join(w["text"] for w in group), "words": group})
            group = []
write_json(HERE / "transcript.draft.json", {"status": "measured-alignment-needs-listening-and-text-review", "segments": segments})
review = {"context": True, "listened": False, "text": False, "approved": False}
clip = {"slug": "before-the-door-opens", "title": "أوعى تمشي قبل ما الباب يتفتح", "start": START, "end": END,
        "reason": "This continuous passage already tells the complete delayed-answer story: question, doctor analogy, persistence and payoff. Other provision/opening passages in the full lesson do not strengthen that specific argument. Review preview only.",
        "keep": [{"start": START, "end": END, "role": "complete-story", "reason": "Preserve the original question, analogy and answer together; no internal joins before listening review."}],
        "captionMode": "word-highlight", "visualMode": "speaker", "fit": "cover", "position": 50,
        "review": review,
        "emphasis": [{"start": 1583.86, "end": 1586.28, "kind": "quote", "text": "أنت ملكش غيره أصلا"},
                     {"start": 1629.76, "end": 1634.00, "kind": "quote", "text": "فلا تستعجل فتح الله"}]}
source = {"video": str(next((ROOT / "projects_assets/Arta7").glob("*.mp4"))), "url": "", "speaker": "د. حازم شومان"}
plan = {"version": 1, "status": "review-preview-not-approved", "source": source, "transcript": "transcript.draft.json", "clips": [clip]}
write_json(HERE / "clips.json", plan)
plan, segments = load_plan(HERE / "clips.json")
static_video = f"projects/{PROJECT_ID}/source-clip.mp4"
data = local_data(plan, clip, segments, static_video)
write_json(SHOT / "clip.json", data)
shutil.copyfile(HERE / "candidate-preview.mp4", MEDIA / "source-clip.mp4")
beats = json.loads((PROJECT / "beats.json").read_text())
beats.update(title=clip["title"], editorialStatus="review-preview-not-approved", source={**source, "start": START, "end": END, "keep": clip["keep"], "review": review},
             narration={"mode": "recorded", "audio": static_video, "embedded": True}, captions={"mode": "word-highlight"},
             vo=[{**c, "words": [{"w": w["text"], "start": w["start"], "end": w["end"]} for w in c["words"]]} for c in data["captions"]],
             beats=data["emphasis"], visualMode="speaker", cutaways=[])
write_json(PROJECT / "beats.json", beats)
(PROJECT / "script.md").write_text("""# أوعى تمشي قبل ما الباب يتفتح

نسخة مراجعة فقط. لم يتم اعتماد السماع أو النص أو النشر.

مصدر متصل من 25:37.920 إلى 27:14.160، من دون حذف داخلي أو تغيير سرعة أو موسيقى.
الافتتاح سؤال عن تأخر الفرج، ثم مثال الإلحاح في الاتصال بالطبيب، ثم الإلحاح في الدعاء، ثم خاتمة أن الدعاء نفسه فتح.

الكابشن مسودة تجمع مقارنة التفريغ المرفق مع تفريغين محليين، ومحاذاة فعلية لصوت المصدر. لا تمثل المحاذاة اعتمادًا لصحة الألفاظ.
تُركت الحكاية الجانبية من 26:09.300 إلى 26:15.560 بلا كابشن لأن ألفاظها غير محسومة. الصوت الأصلي محفوظ بالكامل.
لا آية ولا حديث مقتبس داخل الاختيار بحسب النصوص المقارنة. الكلام السابق عن «من أحصاها» خارج حدود الاختيار.

يلزم قبل الاعتماد: الاستماع المتصل للمقطع، تصحيح الألفاظ وبخاصة 25:44–26:18، مراجعة أول وآخر مقطع صوتي، ومراجعة توقيت الكلمات.
الخطة وملفات المحاذاة والتفريغ موجودة في sources/dawah/arta7. حقول listened/text/approved ما زالت false.
""", encoding="utf-8")
print(json.dumps({"project": str(PROJECT), "captions": len(data["captions"]), "words": len(words), "review": review}, ensure_ascii=False))
