import React from 'react';
import {AbsoluteFill, interpolate, Sequence, useCurrentFrame} from 'remotion';
import {EASINGS} from '../../brand';
import {FONT_BODY, FONT_DISPLAY, FONT_MONO} from '../../fonts';
import {
  CharacterGlyph,
  DrawnUnderline,
  IdeaThread,
  InkPath,
  WHITEBOARD,
  WhiteboardCanvas,
} from '../../lib/whiteboard';

// =============================================================================
// COMPOSITION CONFIG
// =============================================================================
export const compositionConfig = {
  id: 'Video2TwoMinuteRuleSketchbook',
  durationInSeconds: 60,
  fps: 30,
  width: 1920,
  height: 1080,
};

// =============================================================================
// SHARED TIMING + COMPONENTS
// =============================================================================
const SCENE = 300;

const progress = (frame: number, at: number, duration = 18) =>
  interpolate(frame, [at, at + duration], [0, 1], {
    easing: EASINGS.easeOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

const fadeOut = (frame: number) =>
  interpolate(frame, [274, 296], [1, 0], {
    easing: EASINGS.easeIn,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

const Reveal: React.FC<{
  children: React.ReactNode;
  at?: number;
  style?: React.CSSProperties;
}> = ({children, at = 0, style}) => {
  const frame = useCurrentFrame();
  const p = progress(frame, at);
  return (
    <div style={{...style, opacity: p, transform: `translateY(${(1 - p) * 18}px)`}}>
      {children}
    </div>
  );
};

const SceneBoard: React.FC<{
  children: React.ReactNode;
  number: string;
  title: string;
  holdEnd?: boolean;
}> = ({children, number, title, holdEnd = false}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{opacity: holdEnd ? 1 : fadeOut(frame)}}>
      <div style={{position: 'absolute', left: 78, top: 48, fontFamily: FONT_MONO, fontSize: 18, letterSpacing: 3, color: WHITEBOARD.muted}}>
        {number} / {title.toUpperCase()}
      </div>
      <div style={{position: 'absolute', right: 78, top: 48, fontFamily: FONT_MONO, fontSize: 15, letterSpacing: 2, color: WHITEBOARD.muted}}>
        ATOMIC HABITS · ONE IDEA
      </div>
      <InkPath d="M 78 1000 C 520 994, 1070 1008, 1842 998" at={0} duration={36} color={WHITEBOARD.line} width={3} />
      <IdeaThread d={`M 78 1000 C ${78 + (1764 * frame) / (SCENE - 1)} 996, ${78 + (1764 * frame) / (SCENE - 1)} 1004, ${78 + (1764 * frame) / (SCENE - 1)} 1000`} at={0} duration={1} />
      {children}
    </AbsoluteFill>
  );
};

const Heading: React.FC<{children: React.ReactNode; at?: number; width?: number}> = ({children, at = 0, width = 1420}) => (
  <Reveal at={at} style={{position: 'absolute', left: 110, top: 140, width, fontFamily: FONT_DISPLAY, fontSize: 78, lineHeight: 1.06, letterSpacing: -3, fontWeight: 700}}>
    {children}
  </Reveal>
);

// =============================================================================
// SCENE 1 — THE STARTING PROBLEM
// =============================================================================
const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const tiny = progress(frame, 138, 34);
  return (
    <SceneBoard number="01" title="The problem">
      <div style={{position: 'absolute', left: 110, top: 150, fontFamily: FONT_DISPLAY, fontSize: 104, lineHeight: 1.02, letterSpacing: -5, fontWeight: 700}}>
        Starting feels <span style={{color: WHITEBOARD.amber}}>too big.</span>
      </div>
      <DrawnUnderline x={790} y={270} width={390} at={18} color={WHITEBOARD.amber} />

      <Reveal at={42} style={{position: 'absolute', left: 115, top: 340, width: 720, fontFamily: FONT_BODY, fontSize: 35, lineHeight: 1.45, color: WHITEBOARD.muted}}>
        We picture the entire mountain before taking the first step.
      </Reveal>

      <InkPath
        d="M 1020 790 L 1165 650 L 1275 695 L 1435 500 L 1545 550 L 1770 300"
        at={16}
        duration={88}
        color={WHITEBOARD.ink}
        width={7}
        cursor
      />
      <InkPath d="M 1018 790 L 1780 790" at={12} duration={34} color={WHITEBOARD.muted} width={3} />
      <CharacterGlyph x={850} y={655} size={150} at={42} />

      <div style={{position: 'absolute', left: 1060, top: 810, fontFamily: FONT_MONO, fontSize: 18, color: WHITEBOARD.muted, letterSpacing: 2}}>THE WHOLE HABIT</div>
      <div style={{position: 'absolute', left: 115, top: 640, display: 'flex', alignItems: 'center', gap: 26, opacity: tiny}}>
        <div style={{width: 62, height: 62, borderRadius: '50%', background: WHITEBOARD.indigo, color: '#fff', display: 'grid', placeItems: 'center', fontFamily: FONT_DISPLAY, fontSize: 34, fontWeight: 700}}>1</div>
        <div>
          <div style={{fontFamily: FONT_DISPLAY, fontSize: 40, fontWeight: 650}}>Focus on the doorway.</div>
          <div style={{fontFamily: FONT_BODY, fontSize: 28, color: WHITEBOARD.muted, marginTop: 6}}>Make the first move obvious.</div>
        </div>
      </div>
      <IdeaThread d="M 118 760 C 330 815, 590 785, 830 720" at={172} duration={64} />
    </SceneBoard>
  );
};

// =============================================================================
// SCENE 2 — THE TWO-MINUTE RULE
// =============================================================================
const RuleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const two = progress(frame, 56, 20);
  return (
    <SceneBoard number="02" title="The rule">
      <Heading width={980}>The Two-Minute Rule</Heading>
      <DrawnUnderline x={108} y={245} width={790} at={18} />
      <Reveal at={46} style={{position: 'absolute', left: 115, top: 315, width: 820, fontFamily: FONT_BODY, fontSize: 36, lineHeight: 1.5, color: WHITEBOARD.muted}}>
        Scale a new habit down to a starter version that takes under two minutes.
      </Reveal>
      <Reveal at={112} style={{position: 'absolute', left: 115, top: 545, padding: '22px 26px', borderLeft: `6px solid ${WHITEBOARD.indigo}`, background: 'rgba(255,255,255,.54)', fontFamily: FONT_BODY, fontSize: 21, color: WHITEBOARD.muted}}>
        Concept paraphrased from <i>Atomic Habits</i> by James Clear.
      </Reveal>

      <InkPath
        d="M 1410 208 A 265 265 0 1 1 1409.8 208"
        at={18}
        duration={72}
        color={WHITEBOARD.indigo}
        width={9}
        cursor
      />
      <InkPath d="M 1410 240 L 1410 285 M 1410 735 L 1410 780 M 1155 495 L 1110 495 M 1665 495 L 1710 495" at={76} duration={46} color={WHITEBOARD.muted} width={4} />
      <div style={{position: 'absolute', left: 1190, top: 330, width: 440, textAlign: 'center', opacity: two, transform: `scale(${0.94 + two * 0.06})`}}>
        <div style={{fontFamily: FONT_DISPLAY, fontSize: 190, lineHeight: 0.9, letterSpacing: -10, fontWeight: 700, color: WHITEBOARD.indigo}}>2</div>
        <div style={{fontFamily: FONT_MONO, fontSize: 25, letterSpacing: 6, color: WHITEBOARD.muted, marginTop: 26}}>MINUTES</div>
      </div>
      <IdeaThread d="M 1410 208 C 1535 265, 1605 355, 1635 470" at={150} duration={58} />
    </SceneBoard>
  );
};

