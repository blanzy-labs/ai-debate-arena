import pytest

from app.debate.modes import DEBATE_MODES, get_debate_mode
from app.llm.errors import UnsupportedProviderError


EXPECTED_MODES = {
    "optimist_vs_skeptic",
    "builder_vs_breaker",
    "humanist_vs_technologist",
    "security_lead_vs_product_lead",
}


def test_all_v1_modes_exist_with_required_fields() -> None:
    assert set(DEBATE_MODES) == EXPECTED_MODES

    for mode in DEBATE_MODES.values():
        assert mode.slug
        assert mode.display_name
        assert mode.intent
        assert mode.debater_a_role
        assert mode.debater_b_role
        assert mode.judge_guidance
        assert mode.debater_a_guidance
        assert mode.debater_b_guidance


def test_unknown_mode_fails_safely() -> None:
    with pytest.raises(UnsupportedProviderError, match="Unsupported debate mode"):
        get_debate_mode("unknown")
