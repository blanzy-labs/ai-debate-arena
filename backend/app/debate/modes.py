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
            "The Judge should compare promise against risk without declaring certainty."
        ),
    ),
    "builder_vs_breaker": DebateMode(
        slug="builder_vs_breaker",
        display_name="Builder vs Breaker",
        debater_a_role="Builder",
        debater_b_role="Breaker",
        intent="Stress-test implementation versus failure modes.",
        debater_a_guidance=(
            "The Builder should focus on practical execution, sequencing, resources, "
            "and what can be shipped."
        ),
        debater_b_guidance=(
            "The Breaker should look for edge cases, operational failures, dependencies, "
            "hidden costs, and brittle assumptions."
        ),
        judge_guidance=(
            "The Judge should identify what appears buildable, what could break, "
            "and what should be tested first."
        ),
    ),
    "humanist_vs_technologist": DebateMode(
        slug="humanist_vs_technologist",
        display_name="Humanist vs Technologist",
        debater_a_role="Humanist",
        debater_b_role="Technologist",
        intent="Stress-test human impact versus technical capability.",
        debater_a_guidance=(
            "The Humanist should focus on human needs, social effects, ethics, usability, "
            "trust, and lived consequences."
        ),
        debater_b_guidance=(
            "The Technologist should focus on technical feasibility, system design, automation, "
            "scalability, and measurable capability."
        ),
        judge_guidance=(
            "The Judge should compare human impact against technical capability and "
            "identify unresolved tradeoffs."
        ),
    ),
    "security_lead_vs_product_lead": DebateMode(
        slug="security_lead_vs_product_lead",
        display_name="Security Lead vs Product Lead",
        debater_a_role="Security Lead",
        debater_b_role="Product Lead",
        intent="Stress-test risk control versus product delivery.",
        debater_a_guidance=(
            "The Security Lead should focus on threat models, misuse, data exposure, "
            "abuse cases, compliance, and operational risk."
        ),
        debater_b_guidance=(
            "The Product Lead should focus on user value, delivery speed, adoption, "
            "usability, and viable scope."
        ),
        judge_guidance=(
            "The Judge should compare risk control against product momentum and "
            "recommend practical next steps."
        ),
    ),
}


def get_debate_mode(slug: str) -> DebateMode:
    try:
        return DEBATE_MODES[slug]
    except KeyError as error:
        raise UnsupportedProviderError(f"Unsupported debate mode: {slug}.") from error
