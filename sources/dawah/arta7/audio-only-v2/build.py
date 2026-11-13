"""Render the tool's audio-only ASR result without editorial word substitutions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PROJECT_ID = "short-17-before-the-door-opens-audio-only"
PROJECT = ROOT / "shorts" / PROJECT_ID
SHOT = ROOT / "remotion/src/shots/short-17"
edit = json.loads((HERE / "edit.json").read_text())
asr = json.loads((HERE / "transcript.asr.json").read_text())
def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

def mapped(t):
    offset = 0
    for row in edit["keep"]:
        a, b = row["start"], row["end"]
        if t < a:
            return offset
        if a <= t <= b:
            return offset + t-a
        offset += b-a
    return offset

captions = []
original_words = [w for s in asr["segments"] for w in s["words"]]
for row in asr["segments"]:
    group = []
    for index, word in enumerate(row["words"]):
        start, end = mapped(word["start"]), mapped(word["end"])
        if end <= start:
            raise ValueError(f"A recognized word would be removed: {word}")
        group.append({"text": word["text"], "start": start, "end": end})
        if len(group) == 4 or index == len(row["words"])-1:
            captions.append({"text": " ".join(w["text"] for w in group), "start":group[0]["start"], "end":group[-1]["end"], "words":group})
            group = []
output_words = [w for c in captions for w in c["words"]]
assert [w["text"] for w in output_words] == [w["text"] for w in original_words]
assert all(a["end"] <= b["start"]+.00001 for a,b in zip(output_words,output_words[1:]))
emphasis = [
    {"start": 2.8, "end": 6.0, "text": "إصرارك", "kind": "label", "animation": "slide", "paper": "torn"},
    {"start": mapped(91.0), "end": edit["duration"]-.1, "text": "فلا تستعجل فتح الله", "kind": "quote", "animation": "unfold", "paper": "strip"},
]
assert emphasis[1]["text"] in " ".join(w["text"] for w in output_words)
video = f"projects/{PROJECT_ID}/source-clip.mp4"
data = {"video":video, "title":"أوعى تمشي قبل ما الباب يتفتح", "speaker":"د. حازم شومان", "fit":"contain", "position":50,
        "visualMode":"speaker", "captionMode":"word-highlight", "captions":captions, "emphasis":emphasis, "cutaways":[]}
save(SHOT / "clip.json", data)
beats = json.loads((PROJECT / "beats.json").read_text())
beats.update(title=data["title"], editorialStatus="audio-only-asr-experiment", transcriptSource="audio-only-v2/transcript.asr.json; no supplied text or old captions read",
    source={"video":edit["source"], "start":1537.92, "end":1634.16,
            "keep":[{"start":1537.92+w["start"],"end":1537.92+w["end"]} for w in edit["keep"]],
            "review":{"context":True,"listened":False,"text":False,"approved":False}},
    narration={"mode":"recorded","audio":video,"embedded":True}, captions={"mode":"word-highlight"},
    vo=[{**c,"words":[{"w":w["text"],"start":w["start"],"end":w["end"]} for w in c["words"]]} for c in captions],
    beats=emphasis, visualMode="speaker", cutaways=[])
beats["format"]["durationSec"] = edit["duration"]
save(PROJECT / "beats.json", beats)
save(HERE / "captions.output.json", {"status":"raw-audio-asr-words-remapped-no-text-corrections", "captions":captions})
(PROJECT / "script.md").write_text("""# اختبار التفريغ من الصوت فقط

نفس مقطع المصدر 25:37.920 إلى 27:14.160، بعرض الصورة كاملة داخل إطار طولي وخلفية داكنة هادئة.
لا زوم متحرك ولا قص يملأ الشاشة. ضبط العرض من 854 إلى 1080 فقط.

الكابشن مأخوذ حرفيًا من تشغيل أداة transcribe على الصوت المعزول. لم يُقرأ ملف التكست المرفق ولم تُستخدم كلمات النسخة السابقة أو نص مفروض للمزامنة.
أُعيد توزيع توقيت الكلمات حسابيًا عبر قصتين داخل فترتين منخفضتي الطاقة. لا كلمة معترف بها حُذفت من الكابشن. التفريغ الخام محفوظ للتدقيق.
تشغيل آخر على الصوت بعد المونتاج محفوظ للمقارنة فقط؛ استُخدم تشغيل الصوت الأصلي المعزول لأنه أوضح في بداية السؤال.

السكتات المقاسة: 51.974–52.593 و55.250–55.880 من بداية الاختيار. المحذوف 52.100–52.433 و55.400–55.733؛ بقي نحو 125–160 مللي ثانية من الهدوء على الجانبين.
تلاشي بصري خفيف على أربعة فريمات حول كل وصلة؛ تدرج صوتي خمسة مللي ثانية داخل الهدوء فقط، بدون تداخل كلام أو تغيير سرعة.

هذه تجربة لقياس جودة ASR الخام. توجد أخطاء تعرف واضحة، ولم يُعتمد النص دينيًا أو بالسماع المباشر. لا تُعامل كتفريغ مُراجع أو نسخة نشر نهائية.

## النص الناتج من الأداة

""" + "\n\n".join(s["text"] for s in asr["segments"]) + "\n", encoding="utf-8")
print(json.dumps({"captions":len(captions),"words":len(output_words),"duration":edit["duration"],"textPreservedExactly":True}))
