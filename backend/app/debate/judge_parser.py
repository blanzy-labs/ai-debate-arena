import json
import re
from typing import Any


JUDGE_STRING_FIELDS = [
    "judge_summary",
    "strongest_argument_a",
    "strongest_argument_b",
    "weakest_assumption_a",
    "weakest_assumption_b",
]

JUDGE_LIST_FIELDS = [
    "unresolved_questions",
    "recommended_next_steps",
    "suggested_follow_up_debates",
]

FALLBACK_JUDGE_RESULT = {
    "judge_summary": (
        "The judge response could not be parsed as structured JSON. "
        "Review the debate transcript manually."
    ),
    "strongest_argument_a": "",
    "strongest_argument_b": "",
    "weakest_assumption_a": "",
    "weakest_assumption_b": "",
    "unresolved_questions": ["Judge output was not valid JSON."],
    "recommended_next_steps": ["Rerun the debate or revise the judge prompt."],
    "suggested_follow_up_debates": [],
}


def parse_judge_response(raw_response: str) -> dict[str, str | list[str]]:
    cleaned_response = _strip_markdown_fence(raw_response.strip())
    if not cleaned_response:
        return FALLBACK_JUDGE_RESULT.copy()

    try:
        parsed = json.loads(cleaned_response)
    except json.JSONDecodeError:
        return FALLBACK_JUDGE_RESULT.copy()

    if not isinstance(parsed, dict):
        return FALLBACK_JUDGE_RESULT.copy()

    result: dict[str, str | list[str]] = {}
    for field in JUDGE_STRING_FIELDS:
        value = parsed.get(field)
        result[field] = value.strip() if isinstance(value, str) else ""

    for field in JUDGE_LIST_FIELDS:
        result[field] = _coerce_string_list(parsed.get(field))

    return result


def _strip_markdown_fence(value: str) -> str:
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", value, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return value


def _coerce_string_list(value: Any) -> list[str]:
    if isinstance(value, str):
        trimmed = value.strip()
        return [trimmed] if trimmed else []

    if isinstance(value, list):
        return [item.strip() for item in value if isinstance(item, str) and item.strip()]

    return []