// =============================================================================
// SCENE 3 — TRANSLATE AMBITION
// =============================================================================
const EXAMPLES = [
  {before: 'Read every night', after: 'Read one page'},
  {before: 'Work out', after: 'Put on your shoes'},
  {before: 'Meditate daily', after: 'Take one slow breath'},
];

const ExamplesScene: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <SceneBoard number="03" title="Make it tiny">
      <Heading>Translate ambition into an entrance.</Heading>
      <DrawnUnderline x={108} y={245} width={1160} at={20} />
      <div style={{position: 'absolute', left: 150, right: 150, top: 330}}>
        {EXAMPLES.map((item, index) => {
          const at = 38 + index * 48;
          const row = progress(frame, at, 16);
          const after = progress(frame, at + 40, 18);
          const cross = progress(frame, at + 28, 26);
          const y = index * 180;
          return (
            <React.Fragment key={item.before}>
              <div style={{position: 'absolute', left: 0, top: y, width: 1620, height: 132, borderBottom: `2px solid ${WHITEBOARD.line}`, opacity: row, display: 'grid', gridTemplateColumns: '90px 1fr 180px 1fr', alignItems: 'center'}}>
                <div style={{fontFamily: FONT_MONO, fontSize: 20, color: WHITEBOARD.muted}}>0{index + 1}</div>
                <div style={{fontFamily: FONT_BODY, fontSize: 35, color: WHITEBOARD.muted}}>{item.before}</div>
                <div style={{fontFamily: FONT_DISPLAY, fontSize: 48, color: WHITEBOARD.indigo, opacity: after, textAlign: 'center'}}>→</div>
                <div style={{fontFamily: FONT_DISPLAY, fontSize: 39, fontWeight: 650, opacity: after, transform: `translateX(${(1 - after) * 20}px)`}}>{item.after}</div>
                <svg viewBox="0 0 560 60" style={{position: 'absolute', left: 72, top: 40, width: 560, height: 60, overflow: 'visible'}}>
                  <path d="M 0 32 C 145 18, 315 45, 555 25" fill="none" stroke={WHITEBOARD.amber} strokeWidth="5" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - cross} />
                  <path d="M 4 36 C 150 23, 320 49, 551 29" fill="none" stroke={WHITEBOARD.amber} strokeWidth="7" strokeLinecap="round" opacity=".12" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - cross} />
                </svg>
              </div>
            </React.Fragment>
          );
        })}
      </div>
      <IdeaThread d="M 760 884 C 1020 845, 1310 900, 1600 855" at={195} duration={64} />
    </SceneBoard>
  );
};

