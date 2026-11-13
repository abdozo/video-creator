"""Measure approved words against source audio without replacing the script with ASR."""
import json
from pathlib import Path
from tools.prepare_narration import force_align_segments

HERE = Path(__file__).resolve().parent
model = '/Users/abdozo/.cache/huggingface/hub/models--Systran--faster-whisper-small/snapshots/536b0662742c02347bc0e980a01041f333bce120'
groups = [
    ('question-payoff',390,[
        {'start':9.34,'end':12.4,'text':'ليه يتمنع عني حاجة أنا كان نفسي فيها؟'},
        {'start':12.4,'end':21.4,'text':'اعرف إنه ما منعك إلا ليعطيك وما منعك إلا ليحميك وما منعك إلا ليربيك'},
    ]),
    ('wider-door',562,[{'start':7.18,'end':11.7,'text':'ممكن ربنا منعك من باب لأن فيه باب أوسع منه ربنا هيفتحولك'}]),
]
out=[]
for name,offset,rows in groups:
    path=HERE/f'{name}.approved-windows.json'
    path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    words=force_align_segments(HERE/f'{name}.wav',' '.join(r['text'] for r in rows),model,'ar',path)
    out.append({'name':name,'offset':offset,'words':words})
(HERE/'approved-alignment.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False))
