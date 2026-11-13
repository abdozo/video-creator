"""Prepare measured draft captions. This does not certify a listening review."""
import json
from pathlib import Path

from tools.prepare_narration import force_align_segments

ROOT = Path(__file__).resolve().parent
windows = [
    (19.94, 26.00, "طب هو فتح ربنا بيتأخر ليه؟ فتح ربنا بيتأخر عشان يختبر إصرارك. عشان يختبر إصرارك."),
    (26.00, 40.80, "تخيل أنت في البيت ومعاك مثلا والدتك ولا معاك حد حبيبك، فجأة أغمي عليه وقع من طوله. ها لسه حد بيقول لي امبارح، يعني حد من إخواننا زوجته فجأة أغمي عليها، فبيقول لي بيتصل وقاعد بيعيط الحقوني."),
    (40.80, 51.30, "طب افرض بقى اللي أنت بتتصل به، الدكتور اللي بتتصل به ساعتها ما ردش عليك. هتقول يا خسارة الدكتور ما ردش؟ يا راجل ده أنت هتتصل مية مرة، ده أنت هتتصل ميتين مرة."),
    # The anecdote at 51.30–57.56 is deliberately left uncaptioned until heard.
    (57.56, 59.40, "لازم يرد يعني لازم يرد."),
    (59.40, 71.80, "أهو بالضبط كده لو أنت خبطت على باب فرج الله وما اتفتحلكش، تمشي؟ يا ابني أنت ملكش غيره أصلا. خبط. فربنا بيختبر إصرارك. ربنا بيختبر يقينك إنه هو الحل الوحيد."),
    (72.20, 86.20, "ربنا بيختبر ثقتك فيه. ربنا بيختبر، ده أنت ممكن تروح لدكتور يقول لك الحجز بعد شهر، تفضل واقف على بابه شهر كامل. أنت هتفضل واقف على باب ربنا قد إيه؟ مستعد تفضل واقف على الباب قد إيه؟"),
    (86.50, 98.72, "أوعى لحظة ما تزهق وتمشي يكون الباب هيتفتح. أوعى. يا بخت اللي يصبر على باب ربنا، يا بخت اللي يفضل واقف وصابر على باب ربنا سبحانه وتعالى."),
    (98.72, 109.80, "عشان كده ما تقولش الفتح بيتأخر ليه. هو هو اللي أنت فيه ده نفسه فتح. لما ترفع إيدك وتعبد ربنا ده فتح. ده فتح من الله سبحانه وتعالى. ربنا بيحب ده منك."),
    (110.00, 116.16, "فلا تستعجل فتح الله فهو قادم، قادم من الله سبحانه وتعالى."),
]
rows = [{"start": a, "end": b, "text": text} for a, b, text in windows]
path = ROOT / "alignment-windows.draft.json"
path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
model = next(Path("/Users/abdozo/.cache/huggingface/hub/models--Systran--faster-whisper-small/snapshots").iterdir())
words = force_align_segments(ROOT / "candidate-context.wav", " ".join(s["text"] for s in rows), str(model), "ar", path)
(ROOT / "forced-words.draft.json").write_text(json.dumps(words, ensure_ascii=False, indent=2) + "\n")
print("Saved measured draft alignment; listening/text approval remains false.")
