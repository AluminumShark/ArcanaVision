"""圖片合成排版，將故事圖、牌面圖、文字合成最終輸出圖。"""

import logging
import textwrap
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from arcanavision.cards.models import DrawnCard
from arcanavision.reading.models import ReadingResult

logger = logging.getLogger(__name__)

# 視覺參數（春日淺色主題）
CANVAS_WIDTH = 1200
BG_COLOR = (248, 244, 238)  # 暖象牙
TEXT_COLOR = (61, 48, 40)  # 暖深棕
ACCENT_COLOR = (184, 154, 62)  # 柔金
ROSE_COLOR = (212, 135, 154)  # 櫻花粉
MUTED_COLOR = (154, 142, 130)  # 淡棕

CARD_THUMB_W = 150
CARD_THUMB_H = 259
CARD_GAP = 20
PADDING = 60
LINE_HEIGHT_RATIO = 1.6

FONT_DIR = Path("fonts")
ASSETS_DIR = Path("src/arcanavision/cards/assets")


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    font_path = FONT_DIR / "NotoSansCJKtc-Regular.otf"
    if font_path.exists():
        return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def _draw_centered_text(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
) -> int:
    """繪製置中文字，回傳下一行 y 座標。"""
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (CANVAS_WIDTH - w) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return y + bbox[3] - bbox[1]


def _draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    max_width: int,
) -> int:
    """繪製自動換行文字，回傳下一行 y 座標。"""
    lines = textwrap.wrap(text, width=28)
    line_height = int(font.size * LINE_HEIGHT_RATIO)
    for line in lines:
        draw.text((PADDING, y), line, font=font, fill=fill)
        y += line_height
    return y


def _draw_separator(draw: ImageDraw.ImageDraw, y: int) -> int:
    """繪製金色分隔線。"""
    center_y = y + 15
    # 漸層線效果（中間亮，兩端淡）
    for i in range(CANVAS_WIDTH):
        dist = abs(i - CANVAS_WIDTH // 2) / (CANVAS_WIDTH // 2)
        alpha = max(0, int(180 * (1 - dist)))
        draw.point((i, center_y), fill=(*ACCENT_COLOR, alpha))
    # 中心圓點
    draw.ellipse(
        (CANVAS_WIDTH // 2 - 3, center_y - 3, CANVAS_WIDTH // 2 + 3, center_y + 3),
        fill=ACCENT_COLOR,
    )
    return y + 30


def compose_final_image(
    drawn_cards: list[DrawnCard],
    reading: ReadingResult,
    user_question: str,
    story_image: Image.Image | None = None,
) -> Image.Image:
    """合成最終輸出圖。"""
    font_title = _load_font(36)
    font_subtitle = _load_font(22)
    font_body = _load_font(20)
    font_label = _load_font(16)
    font_quote = _load_font(24)
    font_footer = _load_font(14)

    # 先計算高度
    height = PADDING  # top padding
    height += 50  # title
    height += 35  # question
    height += 30  # separator

    if story_image:
        story_display_w = CANVAS_WIDTH - PADDING * 2
        height += story_display_w + 20  # story image (square)

    # 牌卡區
    card_count = len(drawn_cards)
    if card_count <= 5:
        card_rows = 1
    else:
        card_rows = (card_count + 4) // 5  # ceil(n/5)
    height += card_rows * (CARD_THUMB_H + 30) + 20

    height += 30  # separator
    # 故事文字
    story_lines = textwrap.wrap(reading.story, width=28)
    height += len(story_lines) * int(20 * LINE_HEIGHT_RATIO) + 20

    height += 30  # separator
    height += 40  # quote
    height += 30  # separator
    height += 30  # footer
    height += PADDING  # bottom padding

    # 建立畫布
    canvas = Image.new("RGBA", (CANVAS_WIDTH, height), (*BG_COLOR, 255))
    draw = ImageDraw.ImageDraw(canvas)
    y = PADDING

    # 標題
    y = _draw_centered_text(draw, y, "ArcanaVision", font_title, ACCENT_COLOR)
    y += 10
    # 問題
    question_display = (
        f"「{user_question}」"
        if len(user_question) <= 20
        else f"「{user_question[:20]}...」"
    )
    y = _draw_centered_text(draw, y, question_display, font_subtitle, MUTED_COLOR)
    y += 15
    y = _draw_separator(draw, y)

    # 故事主視覺圖
    if story_image:
        story_display_w = CANVAS_WIDTH - PADDING * 2
        resized = story_image.resize((story_display_w, story_display_w), Image.LANCZOS)
        if resized.mode != "RGBA":
            resized = resized.convert("RGBA")
        canvas.paste(resized, (PADDING, y), resized)
        y += story_display_w + 20

    # 牌卡區
    for i, dc in enumerate(drawn_cards):
        row = i // 5
        col = i % 5
        # 重新計算每行
        row_count = min(5, card_count - row * 5)
        row_width = row_count * CARD_THUMB_W + (row_count - 1) * CARD_GAP
        row_start_x = (CANVAS_WIDTH - row_width) // 2

        cx = row_start_x + col * (CARD_THUMB_W + CARD_GAP)
        cy = y + row * (CARD_THUMB_H + 30)

        # 嘗試載入牌面圖
        card_img_path = ASSETS_DIR / f"{dc.card.id}.png"
        if card_img_path.exists():
            card_img = Image.open(card_img_path)
            card_img = card_img.resize((CARD_THUMB_W, CARD_THUMB_H), Image.LANCZOS)
            if dc.is_reversed:
                card_img = card_img.rotate(180)
            if card_img.mode != "RGBA":
                card_img = card_img.convert("RGBA")
            canvas.paste(card_img, (cx, cy), card_img)
        else:
            # placeholder
            draw.rectangle(
                (cx, cy, cx + CARD_THUMB_W, cy + CARD_THUMB_H),
                outline=ACCENT_COLOR,
                width=2,
            )
            orientation = "逆" if dc.is_reversed else "正"
            _draw_centered_text(
                draw,
                cy + CARD_THUMB_H // 2 - 10,
                f"{dc.card.name_zh}({orientation})",
                font_label,
                TEXT_COLOR,
            )

        # 位置標籤
        label = dc.position_name
        label_bbox = draw.textbbox((0, 0), label, font=font_label)
        label_w = label_bbox[2] - label_bbox[0]
        draw.text(
            (cx + (CARD_THUMB_W - label_w) // 2, cy + CARD_THUMB_H + 4),
            label,
            font=font_label,
            fill=MUTED_COLOR,
        )

    y += card_rows * (CARD_THUMB_H + 30) + 10
    y = _draw_separator(draw, y)

    # 故事文字
    y = _draw_wrapped_text(
        draw, y, reading.story, font_body, TEXT_COLOR, CANVAS_WIDTH - PADDING * 2
    )
    y += 10
    y = _draw_separator(draw, y)

    # 命運箴言
    y = _draw_centered_text(
        draw, y, f"「{reading.fortune_quote}」", font_quote, ACCENT_COLOR
    )
    y += 15
    y = _draw_separator(draw, y)

    # Footer
    date_str = datetime.now().strftime("%Y.%m.%d")
    _draw_centered_text(
        draw,
        y,
        f"ArcanaVision · {date_str} · 台大 AI 社 · NTU AI Club · 社團聯展 2026",
        font_footer,
        MUTED_COLOR,
    )

    return canvas.convert("RGB")
