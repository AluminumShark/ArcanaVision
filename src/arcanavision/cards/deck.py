"""牌組載入、洗牌、抽牌邏輯。"""

import json
import random
from pathlib import Path

from .models import Card, DrawnCard

_DECK_PATH = Path(__file__).parent / "data" / "tarot_deck.json"


def load_deck() -> list[Card]:
    """從 tarot_deck.json 載入完整 78 張牌。"""
    with open(_DECK_PATH, encoding="utf-8") as f:
        data = json.load(f)

    cards: list[Card] = []

    for entry in data["major_arcana"]:
        cards.append(Card(**entry))

    for suit in ("wands", "cups", "swords", "pentacles"):
        for entry in data["minor_arcana"][suit]:
            cards.append(Card(**entry))

    return cards


def draw_cards(deck: list[Card], count: int) -> list[DrawnCard]:
    """從牌組中抽取不重複的牌，每張 50% 機率逆位。"""
    if count > len(deck):
        raise ValueError(f"無法從 {len(deck)} 張牌中抽取 {count} 張")

    selected = random.sample(deck, count)
    drawn: list[DrawnCard] = []

    for card in selected:
        drawn.append(
            DrawnCard(
                card=card,
                is_reversed=random.random() < 0.5,
            )
        )

    return drawn
