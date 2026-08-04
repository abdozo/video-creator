import React from 'react';
import {Sequence} from 'remotion';
import {FONT_DISPLAY} from '../../fonts';
import {ActionList, BoardCamera, BookCard, CauseEffect, ConceptMap, EraseReveal, IdeaThread, WHITEBOARD, WhiteboardCanvas} from '../../lib/whiteboard';

export const compositionConfig = {
  id: 'WhiteboardVideoDemo',
  durationInSeconds: 18,
  fps: 30,
  width: 1920,
  height: 1080,
};

const ChapterLabel: React.FC<{n:string; title:string}> = ({n,title}) => <div style={{position:'absolute',left:88,top:58,fontFamily:FONT_DISPLAY,fontSize:22,letterSpacing:4,color:WHITEBOARD.muted}}>{n} / {title.toUpperCase()}</div>;

const WhiteboardVideoDemo: React.FC = () => (
  <WhiteboardCanvas format="video">
    <Sequence durationInFrames={150}>
      <BookCard title="The Practice of Focus" author="A modern summary" subtitle="Three ideas for protecting attention" at={-18}/>
      <IdeaThread d="M 300 830 C 680 900, 1080 760, 1590 840" at={44} duration={65}/>
    </Sequence>
    <Sequence from={150} durationInFrames={150}>
      <ChapterLabel n="01" title="The loop"/>
      <EraseReveal at={8} duration={28}><CauseEffect cause="Every interruption leaves attention residue." effect="The next task begins with less working memory." at={18}/></EraseReveal>
    </Sequence>
    <Sequence from={300} durationInFrames={150}>
      <ChapterLabel n="02" title="The map"/>
      <BoardCamera keyframes={[{frame:0,x:0,y:0,scale:1},{frame:149,x:-55,y:18,scale:1.06}]}>
        <ConceptMap at={14} nodes={[
          {title:'Protect',detail:'Choose one clear outcome.',x:160,y:290},
          {title:'Practice',detail:'Work inside a finite block.',x:780,y:590},
          {title:'Recover',detail:'Reset before the next block.',x:1380,y:290},
        ]} links={[{from:0,to:1},{from:1,to:2}]}/>
      </BoardCamera>
    </Sequence>
    <Sequence from={450} durationInFrames={90}>
      <ChapterLabel n="03" title="Synthesis"/>
      <ActionList items={['Define the finish line.', 'Remove one predictable interruption.', 'Leave a recovery gap.']} at={8}/>
    </Sequence>
  </WhiteboardCanvas>
);

export default WhiteboardVideoDemo;
