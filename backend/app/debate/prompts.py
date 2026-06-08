from app.debate.modes import DebateMode


SAFETY_AND_LIMITATIONS = """Safety and limitations:
- Avoid fake citations: do not invent citations, sources, studies, statistics, or external facts.
- Do not claim you browsed the web, checked live sources, did research, or verified current facts unless those sources are explicitly provided in this prompt.
- Frame conclusions as debate arguments, assumptions, and tradeoffs rather than guaranteed truth.
- Acknowledge uncertainty where the available information is incomplete.
- Avoid giving instructions that would enable harm, fraud, credential theft, privacy invasion, or other unsafe behavior."""


def build_opening_prompt(question: str, mode: DebateMode, side: str) -> str:
    role = mode.debater_a_role if side == "a" else mode.debater_b_role
    guidance = mode.debater_a_guidance if side == "a" else mode.debater_b_guidance

    return f"""You are participating in Mythadis AI Debate Arena, a structured debate tool for stress-testing disagreement. This is not a final answer engine.

Question: {question}
Debate mode: {mode.display_name}
Mode intent: {mode.intent}
Your role: {role}
Role guidance: {guidance}

Task:
Make the strongest useful opening argument from your assigned role while staying focused on the question. State your assumptions clearly. Avoid declaring absolute truth.

{SAFETY_AND_LIMITATIONS}

Use this concise structure:
Position:
Key Arguments:
Assumptions:
Risks or Caveats:
What Would Change My View:"""


def build_rebuttal_prompt(
    question: str,
    mode: DebateMode,
    side: str,
    debater_a_opening: str,
    debater_b_opening: str,
    debater_a_rebuttal: str | None = None,
) -> str:
    role = mode.debater_a_role if side == "a" else mode.debater_b_role
    opposing_role = mode.debater_b_role if side == "a" else mode.debater_a_role
    guidance = mode.debater_a_guidance if side == "a" else mode.debater_b_guidance

    prior_rebuttal = ""
    if debater_a_rebuttal:
        prior_rebuttal = f"\nDebater A rebuttal:\n{debater_a_rebuttal}\n"

    return f"""You are participating in Mythadis AI Debate Arena, a structured debate tool for stress-testing disagreement. This is not a final answer engine.

Question: {question}
Debate mode: {mode.display_name}
Mode intent: {mode.intent}
Your role: {role}
Opposing role: {opposing_role}
Role guidance: {guidance}

Debater A opening:
{debater_a_opening}

Debater B opening:
{debater_b_opening}
{prior_rebuttal}
Task:
Write a direct rebuttal. Address the opposing argument, identify the strongest opposing point, acknowledge valid opposing points, challenge assumptions, and do not merely repeat your opening argument.

{SAFETY_AND_LIMITATIONS}

Use this concise structure:
Strongest Opposing Point:
Response:
Assumptions Challenged:
Valid Points Acknowledged:
Revised Position:"""


def build_judge_prompt(
    question: str,
    mode: DebateMode,
    debater_a_opening: str,
    debater_b_opening: str,
    debater_a_rebuttal: str,
    debater_b_rebuttal: str,
) -> str:
    return f"""Question: {question}
Debate mode: {mode.display_name}
Mode intent: {mode.intent}
Debater A role: {mode.debater_a_role}
Debater A guidance: {mode.debater_a_guidance}
Debater B role: {mode.debater_b_role}
Debater B guidance: {mode.debater_b_guidance}
Judge guidance: {mode.judge_guidance}

Debater A opening:
{debater_a_opening}

Debater B opening:
{debater_b_opening}

Debater A rebuttal:
{debater_a_rebuttal}

Debater B rebuttal:
{debater_b_rebuttal}

Return JSON only. Do not wrap JSON in Markdown fences.
Compare argument quality rather than picking a team theatrically. Do not declare absolute truth.
Identify assumptions, uncertainties, weak assumptions, unresolved issues, useful next steps, and follow-up debates.

{SAFETY_AND_LIMITATIONS}

Use this exact JSON contract:
{{
  "judge_summary": "string",
  "strongest_argument_a": "string",
  "strongest_argument_b": "string",
  "weakest_assumption_a": "string",
  "weakest_assumption_b": "string",
  "unresolved_questions": ["string"],
  "recommended_next_steps": ["string"],
  "suggested_follow_up_debates": ["string"]
}}"""
