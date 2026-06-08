from app.debate.modes import get_debate_mode
from app.debate.prompts import build_judge_prompt, build_opening_prompt, build_rebuttal_prompt


def test_opening_prompt_includes_question_role_and_mode_context() -> None:
    mode = get_debate_mode("builder_vs_breaker")

    prompt = build_opening_prompt("Should cafes use AI?", mode, side="a")

    assert "Should cafes use AI?" in prompt
    assert "Builder vs Breaker" in prompt
    assert "Stress-test implementation versus failure modes." in prompt
    assert "Builder" in prompt
    assert mode.debater_a_guidance in prompt
    assert "avoid fake citations" in prompt.lower()
    assert "Do not claim you browsed the web" in prompt
    assert "verified current facts" in prompt
    assert "Assumptions:" in prompt
    assert "Acknowledge uncertainty" in prompt
    assert "JSON" not in prompt


def test_rebuttal_prompt_includes_opposing_opening() -> None:
    mode = get_debate_mode("builder_vs_breaker")

    prompt = build_rebuttal_prompt(
        "Should cafes use AI?",
        mode,
        side="a",
        debater_a_opening="A opening",
        debater_b_opening="B opposing opening",
    )

    assert "Should cafes use AI?" in prompt
    assert "Builder" in prompt
    assert "A opening" in prompt
    assert "B opposing opening" in prompt
    assert "direct rebuttal" in prompt
    assert "acknowledge valid opposing points" in prompt
    assert "do not merely repeat your opening argument" in prompt
    assert "Avoid fake citations" in prompt
    assert "Do not claim you browsed the web" in prompt
    assert "Strongest Opposing Point:" in prompt
    assert "JSON" not in prompt


def test_rebuttal_prompt_for_debater_b_includes_debater_a_rebuttal() -> None:
    mode = get_debate_mode("builder_vs_breaker")

    prompt = build_rebuttal_prompt(
        "Should cafes use AI?",
        mode,
        side="b",
        debater_a_opening="A opening",
        debater_b_opening="B opening",
        debater_a_rebuttal="A rebuttal",
    )

    assert "A rebuttal" in prompt
    assert "Breaker" in prompt


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

    assert "Should cafes use AI?" in prompt
    assert "A opening" in prompt
    assert "B opening" in prompt
    assert "A rebuttal" in prompt
    assert "B rebuttal" in prompt
    assert mode.judge_guidance in prompt
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
    assert "Do not wrap JSON in Markdown fences" in prompt
    assert "Do not declare absolute truth" in prompt
    assert "Compare argument quality" in prompt
    assert "Avoid fake citations" in prompt
    assert "Do not claim you browsed the web" in prompt
