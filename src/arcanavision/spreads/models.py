"""牌陣資料模型。"""

from pydantic import BaseModel


class SpreadPosition(BaseModel):
    """牌陣中的單一位置。"""

    index: int
    name: str
    description: str


class Spread(BaseModel):
    """牌陣定義。"""

    id: str
    name_en: str
    name_zh: str
    card_count: int
    description: str
    positions: list[SpreadPosition]
