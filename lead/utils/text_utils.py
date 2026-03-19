from __future__ import annotations


def truncate(text: str, max_len: int = 160) -> str:
    text = text.strip().replace("
", " ")
    return text if len(text) <= max_len else text[: max_len - 3] + "..."
