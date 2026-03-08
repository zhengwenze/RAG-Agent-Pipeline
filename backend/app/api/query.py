from fastapi import APIRouter

from app.services.agent.rag_agent import answer_query


router = APIRouter()


@router.get("/query")
async def query(q: str):
    answer = answer_query(q)
    return {"answer": answer}

