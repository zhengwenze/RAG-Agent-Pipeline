from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    """简单健康检查接口，用于确认服务就绪。"""
    return {"status": "ok"}

