from dataclasses import dataclass

from app.llm.errors import UnsupportedProviderError


@dataclass(frozen=True)
class DebateMode:
    slug: str
    display_name: str
    debater_a_role: str
    debater_b_role: str
    intent: str
    debater_a_guidance: str
    debater_b_guidance: str
    judge_guidance: str


DEBATE_MODES: dict[str, DebateMode] = {
    "optimist_vs_skeptic": DebateMode(
        slug="optimist_vs_skeptic",
        display_name="Optimist vs Skeptic",
        debater_a_role="Optimist",
        debater_b_role="Skeptic",
        intent="Stress-test promise versus risk.",
        debater_a_guidance=(
            "The Optimist should argue the strongest positive case, identify upside, "
            "and explain what would make the idea worth pursuing."
        ),
        debater_b_guidance=(
            "The Skeptic should challenge assumptions, expose weak spots, and identify "
            "what could make the idea fail."
        ),
        judge_guidance=(
            "Compare the promise and risk arguments without declaring absolute truth."
        ),
    ),
    "builder_vs_breaker": DebateMode(
        slug="builder_vs_breaker",
        display_name="Builder vs Breaker",
        debater_a_role="Builder",
        debater_b_role="Breaker",
        intent="Stress-test implementation versus failure modes.",
        debater_a_guidance=(
            "The Builder should make the strongest implementation case, explain how it "
            "could work, and name practical requirements."
        ),
        debater_b_guidance=(
            "The Breaker should find failure modes, operational risks, and assumptions "
            "that could collapse under pressure."
        ),
        judge_guidance=(
            "Compare implementation strength against failure modes without declaring absolute truth."
        ),
    ),
    "humanist_vs_technologist": DebateMode(
        slug="humanist_vs_technologist",
        display_name="Humanist vs Technologist",
        debater_a_role="Humanist",
        debater_b_role="Technologist",
        intent="Stress-test human impact versus technical capability.",
        debater_a_guidance=(
            "The Humanist should focus on people, incentives, dignity, access, and social impact."
        ),
        debater_b_guidance=(
            "The Technologist should focus on capabilities, technical constraints, systems, "
            "and what the technology can reliably do."
        ),
        judge_guidance=(
            "Compare human impact and technical capability without declaring absolute truth."
        ),
    ),
    "security_lead_vs_product_lead": DebateMode(
        slug="security_lead_vs_product_lead",
        display_name="Security Lead vs Product Lead",
        debater_a_role="Security Lead",
        debater_b_role="Product Lead",
        intent="Stress-test risk control versus product delivery.",
        debater_a_guidance=(
            "The Security Lead should identify risk, misuse, governance needs, and controls."
        ),
        debater_b_guidance=(
            "The Product Lead should identify user value, delivery constraints, adoption, "
            "and practical tradeoffs."
        ),
        judge_guidance=(
            "Compare risk controls and product delivery tradeoffs without declaring absolute truth."
        ),
    ),
}


def get_debate_mode(slug: str) -> DebateMode:
    try:
        return DEBATE_MODES[slug]
    except KeyError as error:
        raise UnsupportedProviderError(f"Unsupported debate mode: {slug}.") from error