// =============================================================================
// SCENE 4 — LOWER FRICTION
// =============================================================================
const FrictionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const lift = interpolate(frame, [72, 150], [0, 225], {
    easing: EASINGS.easeInOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const walker = interpolate(frame, [132, 232], [0, 760], {
    easing: EASINGS.easeInOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <SceneBoard number="04" title="Lower the threshold">
      <Heading>Reduce the energy required to begin.</Heading>
      <Reveal at={34} style={{position: 'absolute', left: 115, top: 250, fontFamily: FONT_BODY, fontSize: 33, color: WHITEBOARD.muted}}>
        Once motion starts, continuing becomes a separate choice.
      </Reveal>
      <InkPath d="M 330 720 C 650 710, 1040 730, 1570 715" at={28} duration={54} color={WHITEBOARD.muted} width={4} />
      <div style={{position: 'absolute', left: 700, top: 500, width: 130, height: 280, transform: `translateY(-${lift}px)`}}>
        <svg viewBox="0 0 130 280" width="130" height="280">
          <path d="M 8 270 L 8 15 Q 65 -5 122 15 L 122 270" fill="rgba(216,144,67,.12)" stroke={WHITEBOARD.amber} strokeWidth="6" strokeLinecap="round" />
        </svg>
        <div style={{position: 'absolute', left: 34, top: 54, fontFamily: FONT_MONO, fontSize: 16, color: WHITEBOARD.amber, letterSpacing: 2, writingMode: 'vertical-rl'}}>STARTING FRICTION</div>
      </div>
      <div style={{position: 'absolute', left: 270 + walker, top: 574, width: 120, height: 140}}>
        <CharacterGlyph x={0} y={0} size={120} at={50} color={WHITEBOARD.ink} />
      </div>
      <Reveal at={178} style={{position: 'absolute', left: 1040, top: 775, padding: '20px 28px', border: `2px solid ${WHITEBOARD.teal}`, borderRadius: 14, background: 'rgba(255,255,255,.58)', fontFamily: FONT_DISPLAY, fontSize: 34, fontWeight: 650, color: WHITEBOARD.teal}}>
        The doorway is the habit.
      </Reveal>
      <IdeaThread d="M 1110 855 C 1270 890, 1450 850, 1620 875" at={198} duration={48} />
    </SceneBoard>
  );
};

// =============================================================================
// SCENE 5 — MOMENTUM + IDENTITY
// =============================================================================
const MomentumScene: React.FC = () => {
  const frame = useCurrentFrame();
  const stamps = ['START', 'REPEAT', 'REPEAT', 'IDENTITY'];
  const points = [
    {x: 1030, y: 790},
    {x: 1215, y: 665},
    {x: 1410, y: 515},
    {x: 1610, y: 330},
  ];
  return (
    <SceneBoard number="05" title="Momentum">
      <Heading width={820}>Small starts create evidence.</Heading>
      <Reveal at={38} style={{position: 'absolute', left: 115, top: 365, width: 700, fontFamily: FONT_BODY, fontSize: 36, lineHeight: 1.5, color: WHITEBOARD.muted}}>
        Each repetition is a vote for the person you want to become.
      </Reveal>
      <Reveal at={148} style={{position: 'absolute', left: 115, top: 640, fontFamily: FONT_MONO, fontSize: 22, letterSpacing: 3, color: WHITEBOARD.teal}}>
        START → REPEAT → IDENTITY
      </Reveal>

      <IdeaThread d="M 1010 815 C 1120 770, 1140 705, 1215 680 C 1310 650, 1320 565, 1410 530 C 1510 490, 1545 385, 1630 330" at={22} duration={156} />
      {points.map((point, index) => {
        const p = progress(frame, 48 + index * 43, 16);
        return (
          <div key={point.x} style={{position: 'absolute', left: point.x - 22, top: point.y - 22, width: 44, height: 44, borderRadius: '50%', background: index === 3 ? WHITEBOARD.teal : WHITEBOARD.paper, border: `5px solid ${index === 3 ? WHITEBOARD.teal : WHITEBOARD.indigo}`, transform: `scale(${p})`}}>
            <div style={{position: 'absolute', left: -50, top: 52, width: 145, textAlign: 'center', fontFamily: FONT_MONO, fontSize: 15, letterSpacing: 1.5, color: index === 3 ? WHITEBOARD.teal : WHITEBOARD.muted}}>{stamps[index]}</div>
          </div>
        );
      })}
      <InkPath d="M 1585 300 L 1632 330 L 1594 367" at={174} duration={25} color={WHITEBOARD.teal} width={6} />
    </SceneBoard>
  );
};

// =============================================================================
// SCENE 6 — PRACTICAL PLAN
// =============================================================================
const ACTIONS = [
  ['01', 'Choose one habit', 'Name the direction.'],
  ['02', 'Shrink the doorway', 'Make the first move under two minutes.'],
  ['03', 'Show up today', 'Continuing is optional. Starting is the win.'],
];

const ActionScene: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <SceneBoard number="06" title="Try it now" holdEnd>
      <Heading>Make starting the easiest part.</Heading>
      <DrawnUnderline x={108} y={245} width={1090} at={20} />
      <div style={{position: 'absolute', left: 130, right: 130, top: 345, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 42}}>
        {ACTIONS.map(([number, title, detail], index) => {
          const p = progress(frame, 42 + index * 38, 18);
          const check = progress(frame, 102 + index * 34, 14);
          return (
            <div key={number} style={{height: 310, padding: '34px 34px', border: `2px solid ${index === 2 ? WHITEBOARD.teal : WHITEBOARD.ink}`, borderRadius: 18, background: 'rgba(255,255,255,.62)', boxShadow: '8px 12px 0 rgba(30,41,38,.06)', opacity: p, transform: `translateY(${(1 - p) * 20}px) rotate(${index === 1 ? -0.3 : index === 2 ? 0.35 : 0}deg)`}}>
              <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
                <span style={{fontFamily: FONT_MONO, fontSize: 18, color: WHITEBOARD.muted}}>{number}</span>
                <svg width="48" height="48" viewBox="0 0 48 48">
                  <rect x="4" y="4" width="40" height="40" rx="8" fill="none" stroke={WHITEBOARD.teal} strokeWidth="3" />
                  <path d="M 13 25 L 21 33 L 36 15" fill="none" stroke={WHITEBOARD.teal} strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - check} />
                </svg>
              </div>
              <div style={{fontFamily: FONT_DISPLAY, fontSize: 38, fontWeight: 650, marginTop: 34}}>{title}</div>
              <div style={{fontFamily: FONT_BODY, fontSize: 26, lineHeight: 1.4, color: WHITEBOARD.muted, marginTop: 14}}>{detail}</div>
            </div>
          );
        })}
      </div>
      <Reveal at={180} style={{position: 'absolute', left: 250, right: 250, top: 790, textAlign: 'center', fontFamily: FONT_DISPLAY, fontSize: 43, fontWeight: 650, color: WHITEBOARD.indigo}}>
        Tiny enough to begin. Meaningful enough to repeat.
      </Reveal>
      <IdeaThread d="M 380 875 C 710 910, 1190 845, 1530 880" at={192} duration={68} />
    </SceneBoard>
  );
};

// =============================================================================
// MAIN COMPOSITION
// =============================================================================
const Video2TwoMinuteRuleSketchbook: React.FC = () => (
  <WhiteboardCanvas format="video">
    <Sequence durationInFrames={SCENE}><ProblemScene /></Sequence>
    <Sequence from={SCENE} durationInFrames={SCENE}><RuleScene /></Sequence>
    <Sequence from={SCENE * 2} durationInFrames={SCENE}><ExamplesScene /></Sequence>
    <Sequence from={SCENE * 3} durationInFrames={SCENE}><FrictionScene /></Sequence>
    <Sequence from={SCENE * 4} durationInFrames={SCENE}><MomentumScene /></Sequence>
    <Sequence from={SCENE * 5} durationInFrames={SCENE}><ActionScene /></Sequence>
  </WhiteboardCanvas>
);

export default Video2TwoMinuteRuleSketchbook;
