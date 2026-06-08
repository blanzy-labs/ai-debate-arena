from app.debate.judge_parser import FALLBACK_JUDGE_RESULT, parse_judge_response


VALID_JSON = """
{
  "judge_summary": "Summary",
  "strongest_argument_a": "A strong",
  "strongest_argument_b": "B strong",
  "weakest_assumption_a": "A weak",
  "weakest_assumption_b": "B weak",
  "unresolved_questions": ["Question"],
  "recommended_next_steps": ["Step"],
  "suggested_follow_up_debates": ["Follow-up"]
}
"""


def test_clean_valid_json_parses() -> None:
    result = parse_judge_response(VALID_JSON)

    assert result["judge_summary"] == "Summary"
    assert result["unresolved_questions"] == ["Question"]


def test_whitespace_wrapped_json_parses() -> None:
    result = parse_judge_response(f"  {VALID_JSON}  ")

    assert result["strongest_argument_a"] == "A strong"


def test_markdown_fenced_json_parses() -> None:
    result = parse_judge_response(f"```json\n{VALID_JSON}\n```")

    assert result["recommended_next_steps"] == ["Step"]


def test_missing_fields_are_filled_safely() -> None:
    result = parse_judge_response('{"judge_summary": "Summary", "unresolved_questions": "One"}')

    assert result["judge_summary"] == "Summary"
    assert result["strongest_argument_a"] == ""
    assert result["unresolved_questions"] == ["One"]
    assert result["recommended_next_steps"] == []


def test_invalid_json_returns_fallback() -> None:
    assert parse_judge_response("not json") == FALLBACK_JUDGE_RESULT


def test_empty_string_returns_fallback() -> None:
    assert parse_judge_response("") == FALLBACK_JUDGE_RESULT


def test_json_array_returns_fallback() -> None:
    assert parse_judge_response('["not", "object"]') == FALLBACK_JUDGE_RESULT


def test_null_values_do_not_crash() -> None:
    result = parse_judge_response(
        '{"judge_summary": null, "unresolved_questions": null, "recommended_next_steps": [null, "Step"]}'
    )

    assert result["judge_summary"] == ""
    assert result["unresolved_questions"] == []
    assert result["recommended_next_steps"] == ["Step"]
