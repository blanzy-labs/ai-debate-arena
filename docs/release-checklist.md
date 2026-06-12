# Release Checklist

Release target: `v0.1.0 - Local Debate MVP`

## Git Safety

- [ ] `.env` is not tracked.
- [ ] `.env` is not staged.
- [ ] `git ls-files .env` returns nothing.

## Tests

- [ ] Backend tests pass.
- [ ] Frontend build passes.
- [ ] Docker build passes.
- [ ] Docker run smoke test passes.

## Browser Acceptance

- [ ] `/health` works.
- [ ] Debate runs with real local keys.
- [ ] Missing-key error is safe.
- [ ] Markdown export works.
- [ ] Refresh clears result.
- [ ] No key values appear in UI, network responses, source, or exported Markdown.

## Security Checks

- [ ] Secret grep clean.
- [ ] No localStorage/sessionStorage.
- [ ] No backend storage dependencies.
- [ ] No telemetry/analytics.

## Documentation

- [ ] README accurate.
- [ ] Local install guide exists.
- [ ] Security docs exist.
- [ ] Architecture doc exists.
- [ ] Demo script exists.
- [ ] Sample report exists.
- [ ] Contributing guide exists.
- [ ] Issue templates exist.

## Release

- [ ] Tag created as `v0.1.0`.
- [ ] GitHub release created with notes from `docs/release-notes-v0.1.0.md`.
