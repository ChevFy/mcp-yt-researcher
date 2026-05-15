import os

from dotenv import load_dotenv


def load_environment() -> None:
    load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is not set")
    return value


def load_youtube_api_key() -> str:
    return _require_env("YOUTUBE_API_KEY")


def load_gemini_api_key() -> str:
    return _require_env("GEMINI_API_KEY")
