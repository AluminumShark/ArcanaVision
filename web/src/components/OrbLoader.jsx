import { motion } from 'framer-motion';

export default function OrbLoader({ text = '載入中⋯' }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: '2rem',
      padding: '3rem',
    }}>
      {/* Outer ring pulses */}
      <div style={{ position: 'relative', width: 100, height: 100 }}>
        {/* Expanding rings */}
        {[0, 1, 2].map(i => (
          <div
            key={i}
            style={{
              position: 'absolute',
              inset: 0,
              borderRadius: '50%',
              border: '1px solid var(--gold)',
              opacity: 0.15,
              animation: `ringExpand 3s ease-out ${i * 1}s infinite`,
            }}
          />
        ))}
        {/* Main orb */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
          style={{
            position: 'absolute',
            inset: 10,
            borderRadius: '50%',
            background: `conic-gradient(
              from 0deg,
              var(--rose-light),
              var(--gold-light),
              var(--sage-light),
              var(--lavender-light),
              var(--rose-light)
            )`,
            animation: 'breathe 2.5s ease-in-out infinite',
          }}
        />
        {/* Inner bright core */}
        <div
          style={{
            position: 'absolute',
            inset: 25,
            borderRadius: '50%',
            background: 'radial-gradient(circle at 40% 35%, rgba(255,252,248,0.9), var(--gold-light) 70%)',
            animation: 'orbGlow 2.5s ease-in-out infinite',
          }}
        />
      </div>

      <p style={{
        fontFamily: "'Noto Serif TC', serif",
        fontSize: '16px',
        color: 'var(--text-secondary)',
        letterSpacing: '4px',
        animation: 'pulseText 2s ease-in-out infinite',
      }}>
        {text}
      </p>
    </div>
  );
}
