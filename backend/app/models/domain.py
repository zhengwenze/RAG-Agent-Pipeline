from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class DocumentChunk:
    """领域层文档分片对象，用于在服务内部传递。"""

    id: Optional[str]
    text: str
    source: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass
class RetrievalResult:
    """向量检索结果的抽象封装。"""

    score: float
    chunk: DocumentChunk


@dataclass
class AgentThought:
    """Agent 在每一步的思考与行动抽象。"""

    step: int
    description: str
    action: str
    observation: Optional[str] = None

