export function Divider({ width = 320 }) {
  const cx = width / 2;
  return (
    <svg width={width} height="30" viewBox={`0 0 ${width} 30`} style={{ display: 'block', margin: '1.5rem auto' }}>
      <defs>
        <linearGradient id="divGrad" x1="0%" y1="50%" x2="100%" y2="50%">
          <stop offset="0%" stopColor="var(--gold)" stopOpacity="0" />
          <stop offset="20%" stopColor="var(--gold)" stopOpacity="0.3" />
          <stop offset="50%" stopColor="var(--gold)" stopOpacity="0.7" />
          <stop offset="80%" stopColor="var(--gold)" stopOpacity="0.3" />
          <stop offset="100%" stopColor="var(--gold)" stopOpacity="0" />
        </linearGradient>
        <linearGradient id="divGradRose" x1="0%" y1="50%" x2="100%" y2="50%">
          <stop offset="0%" stopColor="var(--rose)" stopOpacity="0" />
          <stop offset="30%" stopColor="var(--rose)" stopOpacity="0.2" />
          <stop offset="50%" stopColor="var(--rose)" stopOpacity="0.4" />
          <stop offset="70%" stopColor="var(--rose)" stopOpacity="0.2" />
          <stop offset="100%" stopColor="var(--rose)" stopOpacity="0" />
        </linearGradient>
      </defs>
      {/* Double lines */}
      <line x1="0" y1="13" x2={width} y2="13" stroke="url(#divGrad)" strokeWidth="0.8" />
      <line x1="0" y1="17" x2={width} y2="17" stroke="url(#divGradRose)" strokeWidth="0.5" />
      {/* Center diamond */}
      <polygon
        points={`${cx},8 ${cx+5},15 ${cx},22 ${cx-5},15`}
        fill="none"
        stroke="var(--gold)"
        strokeWidth="0.8"
        opacity="0.5"
      />
      <circle cx={cx} cy="15" r="2" fill="var(--gold)" opacity="0.6" />
      {/* Side ornaments */}
      <circle cx={cx - 30} cy="15" r="1.5" fill="var(--rose)" opacity="0.4" />
      <circle cx={cx + 30} cy="15" r="1.5" fill="var(--rose)" opacity="0.4" />
      <circle cx={cx - 55} cy="15" r="1" fill="var(--gold)" opacity="0.3" />
      <circle cx={cx + 55} cy="15" r="1" fill="var(--gold)" opacity="0.3" />
      {/* Tiny leaf shapes */}
      <ellipse cx={cx - 18} cy="13" rx="4" ry="1.5" fill="var(--sage)" opacity="0.2" transform={`rotate(-20 ${cx - 18} 13)`} />
      <ellipse cx={cx + 18} cy="13" rx="4" ry="1.5" fill="var(--sage)" opacity="0.2" transform={`rotate(20 ${cx + 18} 13)`} />
    </svg>
  );
}

export function FancyDivider() {
  const w = 360;
  const cx = w / 2;
  return (
    <svg width={w} height="40" viewBox={`0 0 ${w} 40`} style={{ display: 'block', margin: '2rem auto' }}>
      <defs>
        <linearGradient id="fancyGrad" x1="0%" y1="50%" x2="100%" y2="50%">
          <stop offset="0%" stopColor="var(--gold)" stopOpacity="0" />
          <stop offset="30%" stopColor="var(--gold)" stopOpacity="0.5" />
          <stop offset="50%" stopColor="var(--gold)" stopOpacity="0.8" />
          <stop offset="70%" stopColor="var(--gold)" stopOpacity="0.5" />
          <stop offset="100%" stopColor="var(--gold)" stopOpacity="0" />
        </linearGradient>
      </defs>
      {/* Art Nouveau curved lines */}
      <path d={`M 0 20 Q ${w*0.15} 8, ${w*0.3} 20 T ${cx} 20`} fill="none" stroke="url(#fancyGrad)" strokeWidth="0.8" />
      <path d={`M ${w} 20 Q ${w*0.85} 32, ${w*0.7} 20 T ${cx} 20`} fill="none" stroke="url(#fancyGrad)" strokeWidth="0.8" />
      {/* Center flower */}
      {[0, 45, 90, 135].map(angle => (
        <ellipse
          key={angle}
          cx={cx} cy={20}
          rx="6" ry="2.5"
          fill="none"
          stroke="var(--rose)"
          strokeWidth="0.6"
          opacity="0.35"
          transform={`rotate(${angle} ${cx} 20)`}
        />
      ))}
      <circle cx={cx} cy={20} r="2.5" fill="var(--gold)" opacity="0.5" />
      <circle cx={cx} cy={20} r="1" fill="var(--rose-light)" opacity="0.8" />
      {/* Side petals */}
      {[-1, 1].map(dir => (
        <g key={dir}>
          <ellipse
            cx={cx + dir * 40} cy={20}
            rx="3" ry="1.5"
            fill="var(--rose)" opacity="0.2"
            transform={`rotate(${dir * 30} ${cx + dir * 40} 20)`}
          />
          <circle cx={cx + dir * 70} cy={20} r="1.2" fill="var(--sage)" opacity="0.25" />
        </g>
      ))}
    </svg>
  );
}

export function StepLabel({ number, text }) {
  return (
    <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
      <span style={{
        display: 'inline-block',
        padding: '4px 16px',
        border: '1px solid var(--border)',
        borderRadius: 20,
        fontSize: 11,
        letterSpacing: 4,
        textTransform: 'uppercase',
        color: 'var(--text-muted)',
        fontFamily: "'Cormorant Garamond', serif",
        marginBottom: '0.8rem',
      }}>
        Step {number}
      </span>
      <h2 style={{
        fontSize: 'clamp(22px, 5vw, 30px)',
        color: 'var(--text-primary)',
        fontWeight: 400,
      }}>
        {text}
      </h2>
    </div>
  );
}

export function Footer() {
  return (
    <footer style={{
      textAlign: 'center',
      padding: '2rem 1rem',
      borderTop: '1px solid var(--border)',
      marginTop: '2rem',
    }}>
      <Divider width={200} />
      <p style={{
        fontSize: '18px',
        color: 'var(--text-secondary)',
        letterSpacing: '3px',
        lineHeight: 1.8,
        fontWeight: 500,
        fontFamily: "'Noto Serif TC', serif",
      }}>
        台大 AI 社 · NTU AI Club
      </p>
      <p style={{
        fontSize: '14px',
        color: 'var(--text-muted)',
        letterSpacing: '2px',
        marginTop: '0.3rem',
        fontFamily: "'Noto Serif TC', serif",
      }}>
        社團聯展 2026
      </p>
      <p style={{
        fontSize: '11px',
        color: 'var(--text-muted)',
        letterSpacing: '1px',
        marginTop: '0.5rem',
        fontFamily: "'Cormorant Garamond', serif",
      }}>
        Powered by Gemini 2.5 Flash & Imagen
      </p>
    </footer>
  );
}
