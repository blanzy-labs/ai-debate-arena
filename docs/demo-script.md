# Demo Script

## Demo Goal

Show how AI Debate Arena stress-tests a question through structured disagreement, then exports the result as a local Markdown report.

## Suggested Demo Question

Should small cafes use AI tools to improve daily profit decisions?

## 60-90 Second Non-Technical Demo

1. "This tool is for structured disagreement, not one polished answer."
2. Enter the demo question.
3. Choose `Builder vs Breaker`.
4. Choose providers for Debater A, Debater B, and Judge.
5. Run the debate.
6. Show the judge summary first, then the transcript.
7. Export the Markdown report.
8. Say: "Provider-backed debates send the question and debate context to the selected AI providers, so do not use sensitive data unless that is acceptable."

## 5-8 Minute Technical Walkthrough

1. Show repo structure: `backend/`, `frontend/`, `docs/`.
2. Explain `.env.example` and backend-only provider keys.
3. Call `GET /health`.
4. Explain `POST /debate/run`.
5. Show the provider abstraction for OpenAI and Gemini.
6. Walk through the debate order: A opening, B opening, A rebuttal, B rebuttal, judge.
7. Explain judge JSON parsing and fallback behavior.
8. Show frontend result rendering.
9. Export a browser-side Markdown report.
10. Mention backend tests, frontend build, and Docker validation.
11. Reiterate no-storage and no-telemetry defaults.

## Key Talking Points

- Local-first MVP.
- Backend-only API keys.
- Structured disagreement, not guaranteed truth.
- Browser-side Markdown export.
- No database, login, telemetry, analytics, prompt history, or server-side result storage.

## Debate Arena vs Consensus Engine

Consensus Engine seeks the best balanced answer. Debate Arena seeks productive disagreement and argument stress-testing.

## Privacy and Safety Notes

The app does not browse, verify current facts, or generate real citations. Provider-backed debates send content to selected providers. Avoid sensitive or regulated data unless that provider flow is acceptable.

## Markdown Export Demo

After a successful debate, click `Export Markdown Report`. Explain that the file is generated in the browser from the current result and is not stored by the server.

## If Provider Keys Are Unavailable

- Show `/health`.
- Show the safe missing-key error from `/debate/run`.
- Explain that tests use mocked providers.
- Open `docs/sample-report.md`.
- Explain what would happen with valid local keys.

## Closing Line

AI Debate Arena is part of the Blanzy Labs AI app family.
