# Security and Privacy

## Summary

Mythadis AI Debate Arena is a local-first MVP. It is designed to avoid storage and keep provider API keys out of the browser.

## Local-First Does Not Mean Provider-Private

When a debate is run, the question and generated debate context are sent to the selected AI providers. Do not enter sensitive, confidential, regulated, or customer data unless you are comfortable sending it to those providers under their terms and policies.

## API Key Handling

OpenAI and Gemini keys live in backend environment variables. The frontend never receives provider API keys and should never contain provider key fields.

Never commit `.env`, real keys, screenshots with keys, or examples containing key-like fragments.

## Provider Data Flow

The backend sends prompts to the selected provider for each debate step. Provider responses are returned to the browser as a structured debate result.

## No Server-Side Storage

The v0.1.0 MVP has no login, database, telemetry, analytics, prompt history, or server-side result storage.

## Browser-Side Markdown Export

Markdown export is created in the browser from the current result and downloaded locally. The server does not generate, store, or retain exported reports.

## What Not to Enter

Avoid sensitive personal data, customer data, regulated data, confidential business data, secrets, credentials, and private incident details unless sending that content to the selected providers is acceptable.

## Dependency Safety

Dependencies should stay minimal and purposeful. Prefer official SDKs and maintained libraries. Run local dependency checks when preparing releases.

## Contributor Rules

Contributors must not commit `.env`, paste secrets into issues or PRs, add storage by default, add telemetry, or put provider keys in frontend code.

## Known v0.1.0 Security Limitations

This MVP does not include auth, a secrets manager, formal security audit, rate limiting, abuse protection, compliance controls, or deployment hardening.

## Related Documents

- [Security Notes](security-notes.md)
- [Architecture](architecture.md)
- [Local Install Guide](local-install.md)
