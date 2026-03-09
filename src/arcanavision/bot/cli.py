"""CLI 互動式塔羅占卜介面。"""

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

from arcanavision.cards.deck import draw_cards, load_deck
from arcanavision.imagegen.composer import compose_final_image
from arcanavision.imagegen.story_image import generate_story_image
from arcanavision.reading.interpreter import generate_reading
from arcanavision.spreads.engine import assign_positions, list_spreads

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("output")


async def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print()
    print("  ✦ 歡迎來到 ArcanaVision ✦")
    print("  春日慕夏風格塔羅占卜")
    print()

    # 載入牌組
    deck = load_deck()
    spreads = list_spreads()

    # 選擇牌陣
    print("請選擇牌陣：")
    for i, spread in enumerate(spreads, 1):
        print(f"  [{i}] {spread.name_zh} — {spread.description}")
    print()

    while True:
        try:
            choice = input("> ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(spreads):
                selected_spread = spreads[idx]
                break
            print(f"請輸入 1-{len(spreads)} 的數字")
        except (ValueError, EOFError):
            print(f"請輸入 1-{len(spreads)} 的數字")

    print()
    print("請在心中默念你的問題，然後輸入：")
    try:
        question = input("> ").strip()
    except EOFError:
        question = "今天的運勢如何？"

    if not question:
        question = "今天的運勢如何？"

    # 洗牌
    print()
    print("🔮 洗牌中...")
    drawn = draw_cards(deck, selected_spread.card_count)
    assigned = assign_positions(drawn, selected_spread)

    print(f"✨ 為你抽出了 {len(assigned)} 張牌：")
    print()
    for dc in assigned:
        orientation = "逆位" if dc.is_reversed else "正位"
        print(f"  位置「{dc.position_name}」→ {dc.card.name_zh}（{orientation}）")
    print()

    # LLM 解讀
    print("📖 正在解讀命運...")
    try:
        reading = await generate_reading(assigned, selected_spread, question)
    except Exception as e:
        logger.error(f"解讀失敗：{e}")
        print("  ⚠ 解讀生成失敗，請確認 GEMINI_API_KEY 已設定")
        return

    print()
    print("故事解讀：")
    print(f"  {reading.story}")
    print()
    print(f"  ✦ 命運箴言：「{reading.fortune_quote}」")
    print()

    # 故事圖生成
    print("🎨 正在繪製命運之圖...")
    story_image = generate_story_image(reading.scene_prompt, reading.mood)

    # 合成最終圖片
    final_image = compose_final_image(assigned, reading, question, story_image)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"reading_{timestamp}.png"
    final_image.save(str(output_path))

    print(f"✅ 命運之圖已儲存：{output_path}")
    print()
    print("  台大 AI 社 · NTU AI Club · 社團聯展 2025")
    print("  Powered by Gemini 2.0 Flash & Vertex AI Imagen 3")
    print()


def run() -> None:
    """入口函式。"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n  ✦ 感謝使用 ArcanaVision，願命運與你同在 ✦\n")
        sys.exit(0)


if __name__ == "__main__":
    run()
