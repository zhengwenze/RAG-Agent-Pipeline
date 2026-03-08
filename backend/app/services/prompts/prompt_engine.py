QA_TEMPLATE = """
你是一个知识问答助手。
根据文档上下文回答问题：
{context}
用户问题：{question}
回答：
"""


def format_prompt(context: str, question: str) -> str:
    return QA_TEMPLATE.format(context=context, question=question)

