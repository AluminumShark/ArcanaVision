import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Divider } from './Ornaments';

export default function QuestionInput({ spread, onSubmit }) {
  const [question, setQuestion] = useState('');
  const inputRef = useRef(null);

  useEffect(() => {
    const t = setTimeout(() => inputRef.current?.focus(), 400);
    return () => clearTimeout(t);
  }, []);

  const handleSubmit = () => {
    const q = question.trim() || '請為我指引方向';
    onSubmit(q);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '1.5rem',
        padding: '0 1.5rem',
        maxWidth: 480,
        width: '100%',
      }}
    >
      {/* Spread info card */}
      <div style={{
        background: 'var(--card-bg)',
        border: '1px solid var(--border)',
        borderRadius: 14,
        padding: '1.2rem 1.5rem',
        textAlign: 'center',
        width: '100%',
      }}>
        <p style={{
          fontSize: '16px',
          color: 'var(--text-primary)',
          fontWeight: 500,
          fontFamily: "'Noto Serif TC', serif",
        }}>
          {spread.name_zh}
        </p>
        <p style={{
          fontSize: '13px',
          color: 'var(--text-muted)',
          lineHeight: 1.8,
          marginTop: '0.3rem',
        }}>
          {spread.description}
        </p>
      </div>

      <Divider width={200} />

      <p style={{
        fontSize: '15px',
        color: 'var(--text-primary)',
        textAlign: 'center',
        fontFamily: "'Noto Serif TC', serif",
        letterSpacing: '2px',
      }}>
        請在心中默念你的問題
      </p>

      <input
        ref={inputRef}
        type="text"
        value={question}
        onChange={e => setQuestion(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSubmit()}
        placeholder="例如：我的未來會怎樣？"
        style={{
          width: '100%',
          padding: '16px 24px',
          fontSize: '16px',
          fontFamily: "'Noto Serif TC', serif",
          background: 'var(--card-bg)',
          border: '1px solid var(--border)',
          borderRadius: 12,
          color: 'var(--text-primary)',
          outline: 'none',
          transition: 'all 0.4s ease',
          textAlign: 'center',
          boxShadow: '0 2px 15px rgba(184, 154, 62, 0.04)',
        }}
        onFocus={e => {
          e.target.style.borderColor = 'var(--border-active)';
          e.target.style.boxShadow = '0 4px 25px rgba(184, 154, 62, 0.08)';
        }}
        onBlur={e => {
          e.target.style.borderColor = 'var(--border)';
          e.target.style.boxShadow = '0 2px 15px rgba(184, 154, 62, 0.04)';
        }}
      />

      <motion.button
        onClick={handleSubmit}
        whileHover={{
          scale: 1.02,
          boxShadow: '0 8px 35px rgba(184, 154, 62, 0.18)',
        }}
        whileTap={{ scale: 0.97 }}
        style={{
          padding: '16px 48px',
          fontSize: '16px',
          fontFamily: "'Noto Serif TC', serif",
          color: 'var(--card-bg)',
          background: 'linear-gradient(135deg, var(--gold), var(--gold-dark))',
          border: 'none',
          borderRadius: 12,
          letterSpacing: '4px',
          transition: 'all 0.3s',
          minHeight: 52,
          boxShadow: '0 4px 20px rgba(184, 154, 62, 0.15)',
        }}
      >
        開始洗牌
      </motion.button>
    </motion.div>
  );
}
