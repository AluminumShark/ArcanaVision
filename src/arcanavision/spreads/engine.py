"""牌陣載入與位置分配引擎。"""

from pathlib import Path

import yaml

from arcanavision.cards.models import DrawnCard

from .models import Spread, SpreadPosition

_DEFINITIONS_DIR = Path(__file__).parent / "definitions"


def load_spread(spread_id: str) -> Spread:
    """從 YAML 檔案載入指定牌陣。"""
    yaml_path = _DEFINITIONS_DIR / f"{spread_id}.yaml"
    if not yaml_path.exists():
        raise FileNotFoundError(f"找不到牌陣定義：{spread_id}")

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    positions = [SpreadPosition(**p) for p in data["positions"]]

    return Spread(
        id=spread_id,
        name_en=data["name_en"],
        name_zh=data["name_zh"],
        card_count=data["card_count"],
        description=data["description"],
        positions=positions,
    )


def list_spreads() -> list[Spread]:
    """列出所有可用的牌陣。"""
    spreads: list[Spread] = []
    for yaml_file in sorted(_DEFINITIONS_DIR.glob("*.yaml")):
        spread_id = yaml_file.stem
        spreads.append(load_spread(spread_id))
    return spreads


def assign_positions(drawn_cards: list[DrawnCard], spread: Spread) -> list[DrawnCard]:
    """將牌陣位置資訊填入已抽出的牌。"""
    if len(drawn_cards) != spread.card_count:
        raise ValueError(
            f"牌數不符：抽了 {len(drawn_cards)} 張，牌陣需要 {spread.card_count} 張"
        )

    for card, position in zip(drawn_cards, spread.positions):
        card.position_name = position.name
        card.position_description = position.description

    return drawn_cards
