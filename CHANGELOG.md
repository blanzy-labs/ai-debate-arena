# Changelog

## v0.1.0 - Local Debate MVP

Initial local MVP release of Mythadis AI Debate Arena.

### Added

- Local-first FastAPI backend and React/Vite frontend.
- Docker Compose support for the local backend and frontend stack.
- Backend `GET /health` endpoint.
- Backend `POST /debate/run` endpoint.
- OpenAI and Gemini provider support behind a shared provider layer.
- Backend-only provider API key and model configuration.
- Four debate modes: Optimist vs Skeptic, Builder vs Breaker, Humanist vs Technologist, and Security Lead vs Product Lead.
- Full debate workflow with opening arguments, rebuttals, and judge summary.
- Structured judge JSON parsing with safe fallback behavior.
- Frontend debate form, provider selectors, loading/progress states, result display, and safe error handling.
- Browser-side Markdown export of the current debate result.
- Sample report, architecture docs, prompt design docs, local install guide, demo script, security notes, issue templates, and contribution guide.

### Security and Privacy

- Provider API keys stay in backend environment variables and are not sent to the frontend.
- Health responses expose key presence only, not key values.
- Missing-key and provider errors return safe messages.
- Markdown export is generated in the browser and is not stored by the backend.
- The MVP has no login, database, telemetry, analytics, prompt history, report history, localStorage/sessionStorage persistence, or server-side prompt/result storage.

### Not Included

- No login/auth.
- No database.
- No prompt/result history.
- No server-side result storage.
- No telemetry/analytics.
- No localStorage/sessionStorage persistence.
- No streaming.
- No backend export endpoint.
- No PDF/DOCX export.
- No share links.
- No report history.
- No browsing/citation engine.
- No production deployment hardening.
- No enterprise compliance controls.

### Known Limitations

- Provider-backed debates send the question and generated debate context to selected AI providers.
- Debate outputs are structured arguments and summaries, not guaranteed truth or factual verification.
- The app does not browse the web, verify current facts, or generate real citations.
- The release is intended for local use and demo validation, not production hosting.
