# Contributing to Mythadis AI Debate Arena

## Welcome

Thanks for helping improve Mythadis AI Debate Arena. This project is a local-first MVP for structured disagreement.

## Project Principles

- Keep the MVP small.
- Prefer boring, maintainable defaults.
- Avoid overbuilding.
- Preserve no-storage and no-telemetry defaults.
- Treat debate output as structured argument, not guaranteed truth.

## Local Setup

```bash
cp .env.example .env
```

Add provider keys only to `.env`. Never commit `.env`.

## Running Tests

```bash
cd backend
source .venv/bin/activate
pytest
```

## Frontend Build

```bash
cd frontend
npm install
npm run build
```

## Docker Validation

```bash
docker compose config
docker compose build
```

Use `docker compose up -d` when you need to validate the running stack.

## Security and Privacy Rules

- API keys stay backend-only.
- Never commit `.env`.
- Do not paste secrets into issues, PRs, tests, docs, screenshots, or logs.
- Do not add frontend key fields.
- Do not log prompts or results by default.
- Do not add telemetry or analytics.

## Prompt Contribution Rules

Prompt changes should preserve:

- no fake citations
- no hidden browsing claims
- uncertainty handling
- structured disagreement
- judge is not an oracle

## No-Storage Default

Do not add a database, prompt history, report history, localStorage, sessionStorage, or server-side prompt/result storage unless explicitly approved in a scoped slice.

## Pull Request Expectations

Before a PR or release, run backend tests, frontend build, and Docker validation where practical.

Secret check:

```bash
grep -R "OPENAI_API_KEY" frontend/src frontend/index.html frontend/package.json || true
grep -R "GEMINI_API_KEY" frontend/src frontend/index.html frontend/package.json || true
OPENAI_PREFIX="s""k-"
GEMINI_PREFIX="AI""za"
grep -R "$OPENAI_PREFIX" frontend/src frontend/index.html frontend/package.json backend/app docs .env.example || true
grep -R "$GEMINI_PREFIX" frontend/src frontend/index.html frontend/package.json backend/app docs .env.example || true
```

Do not scan or print `.env`.

## Issue Guidelines

Use the issue templates. Do not include secrets, API keys, customer data, or sensitive debate content.

## What Not to Add Without Discussion

- Login/auth
- Database/storage
- Telemetry/analytics
- New providers
- New debate modes
- PDF/DOCX export
- Share links
- Browsing/citation engine
- Deployment hardening or CI/CD

## Release Target

Current release target: `v0.1.0 - Local Debate MVP`.
