# v0.1.0 - Local Debate MVP

Mythadis AI Debate Arena is a local-first open-source debate tool that lets AI personas argue different sides of a question, then produces a structured judge summary and browser-side Markdown report.

The books are fiction. The questions are real.

## What Is Included

- React/Vite frontend and FastAPI backend.
- Docker Compose local stack.
- Backend health endpoint at `GET /health`.
- Debate endpoint at `POST /debate/run`.
- OpenAI and Gemini provider support with backend-only API keys.
- Four V1 debate modes:
  - Optimist vs Skeptic
  - Builder vs Breaker
  - Humanist vs Technologist
  - Security Lead vs Product Lead
- Opening argument, rebuttal, and judge workflow.
- Structured judge JSON summary with safe fallback behavior.
- Frontend debate form, provider selectors, loading/progress states, result panel, and safe error handling.
- Browser-side Markdown export.
- Sample report, architecture docs, prompt design docs, local install guide, demo script, security notes, issue templates, and contribution guide.

## How To Run Locally

```bash
cp .env.example .env
docker compose up --build
```

Add local provider keys to `.env` before running real provider-backed debates. Do not commit `.env`.

Frontend: `http://localhost:5173`

Backend health: `http://localhost:8000/health`

## Privacy And Security

Provider-backed debates send the debate question and generated debate context to the selected AI providers. Do not enter sensitive, confidential, regulated, or customer data unless that provider data flow is acceptable.

Provider API keys are loaded by the backend from local environment variables. The frontend does not receive provider keys.

The MVP has no login, database, telemetry, analytics, prompt history, report history, localStorage/sessionStorage persistence, or server-side prompt/result storage.

## Known Limitations

- Not production hardened.
- No enterprise compliance controls.
- No streaming.
- No backend export endpoint.
- No PDF/DOCX export.
- No share links.
- No browsing/citation engine.
- No factual verification of model outputs.

## Suggested Demo Question

```text
Should small cafes use AI tools to improve daily profit decisions?
```

Suggested selections:

```text
Mode: Builder vs Breaker
Debater A: OpenAI
Debater B: Gemini
Judge: OpenAI
```

## Validation Checklist

- Backend tests pass.
- Frontend build passes.
- Docker Compose build passes.
- Docker Compose smoke test passes.
- `/health` returns safe JSON.
- Browser debate run completes with valid local keys.
- Missing-key error is safe.
- Markdown export works.
- Exported Markdown contains no API keys.
- Refresh clears the current result.
- No result history appears.
- No API key values appear in the UI, network responses, source, or exported Markdown.
