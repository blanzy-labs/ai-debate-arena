# Local Install Guide

## Prerequisites

- Python 3.12+
- Node.js 22+
- npm
- Docker and Docker Compose

## Clone the Repository

```bash
git clone https://github.com/blanzy-labs/ai-debate-arena.git
cd ai-debate-arena
```

## Environment Setup

```bash
cp .env.example .env
```

Never commit `.env`.

## Add Provider Keys

Add local provider keys to `.env` only:

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_MODEL=gemini-2.5-flash
```

Do not put provider keys in frontend variables.

## Run with Docker Compose

```bash
docker compose up --build
```

Backend: `http://127.0.0.1:8000`

Frontend: `http://127.0.0.1:5173`

## Run Backend Manually

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Run Frontend Manually

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

## Validate Health Check

```bash
curl http://127.0.0.1:8000/health
```

Expected: `status` is `ok`, model names are visible, and API key values are hidden.

## Validate Debate Endpoint

```bash
curl -s -X POST http://127.0.0.1:8000/debate/run \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Should small cafes use AI tools to improve daily profit decisions?",
    "debate_mode": "builder_vs_breaker",
    "debater_a_provider": "openai",
    "debater_b_provider": "gemini",
    "judge_provider": "openai"
  }'
```

Without keys, `/debate/run` should return a safe missing-key error. With valid local keys, it should return a structured debate.

## Validate Frontend

Open `http://127.0.0.1:5173`.

Check that the app title, backend status, debate form, mode selector, provider selectors, result area, and export behavior work as expected.

## Export a Markdown Report

After a successful debate result, use `Export Markdown Report`. The report is generated in the browser and downloaded locally. The server does not store it.

## Troubleshooting

See [Troubleshooting](troubleshooting.md) for the standard troubleshooting guide.

- Backend not running: start FastAPI or Docker Compose and retry `/health`.
- Frontend cannot reach backend: check `VITE_API_BASE_URL`, CORS, and port `8000`.
- Missing API key: add provider keys to `.env` and restart the backend.
- Docker port conflicts: stop other services using ports `8000` or `5173`.
- Node/Python install issues: confirm versions and reinstall dependencies.
- Browser/local CORS issue: use `http://127.0.0.1:5173` or `http://localhost:5173` with the backend on port `8000`.

## Safety Reminders

Provider-backed debates send the question and generated context to selected AI providers. Do not enter sensitive data unless that is acceptable. Never commit `.env`.
