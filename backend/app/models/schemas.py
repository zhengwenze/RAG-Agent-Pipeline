from typing import List, Literal, Optional

from pydantic import BaseModel


class Message(BaseModel):
    """对话消息模型，可用于多轮 Agent 任务。"""

    role: Literal["user", "assistant", "system"]
    content: str


class UploadResponse(BaseModel):
    status: str
    chunks: int


class QueryResponse(BaseModel):
    answer: str


class AgentStep(BaseModel):
    step: int
    thought: str
    action: str
    observation: Optional[str] = None


class AgentRequest(BaseModel):
    """多步 Agent 请求体。"""

    goal: str
    history: List[Message] = []
    max_steps: int = 3


class AgentResponse(BaseModel):
    """多步 Agent 返回体。"""

    goal: str
    steps: List[AgentStep]
    final_answer: str


class LLMConfig(BaseModel):
    """前端用于展示/切换当前 LLM 提供方的配置。"""

    provider: Literal["openai", "ollama"]
    openai_model: str
    ollama_model: str

