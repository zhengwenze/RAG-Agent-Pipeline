from typing import Literal

import ollama
from openai import OpenAI

from app.config.runtime import get_llm_provider
from app.config.settings import settings


Provider = Literal["openai", "ollama"]


def _get_provider() -> Provider:
    provider = get_llm_provider().value
    if provider not in ("openai", "ollama"):
        return "openai"
    return provider  # type: ignore[return-value]


def _get_openai_client() -> OpenAI:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY 未配置，但当前 LLM_PROVIDER 为 openai")
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_text(prompt: str, max_tokens: int = 300) -> str:
    """
    根据配置的 LLM_PROVIDER 调用不同后端生成文本。

    - openai: 使用 OpenAI Completion 接口（保持与项目手册一致）
    - ollama: 调用本地 Ollama 服务（默认地址 http://127.0.0.1:11434）
    """
    provider = _get_provider()

    if provider == "ollama":
        # 使用 Ollama 本地模型
        response = ollama.generate(
            model=settings.OLLAMA_MODEL,
            prompt=prompt,
            stream=False,
        )
        # 官方返回结构中 'response' 为完整文本
        return response.get("response", "")

    # 默认使用 OpenAI，与手册保持一致
    client = _get_openai_client()
    completion = client.completions.create(
        model=settings.OPENAI_MODEL,
        prompt=prompt,
        max_tokens=max_tokens,
    )
    return completion.choices[0].text

