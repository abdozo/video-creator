import React from 'react';
import {Sequence} from 'remotion';
import {FONT_BODY, FONT_DISPLAY} from '../../fonts';
import {ActionList, CharacterGlyph, DrawnUnderline, IdeaThread, WHITEBOARD, WhiteboardCanvas} from '../../lib/whiteboard';

export const compositionConfig = {
  id: 'WhiteboardShortDemo',
  durationInSeconds: 8,
  fps: 30,
  width: 1080,
  height: 1920,
};

const WhiteboardShortDemo: React.FC = () => (
  <WhiteboardCanvas format="short">
    <div style={{position:'absolute',top:180,left:92,right:92,fontFamily:FONT_DISPLAY,fontWeight:700,fontSize:92,lineHeight:1.02,letterSpacing:-3}}>
      Procrastination is not a time problem.
    </div>
    <DrawnUnderline x={92} y={500} width={790} at={18} canvas={{w:1080,h:1920}}/>
    <CharacterGlyph x={450} y={640} size={210} at={32}/>
    <IdeaThread d="M 540 820 C 760 850, 920 930, 900 1090 C 890 1270, 820 1390, 790 1510" at={48} duration={70} viewBox="0 0 1080 1920"/>
    <Sequence from={88} layout="none">
      <div style={{position:'absolute',top:930,left:100,right:100,fontFamily:FONT_BODY,fontSize:50,lineHeight:1.28,color:WHITEBOARD.muted}}>
        It is usually an emotion you are trying not to feel.
      </div>
    </Sequence>
    <Sequence from={134} layout="none">
      <ActionList format="short" title="MAKE IT LIGHTER" items={['Name the feeling.', 'Shrink the first step.', 'Start for five minutes.']} at={0}/>
    </Sequence>
  </WhiteboardCanvas>
);

export default WhiteboardShortDemo;
