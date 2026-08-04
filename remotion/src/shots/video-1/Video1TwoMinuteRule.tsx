import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  Sequence,
  useCurrentFrame,
} from 'remotion';
import {COLORS, EASINGS, GRADIENT, SHADOW} from '../../brand';
import {FONT_BODY, FONT_DISPLAY, FONT_MONO} from '../../fonts';
import {MotionCanvas} from '../../lib/video';

// =============================================================================
// COMPOSITION CONFIG
// =============================================================================
export const compositionConfig = {
  id: 'Video1TwoMinuteRule',
  durationInSeconds: 60,
  fps: 30,
  width: 1920,
  height: 1080,
};

// =============================================================================
// TIMELINE + STYLE
// =============================================================================
const SCENE_FRAMES = 300;

const enter = (frame: number, at = 0, duration = 18) =>
  interpolate(frame, [at, at + duration], [0, 1], {
    easing: EASINGS.easeOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

const exit = (frame: number, at = 270, duration = 20) =>
  interpolate(frame, [at, at + duration], [1, 0], {
    easing: EASINGS.easeIn,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

const SceneShell: React.FC<{
  children: React.ReactNode;
  chapter: string;
  number: string;
  light?: boolean;
  holdEnd?: boolean;
}> = ({children, chapter, number, light = false, holdEnd = false}) => {
  const frame = useCurrentFrame();
  const out = holdEnd ? 1 : exit(frame);
  return (
    <AbsoluteFill
      style={{
        color: light ? COLORS.ink : '#fff',
        background: light ? COLORS.paper : 'transparent',
        opacity: out,
        overflow: 'hidden',
      }}
    >
      {light ? (
        <AbsoluteFill
          style={{
            opacity: 0.6,
            backgroundImage: `radial-gradient(${COLORS.line} 1.2px, transparent 1.2px)`,
            backgroundSize: '40px 40px',
          }}
        />
      ) : null}
      <div
        style={{
          position: 'absolute',
          left: 80,
          top: 50,
          fontFamily: FONT_MONO,
          fontSize: 18,
          letterSpacing: 3,
          color: light ? COLORS.muted : COLORS.d400,
        }}
      >
        {number} / {chapter.toUpperCase()}
      </div>
      <div
        style={{
          position: 'absolute',
          left: 80,
          right: 80,
          bottom: 42,
          height: 4,
          borderRadius: 999,
          background: light ? COLORS.line : 'rgba(255,255,255,.12)',
        }}
      >
        <div
          style={{
            width: `${Math.min(100, (frame / (SCENE_FRAMES - 1)) * 100)}%`,
            height: '100%',
            borderRadius: 999,
            background: GRADIENT,
          }}
        />
      </div>
      {children}
    </AbsoluteFill>
  );
};

const Rise: React.FC<{
  children: React.ReactNode;
  at?: number;
  style?: React.CSSProperties;
}> = ({children, at = 0, style}) => {
  const frame = useCurrentFrame();
  const p = enter(frame, at);
  return (
    <div style={{...style, opacity: p, transform: `translateY(${(1 - p) * 28}px)`}}>
      {children}
    </div>
  );
};

// =============================================================================
// SCENE 1 — HOOK
// =============================================================================
const HookScene: React.FC = () => {
  const frame = useCurrentFrame();
  const line = interpolate(frame, [28, 64], [0, 100], {
    easing: EASINGS.easeOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const blockScale = interpolate(frame, [76, 140], [1, 0.42], {
    easing: EASINGS.easeInOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const blockX = interpolate(frame, [76, 140], [0, 390], {
    easing: EASINGS.easeInOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <SceneShell number="01" chapter="The problem">
      <div style={{position: 'absolute', left: 130, top: 205, width: 1080}}>
        <div style={{fontFamily: FONT_DISPLAY, fontSize: 102, lineHeight: 1.03, fontWeight: 700, letterSpacing: -4}}>
          Starting feels
          <br />
          <span style={{color: COLORS.warn}}>too big.</span>
        </div>
        <div style={{width: `${line}%`, maxWidth: 620, height: 9, borderRadius: 99, background: COLORS.warn, marginTop: 25}} />
        <Rise at={88} style={{marginTop: 50, fontFamily: FONT_BODY, fontSize: 34, lineHeight: 1.45, color: COLORS.d300, maxWidth: 820}}>
          The goal is not to make the whole habit easy.
          <br />It is to make the first move obvious.
        </Rise>
      </div>

      <div
        style={{
          position: 'absolute',
          right: 145,
          top: 230,
          width: 430,
          height: 430,
          borderRadius: 34,
          background: `linear-gradient(145deg, ${COLORS.accent}, ${COLORS.accent2})`,
          boxShadow: '0 30px 100px rgba(99,102,241,.38)',
          transform: `translateX(${blockX}px) scale(${blockScale})`,
          transformOrigin: 'center',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: FONT_DISPLAY,
          fontSize: 70,
          fontWeight: 700,
          textAlign: 'center',
          lineHeight: 1.05,
        }}
      >
        THE
        <br />
        WHOLE
        <br />
        HABIT
      </div>
      <Rise at={146} style={{position: 'absolute', right: 155, top: 690, width: 410, textAlign: 'center'}}>
        <div style={{fontFamily: FONT_MONO, fontSize: 20, color: COLORS.signal, letterSpacing: 2}}>SHRINK THE ENTRY</div>
      </Rise>
    </SceneShell>
  );
};

// =============================================================================
// SCENE 2 — RULE
// =============================================================================
const RuleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const ring = interpolate(frame, [48, 100], [0, 360], {
    easing: EASINGS.easeOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const pulse = interpolate(frame, [126, 154, 182], [1, 1.045, 1], {
    easing: EASINGS.easeInOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <SceneShell number="02" chapter="The rule" light>
      <div style={{position: 'absolute', left: 120, top: 205, width: 850}}>
        <Rise at={0}>
          <div style={{fontFamily: FONT_MONO, fontSize: 22, color: COLORS.accent, letterSpacing: 3, marginBottom: 20}}>ATOMIC HABITS · JAMES CLEAR</div>
          <div style={{fontFamily: FONT_DISPLAY, fontSize: 92, lineHeight: 1.04, fontWeight: 700, letterSpacing: -4}}>
            The Two-Minute
            <br />Rule
          </div>
        </Rise>
        <Rise at={44} style={{fontFamily: FONT_BODY, fontSize: 36, lineHeight: 1.5, color: COLORS.muted, marginTop: 42, maxWidth: 790}}>
          Scale a new habit down to a starter version that takes under two minutes.
        </Rise>
        <Rise at={112} style={{fontFamily: FONT_BODY, fontSize: 22, color: COLORS.muted, marginTop: 28}}>
          Concept paraphrased from <i>Atomic Habits</i>.
        </Rise>
      </div>

      <div
        style={{
          position: 'absolute',
          right: 210,
          top: 230,
          width: 500,
          height: 500,
          borderRadius: '50%',
          background: `conic-gradient(${COLORS.accent} ${ring}deg, ${COLORS.line} ${ring}deg)`,
          transform: `scale(${pulse})`,
          boxShadow: SHADOW.card,
          display: 'grid',
          placeItems: 'center',
        }}
      >
        <div style={{width: 420, height: 420, borderRadius: '50%', background: COLORS.paper, display: 'grid', placeItems: 'center', textAlign: 'center'}}>
          <div>
            <div style={{fontFamily: FONT_DISPLAY, fontSize: 170, fontWeight: 700, lineHeight: 0.8, letterSpacing: -10, color: COLORS.accent}}>2</div>
            <div style={{fontFamily: FONT_MONO, fontSize: 26, fontWeight: 700, letterSpacing: 5, color: COLORS.muted, marginTop: 25}}>MINUTES</div>
          </div>
        </div>
      </div>
    </SceneShell>
  );
};

// =============================================================================
// SCENE 3 — EXAMPLES
// =============================================================================
const EXAMPLES = [
  {big: 'Read every night', tiny: 'Read one page', icon: '01'},
  {big: 'Work out', tiny: 'Put on your shoes', icon: '02'},
  {big: 'Meditate daily', tiny: 'Take one slow breath', icon: '03'},
];

const ExamplesScene: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <SceneShell number="03" chapter="Make it tiny">
      <div style={{position: 'absolute', left: 120, right: 120, top: 145}}>
        <Rise>
          <div style={{fontFamily: FONT_DISPLAY, fontWeight: 700, fontSize: 74, letterSpacing: -3}}>Translate ambition into an entrance.</div>
        </Rise>
        <div style={{display: 'flex', flexDirection: 'column', gap: 20, marginTop: 55}}>
          {EXAMPLES.map((item, index) => {
            const p = enter(frame, 38 + index * 36, 18);
            const swap = enter(frame, 112 + index * 28, 20);
            return (
              <div
                key={item.icon}
                style={{
                  height: 164,
                  borderRadius: 18,
                  background: 'rgba(22,27,34,.92)',
                  border: `1px solid ${COLORS.d600}`,
                  boxShadow: '0 18px 55px rgba(0,0,0,.18)',
                  display: 'grid',
                  gridTemplateColumns: '110px 1fr 130px 1fr',
                  alignItems: 'center',
                  padding: '0 42px',
                  opacity: p,
                  transform: `translateY(${(1 - p) * 22}px)`,
                }}
              >
                <div style={{fontFamily: FONT_MONO, color: COLORS.d400, fontSize: 24}}>{item.icon}</div>
                <div style={{fontFamily: FONT_BODY, fontSize: 34, color: COLORS.d400, textDecoration: swap > 0.6 ? 'line-through' : 'none', textDecorationColor: COLORS.d600}}>{item.big}</div>
                <div style={{textAlign: 'center', fontFamily: FONT_DISPLAY, fontSize: 45, color: COLORS.accent, opacity: swap}}>→</div>
                <div style={{fontFamily: FONT_DISPLAY, fontWeight: 600, fontSize: 39, color: COLORS.paper, opacity: swap, transform: `translateX(${(1 - swap) * 24}px)`}}>{item.tiny}</div>
              </div>
            );
          })}
        </div>
      </div>
    </SceneShell>
  );
};

// =============================================================================
// SCENE 4 — FRICTION
// =============================================================================
const FrictionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const gate = interpolate(frame, [60, 136], [0, 230], {
    easing: EASINGS.easeInOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const dot = interpolate(frame, [118, 214], [0, 980], {
    easing: EASINGS.easeInOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const dotScale = interpolate(frame, [114, 136, 214, 236], [0.7, 1, 1, 1.25], {
    easing: EASINGS.easeOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <SceneShell number="04" chapter="Lower the threshold" light>
      <div style={{position: 'absolute', left: 120, top: 160}}>
        <Rise>
          <div style={{fontFamily: FONT_DISPLAY, fontSize: 80, fontWeight: 700, letterSpacing: -3}}>Reduce the energy required to begin.</div>
          <div style={{fontFamily: FONT_BODY, fontSize: 34, color: COLORS.muted, marginTop: 18}}>Once motion starts, continuing becomes a separate choice.</div>
        </Rise>
      </div>
      <div style={{position: 'absolute', left: 230, right: 230, top: 650, height: 12, borderRadius: 99, background: COLORS.line}}>
        <div style={{position: 'absolute', left: 0, top: -18, width: 48, height: 48, borderRadius: '50%', background: COLORS.accent, transform: `translateX(${dot}px) scale(${dotScale})`, boxShadow: '0 12px 35px rgba(99,102,241,.35)'}} />
        <div style={{position: 'absolute', left: 980, top: -40, width: 92, height: 92, borderRadius: '50%', background: COLORS.signal, display: 'grid', placeItems: 'center', color: '#fff', fontFamily: FONT_DISPLAY, fontWeight: 700, fontSize: 35}}>GO</div>
      </div>
      <div style={{position: 'absolute', left: 760, top: 610, width: 110, height: 245, borderRadius: 16, background: COLORS.d800, transform: `translateY(-${gate}px)`, boxShadow: SHADOW.soft}}>
        <div style={{fontFamily: FONT_MONO, fontSize: 17, color: COLORS.d400, writingMode: 'vertical-rl', margin: '42px auto 0', letterSpacing: 3}}>STARTING FRICTION</div>
      </div>
      <Rise at={160} style={{position: 'absolute', left: 640, top: 785, width: 640, textAlign: 'center'}}>
        <span style={{fontFamily: FONT_MONO, fontSize: 22, color: COLORS.signal, letterSpacing: 3}}>THE DOORWAY IS THE HABIT</span>
      </Rise>
    </SceneShell>
  );
};

// =============================================================================
// SCENE 5 — MOMENTUM
// =============================================================================
const MomentumScene: React.FC = () => {
  const frame = useCurrentFrame();
  const path = interpolate(frame, [56, 235], [0, 100], {
    easing: EASINGS.easeInOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <SceneShell number="05" chapter="Momentum">
      <div style={{position: 'absolute', left: 120, top: 160, width: 760}}>
        <Rise>
          <div style={{fontFamily: FONT_DISPLAY, fontSize: 82, fontWeight: 700, letterSpacing: -3}}>Small starts create evidence.</div>
        </Rise>
        <Rise at={40} style={{fontFamily: FONT_BODY, fontSize: 36, lineHeight: 1.45, color: COLORS.d300, marginTop: 36}}>
          Each repetition is a vote for the person you want to become.
        </Rise>
        <Rise at={146} style={{marginTop: 50, padding: '26px 30px', width: 520, borderLeft: `5px solid ${COLORS.signal}`, background: 'rgba(22,27,34,.75)', borderRadius: 12, fontFamily: FONT_MONO, fontSize: 23, color: COLORS.signal}}>
          START → REPEAT → IDENTITY
        </Rise>
      </div>
      <div style={{position: 'absolute', right: 160, top: 190, width: 720, height: 630}}>
        <svg width="720" height="630" viewBox="0 0 720 630">
          <defs>
            <linearGradient id="momentumGradient" x1="0" y1="1" x2="1" y2="0">
              <stop offset="0" stopColor={COLORS.accent} />
              <stop offset="0.55" stopColor={COLORS.accent2} />
              <stop offset="1" stopColor={COLORS.signal} />
            </linearGradient>
          </defs>
          <path d="M 60 540 C 190 520, 220 445, 305 420 C 390 395, 390 300, 470 275 C 560 245, 590 150, 660 70" fill="none" stroke={COLORS.d600} strokeWidth="18" strokeLinecap="round" />
          <path d="M 60 540 C 190 520, 220 445, 305 420 C 390 395, 390 300, 470 275 C 560 245, 590 150, 660 70" fill="none" stroke="url(#momentumGradient)" strokeWidth="18" strokeLinecap="round" pathLength="100" strokeDasharray="100" strokeDashoffset={100 - path} />
        </svg>
        {[{x: 42, y: 522, at: 56}, {x: 287, y: 402, at: 112}, {x: 452, y: 257, at: 168}, {x: 642, y: 52, at: 220}].map((point, index) => {
          const p = enter(frame, point.at, 14);
          return <div key={point.x} style={{position: 'absolute', left: point.x, top: point.y, width: 48, height: 48, borderRadius: '50%', background: index === 3 ? COLORS.signal : COLORS.accent, border: '8px solid #0d1117', transform: `scale(${p})`, boxShadow: `0 0 0 2px ${index === 3 ? COLORS.signal : COLORS.accent}`}} />;
        })}
      </div>
    </SceneShell>
  );
};

// =============================================================================
// SCENE 6 — ACTION
// =============================================================================
const ACTIONS = [
  ['1', 'Choose one habit', 'Name the direction.'],
  ['2', 'Shrink the doorway', 'Make the first move under two minutes.'],
  ['3', 'Show up today', 'Continuing is optional. Starting is the win.'],
];

const ActionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const glow = interpolate(frame, [170, 220, 270], [0.18, 0.34, 0.18], {
    easing: EASINGS.easeInOut,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <SceneShell number="06" chapter="Try it now" light holdEnd>
      <AbsoluteFill style={{background: `radial-gradient(circle at 78% 24%, rgba(99,102,241,${glow}), transparent 34%)`}} />
      <div style={{position: 'absolute', left: 120, right: 120, top: 135}}>
        <Rise>
          <div style={{fontFamily: FONT_MONO, fontSize: 22, color: COLORS.accent, letterSpacing: 4}}>YOUR TWO-MINUTE PLAN</div>
          <div style={{fontFamily: FONT_DISPLAY, fontSize: 82, fontWeight: 700, letterSpacing: -3, marginTop: 20}}>Make starting the easiest part.</div>
        </Rise>
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 22, marginTop: 62}}>
          {ACTIONS.map(([number, title, detail], index) => {
            const p = enter(frame, 46 + index * 36, 20);
            return (
              <div key={number} style={{height: 310, padding: '34px 34px', borderRadius: 18, background: 'rgba(255,254,247,.94)', border: `1px solid ${COLORS.line}`, boxShadow: SHADOW.card, opacity: p, transform: `translateY(${(1 - p) * 26}px)`}}>
                <div style={{width: 50, height: 50, borderRadius: '50%', background: index === 2 ? COLORS.signal : COLORS.accent, color: '#fff', display: 'grid', placeItems: 'center', fontFamily: FONT_MONO, fontWeight: 700, fontSize: 22}}>{number}</div>
                <div style={{fontFamily: FONT_DISPLAY, fontSize: 38, fontWeight: 600, marginTop: 28}}>{title}</div>
                <div style={{fontFamily: FONT_BODY, fontSize: 27, lineHeight: 1.4, color: COLORS.muted, marginTop: 14}}>{detail}</div>
              </div>
            );
          })}
        </div>
        <Rise at={178} style={{textAlign: 'center', marginTop: 48}}>
          <div style={{fontFamily: FONT_DISPLAY, fontWeight: 700, fontSize: 44, color: COLORS.accent}}>Tiny enough to begin. Meaningful enough to repeat.</div>
        </Rise>
      </div>
    </SceneShell>
  );
};

// =============================================================================
// MAIN COMPOSITION
// =============================================================================
const Video1TwoMinuteRule: React.FC = () => (
  <MotionCanvas format="video">
    <Sequence durationInFrames={SCENE_FRAMES}><HookScene /></Sequence>
    <Sequence from={SCENE_FRAMES} durationInFrames={SCENE_FRAMES}><RuleScene /></Sequence>
    <Sequence from={SCENE_FRAMES * 2} durationInFrames={SCENE_FRAMES}><ExamplesScene /></Sequence>
    <Sequence from={SCENE_FRAMES * 3} durationInFrames={SCENE_FRAMES}><FrictionScene /></Sequence>
    <Sequence from={SCENE_FRAMES * 4} durationInFrames={SCENE_FRAMES}><MomentumScene /></Sequence>
    <Sequence from={SCENE_FRAMES * 5} durationInFrames={SCENE_FRAMES}><ActionScene /></Sequence>
  </MotionCanvas>
);

export default Video1TwoMinuteRule;
