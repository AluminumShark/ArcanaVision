"""解讀結果資料模型。"""

from pydantic import BaseModel


class ReadingResult(BaseModel):
    """LLM 生成的塔羅解讀結果。"""

    story: str  # 300-500 字中文故事解讀
    fortune_quote: str  # 一句命運箴言
    scene_prompt: str  # 英文場景描述（50-80 words），用於故事圖生成
    mood: str  # 整體氛圍關鍵字（如 mysterious, hopeful, turbulent）
