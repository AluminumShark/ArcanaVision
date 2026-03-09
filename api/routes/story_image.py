"""故事圖生成 API（獨立端點，由前端觸發）。"""

import base64
import io
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from arcanavision.imagegen.story_image import generate_story_image

logger = logging.getLogger(__name__)

router = APIRouter()


class StoryImageRequest(BaseModel):
    scene_prompt: str
    mood: str


class StoryImageResponse(BaseModel):
    image_base64: str | None = None


@router.post("/api/story-image", response_model=StoryImageResponse)
async def create_story_image(req: StoryImageRequest) -> StoryImageResponse:
    """根據 scene_prompt 與 mood 生成故事圖。"""
    try:
        img = generate_story_image(req.scene_prompt, req.mood)
        if img:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            image_b64 = base64.b64encode(buf.getvalue()).decode()
            return StoryImageResponse(image_base64=image_b64)
        else:
            raise HTTPException(status_code=500, detail="圖片生成失敗")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"故事圖 API 失敗：{e}")
        raise HTTPException(status_code=500, detail="圖片生成失敗，請稍後再試")
