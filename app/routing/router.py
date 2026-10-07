import os
import re


def contains_code(text: str) -> bool:
    patterns = [
        r"\bpython\b",
        r"\bjavascript\b",
        r"\btypescript\b",
        r"\bjava\b",
        r"\bbug\b",
        r"\berror\b",
        r"\bdebug\b",
        r"```",
    ]
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def is_complex(text: str) -> bool:
    terms = ["analyze", "compare", "design", "architecture", "trade-off", "reason"]
    return len(text.split()) > 120 or any(term in text.lower() for term in terms)


def select_model(task: str) -> tuple[str, str]:
    if contains_code(task):
        return os.getenv("STRONG_MODEL", "openai/gpt-4.1"), "coding"

    if is_complex(task):
        return os.getenv("STRONG_MODEL", "openai/gpt-4.1"), "complex"

    return os.getenv("FAST_MODEL", "openai/gpt-4o-mini"), "general"