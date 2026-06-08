import pytest

from app.config import Settings
from app.debate.schemas import DebateRequest
from app.debate.service import run_debate
from app.llm.errors import ProviderCallError


class FakeProvider:
    def __init__(
        self,
        provider_name: str,
        model_name: str,
        outputs: list[str],
        calls: list[str],
        label: str,
        error: Exception | None = None,
    ) -> None:
        self.provider_name = provider_name
        self.model_name = model_name
        self._outputs = outputs
        self._calls = calls
        self._label = label
        self._error = error

    async def generate(self, prompt: str) -> str:
        self._calls.append(self._label)
        if self._error:
            raise self._error
        return self._outputs.pop(0)


def make_request() -> DebateRequest:
    return DebateRequest(
        question="Should cafes use AI?",
        debate_mode="builder_vs_breaker",
        debater_a_provider="openai",
        debater_b_provider="gemini",
        judge_provider="openai",
    )


@pytest.mark.asyncio
async def test_debate_provider_call_order_and_response_fields() -> None:
    calls: list[str] = []
    providers = {
        "a": FakeProvider("openai", "model-a", ["A opening", "A rebuttal"], calls, "debater_a"),
        "b": FakeProvider("gemini", "model-b", ["B opening", "B rebuttal"], calls, "debater_b"),
        "judge": FakeProvider(
            "openai",
            "judge-model",
            [
                """
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
            ],
            calls,
            "judge",
        ),
    }

    openai_requests = 0

    def factory(provider_name: str, settings: Settings) -> FakeProvider:
        nonlocal openai_requests
        if provider_name == "gemini":
            return providers["b"]
        openai_requests += 1
        return providers["a"] if openai_requests == 1 else providers["judge"]

    response = await run_debate(make_request(), Settings(), provider_factory=factory)

    assert calls == ["debater_a", "debater_b", "debater_a", "debater_b", "judge"]
    assert response.debater_a_opening == "A opening"
    assert response.debater_b_rebuttal == "B rebuttal"
    assert response.judge_summary == "Summary"
    assert response.models_used.debater_a.model == "model-a"
    assert response.models_used.debater_b.provider == "gemini"
    assert response.models_used.judge.model == "judge-model"


@pytest.mark.asyncio
async def test_invalid_judge_json_returns_safe_structured_response() -> None:
    calls: list[str] = []
    providers = {
        "openai": FakeProvider("openai", "model-a", ["A opening", "A rebuttal"], calls, "debater_a"),
        "gemini": FakeProvider("gemini", "model-b", ["B opening", "B rebuttal"], calls, "debater_b"),
        "judge": FakeProvider("openai", "judge-model", ["not json"], calls, "judge"),
    }
    openai_requests = 0

    def factory(provider_name: str, settings: Settings) -> FakeProvider:
        nonlocal openai_requests
        if provider_name == "gemini":
            return providers["gemini"]
        openai_requests += 1
        return providers["openai"] if openai_requests == 1 else providers["judge"]

    response = await run_debate(make_request(), Settings(), provider_factory=factory)

    assert response.judge_summary.startswith("The judge response could not be parsed")
    assert response.unresolved_questions == ["Judge output was not valid JSON."]


@pytest.mark.asyncio
async def test_provider_failures_raise_safe_errors() -> None:
    secret = "test-openai-key"
    calls: list[str] = []
    failing_provider = FakeProvider(
        "openai",
        "model-a",
        [],
        calls,
        "debater_a",
        error=ProviderCallError("OpenAI provider call failed."),
    )

    def factory(provider_name: str, settings: Settings) -> FakeProvider:
        return failing_provider

    with pytest.raises(ProviderCallError) as raised:
        await run_debate(make_request(), Settings(openai_api_key=secret), provider_factory=factory)

    assert str(raised.value) == "OpenAI provider call failed."
    assert secret not in str(raised.value)
