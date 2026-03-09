"""批量生成 78 張慕夏春日風格牌面圖（支援斷點續跑）。

使用 gemini-2.5-flash-image 原生圖片生成，無嚴格每日限額。
"""

import json
import logging
import time
from pathlib import Path

from google import genai
from google.genai import types

from arcanavision.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IMAGE_MODEL = "gemini-2.5-flash-image"

CARD_STYLE_PREFIX = (
    "Generate a tarot card image in vertical 3:4 portrait aspect ratio. "
    "Art Nouveau illustration style of Alphonse Mucha. "
    "Highly consistent uniform style across all cards in the deck. "
    "The card has an ornate Art Nouveau decorative border frame with "
    "flowing cherry blossom vines, circular floral medallion patterns, "
    "and elegant scrollwork in muted warm browns, pinks, and sage greens. "
    "Rounded corners on the card. "
    "Warm ivory cream background in the center scene area. "
    "Elegant flowing lines, soft spring pastel color palette: warm golds, "
    "cherry blossom pinks, fresh sage greens, gentle lavender. "
    "Ethereal figure(s) with flowing hair and draped clothing. "
    "Decorative halo/nimbus motifs with spring flowers and fresh botanical elements. "
    "Mosaic-like background details. Flat yet dimensional lithographic quality. "
    "Rich botanical and celestial decorative elements. "
    "Bright, airy, spring garden atmosphere. "
    "Professional tarot card art. "
)

ROMAN = {
    0: "0", 1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII",
    8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII", 13: "XIII", 14: "XIV",
    15: "XV", 16: "XVI", 17: "XVII", 18: "XVIII", 19: "XIX", 20: "XX", 21: "XXI",
}

ASSETS_DIR = Path("src/arcanavision/cards/assets")
LOG_PATH = Path("generation_log.json")

# 每次請求間隔秒數，避免觸發速率限制
REQUEST_DELAY = 3


def _load_log() -> dict:
    if LOG_PATH.exists():
        with open(LOG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "failed": []}


def _save_log(log: dict) -> None:
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def _load_all_cards() -> list[dict]:
    deck_path = Path("src/arcanavision/cards/data/tarot_deck.json")
    with open(deck_path, encoding="utf-8") as f:
        deck_data = json.load(f)

    cards: list[dict] = []
    cards.extend(deck_data["major_arcana"])
    for suit in ("wands", "cups", "swords", "pentacles"):
        cards.extend(deck_data["minor_arcana"][suit])
    return cards


def _build_prompt(card: dict) -> str:
    """組合完整 prompt。所有牌卡統一使用羅馬數字，統一牌名標示風格。"""
    number = card.get("number", "")
    name_en = card["name_en"]
    num_text = ROMAN.get(number, str(number))
    label = name_en.upper()

    return (
        CARD_STYLE_PREFIX
        + f"TEXT LAYOUT — Display the Roman numeral \"{num_text}\" at the TOP center "
        + "of the card in dark elegant serif typography. "
        + f"At the BOTTOM center, display \"{label}\" inside a simple clean "
        + "rectangular text banner with serif uppercase typography. "
        + "The text banner style must be identical and consistent across all cards. "
        + f"SCENE — The card depicts: {card['image_prompt_seed']}"
    )


def _generate_image(client: genai.Client, prompt: str) -> bytes | None:
    """使用 gemini-2.5-flash-image 生成圖片，回傳 PNG bytes。"""
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )
    if not response.candidates:
        return None
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            return part.inline_data.data
    return None


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    cards = _load_all_cards()
    log = _load_log()
    completed = set(log["completed"])

    client = genai.Client(api_key=settings.gemini_api_key)

    for i, card in enumerate(cards):
        card_id = card["id"]

        if card_id in completed:
            output_path = ASSETS_DIR / f"{card_id}.png"
            if output_path.exists():
                logger.info(f"已完成，跳過：{card_id}")
                continue
            # log 說完成但檔案不存在，需重新生成
            completed.discard(card_id)
            log["completed"] = [c for c in log["completed"] if c != card_id]
            _save_log(log)
            logger.info(f"檔案遺失，重新生成：{card_id}")

        output_path = ASSETS_DIR / f"{card_id}.png"
        prompt = _build_prompt(card)
        logger.info(f"[{i+1}/{len(cards)}] 生成中：{card_id} ({card['name_en']})...")

        try:
            img_bytes = _generate_image(client, prompt)
            if img_bytes is None:
                raise RuntimeError("無圖片回傳")
            output_path.write_bytes(img_bytes)
            log["completed"].append(card_id)
            if card_id in log.get("failed", []):
                log["failed"] = [c for c in log["failed"] if c != card_id]
            _save_log(log)
            completed.add(card_id)
            logger.info(f"  成功：{output_path}")
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                logger.warning(f"  達到速率限制，等待 60 秒後重試...")
                time.sleep(60)
                try:
                    img_bytes = _generate_image(client, prompt)
                    if img_bytes is None:
                        raise RuntimeError("無圖片回傳")
                    output_path.write_bytes(img_bytes)
                    log["completed"].append(card_id)
                    if card_id in log.get("failed", []):
                        log["failed"] = [c for c in log["failed"] if c != card_id]
                    _save_log(log)
                    completed.add(card_id)
                    logger.info(f"  重試成功：{output_path}")
                except Exception as retry_e:
                    logger.error(f"  重試失敗：{card_id} — {retry_e}")
                    if card_id not in log.get("failed", []):
                        log.setdefault("failed", []).append(card_id)
                    _save_log(log)
            else:
                logger.error(f"  失敗：{card_id} — {e}")
                if card_id not in log.get("failed", []):
                    log.setdefault("failed", []).append(card_id)
                _save_log(log)

        # 避免觸發速率限制
        if i < len(cards) - 1:
            time.sleep(REQUEST_DELAY)

    total = len(cards)
    done = len([c for c in log["completed"] if c in {card["id"] for card in cards}])
    failed = len(log.get("failed", []))
    logger.info(f"完成：{done}/{total}，失敗：{failed}")


if __name__ == "__main__":
    main()
