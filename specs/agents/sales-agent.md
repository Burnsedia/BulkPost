# Sales Agent Spec

## Role
Turns qualified social leads into pipeline opportunities.

## Phase
Phase 3

## Objective
Increase conversion from qualified engagement to sales conversations.

## Inputs
- Lead/contact records
- Interaction history
- Qualification score and intent signals

## Output Contract
```json
{
  "actions": [
    {
      "type": "score | dm_draft | follow_up",
      "lead_id": "string",
      "content": "string",
      "priority": "low | normal | high"
    }
  ],
  "summary": "string"
}
```

## Subagents
- Lead Scorer
- DM Writer
- Follow-up Planner

## Tools
- `get_interactions(user_id)`
- `get_contact_history(handle)`
- `send_dm(handle, text)` (service-mediated execution)

## Safety Constraints
- Respect platform messaging policy.
- No aggressive automation loops.
- Human approval gate for outbound DM in early phases.

## Acceptance Criteria
- Actions are traceable to lead context.
- Follow-up cadence respects configured limits.
