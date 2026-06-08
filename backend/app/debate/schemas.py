from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


ProviderName = Literal["openai", "gemini"]
DebateModeSlug = Literal[
    "optimist_vs_skeptic",
    "builder_vs_breaker",
    "humanist_vs_technologist",
    "security_lead_vs_product_lead",
]


class DebateRequest(BaseModel):
    question: str = Field(min_length=1)
    debate_mode: DebateModeSlug
    debater_a_provider: ProviderName
    debater_b_provider: ProviderName
    judge_provider: ProviderName

    @field_validator("question")
    @classmethod
    def trim_question(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Question must not be empty.")
        return trimmed


class ModelUsed(BaseModel):
    provider: ProviderName
    model: str


class ModelsUsed(BaseModel):
    debater_a: ModelUsed
    debater_b: ModelUsed
    judge: ModelUsed


class DebateResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    question: str
    debate_mode: DebateModeSlug
    debater_a_role: str
    debater_b_role: str
    debater_a_opening: str
    debater_b_opening: str
    debater_a_rebuttal: str
    debater_b_rebuttal: str
    judge_summary: str
    strongest_argument_a: str
    strongest_argument_b: str
    weakest_assumption_a: str
    weakest_assumption_b: str
    unresolved_questions: list[str]
    recommended_next_steps: list[str]
    suggested_follow_up_debates: list[str]
    models_used: ModelsUsed
