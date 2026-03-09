"""LLM 解讀引擎，使用 Gemini 2.0 Flash 生成塔羅故事。"""

import json
import logging
import re
from pathlib import Path

from google import genai

from arcanavision.cards.models import DrawnCard
from arcanavision.config import settings
from arcanavision.spreads.models import Spread

from .models import ReadingResult

logger = logging.getLogger(__name__)

_PROMPT_PATH = Path(__file__).parent / "prompts" / "reading_prompt.txt"
_PROMPT_TEMPLATE = _PROMPT_PATH.read_text(encoding="utf-8")


def _format_cards(drawn_cards: list[DrawnCard]) -> str:
    """將抽牌結果格式化為 prompt 用的文字。"""
    lines: list[str] = []
    for dc in drawn_cards:
        orientation = "逆位" if dc.is_reversed else "正位"
        keywords = (
            dc.card.reversed_keywords if dc.is_reversed else dc.card.upright_keywords
        )
        keywords_str = "、".join(keywords)
        lines.append(f"位置「{dc.position_name}」→ {dc.card.name_zh}（{orientation}）")
        lines.append(f"  關鍵字：{keywords_str}")
        lines.append(f"  位置含義：{dc.position_description}")
        lines.append("")
    return "\n".join(lines)


def _parse_response(text: str) -> ReadingResult:
    """解析 LLM 回傳的 JSON，處理可能的 markdown code fence。"""
    cleaned = re.sub(r"```(?:json)?\s*", "", text)
    cleaned = cleaned.strip().rstrip("`")
    data = json.loads(cleaned)
    return ReadingResult(**data)


async def generate_reading(
    drawn_cards: list[DrawnCard],
    spread: Spread,
    user_question: str,
) -> ReadingResult:
    """呼叫 Gemini API 生成塔羅解讀。"""
    formatted_cards = _format_cards(drawn_cards)
    prompt = _PROMPT_TEMPLATE.format(
        user_question=user_question,
        spread_name=f"{spread.name_zh} {spread.name_en}",
        spread_description=spread.description,
        formatted_cards=formatted_cards,
    )

    client = genai.Client(api_key=settings.gemini_api_key)

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.8,
                    response_mime_type="application/json",
                ),
            )
            return _parse_response(response.text or "")
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.warning(f"解讀解析失敗（第 {attempt + 1} 次）：{e}")
            if attempt == 1:
                raise
        except Exception as e:
            logger.error(f"Gemini API 呼叫失敗：{e}")
            raise

    raise RuntimeError("解讀生成失敗")
