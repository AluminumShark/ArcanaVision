"""塔羅牌資料模型。"""

from pydantic import BaseModel


class Card(BaseModel):
    """單張塔羅牌的完整資料。"""

    id: str
    name_en: str
    name_zh: str
    number: int
    arcana: str  # "major" | "minor"
    suit: str | None = None  # "wands" | "cups" | "swords" | "pentacles" | None
    upright_keywords: list[str]
    reversed_keywords: list[str]
    upright_meaning: str
    reversed_meaning: str
    symbolism: str
    image_prompt_seed: str


class DrawnCard(BaseModel):
    """抽出的一張牌，包含正逆位與牌陣位置資訊。"""

    card: Card
    is_reversed: bool
    position_name: str = ""
    position_description: str = ""
