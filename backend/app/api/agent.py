from fastapi import APIRouter

from app.models.schemas import AgentRequest, AgentResponse
from app.services.agent.rag_agent import run_agent_task


router = APIRouter()


@router.post("/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest) -> AgentResponse:
    """多步 Agent 接口，接收目标与历史，返回执行步骤与最终回答。"""
    return run_agent_task(request)

