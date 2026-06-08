import pytest
from fastapi.testclient import TestClient

from app.debate.schemas import DebateResponse
from app import main
from app.llm.errors import MissingProviderKeyError, ProviderCallError


def valid_payload() -> dict:
    return {
        "question": "Should cafes use AI?",
        "debate_mode": "builder_vs_breaker",
        "debater_a_provider": "openai",
        "debater_b_provider": "gemini",
        "judge_provider": "openai",
    }


def route_response() -> DebateResponse:
    return DebateResponse(
        question="Should cafes use AI?",
        debate_mode="builder_vs_breaker",
        debater_a_role="Builder",
        debater_b_role="Breaker",
        debater_a_opening="A opening",
        debater_b_opening="B opening",
        debater_a_rebuttal="A rebuttal",
        debater_b_rebuttal="B rebuttal",
        judge_summary="Summary",
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


def test_debate_run_route_returns_structured_response(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_run_debate(request, settings):
        return route_response()

    monkeypatch.setattr("app.debate.router.run_debate", fake_run_debate)

    response = TestClient(main.app).post("/debate/run", json=valid_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["judge_summary"] == "Summary"
    assert body["models_used"]["debater_b"]["provider"] == "gemini"


def test_debate_run_invalid_request_returns_422() -> None:
    payload = valid_payload()
    payload["question"] = "   "

    response = TestClient(main.app).post("/debate/run", json=payload)

    assert response.status_code == 422


def test_missing_provider_key_maps_to_safe_400(monkeypatch: pytest.MonkeyPatch) -> None:
    secret = "test-openai-key"

    async def fake_run_debate(request, settings):
        raise MissingProviderKeyError("OpenAI API key is not configured.")

    monkeypatch.setattr("app.debate.router.run_debate", fake_run_debate)

    response = TestClient(main.app).post("/debate/run", json=valid_payload())

    assert response.status_code == 400
    assert response.json() == {"detail": "OpenAI API key is not configured."}
    assert secret not in response.text


def test_provider_call_failure_maps_to_safe_502(monkeypatch: pytest.MonkeyPatch) -> None:
    secret = "test-gemini-key"

    async def fake_run_debate(request, settings):
        raise ProviderCallError("Gemini provider call failed.")

    monkeypatch.setattr("app.debate.router.run_debate", fake_run_debate)

    response = TestClient(main.app).post("/debate/run", json=valid_payload())

    assert response.status_code == 502
    assert response.json() == {"detail": "Gemini provider call failed."}
    assert secret not in response.text


def test_health_still_returns_200() -> None:
    response = TestClient(main.app).get("/health")

    assert response.status_code == 200
