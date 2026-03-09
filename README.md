<h1 align="center">ArcanaVision</h1>

<p align="center">
  慕夏 Art Nouveau 風格塔羅占卜 Web App<br>
  <strong>台大 AI 社（NTU AI Club）社團聯展 2026</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?logo=google&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/Vite-6-646CFF?logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/github/license/AluminumShark/ArcanaVision" alt="License">
</p>

---

## Features

- 78 張偉特塔羅完整正逆位支援，6 種牌陣
- Gemini 2.5 Flash LLM 敘事式解讀（白話風格）
- AI 生成慕夏風格「命運之圖」（Gemini Flash Image）
- 春日 Art Nouveau 風格前端（React + Framer Motion）
- Mobile-first 設計，展場 QR code 掃碼即用

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12+, FastAPI, Pydantic |
| LLM | Gemini 2.5 Flash |
| Image Gen | Gemini 2.5 Flash Image |
| Frontend | React (Vite), Framer Motion |
| Fonts | Cormorant Garamond + Noto Serif TC |
| Package Mgr | uv (Python), pnpm (Node) |

## Quick Start

### Setup

```bash
cp .env.example .env
# Edit .env and fill in GEMINI_API_KEY
```

### Install

```bash
# Python
uv sync

# Frontend
cd web && pnpm install
```

### Download Font

Download [Noto Serif TC](https://fonts.google.com/noto/specimen/Noto+Serif+TC) and place at `fonts/NotoSerifTC-Regular.otf`.

### Generate Card Art (first time)

```bash
uv run python scripts/generate_card_art.py
```

78 Mucha-style card images will be saved to `src/arcanavision/cards/assets/`.

### Run Dev Server

```bash
# Terminal 1: Backend
uv run python main.py

# Terminal 2: Frontend
cd web && pnpm dev
```

Frontend at `http://localhost:5173`, backend at `http://localhost:8000`.

## Project Structure

```
├── api/                    # FastAPI routes & schemas
│   ├── main.py
│   ├── schemas.py
│   └── routes/
│       ├── reading.py      # POST /api/reading
│       ├── spreads.py      # GET /api/spreads
│       └── story_image.py  # POST /api/story-image
│
├── src/arcanavision/       # Core Python modules
│   ├── cards/              # Deck data & logic
│   ├── spreads/            # Spread definitions (YAML)
│   ├── reading/            # LLM interpreter (Gemini)
│   └── imagegen/           # Image generation
│
├── web/                    # React frontend
│   └── src/
│       ├── components/     # TarotCard, ReadingResult, etc.
│       ├── styles/         # CSS variables, animations
│       ├── hooks/          # useReading
│       └── utils/          # API wrapper
│
├── scripts/                # Card art generation scripts
├── tests/                  # pytest tests
└── fonts/                  # CJK font (download separately)
```

## Spreads

| Spread | Cards | Description |
|--------|-------|-------------|
| 每日一牌 | 1 | Daily guidance |
| 聖三角 | 3 | Past / Present / Future |
| 四元素 | 4 | Fire, Water, Air, Earth |
| 時間之流 | 5 | Timeline progression |
| 愛情十字 | 5 | Relationship reading |
| 凱爾特十字 | 10 | Deep comprehensive analysis |

## Deployment

```bash
# Option A: Local (laptop + same Wi-Fi)
uv run python main.py
# Visit http://<laptop-ip>:8000 from phone

# Option B: Cloud Run
gcloud run deploy arcanavision --source . --region asia-east1 --allow-unauthenticated
```

## License

[MIT](LICENSE)
