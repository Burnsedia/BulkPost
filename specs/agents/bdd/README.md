# Agent BDD Scenarios

This folder maps each agent spec to executable behavior scenarios.

Files:
- `autopilot-agent-bdd.md`
- `content-agent-bdd.md`
- `engagement-agent-bdd.md`
- `safety-agent-bdd.md`
- `style-profiler-agent-bdd.md`
- `optimization-agent-bdd.md`
- `trend-agent-bdd.md`
- `strategy-agent-bdd.md`
- `sales-agent-bdd.md`

Guidelines:
- Keep scenarios deterministic and implementation-agnostic.
- Assert structured output shape first, then business behavior.
- Treat services as external executors; agents only decide.
