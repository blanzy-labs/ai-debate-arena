# Mythadis AI Debate Arena

**The books are fiction. The questions are real.**

Mythadis AI Debate Arena is a local-first open-source tool for structured disagreement and argument stress-testing. It lets two AI personas argue different sides of a question, then asks a judge model to summarize argument quality, assumptions, unresolved questions, and next steps.

Release target: `v0.1.0 - Local Debate MVP`.

## Mythadis Labs Context

Mythadis Labs is the open-source project series connected to the broader Mythadis creative work. The fictional books provide the atmosphere; the software projects are real tools built around practical questions.

AI Debate Arena is App #2 in the Mythadis Labs series. It is designed to stress-test ideas through structured disagreement rather than produce a single consensus answer.

## What The App Does

Debate Arena runs a local FastAPI backend and React/Vite frontend. The browser collects a question, debate mode, and provider choices. The backend calls configured OpenAI and Gemini providers, runs opening arguments, rebuttals, and a judge step, then returns a structured debate result for display and browser-side Markdown export.

Provider API keys stay in backend environment variables. The frontend never receives provider keys.

## Debate Arena vs Consensus Engine

Consensus Engine seeks the best balanced answer. Debate Arena seeks productive disagreement.

Debate Arena is useful when you want to expose assumptions, tradeoffs, weak points, and follow-up questions before making a decision. The judge summary is not an oracle or a fact-checking engine; it is a structured synthesis of the debate.

## Current v0.1.0 Features

- React/Vite frontend
- FastAPI backend
- Docker Compose local stack
- Backend `GET /health`
- Backend `POST /debate/run`
- Provider layer for OpenAI and Gemini
- Configurable backend-only API keys and model names
- Four V1 debate modes:
  - Optimist vs Skeptic
  - Builder vs Breaker
  - Humanist vs Technologist
  - Security Lead vs Product Lead
- Opening argument, rebuttal, and judge workflow
- Structured judge JSON parsing with safe fallback
- Frontend debate form
- Provider selectors
- Loading and progress states
- Result display panel with judge summary, transcript, and models used
- Safe frontend error handling for network, CORS, validation, missing-key, and provider errors
- Browser-side Markdown export
- Sample report
- Security and privacy docs
- Issue templates
- Contribution guide

## Intentionally Not Included

The `v0.1.0` local MVP intentionally does not include:

- No login/auth
- No database
- No prompt/result history
- No server-side result storage
- No telemetry/analytics
- No localStorage/sessionStorage persistence
- No streaming
- No backend export endpoint
- No PDF/DOCX export
- No share links
- No report history
- No browsing/citation engine
- No production deployment hardening
- No enterprise compliance controls

## Prerequisites

- Python 3.12+
- Node.js 22+
- npm
- Docker and Docker Compose, for containerized local runs

## Setup

Create a local environment file:

```bash
cp .env.example .env
```

Add provider keys to `.env` only. Never commit `.env`.

## Environment Variables

Backend configuration is loaded from environment variables. API keys stay backend-only and are never sent to the frontend. The health endpoint exposes only whether provider keys are configured.

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_MODEL=gemini-2.5-flash
```

Empty API keys do not break health checks. Running a provider-backed debate requires valid local keys for the selected providers.

## Run With Docker Compose

Run the full local stack:

```bash
docker compose up --build
```

Frontend: `http://localhost:5173`

Backend health: `http://localhost:8000/health`

Stop the stack:

```bash
docker compose down
```

Docker Compose reads `.env`, not `.env.example`.

## Run Manually

Install and run the backend locally:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Install and run the frontend locally in a separate terminal:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Open the frontend at `http://localhost:5173`. The backend health endpoint is available at `http://localhost:8000/health`.

## Browser Testing

Suggested smoke test:

1. Open `http://localhost:5173`.
2. Confirm backend status is available.
3. Submit an empty debate topic and confirm client-side validation appears.
4. Submit a real topic with valid local provider keys.
5. Confirm the debate completes.
6. Confirm the judge summary, transcript, models used, and export button appear.
7. Refresh the page and confirm the result is cleared.

Suggested question:

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

## Markdown Export

After a successful debate, use `Export Markdown Report`. The Markdown report is generated in the browser from the current result and downloaded locally. The backend does not create, store, or retain exported reports.

A static example is available in [Sample Report](docs/sample-report.md).

## Privacy And Data Flow

Mythadis AI Debate Arena is local-first, but provider-backed debates still send the debate question and generated debate context to the selected AI providers when a debate is run.

API keys are loaded by the FastAPI backend from local environment variables. The frontend never receives OpenAI or Gemini keys.

The `v0.1.0` local MVP has no login, database, telemetry, analytics, prompt history, local browser persistence, or server-side prompt/result storage.

Do not enter sensitive, confidential, regulated, or customer data unless you are comfortable sending that content to the selected providers under their terms and policies.

## Documentation

- [Architecture](docs/architecture.md)
- [Security and Privacy](docs/security.md)
- [Security Notes](docs/security-notes.md)
- [Prompt Design](docs/prompt-design.md)
- [Local Install Guide](docs/local-install.md)
- [Demo Script](docs/demo-script.md)
- [Sample Report](docs/sample-report.md)
- [Release Notes v0.1.0](docs/release-notes-v0.1.0.md)
- [Release Checklist](docs/release-checklist.md)
- [Disclaimer](docs/disclaimer.md)
- [Changelog](CHANGELOG.md)

## Contributing And Security

- [Contributing](CONTRIBUTING.md)
- [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- [Prompt Improvement Template](.github/ISSUE_TEMPLATE/prompt_improvement.md)

Do not include `.env`, API keys, secrets, customer data, or sensitive debate content in issues, pull requests, screenshots, logs, or exported reports.

## Release Status

`v0.1.0 - Local Debate MVP` is release-ready for local use and demo validation. It is not production hardened and does not claim enterprise compliance, hosted deployment readiness, or factual verification of model outputs.
