"""
Loads prompt templates from app/prompts/ so prompt copy is decoupled from code
(product/research folks can iterate on wording without touching Python).
"""
from functools import lru_cache
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class PromptManager:
    @staticmethod
    @lru_cache(maxsize=32)
    def load(relative_path: str) -> str:
        """
        relative_path example: 'persona/system.txt'
        """
        path = PROMPTS_DIR / relative_path
        if not path.exists():
            raise FileNotFoundError(f"Prompt template not found: {path}")
        return path.read_text(encoding="utf-8")

    @staticmethod
    def render(relative_path: str, **kwargs) -> str:
        """Loads a template and fills in {placeholders} with kwargs."""
        template = PromptManager.load(relative_path)
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing template variable {e} for prompt '{relative_path}'") from e
