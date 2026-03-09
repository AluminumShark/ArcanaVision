"""驗證 78 張牌面圖的完整性與尺寸一致性。"""

import json
import logging
from pathlib import Path

from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ASSETS_DIR = Path("src/arcanavision/cards/assets")


def main() -> None:
    deck_path = Path("src/arcanavision/cards/data/tarot_deck.json")
    with open(deck_path, encoding="utf-8") as f:
        deck_data = json.load(f)

    all_ids: list[str] = []
    for card in deck_data["major_arcana"]:
        all_ids.append(card["id"])
    for suit in ("wands", "cups", "swords", "pentacles"):
        for card in deck_data["minor_arcana"][suit]:
            all_ids.append(card["id"])

    missing: list[str] = []
    sizes: dict[str, tuple[int, int]] = {}

    for card_id in all_ids:
        img_path = ASSETS_DIR / f"{card_id}.png"
        if not img_path.exists():
            missing.append(card_id)
            continue

        with Image.open(img_path) as img:
            sizes[card_id] = img.size

    if missing:
        logger.warning(f"缺少 {len(missing)} 張圖：{missing}")
    else:
        logger.info("所有 78 張圖都存在")

    if sizes:
        unique_sizes = set(sizes.values())
        if len(unique_sizes) == 1:
            size = unique_sizes.pop()
            logger.info(f"所有圖片尺寸一致：{size[0]}×{size[1]}")
        else:
            logger.warning(f"發現 {len(unique_sizes)} 種不同尺寸：")
            for size in unique_sizes:
                cards_with_size = [k for k, v in sizes.items() if v == size]
                logger.warning(f"  {size[0]}×{size[1]}: {len(cards_with_size)} 張")

    logger.info(f"驗證完成：{len(sizes)}/{len(all_ids)} 張圖存在")


if __name__ == "__main__":
    main()
