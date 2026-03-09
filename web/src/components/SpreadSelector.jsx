import { motion } from 'framer-motion';

const CARD_COUNTS = {
  daily_draw: '1 牌',
  three_card: '3 牌',
  four_elements: '4 牌',
  timeline: '5 牌',
  relationship: '5 牌',
  celtic_cross: '10 牌',
};

const ICONS = {
  daily_draw: '\u2729',
  three_card: '\u2727',
  four_elements: '\u2726',
  timeline: '\u2728',
  relationship: '\u2661',
  celtic_cross: '\u2748',
};

export default function SpreadSelector({ spreads, onSelect }) {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(2, 1fr)',
      gap: '16px',
      padding: '0 1rem',
      maxWidth: 520,
      width: '100%',
    }}>
      {spreads.map((s, i) => (
        <motion.button
          key={s.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1, duration: 0.6, ease: 'easeOut' }}
          onClick={() => onSelect(s)}
          style={{
            background: 'var(--card-bg)',
            border: '1px solid var(--border)',
            borderRadius: 14,
            padding: '1.4rem 0.8rem',
            textAlign: 'center',
            transition: 'all 0.4s ease',
            cursor: 'pointer',
            position: 'relative',
            overflow: 'hidden',
          }}
          whileHover={{
            y: -3,
            borderColor: 'rgba(184, 154, 62, 0.6)',
            boxShadow: '0 8px 35px rgba(184, 154, 62, 0.12), 0 0 0 1px rgba(212, 135, 154, 0.1)',
          }}
          whileTap={{ scale: 0.97 }}
        >
          {/* Subtle inner glow */}
          <div style={{
            position: 'absolute',
            inset: 0,
            background: 'radial-gradient(ellipse at center, rgba(184,154,62,0.03) 0%, transparent 70%)',
            pointerEvents: 'none',
          }} />

          {/* Icon */}
          <div style={{
            fontSize: '22px',
            marginBottom: '0.3rem',
            opacity: 0.5,
            animation: 'gentleFloat 3s ease-in-out infinite',
            animationDelay: `${i * 0.3}s`,
          }}>
            {ICONS[s.id] || '\u2726'}
          </div>

          <div style={{
            fontFamily: "'Noto Serif TC', serif",
            fontSize: '17px',
            color: 'var(--text-primary)',
            fontWeight: 500,
            marginBottom: '0.3rem',
            position: 'relative',
          }}>
            {s.name_zh}
          </div>
          <div style={{
            fontSize: '10px',
            color: 'var(--gold)',
            letterSpacing: '2px',
            fontFamily: "'Cormorant Garamond', serif",
            textTransform: 'uppercase',
            marginBottom: '0.5rem',
          }}>
            {CARD_COUNTS[s.id] || `${s.card_count} cards`}
          </div>
          <div style={{
            fontSize: '12px',
            color: 'var(--text-muted)',
            lineHeight: 1.7,
            position: 'relative',
          }}>
            {s.description}
          </div>
        </motion.button>
      ))}
    </div>
  );
}
