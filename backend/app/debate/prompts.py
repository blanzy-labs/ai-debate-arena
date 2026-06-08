from app.debate.modes import DebateMode


def build_opening_prompt(question: str, mode: DebateMode, side: str) -> str:
    role = mode.debater_a_role if side == "a" else mode.debater_b_role
    guidance = mode.debater_a_guidance if side == "a" else mode.debater_b_guidance

    return f"""Question: {question}
Debate mode: {mode.display_name}
Mode intent: {mode.intent}
Your role: {role}
Role guidance: {guidance}

Write your opening argument.
Stay in role, make a clear argument, state assumptions, avoid fake citations, and avoid claiming certainty where uncertainty exists.
Keep the answer concise enough for an MVP."""


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

    return f"""Question: {question}
Debate mode: {mode.display_name}
Your role: {role}
Opposing role: {opposing_role}
Role guidance: {guidance}

Debater A opening:
{debater_a_opening}

Debater B opening:
{debater_b_opening}
{prior_rebuttal}
Write your rebuttal.
Respond directly to the opposing opening, identify the strongest challenge, acknowledge valid opposing points, and avoid simply repeating your opening.
Avoid fake citations and avoid claiming certainty where uncertainty exists."""


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
Debater B role: {mode.debater_b_role}
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
Do not declare absolute truth. Compare argument quality and assumptions, identify unresolved issues, recommend next steps, and suggest follow-up debates.
Avoid fake citations.

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
