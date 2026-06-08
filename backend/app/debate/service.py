from collections.abc import Callable

from app.config import Settings
from app.debate.judge_parser import parse_judge_response
from app.debate.modes import get_debate_mode
from app.debate.prompts import build_judge_prompt, build_opening_prompt, build_rebuttal_prompt
from app.debate.schemas import DebateRequest, DebateResponse, ModelUsed, ModelsUsed
from app.llm.base import LLMProvider
from app.llm.factory import get_provider

ProviderFactory = Callable[[str, Settings], LLMProvider]


async def run_debate(
    request: DebateRequest,
    settings: Settings,
    provider_factory: ProviderFactory = get_provider,
) -> DebateResponse:
    mode = get_debate_mode(request.debate_mode)

    debater_a = provider_factory(request.debater_a_provider, settings)
    debater_b = provider_factory(request.debater_b_provider, settings)
    judge = provider_factory(request.judge_provider, settings)

    debater_a_opening = await debater_a.generate(
        build_opening_prompt(request.question, mode, side="a")
    )
    debater_b_opening = await debater_b.generate(
        build_opening_prompt(request.question, mode, side="b")
    )
    debater_a_rebuttal = await debater_a.generate(
        build_rebuttal_prompt(
            request.question,
            mode,
            side="a",
            debater_a_opening=debater_a_opening,
            debater_b_opening=debater_b_opening,
        )
    )
    debater_b_rebuttal = await debater_b.generate(
        build_rebuttal_prompt(
            request.question,
            mode,
            side="b",
            debater_a_opening=debater_a_opening,
            debater_b_opening=debater_b_opening,
            debater_a_rebuttal=debater_a_rebuttal,
        )
    )
    raw_judge_response = await judge.generate(
        build_judge_prompt(
            request.question,
            mode,
            debater_a_opening,
            debater_b_opening,
            debater_a_rebuttal,
            debater_b_rebuttal,
        )
    )
    judge_fields = parse_judge_response(raw_judge_response)

    return DebateResponse(
        question=request.question,
        debate_mode=request.debate_mode,
        debater_a_role=mode.debater_a_role,
        debater_b_role=mode.debater_b_role,
        debater_a_opening=debater_a_opening,
        debater_b_opening=debater_b_opening,
        debater_a_rebuttal=debater_a_rebuttal,
        debater_b_rebuttal=debater_b_rebuttal,
        models_used=ModelsUsed(
            debater_a=ModelUsed(provider=debater_a.provider_name, model=debater_a.model_name),
            debater_b=ModelUsed(provider=debater_b.provider_name, model=debater_b.model_name),
            judge=ModelUsed(provider=judge.provider_name, model=judge.model_name),
        ),
        **judge_fields,
    )
