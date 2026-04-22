# Twitter Autopilot MVP Todo

- [ ] Wire PydanticAI `RunContext` deps (`user_id`, `GrowthPolicy`, `SystemPrompt`, `timezone`) into generation pipeline.
- [ ] Make `SystemPrompt` actively drive tweet/reply generation, with `.opencode` overlay fallback.
- [ ] Add safety gates before publish: duplicate check, polite/toxicity filter, high-risk review routing, kill-switch enforcement.
- [ ] Implement VPS scheduling runbook (cron/systemd timers) for all management commands with retry/backoff behavior.
- [ ] Harden production settings: env-based `SECRET_KEY`, prod `DEBUG=False`, `ALLOWED_HOSTS`, secure cookie/CSRF settings.
- [ ] Add automated tests for caps, spacing intervals, queue transitions, and publish idempotency.
- [ ] Upgrade analytics collection to pull real X metrics and persist follow/profile-visit signals.
- [ ] Add admin/API controls for growth modes and ramp schedule (`5/20 -> 8/30 -> 12/40 -> 17/50`).
- [ ] Validate prompt provenance workflow (source hash checks) and enforce manifest-based runtime loading.
- [ ] Run VPS dry-run go-live checklist and document rollback/incident response steps.
