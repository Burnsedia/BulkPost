# Strategy Agent Spec

## Role
Converts trend and optimization insights into actionable plans.

## Phase
Phase 2

## Objective
Generate weekly content strategy with concrete hooks and angles.

## Inputs
- Trend Agent output
- Optimization Agent output
- Campaign constraints

## Output Contract
```json
{
  "topics": ["string"],
  "angles": ["string"],
  "hooks": ["string"],
  "weekly_plan": [
    {
      "day": "Mon",
      "topic": "string",
      "angle": "string",
      "hook": "string"
    }
  ]
}
```

## Tools
- `get_campaign_context(campaign_id)`
- `get_trend_report(user_id)`
- `get_optimization_report(user_id)`

## Acceptance Criteria
- Plan is executable by Content Agent.
- Coverage aligns with campaign goals and constraints.
