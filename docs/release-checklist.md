# Release Checklist

Release target: `v0.1.1 - Blanzy Labs Standardization Patch`

## Repo Identity

- [ ] Canonical repo name is `ai-debate-arena`.
- [ ] Display name is AI Debate Arena.
- [ ] README uses the Blanzy Labs AI app family positioning.
- [ ] GitHub description and topics are current.
- [ ] Default branch is `main`, or the reason it was not changed is documented.

## Documentation

- [ ] README is accurate.
- [ ] `docs/disclaimer.md` exists and is linked from README.
- [ ] `docs/security-and-privacy.md` exists and is linked from README.
- [ ] `docs/local-install.md` exists.
- [ ] `docs/troubleshooting.md` exists.
- [ ] `docs/architecture.md` exists.
- [ ] Demo and sample report docs exist.
- [ ] Release notes exist under `docs/release-notes/`.
- [ ] Validation docs exist under `docs/validation/`.

## Git Safety

- [ ] No tag movement.
- [ ] No release overwrite.
- [ ] Existing `v0.1.0` tag and release remain unchanged.
- [ ] `.env` is not tracked.
- [ ] `.env` is not staged.
- [ ] `.env` is ignored by git.
- [ ] No secrets, API keys, tokens, credentials, private prompts, or sensitive data are committed.

## Validation

- [ ] Backend dependencies install cleanly.
- [ ] Backend tests pass.
- [ ] Frontend dependencies install cleanly.
- [ ] Frontend build passes.
- [ ] Frontend tests pass, if a test script exists.
- [ ] Docker Compose build passes.
- [ ] Docker smoke test passes where practical.
- [ ] `/health` returns safe JSON and does not expose key values.
- [ ] Missing-key behavior is safe.

## Security And Privacy

- [ ] Provider keys remain backend-only.
- [ ] No provider keys appear in frontend source, network responses, exported Markdown, logs, issues, screenshots, or docs.
- [ ] No localStorage/sessionStorage persistence was added.
- [ ] No database or backend storage was added.
- [ ] No telemetry or analytics was added.
- [ ] Disclaimer and security/privacy docs warn users about usage, costs, provider data flow, and sensitive data.

## Release

- [ ] Commit message: `Standardize AI Debate Arena repo documentation`.
- [ ] Tag: `v0.1.1`.
- [ ] GitHub release title: `v0.1.1 - Blanzy Labs Standardization Patch`.
- [ ] GitHub release notes source: `docs/release-notes/v0.1.1.md`.
