import json
from typing import Any


def safe_json_loads(data: str) -> Any:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None


def truncate_text(text: str, max_length: int = 4000) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
