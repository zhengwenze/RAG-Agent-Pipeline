from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM / Embedding 相关
    OPENAI_API_KEY: str | None = None
    LLM_PROVIDER: str = "openai"  # 可选：openai / ollama
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OLLAMA_MODEL: str = "qwen2.5-coder:7b"

    # 向量数据库相关
    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: str = "19530"
    VECTOR_DIM: int = 1536

    class Config:
        env_file = ".env"


settings = Settings()
