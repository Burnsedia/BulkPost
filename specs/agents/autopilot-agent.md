# Autopilot Agent Spec

## Role
Primary orchestrator for autonomous runs. Decides whether the system should `post`, `engage`, or `skip`.

## Phase
MVP

## Objective
Maximize consistent safe activity within policy constraints.

## Inputs
- GrowthPolicy
- DailyUsage (today)
- Queue health (pending/failed counts)
- Recent performance summary
- Pending reply targets count
- Last run outcomes

## Output Contract
```json
{
  "action": "post | engage | skip",
  "reason": "string",
  "priority": "low | normal | high",
  "cooldown_minutes": 0
}
```

## Decision Rules
1. If `kill_switch=true` -> `skip`.
2. If daily caps reached -> `skip`.
3. If posting window open and post quota not met -> prefer `post`.
4. If enough targets available and reply quota not met -> prefer `engage`.
5. If risk signals elevated or repeated failures -> `skip` with cooldown.

## Tools (read-only)
- `get_growth_policy(user_id)`
- `get_daily_usage(user_id, date)`
- `get_queue_state(user_id)`
- `get_recent_metrics(user_id)`
- `get_pending_reply_targets(user_id)`

## Safety Constraints
- Never requests direct DB writes.
- Never calls external platform APIs directly.
- Must include human-readable reason.

## Failure Handling
- On missing critical inputs: return `skip` with diagnostic reason.
- Log decision and context snapshot.

## Acceptance Criteria
- Produces valid structured action every run.
- Obeys kill switch and caps 100% of time.
