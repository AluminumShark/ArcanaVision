import { motion } from 'framer-motion';

export default function ShuffleAnimation() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '2.5rem',
      padding: '3rem 0',
    }}>
      {/* Decorative arc above cards */}
      <svg width="200" height="30" viewBox="0 0 200 30" style={{ opacity: 0.3 }}>
        <path d="M 10 28 Q 100 0, 190 28" fill="none" stroke="var(--gold)" strokeWidth="0.8" />
        <circle cx="100" cy="8" r="2" fill="var(--gold)" opacity="0.5" />
      </svg>

      <div style={{ display: 'flex', gap: 16, perspective: 600 }}>
        {[0, 1, 2].map(i => (
          <motion.div
            key={i}
            animate={{
              rotate: [-3, 3, -2, 4, -3],
              y: [0, -12, 4, -6, 0],
              rotateY: [0, 5, -5, 3, 0],
            }}
            transition={{
              duration: 0.7,
              repeat: Infinity,
              delay: i * 0.15,
              ease: 'easeInOut',
            }}
            style={{
              width: 70,
              height: 121,
              background: 'var(--card-bg)',
              border: '2px solid var(--border-active)',
              borderRadius: 10,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 6px 25px rgba(184, 154, 62, 0.12)',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            {/* Card back design */}
            <div style={{
              width: '70%',
              height: '50%',
              borderRadius: '50%',
              border: '1px solid var(--gold)',
              opacity: 0.2,
              position: 'absolute',
            }} />
            <div style={{
              width: '45%',
              height: '33%',
              borderRadius: '50%',
              border: '1px solid var(--rose)',
              opacity: 0.15,
              position: 'absolute',
            }} />
            {/* Corner dots */}
            {[
              { top: 6, left: 6 },
              { top: 6, right: 6 },
              { bottom: 6, left: 6 },
              { bottom: 6, right: 6 },
            ].map((pos, j) => (
              <div key={j} style={{
                position: 'absolute',
                ...pos,
                width: 5,
                height: 5,
                borderRadius: '50%',
                background: 'var(--rose-light)',
                opacity: 0.4,
              }} />
            ))}
          </motion.div>
        ))}
      </div>

      <p style={{
        fontFamily: "'Noto Serif TC', serif",
        fontSize: '16px',
        color: 'var(--text-secondary)',
        letterSpacing: '5px',
        animation: 'pulseText 2s ease-in-out infinite',
      }}>
        洗牌中⋯
      </p>
    </div>
  );
}
