# ArcanaVision

慕夏 Art Nouveau 風格塔羅占卜 Web App — **台大 AI 社（NTU AI Club）社團聯展 2026** 展示專案。

## 功能

- 78 張偉特塔羅完整正逆位支援，6 種牌陣
- Gemini 2.5 Flash LLM 敘事式解讀（白話風格）
- AI 生成慕夏風格「命運之圖」（Gemini Flash Image）
- 春日 Art Nouveau 風格前端（React + Framer Motion）
- Mobile-first 設計，展場 QR code 掃碼即用

## 技術棧

| 層級 | 技術 |
|------|------|
| 後端 | Python 3.12+, FastAPI, Pydantic |
| LLM | Gemini 2.5 Flash |
| 圖片生成 | Gemini 2.5 Flash Image |
| 前端 | React (Vite), Framer Motion |
| 字型 | Cormorant Garamond + Noto Serif TC |
| 套件管理 | uv (Python), pnpm (Node) |

## 快速開始

### 環境設定

```bash
cp .env.example .env
# 編輯 .env 填入 GEMINI_API_KEY
```

### 安裝依賴

```bash
# Python
uv sync

# 前端
cd web && pnpm install
```

### 下載字型

下載 [Noto Serif TC](https://fonts.google.com/noto/specimen/Noto+Serif+TC) 並放置於 `fonts/NotoSerifTC-Regular.otf`。

### 生成牌面圖（首次）

```bash
uv run python scripts/generate_card_art.py
```

78 張慕夏風格牌面圖會存到 `src/arcanavision/cards/assets/`。

### 啟動開發伺服器

```bash
# 終端 1：後端
uv run python main.py

# 終端 2：前端
cd web && pnpm dev
```

前端預設 `http://localhost:5173`，後端 `http://localhost:8000`。

## 專案結構

```
├── api/                    # FastAPI 路由與 schemas
│   ├── main.py
│   ├── schemas.py
│   └── routes/
│       ├── reading.py      # POST /api/reading
│       ├── spreads.py      # GET /api/spreads
│       └── story_image.py  # POST /api/story-image
│
├── src/arcanavision/       # 核心 Python 模組
│   ├── cards/              # 牌卡資料與牌組邏輯
│   ├── spreads/            # 牌陣定義（YAML）與引擎
│   ├── reading/            # LLM 解讀（Gemini）
│   └── imagegen/           # 圖片生成（故事圖 + 合成）
│
├── web/                    # React 前端
│   └── src/
│       ├── components/     # TarotCard, ReadingResult, etc.
│       ├── styles/         # CSS variables, animations
│       ├── hooks/          # useReading
│       └── utils/          # API wrapper
│
├── scripts/                # 牌面圖生成腳本
├── tests/                  # pytest 測試
└── fonts/                  # 中文字型（需自行下載）
```

## 展場部署

```bash
# 方案 A：本地（筆電 + 同 Wi-Fi 手機）
uv run python main.py
# 手機訪問 http://<筆電IP>:8000

# 方案 B：Cloud Run
gcloud run deploy arcanavision --source . --region asia-east1 --allow-unauthenticated
```

## 牌陣

| 牌陣 | 張數 | 說明 |
|------|------|------|
| 每日一牌 | 1 | 簡單日常指引 |
| 聖三角 | 3 | 過去／現在／未來 |
| 四元素 | 4 | 火水風土全面分析 |
| 時間之流 | 5 | 事件發展脈絡 |
| 愛情十字 | 5 | 感情問題 |
| 凱爾特十字 | 10 | 深度全面解析 |

## License

MIT
