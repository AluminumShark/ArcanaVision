"""ArcanaVision FastAPI 主應用程式。"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes.reading import router as reading_router
from api.routes.spreads import router as spreads_router
from api.routes.story_image import router as story_image_router

app = FastAPI(title="ArcanaVision API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(spreads_router)
app.include_router(reading_router)
app.include_router(story_image_router)

# 靜態檔案（牌面圖）
assets_dir = Path("src/arcanavision/cards/assets")
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

# 前端靜態檔案（production build）
web_dist = Path("web/dist")
if web_dist.exists():
    app.mount("/", StaticFiles(directory=str(web_dist), html=True), name="web")
