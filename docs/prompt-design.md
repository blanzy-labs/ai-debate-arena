# Mythadis AI Debate Arena Prompt Design

## Purpose

Mythadis AI Debate Arena uses prompts to create structured disagreement around a question. The goal is not to produce a single final answer. The goal is to make assumptions, tradeoffs, risks, and unresolved questions easier to inspect.

Provider calls are made only when a debate is run. The app does not browse the web, create real citations, or store prompt/result history.

## Debate Arena vs Consensus Engine

Mythadis Consensus Engine seeks the best balanced answer.

Mythadis AI Debate Arena seeks useful disagreement. Debaters argue from different roles, then a judge summarizes argument quality, weak assumptions, unresolved issues, and practical next steps. The judge is not an oracle and does not declare absolute truth.

## Prompt Design Principles

- Keep prompts clear, practical, and short enough for the local MVP.
- Make each debater stay in a selected role without theatrical roleplay.
- Require assumptions and uncertainty to be visible.
- Treat outputs as debate arguments and tradeoffs, not guaranteed truth.
- Avoid fake citations, fake browsing claims, and unsupported certainty.
- Ask the judge to compare argument quality, not crown a permanent winner.

## Opening Argument Prompt

The opening prompt gives the debater:

- App context: structured debate, not a final answer engine
- The question
- Debate mode display name and intent
- Assigned role and role guidance
- Safety and limitation instructions
- A concise text structure

Openings use plain text, not JSON:

```text
Position:
Key Arguments:
Assumptions:
Risks or Caveats:
What Would Change My View:
```

## Rebuttal Prompt

The rebuttal prompt includes the question, mode, role guidance, both openings, and Debater A's rebuttal when Debater B is responding. It asks the debater to directly address the opposing argument, identify the strongest opposing point, acknowledge valid points, challenge assumptions, and avoid repeating the opening.

Rebuttals use plain text, not JSON:

```text
Strongest Opposing Point:
Response:
Assumptions Challenged:
Valid Points Acknowledged:
Revised Position:
```

## Judge Prompt

The judge prompt includes the full debate transcript, both role profiles, and mode-specific judge guidance. It asks for valid JSON only and tells the judge not to wrap JSON in Markdown fences.

The judge compares argument quality, assumptions, uncertainties, weak points, unresolved issues, and next steps. It does not pretend to declare absolute truth.

## Debate Mode Profiles

V1 supports four hard-coded mode profiles:

- Optimist vs Skeptic: stress-test promise versus risk.
- Builder vs Breaker: stress-test implementation versus failure modes.
- Humanist vs Technologist: stress-test human impact versus technical capability.
- Security Lead vs Product Lead: stress-test risk control versus product delivery.

Each mode defines a display name, intent, Debater A role and guidance, Debater B role and guidance, and judge guidance.

## Required Judge JSON Contract

```json
{
  "judge_summary": "string",
  "strongest_argument_a": "string",
  "strongest_argument_b": "string",
  "weakest_assumption_a": "string",
  "weakest_assumption_b": "string",
  "unresolved_questions": ["string"],
  "recommended_next_steps": ["string"],
  "suggested_follow_up_debates": ["string"]
}
```

If the judge returns invalid JSON, the backend falls back to a safe structured response so the route does not crash.

## Safety And Limitation Rules

All debate prompts include guidance to:

- Avoid inventing citations, sources, studies, statistics, or external facts.
- Avoid claiming hidden browsing, research, live checks, or external verification.
- Frame conclusions as arguments, assumptions, and tradeoffs.
- Acknowledge uncertainty when information is incomplete.
- Avoid instructions that enable harm, fraud, credential theft, privacy invasion, or other unsafe behavior.

## What v0.1.0 Intentionally Does Not Do

- No frontend debate form yet.
- No Markdown export.
- No database, login, prompt history, telemetry, or analytics.
- No server-side prompt/result storage.
- No browsing feature or citation engine.
- No streaming, background jobs, custom prompt editor, or prompt template UI.
- No provider calls during app startup.

## Future Prompt Improvements

Future slices may refine prompt wording, add richer evaluation rubrics, improve provider-specific formatting, and expose better user controls. Those changes should preserve the core product identity: structured disagreement, not consensus by default.
