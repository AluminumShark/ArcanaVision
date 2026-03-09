"""應用程式設定，從 .env 讀取環境變數。"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Gemini API
    gemini_api_key: str = ""

    # Exhibition settings
    exhibition_mode: bool = True
    max_concurrent_readings: int = 5
    reading_timeout: int = 30
    enable_story_image: bool = True

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
