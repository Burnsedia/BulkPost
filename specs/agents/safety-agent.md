# Safety Agent Spec

## Role
Evaluates risk and compliance for generated posts/replies before queueing or publish.

## Phase
MVP

## Objective
Prevent unsafe, spammy, or policy-violating content/actions.

## Inputs
- Candidate text
- Recent posting/reply cadence
- Growth policy settings
- Optional conversation context

## Output Contract
```json
{
  "risk_score": 0.0,
  "should_post": true,
  "severity": "low | medium | high",
  "reason": "string",
  "flags": ["spam_risk", "policy_risk", "toxicity_risk", "duplicate_risk"]
}
```

## Rules
1. High risk -> block (`should_post=false`).
2. Medium risk -> require review.
3. Low risk -> allow.
4. Must return explicit reason and flags.

## Tools
- `get_growth_policy(user_id)`
- `get_recent_posts(user_id, limit)`
- `get_recent_replies(user_id, limit)`

## Failure Handling
- If analysis fails, default to block with diagnostic reason.

## Acceptance Criteria
- No unsafe publish when blocked.
- Consistent scoring behavior across similar inputs.
