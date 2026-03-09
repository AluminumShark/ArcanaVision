"""牌陣列表 API。"""

from fastapi import APIRouter

from api.schemas import SpreadInfo
from arcanavision.spreads.engine import list_spreads

router = APIRouter()


@router.get("/api/spreads", response_model=list[SpreadInfo])
async def get_spreads() -> list[SpreadInfo]:
    """回傳所有可用牌陣。"""
    spreads = list_spreads()
    return [
        SpreadInfo(
            id=s.id,
            name_en=s.name_en,
            name_zh=s.name_zh,
            card_count=s.card_count,
            description=s.description,
        )
        for s in spreads
    ]
