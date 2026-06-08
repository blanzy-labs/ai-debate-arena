import pytest
from pydantic import ValidationError

from app.debate.schemas import DebateRequest, DebateResponse


def test_valid_debate_request_passes_and_trims_question() -> None:
    request = DebateRequest(
        question="  Should small businesses use AI agents?  ",
        debate_mode="builder_vs_breaker",
        debater_a_provider="openai",
        debater_b_provider="gemini",
        judge_provider="openai",
    )

    assert request.question == "Should small businesses use AI agents?"


@pytest.mark.parametrize("question", ["", "   "])
def test_empty_question_fails(question: str) -> None:
    with pytest.raises(ValidationError):
        DebateRequest(
            question=question,
            debate_mode="builder_vs_breaker",
            debater_a_provider="openai",
            debater_b_provider="gemini",
            judge_provider="openai",
        )


def test_invalid_provider_fails() -> None:
    with pytest.raises(ValidationError):
        DebateRequest(
            question="Should we use AI agents?",
            debate_mode="builder_vs_breaker",
            debater_a_provider="anthropic",
            debater_b_provider="gemini",
            judge_provider="openai",
        )


def test_invalid_debate_mode_fails() -> None:
    with pytest.raises(ValidationError):
        DebateRequest(
            question="Should we use AI agents?",
            debate_mode="unknown",
            debater_a_provider="openai",
            debater_b_provider="gemini",
            judge_provider="openai",
        )


def test_response_schema_accepts_required_fields() -> None:
    response = DebateResponse(
        question="Should we use AI agents?",
        debate_mode="builder_vs_breaker",
        debater_a_role="Builder",
        debater_b_role="Breaker",
        debater_a_opening="A opening",
        debater_b_opening="B opening",
        debater_a_rebuttal="A rebuttal",
        debater_b_rebuttal="B rebuttal",
        judge_summary="Balanced summary",
        strongest_argument_a="A strong",
        strongest_argument_b="B strong",
        weakest_assumption_a="A weak",
        weakest_assumption_b="B weak",
        unresolved_questions=["Question"],
        recommended_next_steps=["Step"],
        suggested_follow_up_debates=["Follow-up"],
        models_used={
            "debater_a": {"provider": "openai", "model": "gpt-4.1-mini"},
            "debater_b": {"provider": "gemini", "model": "gemini-2.5-flash"},
            "judge": {"provider": "openai", "model": "gpt-4.1-mini"},
        },
    )

    assert response.judge_summary == "Balanced summary"
    assert response.models_used.debater_b.provider == "gemini"
