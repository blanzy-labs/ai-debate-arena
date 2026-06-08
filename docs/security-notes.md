# Mythadis AI Debate Arena Security Notes

## Local-First Security Posture

The v0.1.0 MVP is designed to run locally. It has no login, database, telemetry, analytics, prompt history, or server-side prompt/result storage.

## API Key Handling

OpenAI and Gemini keys are backend-only environment variables. Never put provider keys in frontend code, docs, tests, screenshots, issue reports, or commits. Never commit `.env`.

## Provider Data Flow

When a debate is run, the debate question and generated debate context are sent to the selected AI providers. Do not use sensitive, confidential, regulated, or customer data unless that provider data flow is acceptable.

## No-Storage MVP Design

The backend does not store prompts or results. The frontend does not use localStorage, sessionStorage, or IndexedDB for debate history. Refreshing the page clears the current browser state.

## Browser-Side Markdown Export

Markdown export is generated in the browser from the current result and downloaded locally. There is no backend export endpoint and no server-side report retention.

## Dependency Policy

Keep dependencies minimal. Prefer official SDKs and well-maintained packages. Avoid adding packages for trivial utilities. Review transitive dependencies before adding new libraries. Do not add telemetry or analytics packages to v0.1.0.

## Suggested Local Dependency Checks

Backend:

```bash
cd backend
pip list
python -m pip audit
```

If `pip-audit` is not installed:

```bash
python -m pip install pip-audit
python -m pip audit
```

Frontend:

```bash
cd frontend
npm audit
```

Audit results can change as public advisories change, so these commands are suggested local checks rather than runtime dependencies.

## Contributor Safety Checklist

- Never commit `.env`.
- Never put API keys in frontend code.
- Never paste real keys into tests or docs.
- Avoid adding storage unless explicitly approved.
- Avoid logging prompts or results by default.
- Run backend tests and frontend build before a PR or release.
- Run secret greps before commit.

## Known v0.1.0 Security Limitations

This MVP does not include auth, a secrets manager, deployment hardening, encryption workflows, compliance controls, an advanced safety classifier, or CI security scanning. It is a local MVP for structured debate, not an enterprise security product.
