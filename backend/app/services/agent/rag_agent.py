from typing import Any, List

from app.models.schemas import AgentRequest, AgentResponse, AgentStep
from app.services.embedding.embeddings import embed_text
from app.services.llm.llm_client import generate_text
from app.services.prompts.prompt_engine import format_prompt
from app.services.vectorstore.vector_db import search
from app.utils.text_utils import merge_texts, truncate_text


def answer_query(query: str) -> str:
    """RAG 问答主流程：query -> 检索 -> 拼接上下文 -> 调用 LLM。"""
    vec: List[float] = embed_text(query)
    results: Any = search(vec, top_k=5)

    # 按手册示例，从检索结果的 metadata 中取出 text 字段。
    context_parts: list[str] = []
    for r in results:
        # 不对 schema 做过多假设，宽松访问 metadata
        metadata = getattr(r, "metadata", None) or getattr(r, "entity", None) or {}
        text = metadata.get("text") if isinstance(metadata, dict) else None
        if text:
            context_parts.append(text)

    context = merge_texts(context_parts)
    prompt = format_prompt(context=context, question=query)

    # 通过统一的 LLM 客户端调用具体模型（OpenAI 或 Ollama）
    return generate_text(prompt, max_tokens=300)


def _plan_subtasks(goal: str, max_steps: int) -> list[str]:
    """使用 LLM 规划子任务列表。"""
    planning_prompt = (
        "你是一个任务规划助手，请根据用户的最终目标，将任务拆分为 1-N 个可以依次完成的子任务，"
        "每行一个子任务，越具体越好，不要输出多余解释。\n\n"
        f"用户目标：{goal}\n\n子任务列表："
    )
    text = generate_text(planning_prompt, max_tokens=300).strip()
    subtasks: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # 去掉前缀编号（如 1. / 1、 等）
        while line and (line[0].isdigit() or line[0] in ("-", "•")):
            # 找到第一个空格或句点之后
            if "." in line:
                _, line = line.split(".", 1)
            elif "、" in line:
                _, line = line.split("、", 1)
            else:
                line = line[1:]
            line = line.strip()
        if line:
            subtasks.append(line)
        if len(subtasks) >= max_steps:
            break
    return subtasks


def run_agent_task(request: AgentRequest) -> AgentResponse:
    """
    多步 Agent 流程：
    1. 基于用户 goal 规划子任务
    2. 针对每个子任务调用 RAG 问答获取观察结果
    3. 汇总所有观察结果，生成最终回答
    """
    subtasks = _plan_subtasks(request.goal, request.max_steps)
    steps: list[AgentStep] = []
    observations: list[str] = []

    for idx, sub in enumerate(subtasks, start=1):
        thought = f"为了完成总体目标，当前执行的子任务是：{sub}"
        action = f"调用 RAG 问答来解决子任务：{sub}"
        try:
            observation = answer_query(sub)
        except Exception as exc:  # 避免整个 Agent 崩溃
            observation = f"执行子任务时发生错误：{exc}"
        observations.append(f"子任务 {idx}: {sub}\n结果: {observation}")
        steps.append(
            AgentStep(
                step=idx,
                thought=thought,
                action=action,
                observation=observation,
            )
        )

    # 将所有观察结果截断后交给 LLM 生成最终总结回答
    combined_obs = truncate_text(merge_texts(observations), max_len=4000)
    final_prompt = (
        "你是一个善于总结的智能助手。\n"
        "下面是为完成用户目标而执行的一系列子任务及其结果，请综合这些信息，"
        "用清晰、有条理的方式给出对用户目标的最终回答。\n\n"
        f"用户目标：{request.goal}\n\n"
        f"子任务及结果：\n{combined_obs}\n\n"
        "请给出对用户的最终回答："
    )
    final_answer = generate_text(final_prompt, max_tokens=500)

    return AgentResponse(goal=request.goal, steps=steps, final_answer=final_answer)

