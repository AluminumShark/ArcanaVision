import { useState } from 'react';
import { motion } from 'framer-motion';
import TarotCard from './TarotCard';
import TypewriterText from './TypewriterText';
import OrbLoader from './OrbLoader';
import { Divider, FancyDivider } from './Ornaments';
import { fetchStoryImage } from '../utils/api';

export default function ReadingResult({ result, onRestart }) {
  const [storyDone, setStoryDone] = useState(false);
  const [imageState, setImageState] = useState('idle'); // idle | loading | done | error
  const [storyImageB64, setStoryImageB64] = useState(null);

  const handleGenerateImage = async () => {
    setImageState('loading');
    try {
      const data = await fetchStoryImage(result.scene_prompt, result.mood);
      if (data.image_base64) {
        setStoryImageB64(data.image_base64);
        setImageState('done');
      } else {
        setImageState('error');
      }
    } catch {
      setImageState('error');
    }
  };

  const handleDownload = () => {
    if (!storyImageB64) return;
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${storyImageB64}`;
    link.download = `arcana_vision_${Date.now()}.png`;
    link.click();
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.8 }}
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '1.5rem',
        padding: '0 1rem',
        maxWidth: 700,
        width: '100%',
      }}
    >
      {/* Section header */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        style={{ textAlign: 'center' }}
      >
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
          marginBottom: '0.5rem',
        }}>
          Your Reading
        </span>
      </motion.div>

      {/* Cards */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '16px',
        }}
      >
        {result.cards.map((card, i) => (
          <TarotCard key={card.id} card={card} revealed delay={i * 0.2} />
        ))}
      </motion.div>

      <FancyDivider />

      {/* Story */}
      <div style={{
        width: '100%',
        padding: '0 0.5rem',
        background: 'var(--card-bg)',
        borderRadius: 16,
        border: '1px solid var(--border)',
        padding: '1.5rem 1.2rem',
      }}>
        <TypewriterText text={result.story} onDone={() => setStoryDone(true)} />
      </div>

      {/* Fortune quote */}
      {storyDone && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          style={{
            textAlign: 'center',
            padding: '1.5rem 1rem',
            margin: '0.5rem 0',
            background: 'linear-gradient(135deg, rgba(184,154,62,0.04), rgba(212,135,154,0.03))',
            borderRadius: 16,
            border: '1px solid var(--border)',
          }}
        >
          <Divider width={250} />
          <p style={{
            fontFamily: "'Noto Serif TC', serif",
            fontSize: 'clamp(18px, 5vw, 24px)',
            color: 'var(--gold)',
            fontWeight: 500,
            letterSpacing: '2px',
            lineHeight: 2,
          }}>
            {'\u300C'}{result.fortune_quote}{'\u300D'}
          </p>
          <Divider width={250} />
        </motion.div>
      )}

      {/* Generate Image / Download / Restart buttons */}
      {storyDone && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '16px',
            marginBottom: '1rem',
            width: '100%',
          }}
        >
          {/* Story image area */}
          {imageState === 'loading' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              style={{
                width: '100%',
                display: 'flex',
                justifyContent: 'center',
                padding: '1rem 0',
              }}
            >
              <OrbLoader text="繪製命運之圖中⋯" />
            </motion.div>
          )}

          {imageState === 'done' && storyImageB64 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8 }}
              style={{
                width: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '1rem',
              }}
            >
              <FancyDivider />
              <p style={{
                fontSize: '13px',
                color: 'var(--text-muted)',
                letterSpacing: '3px',
                fontFamily: "'Cormorant Garamond', serif",
                textTransform: 'uppercase',
              }}>
                Your Destiny Image
              </p>
              <img
                src={`data:image/png;base64,${storyImageB64}`}
                alt="命運之圖"
                style={{
                  width: '100%',
                  maxWidth: 500,
                  borderRadius: 16,
                  boxShadow: '0 8px 50px rgba(184, 154, 62, 0.15), 0 0 0 1px rgba(184, 154, 62, 0.1)',
                  border: '2px solid var(--border)',
                }}
              />
              <motion.button
                onClick={handleDownload}
                whileHover={{ scale: 1.02, boxShadow: '0 8px 35px rgba(184, 154, 62, 0.18)' }}
                whileTap={{ scale: 0.97 }}
                style={{
                  padding: '14px 40px',
                  fontSize: '16px',
                  fontFamily: "'Noto Serif TC', serif",
                  color: 'var(--card-bg)',
                  background: 'linear-gradient(135deg, var(--gold), var(--gold-dark))',
                  border: 'none',
                  borderRadius: 12,
                  letterSpacing: '3px',
                  boxShadow: '0 4px 20px rgba(184, 154, 62, 0.15)',
                }}
              >
                儲存圖片
              </motion.button>
            </motion.div>
          )}

          {imageState === 'error' && (
            <p style={{
              color: 'var(--rose)',
              fontSize: '14px',
              textAlign: 'center',
              marginBottom: '0.5rem',
            }}>
              圖片生成失敗，可再試一次
            </p>
          )}

          {/* Generate image button */}
          {(imageState === 'idle' || imageState === 'error') && (
            <motion.button
              onClick={handleGenerateImage}
              whileHover={{
                scale: 1.02,
                boxShadow: '0 8px 35px rgba(184, 154, 62, 0.18)',
              }}
              whileTap={{ scale: 0.97 }}
              style={{
                padding: '16px 40px',
                fontSize: '16px',
                fontFamily: "'Noto Serif TC', serif",
                color: 'var(--card-bg)',
                background: 'linear-gradient(135deg, var(--gold), var(--gold-dark))',
                border: 'none',
                borderRadius: 12,
                letterSpacing: '3px',
                boxShadow: '0 4px 20px rgba(184, 154, 62, 0.15)',
              }}
            >
              生成命運之圖
            </motion.button>
          )}

          {/* Restart button */}
          <motion.button
            onClick={onRestart}
            whileHover={{ scale: 1.02, boxShadow: '0 6px 30px rgba(212, 135, 154, 0.12)' }}
            whileTap={{ scale: 0.97 }}
            style={{
              padding: '14px 40px',
              fontSize: '15px',
              fontFamily: "'Noto Serif TC', serif",
              color: 'var(--text-primary)',
              background: 'linear-gradient(135deg, rgba(212,135,154,0.10), rgba(184,154,62,0.06))',
              border: '1px solid var(--border-rose)',
              borderRadius: 12,
              letterSpacing: '3px',
            }}
          >
            再次占卜
          </motion.button>
        </motion.div>
      )}
    </motion.div>
  );
}
