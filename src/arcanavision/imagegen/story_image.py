"""故事主視覺圖生成，使用 Gemini 2.5 Flash Image。"""

import base64
import io
import logging

from google import genai
from google.genai import types
from PIL import Image

from arcanavision.config import settings

logger = logging.getLogger(__name__)

IMAGE_MODEL = "gemini-2.5-flash-image"

STORY_STYLE_PREFIX = (
    "Generate a square 1:1 aspect ratio image. "
    "A cinematic digital painting in Art Nouveau style inspired by Alphonse Mucha. "
    "Soft warm spring sunlight, flowing organic forms, rich symbolic details. "
    "Light pastel color palette with cherry blossom pink, fresh greens, and warm gold. "
    "Bright airy spring garden dreamlike atmosphere. "
    "The overall tone must be POSITIVE, HOPEFUL, and UPLIFTING — "
    "warm golden light, blooming flowers, a sense of new beginnings and growth. "
    "No text, no words, no letters, no borders, no frames. "
    "The scene depicts: "
)


def generate_story_image(scene_prompt: str, mood: str) -> Image.Image | None:
    """生成故事主視覺圖。失敗時回傳 None。"""
    if not settings.enable_story_image:
        logger.info("故事圖生成已停用")
        return None

    full_prompt = f"{STORY_STYLE_PREFIX}Mood: {mood}. {scene_prompt}"

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                raw = part.inline_data.data
                image_bytes = raw if isinstance(raw, bytes) else base64.b64decode(raw)
                logger.info("故事圖生成成功")
                return Image.open(io.BytesIO(image_bytes))
        logger.error("故事圖生成無圖片回傳")
        return None
    except Exception as e:
        logger.error(f"故事圖生成失敗：{e}")
        return None
