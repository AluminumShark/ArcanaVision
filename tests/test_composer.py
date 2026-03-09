"""測試圖片合成模組。"""

from PIL import Image

from arcanavision.cards.deck import draw_cards, load_deck
from arcanavision.imagegen.composer import compose_final_image
from arcanavision.reading.models import ReadingResult
from arcanavision.spreads.engine import assign_positions, load_spread


def _make_reading_result() -> ReadingResult:
    return ReadingResult(
        story="命運的轉盤正在為你旋轉。你站在人生的十字路口，過去的經歷像一面鏡子，映照出你內心深處的渴望。"
        "現在的你正處於一個關鍵的轉折點，舊有的模式正在瓦解，新的可能性正在萌芽。"
        "不要害怕改變，因為每一次蛻變都是成長的機會。星星在你的未來閃耀，指引你走向更光明的道路。",
        fortune_quote="勇氣不是沒有恐懼，而是帶著恐懼仍然前行",
        scene_prompt="A figure standing at a crossroads in a magical spring garden",
        mood="hopeful",
    )


def test_compose_without_story_image():
    deck = load_deck()
    spread = load_spread("three_card")
    drawn = draw_cards(deck, spread.card_count)
    assigned = assign_positions(drawn, spread)
    reading = _make_reading_result()

    result = compose_final_image(assigned, reading, "我的未來會怎樣？")

    assert isinstance(result, Image.Image)
    assert result.size[0] == 1200
    assert result.size[1] > 0


def test_compose_with_story_image():
    deck = load_deck()
    spread = load_spread("three_card")
    drawn = draw_cards(deck, spread.card_count)
    assigned = assign_positions(drawn, spread)
    reading = _make_reading_result()

    # 模擬故事圖
    story_img = Image.new("RGB", (1024, 1024), (200, 180, 160))

    result = compose_final_image(
        assigned, reading, "我的職涯發展？", story_image=story_img
    )

    assert isinstance(result, Image.Image)
    assert result.size[0] == 1200


def test_compose_single_card():
    deck = load_deck()
    spread = load_spread("daily_draw")
    drawn = draw_cards(deck, spread.card_count)
    assigned = assign_positions(drawn, spread)
    reading = _make_reading_result()

    result = compose_final_image(assigned, reading, "今天的運勢如何？")
    assert isinstance(result, Image.Image)


def test_compose_celtic_cross():
    deck = load_deck()
    spread = load_spread("celtic_cross")
    drawn = draw_cards(deck, spread.card_count)
    assigned = assign_positions(drawn, spread)
    reading = _make_reading_result()

    result = compose_final_image(assigned, reading, "深度分析我的處境")
    assert isinstance(result, Image.Image)
