"""Assemble the owner-approved paper-only Short in editorial playback order."""
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
PROJECT_ID='short-18-the-closed-door'
PROJECT=ROOT/'shorts'/PROJECT_ID
SHOT=ROOT/'remotion/src/shots/short-18'
MEDIA=ROOT/'media/projects'/PROJECT_ID
source=next((ROOT/'projects_assets/Arta7').glob('*.mp4'))
keep=[
    {'start':399+10/30,'end':402.4,'role':'hook','text':'ليه يتمنع عني حاجة أنا كان نفسي فيها؟'},
    {'start':569+5/30,'end':573+19/30,'role':'development','text':'ممكن ربنا منعك من باب لأن فيه باب أوسع منه ربنا هيفتحولك'},
    {'start':402.4,'end':411.4,'role':'payoff','text':'اعرف إنه ما منعك إلا ليعطيك وما منعك إلا ليحميك وما منعك إلا ليربيك'},
]
duration=sum(r['end']-r['start'] for r in keep)
assert round(duration*30)==496
joins=[keep[0]['end']-keep[0]['start'], sum(r['end']-r['start'] for r in keep[:2])]
alignment=json.loads((HERE/'approved-alignment.json').read_text())
words=[{'text':w['word'],'start':g['offset']+w['start'],'end':g['offset']+w['end']} for g in alignment for w in g['words']]
output_words=[]
offset=0
for row in keep:
    selected=[w for w in words if row['start']<=w['start']<row['end']]
    output_words.extend({**w,'start':w['start']-row['start']+offset,'end':min(w['end'],row['end'])-row['start']+offset} for w in selected)
    offset+=row['end']-row['start']
assert len(output_words)==34
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cues=[
    {'start':0,'end':3.03,'text':'ليه الباب\nاتقفل؟','motion':'book','angle':-1.4},
    {'start':3.0666666667,'end':5.7,'text':'مش كل منع\nحرمان','motion':'page','angle':1.3},
    {'start':5.7333333333,'end':11.2666666667,'text':'يمكن فيه\nباب أوسع','motion':'book','angle':-1},
    {'start':11.3,'end':13.7666666667,'text':'قد يكون المنع\nحماية','motion':'lift','angle':.8},
    {'start':13.8,'end':duration+1,'text':'اطمّن لحكمة\nربنا','motion':'book','angle':-1.6},
]
save(SHOT/'edit.json',{'joins':joins,'cues':cues,'storyDuration':duration,'duration':duration+1,'endFadeSeconds':1})
static_video=f'projects/{PROJECT_ID}/source-clip.mp4'
save(SHOT/'clip.json',{'video':static_video,'title':'الباب اللي اتقفل','speaker':'د. حازم شومان','fit':'cover','position':50,'captionMode':'none','captions':[],'emphasis':[],'visualMode':'speaker'})
save(HERE/'edit-plan.json',{'source':str(source),'keep':keep,'duration':duration,'joins':joins,'words':output_words,'scriptApproved':True,'listened':False,'captions':'none','paperText':'approved editorial slogans, not spoken quotations'})
beats=json.loads((PROJECT/'beats.json').read_text())
beats['format']['durationSec']=duration+1
beats['ending']={'freezeAtFrame':495,'fadeStartFrame':496,'blackFrame':525}
beats.update(title='الباب اللي اتقفل',editorialStatus='approved-script-render-for-review',source={'video':str(source),'keep':keep,'review':{'context':True,'scriptApproved':True,'listened':False}},
    narration={'mode':'recorded','audio':static_video,'embedded':True},captions={'mode':'none'},
    vo=[{'text':r['text'],'sourceStart':r['start'],'sourceEnd':r['end']} for r in keep],beats=[{**c,'kind':'editorial-label'} for c in cues])
save(PROJECT/'beats.json',beats)
script='\n\n'.join(r['text'] for r in keep)
(PROJECT/'script.md').write_text('# الباب اللي اتقفل\n\nنص وافق عليه المستخدم قبل التنفيذ.\n\n'+script+'\n\n## المونتاج\n\n'+ '\n'.join(f"- {r['start']:.3f}–{r['end']:.3f}: {r['role']}" for r in keep)+ '\n\nفيديو طولي يملأ الشاشة، بدون كابشن. خمس شعارات تحريرية على ورق أصفر بحواف بيضاء ممزقة وظل وحركة فتح صفحات. لا موسيقى ولا TTS.\n\nاستُخدم النص المعتمد للمحاذاة، لا لاستبدال صوت الشيخ. حدود القص مقاسة بمحاذاة محلية؛ لم يُسجّل اعتماد استماع مباشر.\n',encoding='utf-8')
tsx=next(SHOT.glob('Short18*.tsx'))
tsx.write_text(re.sub(r'durationInSeconds: [0-9.]+,', 'durationInSeconds: 17.533333333333335,', tsx.read_text()))
args=['ffmpeg','-v','error','-nostdin','-y']
for r in keep:
    args+=['-ss',str(r['start']),'-t',str(r['end']-r['start']),'-i',str(source)]
filters=[]
for i,r in enumerate(keep):
    frames=round((r['end']-r['start'])*30)
    filters += [f'[{i}:v]setpts=PTS-STARTPTS,fps=30,trim=end_frame={frames},format=yuv420p[v{i}]', f'[{i}:a]asetpts=PTS-STARTPTS[a{i}]']
filters.append(''.join(f'[v{i}][a{i}]' for i in range(len(keep)))+'concat=n=3:v=1:a=1[v][a]')
args+=['-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-movflags','+faststart',str(MEDIA/'source-clip.mp4')]
subprocess.run(args,check=True)
print(json.dumps({'duration':duration,'joins':joins,'approvedWords':len(output_words)}))
