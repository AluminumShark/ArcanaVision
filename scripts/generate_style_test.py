"""測試慕夏春日風格牌面圖生成（5 張代表牌）。"""

import json
import logging
from pathlib import Path

from google import genai
from google.genai import types

from arcanavision.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IMAGE_MODEL = "imagen-4.0-ultra-generate-001"

CARD_STYLE_PREFIX = (
    "A tarot card illustration in the Art Nouveau style of Alphonse Mucha. "
    "Highly consistent uniform style. Full-bleed, borderless artwork extending to the very edge of the image (NO white or blank margins). "
    "Elegant flowing lines, integrated organic floral and geometric patterns without external frames. "
    "Soft spring pastel color palette with warm golds, cherry blossom pinks, fresh sage greens, and gentle lavender. "
    "Light warm ivory cream background. Ethereal figure(s) with flowing hair and draped clothing. "
    "Decorative halo/nimbus motifs with spring flowers and fresh botanical elements. "
    "Mosaic-like background details. Flat yet dimensional lithographic quality. "
    "Rich botanical and celestial decorative elements. Bright, airy, spring garden atmosphere. "
    "Professional tarot card art, vertical composition. "
)

ROMAN = {
    0: "0",
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X",
    11: "XI",
    12: "XII",
    13: "XIII",
    14: "XIV",
    15: "XV",
    16: "XVI",
    17: "XVII",
    18: "XVIII",
    19: "XIX",
    20: "XX",
    21: "XXI",
}

TEST_CARD_IDS = ["major_00", "major_02", "major_13", "wands_01", "cups_10"]

OUTPUT_DIR = Path("output/style_test")


def _build_prompt(card: dict) -> str:
    """組合完整 prompt，包含牌面場景與底部牌名。"""
    number = card.get("number", "")
    name_en = card["name_en"]
    if card["arcana"] == "major":
        num_text = ROMAN.get(number, str(number))
        label = f"{num_text} — {name_en}"
        top_text = num_text
    else:
        label = name_en
        top_text = str(number)

    return (
        CARD_STYLE_PREFIX
        + f'CRITICAL TEXT INSTRUCTION: You MUST boldly and clearly write the exact text "{top_text}" at the TOP center of the card. '
        + f'CRITICAL TEXT INSTRUCTION: You MUST boldly and clearly write the exact text "{label}" at the BOTTOM center of the card in elegant serif typography. '
        + f"The card depicts: {card['image_prompt_seed']}"
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    deck_path = Path("src/arcanavision/cards/data/tarot_deck.json")
    with open(deck_path, encoding="utf-8") as f:
        deck_data = json.load(f)

    all_cards = {}
    for card in deck_data["major_arcana"]:
        all_cards[card["id"]] = card
    for suit in ("wands", "cups", "swords", "pentacles"):
        for card in deck_data["minor_arcana"][suit]:
            all_cards[card["id"]] = card

    client = genai.Client(api_key=settings.gemini_api_key)

    for card_id in TEST_CARD_IDS:
        card = all_cards[card_id]
        prompt = _build_prompt(card)
        output_path = OUTPUT_DIR / f"{card_id}.png"

        if output_path.exists():
            logger.info(f"已存在，跳過：{card_id}")
            continue

        logger.info(f"生成中：{card_id} ({card['name_en']})...")

        try:
            response = client.models.generate_images(
                model=IMAGE_MODEL,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="3:4",
                    safety_filter_level="BLOCK_LOW_AND_ABOVE",
                    person_generation="ALLOW_ADULT",
                ),
            )
            if response.generated_images:
                response.generated_images[0].image.save(str(output_path))
                logger.info(f"成功：{output_path}")
            else:
                logger.error(f"無圖片回傳：{card_id}")
        except Exception as e:
            logger.error(f"失敗：{card_id} — {e}")


if __name__ == "__main__":
    main()
