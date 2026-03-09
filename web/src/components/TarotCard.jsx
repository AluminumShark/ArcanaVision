import { useState } from 'react';
import { motion } from 'framer-motion';

const CARD_W_SM = 100;
const CARD_H_SM = 173;
const CARD_W = 140;
const CARD_H = 242;

function CardBack({ width, height }) {
  return (
    <div style={{
      width, height,
      background: 'var(--card-bg)',
      border: '2px solid var(--border-active)',
      borderRadius: 10,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative',
      overflow: 'hidden',
      boxShadow: '0 4px 20px rgba(184, 154, 62, 0.08)',
    }}>
      {/* Inner border */}
      <div style={{
        position: 'absolute',
        inset: 4,
        border: '1px solid var(--border)',
        borderRadius: 6,
        pointerEvents: 'none',
      }} />
      {/* Inner ornamental circles */}
      <div style={{
        width: '60%',
        height: '45%',
        borderRadius: '50%',
        border: '1px solid var(--gold)',
        opacity: 0.25,
        position: 'absolute',
      }} />
      <div style={{
        width: '40%',
        height: '30%',
        borderRadius: '50%',
        border: '1px solid var(--rose)',
        opacity: 0.2,
        position: 'absolute',
      }} />
      <div style={{
        width: '20%',
        height: '15%',
        borderRadius: '50%',
        border: '1px solid var(--sage)',
        opacity: 0.15,
        position: 'absolute',
      }} />
      {/* Corner flowers */}
      {[{ top: 8, left: 8 }, { top: 8, right: 8 }, { bottom: 8, left: 8 }, { bottom: 8, right: 8 }].map((pos, i) => (
        <div key={i} style={{
          position: 'absolute',
          ...pos,
          width: 7,
          height: 7,
          borderRadius: '50%',
          background: i % 2 === 0 ? 'var(--rose-light)' : 'var(--gold-light)',
          opacity: 0.45,
        }} />
      ))}
    </div>
  );
}

export default function TarotCard({ card, revealed = false, delay = 0 }) {
  const [flipped, setFlipped] = useState(revealed);
  const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
  const w = isMobile ? CARD_W_SM : CARD_W;
  const h = isMobile ? CARD_H_SM : CARD_H;

  if (revealed && !flipped) setFlipped(true);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
      <motion.div
        initial={revealed ? { rotateY: 180, scale: 0.8, opacity: 0 } : {}}
        animate={revealed ? { rotateY: 0, scale: 1, opacity: 1 } : {}}
        transition={{ delay, duration: 0.8, ease: 'easeOut' }}
        style={{
          width: w, height: h,
          perspective: 800,
          transformStyle: 'preserve-3d',
          transform: card?.is_reversed ? 'rotate(180deg)' : 'none',
        }}
      >
        {flipped && card ? (
          <div style={{
            width: w, height: h,
            background: 'var(--card-bg)',
            border: '2px solid var(--gold)',
            borderRadius: 10,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 3,
            boxShadow: '0 6px 25px rgba(184, 154, 62, 0.12), 0 0 0 1px rgba(212, 135, 154, 0.08)',
            overflow: 'hidden',
            position: 'relative',
          }}>
            {/* Card image */}
            <img
              src={card.asset_url}
              alt={card.name_zh}
              style={{
                position: 'absolute',
                inset: 3,
                width: 'calc(100% - 6px)',
                height: 'calc(100% - 6px)',
                objectFit: 'cover',
                borderRadius: 7,
              }}
              onError={e => { e.target.style.display = 'none'; }}
            />
            {/* Fallback text overlay */}
            <div style={{
              position: 'relative',
              zIndex: 1,
              textAlign: 'center',
              padding: '4px 6px',
              background: 'rgba(255,252,248,0.88)',
              borderRadius: 6,
              border: '1px solid rgba(184, 154, 62, 0.15)',
              transform: card.is_reversed ? 'rotate(180deg)' : 'none',
            }}>
              <div style={{
                fontSize: isMobile ? 9 : 11,
                color: 'var(--gold)',
                fontFamily: "'Cormorant Garamond', serif",
                fontWeight: 500,
              }}>
                {card.number !== undefined ? toRoman(card.number) : ''}
              </div>
              <div style={{
                fontSize: isMobile ? 12 : 15,
                fontWeight: 500,
                color: 'var(--text-primary)',
                fontFamily: "'Noto Serif TC', serif",
              }}>
                {card.name_zh}
              </div>
              <div style={{
                fontSize: isMobile ? 7 : 9,
                color: 'var(--text-muted)',
                fontFamily: "'Cormorant Garamond', serif",
                letterSpacing: '1px',
                textTransform: 'uppercase',
              }}>
                {card.name_en}
              </div>
            </div>
          </div>
        ) : (
          <CardBack width={w} height={h} />
        )}
      </motion.div>

      {/* Position label + reversed badge */}
      {card && (
        <div style={{
          textAlign: 'center',
          transform: card.is_reversed ? 'rotate(0deg)' : 'none',
        }}>
          <span style={{
            fontSize: 12,
            color: 'var(--text-muted)',
            letterSpacing: '1px',
            fontFamily: "'Noto Serif TC', serif",
          }}>
            {card.position_name}
          </span>
          {card.is_reversed && (
            <span style={{
              display: 'inline-block',
              fontSize: 9,
              color: 'var(--rose)',
              marginLeft: 4,
              border: '1px solid var(--border-rose)',
              borderRadius: 4,
              padding: '1px 4px',
              fontFamily: "'Noto Serif TC', serif",
            }}>
              逆位
            </span>
          )}
        </div>
      )}
    </div>
  );
}

function toRoman(num) {
  if (num === 0) return '0';
  const vals = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1];
  const syms = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I'];
  let result = '';
  for (let i = 0; i < vals.length; i++) {
    while (num >= vals[i]) {
      result += syms[i];
      num -= vals[i];
    }
  }
  return result;
}
