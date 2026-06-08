from app.debate.modes import get_debate_mode
from app.debate.prompts import build_judge_prompt, build_opening_prompt, build_rebuttal_prompt


def test_opening_prompt_includes_question_role_and_mode_context() -> None:
    mode = get_debate_mode("builder_vs_breaker")

    prompt = build_opening_prompt("Should cafes use AI?", mode, side="a")

    assert "Should cafes use AI?" in prompt
    assert "Builder" in prompt
    assert "Builder vs Breaker" in prompt
    assert "avoid fake citations" in prompt


def test_rebuttal_prompt_includes_opposing_opening() -> None:
    mode = get_debate_mode("builder_vs_breaker")

    prompt = build_rebuttal_prompt(
        "Should cafes use AI?",
        mode,
        side="a",
        debater_a_opening="A opening",
        debater_b_opening="B opposing opening",
    )

    assert "B opposing opening" in prompt
    assert "Respond directly" in prompt
    assert "Avoid fake citations" in prompt


def test_judge_prompt_includes_required_json_keys_and_json_only_instruction() -> None:
    mode = get_debate_mode("builder_vs_breaker")

    prompt = build_judge_prompt(
        "Should cafes use AI?",
        mode,
        "A opening",
        "B opening",
        "A rebuttal",
        "B rebuttal",
    )

    for key in [
        "judge_summary",
        "strongest_argument_a",
        "strongest_argument_b",
        "weakest_assumption_a",
        "weakest_assumption_b",
        "unresolved_questions",
        "recommended_next_steps",
        "suggested_follow_up_debates",
    ]:
        assert key in prompt

    assert "Return JSON only" in prompt
    assert "Do not declare absolute truth" in prompt
    assert "Avoid fake citations" in prompt
