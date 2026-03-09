import { useState, useEffect, useCallback } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import Particles from './components/Particles';
import SpreadSelector from './components/SpreadSelector';
import QuestionInput from './components/QuestionInput';
import ShuffleAnimation from './components/ShuffleAnimation';
import OrbLoader from './components/OrbLoader';
import ReadingResult from './components/ReadingResult';
import { Divider, FancyDivider, StepLabel, Footer } from './components/Ornaments';
import { useReading } from './hooks/useReading';
import { fetchSpreads } from './utils/api';

const PHASES = {
  WELCOME: 'WELCOME',
  SPREAD_SELECT: 'SPREAD_SELECT',
  QUESTION: 'QUESTION',
  SHUFFLING: 'SHUFFLING',
  READING_LOADING: 'READING_LOADING',
  RESULT: 'RESULT',
};

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.7, ease: 'easeOut' } },
  exit: { opacity: 0, y: -10, transition: { duration: 0.3 } },
};

export default function App() {
  const [phase, setPhase] = useState(PHASES.WELCOME);
  const [spreads, setSpreads] = useState([]);
  const [selectedSpread, setSelectedSpread] = useState(null);
  const [question, setQuestion] = useState('');
  const { loading, result, error, doReading, reset } = useReading();

  // Load spreads
  useEffect(() => {
    fetchSpreads().then(setSpreads).catch(console.error);
  }, []);

  const handleStart = () => setPhase(PHASES.SPREAD_SELECT);

  const handleSpreadSelect = (spread) => {
    setSelectedSpread(spread);
    setPhase(PHASES.QUESTION);
  };

  const handleQuestion = useCallback(async (q) => {
    setQuestion(q);
    setPhase(PHASES.SHUFFLING);

    // 2.5s shuffle animation then start reading
    setTimeout(async () => {
      setPhase(PHASES.READING_LOADING);
      try {
        await doReading(selectedSpread.id, q);
        setPhase(PHASES.RESULT);
      } catch {
        setPhase(PHASES.RESULT);
      }
    }, 2500);
  }, [selectedSpread, doReading]);

  const handleRestart = () => {
    reset();
    setSelectedSpread(null);
    setQuestion('');
    setPhase(PHASES.WELCOME);
  };

  return (
    <>
      <Particles count={30} />

      <div style={{
        width: '100%',
        maxWidth: 680,
        minHeight: '100dvh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: phase === PHASES.WELCOME ? 'center' : 'flex-start',
        padding: '2rem 0',
      }}>
        <AnimatePresence mode="wait">
          {/* WELCOME */}
          {phase === PHASES.WELCOME && (
            <motion.div
              key="welcome"
              variants={pageVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '1rem',
              }}
            >
              {/* Badge */}
              <span style={{
                display: 'inline-block',
                padding: '5px 18px',
                border: '1px solid var(--border)',
                borderRadius: 20,
                fontSize: 10,
                letterSpacing: 3,
                textTransform: 'uppercase',
                color: 'var(--text-muted)',
                fontFamily: "'Cormorant Garamond', serif",
              }}>
                NTU AI Club · 社團聯展 2026
              </span>

              {/* Decorative arc */}
              <svg width="200" height="40" viewBox="0 0 200 40" style={{ opacity: 0.25, marginTop: '0.5rem' }}>
                <path d="M 20 35 Q 100 0, 180 35" fill="none" stroke="var(--gold)" strokeWidth="0.8" />
                <path d="M 40 35 Q 100 8, 160 35" fill="none" stroke="var(--rose)" strokeWidth="0.5" />
                <circle cx="100" cy="10" r="2" fill="var(--gold)" opacity="0.5" />
              </svg>

              {/* Logo orb */}
              <div style={{ position: 'relative', width: 120, height: 120 }}>
                {/* Outer decorative ring */}
                <div style={{
                  position: 'absolute',
                  inset: 0,
                  borderRadius: '50%',
                  border: '1px solid var(--gold)',
                  opacity: 0.2,
                  animation: 'borderGlow 3s ease-in-out infinite',
                }} />
                {/* Main orb */}
                <div style={{
                  position: 'absolute',
                  inset: 10,
                  borderRadius: '50%',
                  background: `conic-gradient(
                    from 45deg,
                    var(--rose-light),
                    var(--gold-light),
                    var(--sage-light),
                    var(--lavender-light),
                    var(--rose-light)
                  )`,
                  animation: 'orbGlow 3s ease-in-out infinite',
                }} />
                {/* Inner core */}
                <div style={{
                  position: 'absolute',
                  inset: 30,
                  borderRadius: '50%',
                  background: 'radial-gradient(circle at 40% 35%, rgba(255,252,248,0.95), var(--gold-light) 80%)',
                }} />
              </div>

              {/* Title */}
              <h1 style={{
                fontFamily: "'Cormorant Garamond', serif",
                fontSize: 'clamp(34px, 9vw, 52px)',
                fontWeight: 300,
                color: 'var(--text-primary)',
                letterSpacing: '10px',
                textAlign: 'center',
                marginTop: '0.5rem',
              }}>
                ArcanaVision
              </h1>

              <p style={{
                fontFamily: "'Noto Serif TC', serif",
                fontSize: '15px',
                color: 'var(--text-secondary)',
                letterSpacing: '6px',
              }}>
                春日塔羅占卜
              </p>

              <FancyDivider />

              <motion.button
                onClick={handleStart}
                whileHover={{
                  scale: 1.03,
                  boxShadow: '0 8px 35px rgba(184, 154, 62, 0.18)',
                }}
                whileTap={{ scale: 0.97 }}
                style={{
                  padding: '18px 56px',
                  fontSize: '17px',
                  fontFamily: "'Noto Serif TC', serif",
                  color: 'var(--card-bg)',
                  background: 'linear-gradient(135deg, var(--gold), var(--gold-dark))',
                  border: 'none',
                  borderRadius: 14,
                  letterSpacing: '6px',
                  transition: 'all 0.3s',
                  marginTop: '0.5rem',
                  boxShadow: '0 4px 25px rgba(184, 154, 62, 0.15)',
                }}
              >
                開始占卜
              </motion.button>

              {/* Bottom decorative arc */}
              <svg width="160" height="30" viewBox="0 0 160 30" style={{ opacity: 0.2, marginTop: '0.5rem' }}>
                <path d="M 10 5 Q 80 30, 150 5" fill="none" stroke="var(--gold)" strokeWidth="0.8" />
              </svg>
            </motion.div>
          )}

          {/* SPREAD SELECT */}
          {phase === PHASES.SPREAD_SELECT && (
            <motion.div
              key="spread"
              variants={pageVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
            >
              <StepLabel number="I" text="選擇牌陣" />
              <SpreadSelector spreads={spreads} onSelect={handleSpreadSelect} />
            </motion.div>
          )}

          {/* QUESTION */}
          {phase === PHASES.QUESTION && selectedSpread && (
            <motion.div
              key="question"
              variants={pageVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '2rem' }}
            >
              <StepLabel number="II" text="心中默念問題" />
              <QuestionInput spread={selectedSpread} onSubmit={handleQuestion} />
            </motion.div>
          )}

          {/* SHUFFLING */}
          {phase === PHASES.SHUFFLING && (
            <motion.div
              key="shuffle"
              variants={pageVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '4rem' }}
            >
              <ShuffleAnimation />
            </motion.div>
          )}

          {/* READING LOADING */}
          {phase === PHASES.READING_LOADING && (
            <motion.div
              key="loading"
              variants={pageVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '4rem' }}
            >
              <OrbLoader text="解讀命運中⋯" />
            </motion.div>
          )}

          {/* RESULT */}
          {phase === PHASES.RESULT && (
            <motion.div
              key="result"
              variants={pageVariants}
              initial="initial"
              animate="animate"
              exit="exit"
              style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}
            >
              {error && !result ? (
                <div style={{ textAlign: 'center', padding: '2rem' }}>
                  <p style={{ color: 'var(--rose)', marginBottom: '1rem', fontFamily: "'Noto Serif TC', serif" }}>
                    占卜過程中遇到了障礙：{error}
                  </p>
                  <motion.button
                    onClick={handleRestart}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    style={{
                      padding: '12px 30px',
                      fontSize: '14px',
                      fontFamily: "'Noto Serif TC', serif",
                      color: 'var(--text-primary)',
                      background: 'var(--card-bg)',
                      border: '1px solid var(--border)',
                      borderRadius: 10,
                    }}
                  >
                    重新開始
                  </motion.button>
                </div>
              ) : result ? (
                <ReadingResult result={result} onRestart={handleRestart} />
              ) : (
                <OrbLoader text="處理中⋯" />
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        {(phase === PHASES.WELCOME || phase === PHASES.RESULT) && <Footer />}
      </div>
    </>
  );
}
