import { useMemo } from 'react';

const SHAPES = ['circle', 'petal', 'star'];
const COLORS = [
  'rgba(184, 154, 62, 0.35)',
  'rgba(212, 135, 154, 0.30)',
  'rgba(240, 198, 210, 0.35)',
  'rgba(122, 171, 126, 0.25)',
  'rgba(165, 148, 196, 0.20)',
  'rgba(212, 188, 106, 0.25)',
];

function Petal({ size, color, style }) {
  return (
    <svg
      width={size * 2.5}
      height={size * 2.5}
      viewBox="0 0 20 20"
      style={{ ...style, position: 'absolute' }}
    >
      <path
        d="M10 2 C6 6, 2 10, 10 18 C18 10, 14 6, 10 2Z"
        fill={color}
      />
    </svg>
  );
}

function Star({ size, color, style }) {
  return (
    <svg
      width={size * 2}
      height={size * 2}
      viewBox="0 0 20 20"
      style={{ ...style, position: 'absolute' }}
    >
      <polygon
        points="10,2 12,8 18,8 13,12 15,18 10,14 5,18 7,12 2,8 8,8"
        fill={color}
      />
    </svg>
  );
}

export default function Particles({ count = 30 }) {
  const particles = useMemo(() =>
    Array.from({ length: count }, (_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      size: 3 + Math.random() * 6,
      duration: 8 + Math.random() * 10,
      delay: Math.random() * 12,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      shape: SHAPES[Math.floor(Math.random() * SHAPES.length)],
    })),
    [count]
  );

  return (
    <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 0, overflow: 'hidden' }}>
      {particles.map(p => {
        const baseStyle = {
          left: p.left,
          bottom: '-10px',
          animation: `floatParticle ${p.duration}s ease-in-out ${p.delay}s infinite`,
        };

        if (p.shape === 'petal') {
          return <Petal key={p.id} size={p.size} color={p.color} style={baseStyle} />;
        }
        if (p.shape === 'star') {
          return <Star key={p.id} size={p.size} color={p.color} style={baseStyle} />;
        }
        return (
          <div
            key={p.id}
            style={{
              ...baseStyle,
              position: 'absolute',
              width: p.size,
              height: p.size,
              borderRadius: '50%',
              background: p.color,
            }}
          />
        );
      })}
    </div>
  );
}
