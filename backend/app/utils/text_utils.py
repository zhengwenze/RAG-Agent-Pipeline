from typing import Iterable, List


def normalize_whitespace(text: str) -> str:
    """简单归一化空白字符，去掉多余换行与空格。"""
    return " ".join(text.split())


def merge_texts(texts: Iterable[str]) -> str:
    """将多个文本片段合并为单一上下文字符串。"""
    return "\n\n".join(t for t in texts if t)


def truncate_text(text: str, max_len: int) -> str:
    """按字符长度简单截断文本，以避免 prompt 过长。"""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."

