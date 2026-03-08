from enum import Enum

from app.config.settings import Settings, settings


class LLMProvider(str, Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"


def _initial_provider_from_settings(cfg: Settings) -> LLMProvider:
    value = (cfg.LLM_PROVIDER or "openai").lower()
    if value == "ollama":
        return LLMProvider.OLLAMA
    return LLMProvider.OPENAI


_current_llm_provider: LLMProvider = _initial_provider_from_settings(settings)


def get_llm_provider() -> LLMProvider:
    return _current_llm_provider


def set_llm_provider(provider: str) -> LLMProvider:
    global _current_llm_provider
    value = provider.lower()
    if value == "ollama":
        _current_llm_provider = LLMProvider.OLLAMA
    elif value == "openai":
        _current_llm_provider = LLMProvider.OPENAI
    # 如果传入非法值，则保持当前不变
    return _current_llm_provider

