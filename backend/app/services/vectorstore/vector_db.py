from typing import Any, List, Optional

from pymilvus import Collection, connections

from app.config.settings import settings


_collection: Optional[Collection] = None


def _get_collection() -> Collection:
    """
    延迟获取 Milvus Collection，避免在服务启动时因为 Milvus 未就绪而直接崩溃。

    如果连接失败，会抛出 RuntimeError，由上层捕获并返回友好的错误信息。
    """
    global _collection
    if _collection is not None:
        return _collection

    try:
        connections.connect("default", host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)
        # NOTE: 按手册假定已在 Milvus 中创建名为 'documents' 的集合，
        # 并包含用于向量检索的 'embedding' 字段以及元数据字段。
        _collection = Collection("documents")
        return _collection
    except Exception as exc:  # pragma: no cover - 主要是运行时环境相关问题
        raise RuntimeError(
            f"无法连接 Milvus（{settings.MILVUS_HOST}:{settings.MILVUS_PORT}）：{exc}"
        ) from exc


def insert_vectors(vectors: List[List[float]], metadatas: List[dict[str, Any]]) -> None:
    """Insert vectors and their metadatas into the collection."""
    collection = _get_collection()
    # 这里严格按照手册示例，直接插入 [vectors, metadatas]。
    collection.insert([vectors, metadatas])


def search(query_vector: List[float], top_k: int = 5):
    """Search similar vectors from the collection."""
    collection = _get_collection()
    return collection.search(query_vector, "embedding", limit=top_k)

