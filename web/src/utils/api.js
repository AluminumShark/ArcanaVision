const BASE = '';

export async function fetchSpreads() {
  const res = await fetch(`${BASE}/api/spreads`);
  if (!res.ok) throw new Error('無法載入牌陣');
  return res.json();
}

export async function fetchReading(spreadId, question) {
  const res = await fetch(`${BASE}/api/reading`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ spread_id: spreadId, question }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || '解讀失敗');
  }
  return res.json();
}

export async function fetchStoryImage(scenePrompt, mood) {
  const res = await fetch(`${BASE}/api/story-image`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scene_prompt: scenePrompt, mood }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || '圖片生成失敗');
  }
  return res.json();
}
