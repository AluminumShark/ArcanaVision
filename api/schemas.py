"""FastAPI Request/Response 資料模型。"""

from pydantic import BaseModel


class SpreadInfo(BaseModel):
    id: str
    name_en: str
    name_zh: str
    card_count: int
    description: str


class ReadingRequest(BaseModel):
    spread_id: str
    question: str


class CardResult(BaseModel):
    id: str
    name_zh: str
    name_en: str
    number: int
    is_reversed: bool
    position_name: str
    position_description: str
    keywords: list[str]
    asset_url: str


class ReadingResponse(BaseModel):
    cards: list[CardResult]
    story: str
    fortune_quote: str
    scene_prompt: str
    mood: str