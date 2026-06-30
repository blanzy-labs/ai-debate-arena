# AI Debate Arena Architecture

## Purpose

AI Debate Arena is a local-first Blanzy Labs AI app for structured disagreement. It lets two AI personas argue different sides of a question, then asks a judge model to summarize argument quality and unresolved issues.

## High-Level Architecture

```text
Browser UI
  -> FastAPI /health
  -> FastAPI /debate/run
    -> Debater A provider
    -> Debater B provider
    -> Debater A provider
    -> Debater B provider
    -> Judge provider
  <- Structured debate response
  -> Browser-side Markdown export
```

## Frontend

The frontend is React, TypeScript, and Vite. It renders the debate form, mode/provider selectors, backend status, loading hints, result panel, safe errors, and browser-side Markdown export.

The frontend calls only local backend endpoints:

- `GET /health`
- `POST /debate/run`

The frontend does not receive provider API keys and does not provide API key fields.

## Backend

The backend is Python and FastAPI. It exposes health and debate endpoints, loads configuration from environment variables, validates requests with Pydantic, and coordinates the debate workflow.

## Provider Layer

The provider layer supports OpenAI and Gemini through small provider classes behind a shared async interface. API keys and model names are loaded from backend configuration. Missing keys and provider failures return safe errors.

## Debate Workflow

`POST /debate/run` performs the workflow in a deterministic order:

1. Debater A opening
2. Debater B opening
3. Debater A rebuttal
4. Debater B rebuttal
5. Judge structured summary

The backend does not make provider calls during app startup.

## Judge JSON Contract

The judge prompt asks for JSON only. The backend parses the judge output into consistent response fields and falls back safely if JSON is invalid or incomplete.

## Browser-Side Markdown Export

Markdown export is generated in the browser from the current successful debate result. The backend does not create, store, or retain exported reports.

## Configuration

Backend provider keys and model names are configured through local environment variables. API keys remain backend-only. `VITE_API_BASE_URL` may be used by the frontend to choose the backend URL; it is not a provider secret.

## Security and Privacy Boundaries

The app is local-first, but provider-backed debates send the question and generated debate context to selected AI providers. Users should not enter sensitive, confidential, regulated, or customer data unless that provider data flow is acceptable.

See [Security And Privacy](security-and-privacy.md) and [Disclaimer](disclaimer.md).

## No-Storage MVP Design

The local MVP has no database, no login, no telemetry, no analytics, no prompt history, and no server-side prompt/result storage.

## Docker and Local Development

Docker Compose starts the backend and frontend locally. Manual startup is also supported with a Python virtual environment for the backend and npm for the frontend.

## Current Limitations

This MVP does not include auth, persistence, streaming, browsing, citation generation, provider retries beyond safe wrapping, report history, share links, or production deployment hardening.

## Future Architecture Ideas

Future work may add richer prompt controls, more robust provider handling, optional persistence, and deployment guidance. Those changes should be explicit slices, not accidental expansion.
