from fastapi import APIRouter

from app.config.runtime import get_llm_provider, set_llm_provider
from app.config.settings import settings
from app.models.schemas import LLMConfig


router = APIRouter()


@router.get("/config/llm", response_model=LLMConfig)
async def get_llm_config() -> LLMConfig:
    """获取当前 LLM 配置（供前端展示）。"""
    provider = get_llm_provider().value
    return LLMConfig(
        provider=provider,
        openai_model=settings.OPENAI_MODEL,
        ollama_model=settings.OLLAMA_MODEL,
    )


@router.post("/config/llm", response_model=LLMConfig)
async def set_llm_config(config: LLMConfig) -> LLMConfig:
    """
    切换当前使用的 LLM 提供方。
    - 仅 provider 字段会影响运行时行为，模型名称仍然从 Settings 中读取
    """
    provider = set_llm_provider(config.provider)
    return LLMConfig(
        provider=provider.value,
        openai_model=settings.OPENAI_MODEL,
        ollama_model=settings.OLLAMA_MODEL,
    )

