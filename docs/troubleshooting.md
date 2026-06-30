# Troubleshooting

## Backend Unavailable

Confirm the backend is running:

```bash
curl http://localhost:8000/health
```

If it fails, start the backend with Docker Compose or from `backend/`:

```bash
docker compose up --build
```

or:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Cannot Reach Backend

- Confirm the backend is on port `8000`.
- Confirm the frontend uses `VITE_API_BASE_URL=http://localhost:8000`.
- Restart the frontend after changing environment variables.
- Use `http://localhost:5173` or `http://127.0.0.1:5173` with the backend on port `8000`.

## Provider Key Is Missing

Copy the example file and add provider keys locally:

```bash
cp .env.example .env
```

Set keys only in `.env`:

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
```

Do not commit `.env`, paste keys into frontend files, or include keys in issues, logs, screenshots, or exported reports.

## Provider Call Fails

- Confirm the selected provider has a valid local key.
- Confirm the configured model name is available to your provider account.
- Check provider rate limits, billing status, and usage limits.
- Try `/health` to confirm the backend sees key presence without exposing key values.

## Docker Port Conflicts

AI Debate Arena uses:

- Backend: `8000`
- Frontend: `5173`

Stop other local services on those ports, or update `docker-compose.yml` locally for your environment.

## Markdown Export Does Not Download

- Run a debate successfully first.
- Check browser download permissions.
- Confirm pop-up/download blocking is not preventing the file save.

## Sensitive Data Reminder

Provider-backed debates send the question and generated debate context to selected providers. Do not enter sensitive, confidential, regulated, proprietary, personal, or client data unless you understand and accept the provider and infrastructure risks.
