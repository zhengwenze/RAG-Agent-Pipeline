from typing import List

import ollama

from app.config.settings import settings


def embed_text(text: str) -> List[float]:
    """
    使用 Ollama 本地模型生成单条文本的向量。

    注意：Milvus 中 `documents` 集合的向量维度必须与该模型返回的维度一致，
    请根据实际模型返回的 embedding 长度来配置/创建集合。
    """
    response = ollama.embeddings(model=settings.OLLAMA_MODEL, prompt=text)
    return response.get("embedding", [])


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """Embed a list of text chunks into vectors via Ollama embeddings."""
    return [embed_text(c) for c in chunks]

