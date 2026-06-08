# Mythadis AI Debate Arena

**The books are fiction. The questions are real.**

Mythadis AI Debate Arena is a local-first open-source tool for structured disagreement and argument stress-testing. This repository is App #2 in the Mythadis Labs project series.

This release target is `v0.1.0 - Local Debate MVP`. The current implementation is the project foundation only: a FastAPI backend skeleton, a React/Vite frontend skeleton, environment configuration, Docker Compose, and starter documentation.

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
npm run dev
```

Open the frontend at `http://localhost:5173`. The backend health endpoint is available at `http://localhost:8000/health`.

## Environment Variables

Backend configuration is loaded from environment variables. API keys stay backend-only and are never sent to the frontend. The health endpoint exposes only whether provider keys are configured.

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_MODEL=gemini-2.5-flash
```

Empty API keys are valid for this foundation slice and do not break health checks.

## Privacy and Data Flow

Mythadis AI Debate Arena is local-first, but provider-backed debates still send the debate question and generated debate context to the selected AI providers when a debate is run.

API keys are loaded by the FastAPI backend from local environment variables. The frontend never receives OpenAI or Gemini keys.

The `v0.1.0` local MVP does not include login, a database, telemetry, analytics, prompt history, or server-side result storage.

Markdown export is generated in the browser from the current result and downloaded locally. The server does not create, store, or retain exported reports.

Do not enter sensitive, confidential, regulated, or customer data unless you are comfortable sending that content to the selected AI providers under their terms and policies.

## Docker Commands

Run the full local stack:

```bash
docker compose up --build
```

Stop the stack:

```bash
docker compose down
```

Docker Compose reads `.env`, not `.env.example`.

## Current Scope

Included in this slice:

- Monorepo structure with `backend/`, `frontend/`, and `docs/`
- FastAPI app with `GET /health`
- React/Vite frontend with backend status display
- Environment config for OpenAI and Gemini key presence plus model names
- Docker Compose for local backend and frontend services

Not included yet:

- Login
- Database
- Server-side prompt or result storage
- Prompt history
- Telemetry or analytics
- Real OpenAI or Gemini calls
- Debate workflow
- Markdown export
- Frontend debate form
- Provider abstraction
