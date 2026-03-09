"""塔羅解讀 API。"""

import logging

from fastapi import APIRouter, HTTPException

from api.schemas import CardResult, ReadingRequest, ReadingResponse
from arcanavision.cards.deck import draw_cards, load_deck
from arcanavision.reading.interpreter import generate_reading
from arcanavision.spreads.engine import assign_positions, load_spread

logger = logging.getLogger(__name__)

router = APIRouter()

_deck = load_deck()


@router.post("/api/reading", response_model=ReadingResponse)
async def create_reading(req: ReadingRequest) -> ReadingResponse:
    """完整算牌流程：載入牌陣 → 抽牌 → LLM 解讀（不含圖片生成）。"""
    try:
        spread = load_spread(req.spread_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"找不到牌陣：{req.spread_id}")

    drawn = draw_cards(_deck, spread.card_count)
    assigned = assign_positions(drawn, spread)

    try:
        reading = await generate_reading(assigned, spread, req.question)
    except Exception as e:
        logger.error(f"LLM 解讀失敗：{e}")
        raise HTTPException(status_code=500, detail="解讀生成失敗，請稍後再試")

    cards = []
    for dc in assigned:
        keywords = dc.card.reversed_keywords if dc.is_reversed else dc.card.upright_keywords
        cards.append(
            CardResult(
                id=dc.card.id,
                name_zh=dc.card.name_zh,
                name_en=dc.card.name_en,
                number=dc.card.number,
                is_reversed=dc.is_reversed,
                position_name=dc.position_name,
                position_description=dc.position_description,
                keywords=keywords,
                asset_url=f"/assets/{dc.card.id}.png",
            )
        )

    return ReadingResponse(
        cards=cards,
        story=reading.story,
        fortune_quote=reading.fortune_quote,
        scene_prompt=reading.scene_prompt,
        mood=reading.mood,
    )
