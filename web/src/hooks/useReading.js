import { useState, useCallback } from 'react';
import { fetchReading } from '../utils/api';

export function useReading() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const doReading = useCallback(async (spreadId, question) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await fetchReading(spreadId, question);
      setResult(data);
      return data;
    } catch (e) {
      setError(e.message);
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
    setLoading(false);
  }, []);

  return { loading, result, error, doReading, reset };
}
