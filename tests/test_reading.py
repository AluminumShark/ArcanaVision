"""測試 LLM 解讀引擎（mock API）。"""

import json
from unittest.mock import MagicMock, patch

import pytest

from arcanavision.cards.deck import draw_cards, load_deck
from arcanavision.reading.interpreter import (
    _format_cards,
    _parse_response,
    generate_reading,
)
from arcanavision.reading.models import ReadingResult
from arcanavision.spreads.engine import assign_positions, load_spread


def _make_drawn_cards():
    deck = load_deck()
    spread = load_spread("three_card")
    drawn = draw_cards(deck, spread.card_count)
    return assign_positions(drawn, spread), spread


def test_format_cards():
    drawn, _ = _make_drawn_cards()
    result = _format_cards(drawn)
    assert "位置「過去」" in result
    assert "位置「現在」" in result
    assert "位置「未來」" in result


def test_parse_response_valid_json():
    raw = json.dumps(
        {
            "story": "這是一個測試故事...",
            "fortune_quote": "命運在微笑",
            "scene_prompt": "A dreamy garden scene with golden light",
            "mood": "hopeful",
        }
    )
    result = _parse_response(raw)
    assert isinstance(result, ReadingResult)
    assert result.mood == "hopeful"


def test_parse_response_with_code_fence():
    raw = '```json\n{"story": "test", "fortune_quote": "q", "scene_prompt": "s", "mood": "m"}\n```'
    result = _parse_response(raw)
    assert result.story == "test"


@pytest.mark.asyncio
async def test_generate_reading_mocked():
    drawn, spread = _make_drawn_cards()

    mock_response = MagicMock()
    mock_response.text = json.dumps(
        {
            "story": "命運的轉盤正在為你旋轉...",
            "fortune_quote": "勇氣是穿越黑暗的唯一燈火",
            "scene_prompt": "A mystical garden bathed in spring light with cherry blossoms falling",
            "mood": "hopeful",
        }
    )

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = mock_response

    with patch(
        "arcanavision.reading.interpreter.genai.Client", return_value=mock_client
    ):
        result = await generate_reading(drawn, spread, "我的未來會怎樣？")

    assert isinstance(result, ReadingResult)
    assert len(result.story) > 0
    assert result.mood == "hopeful"
