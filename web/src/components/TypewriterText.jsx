import { useState, useEffect } from 'react';

export default function TypewriterText({ text, speed = 30, onDone }) {
  const [displayed, setDisplayed] = useState('');
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!text) return;
    setDisplayed('');
    setDone(false);
    let i = 0;
    const id = setInterval(() => {
      i += 2; // 每次顯示 2 字
      if (i >= text.length) {
        setDisplayed(text);
        setDone(true);
        clearInterval(id);
        onDone?.();
      } else {
        setDisplayed(text.slice(0, i));
      }
    }, speed);
    return () => clearInterval(id);
  }, [text, speed]);

  return (
    <div style={{
      fontFamily: "'Noto Serif TC', serif",
      fontSize: 'clamp(17px, 4.5vw, 20px)',
      color: 'var(--text-primary)',
      lineHeight: 2.2,
      textAlign: 'justify',
      padding: '0 0.5rem',
    }}>
      {displayed}
      {!done && (
        <span style={{
          display: 'inline-block',
          width: 2,
          height: '1em',
          background: 'var(--gold)',
          marginLeft: 2,
          verticalAlign: 'text-bottom',
          animation: 'cursorBlink 0.8s step-end infinite',
        }} />
      )}
    </div>
  );
}
