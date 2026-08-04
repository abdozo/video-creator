import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import {VocabularyCard, SentenceParts, Correction, Pronunciation, FillBlank} from '../../lib/english';
import {ChapterCard, ChapterProgress, MotionCanvas} from '../../lib/video';

export const compositionConfig = {
  id: 'EnglishLessonDemo',
  durationInSeconds: 15,
  fps: 30,
  width: 1920,
  height: 1080,
};

const Center: React.FC<{children:React.ReactNode}> = ({children}) => <AbsoluteFill style={{justifyContent:'center',alignItems:'center',padding:'10%'}}>{children}</AbsoluteFill>;

const EnglishLessonDemo: React.FC = () => {
  const frame = useCurrentFrame();
  const active = frame < 180 ? 0 : frame < 360 ? 1 : frame < 405 ? 2 : 3;
  return <MotionCanvas format="video">
    <ChapterProgress chapters={['Meaning','Grammar','Pronunciation','Practice']} active={active}/>
    <Sequence durationInFrames={90}><ChapterCard kicker="ENGLISH IN CONTEXT" title="Use “depend on” naturally" subtitle="Teaching text stays readable even without subtitles." at={-18}/></Sequence>
    <Sequence from={90} durationInFrames={90}><Center><VocabularyCard word="depend on" meaning="to need or be decided by something" example="The result depends on how often you practice."/></Center></Sequence>
    <Sequence from={180} durationInFrames={90}><Center><SentenceParts parts={[{text:'The result',role:'subject'},{text:'depends on',role:'verb'},{text:'practice',role:'object'}]}/></Center></Sequence>
    <Sequence from={270} durationInFrames={90}><Center><Correction wrong="It depends of the weather." correct="It depends on the weather." revealAt={24}/></Center></Sequence>
    <Sequence from={360} durationInFrames={90}><Center><div style={{display:'grid',gap:70}}><Pronunciation word="depend" phonetic="/dɪˈpend/" syllables={['de','PEND']} stress={1}/><FillBlank before="It depends" answer="on" after="the context." revealAt={34}/></div></Center></Sequence>
  </MotionCanvas>;
};

export default EnglishLessonDemo;
