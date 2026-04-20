# Sales Agent Spec

## Role
Turns qualified social leads into pipeline opportunities.

## Phase
MVP

## Objective
Increase conversion from qualified engagement to conversations by autonomously DMing a lead magnet and app link.

## Inputs
- Lead/contact records
- Interaction history
- Qualification score and intent signals
- Suppression and cooldown state

## Output Contract
```json
{
  "actions": [
    {
      "type": "score | send_offer_dm | follow_up | suppress",
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
- Offer DM Writer
- Follow-up Planner

## Tools
- `get_interactions(user_id)`
- `get_contact_history(handle)`
- `get_qualified_leads(user_id)`
- `get_suppression_state(user_id, lead_id)`
- `send_dm(handle, text)` (service-mediated execution)

## Safety Constraints
- Respect platform messaging policy.
- No aggressive automation loops.
- DM only if score threshold is met (recommended `>= 70`).
- Enforce per-lead cooldown and do-not-contact suppression.
- Send only approved offer payload (lead magnet + app link).

## Acceptance Criteria
- Actions are traceable to lead context.
- Follow-up cadence respects configured limits.
- Sales action output includes structured offer tracking context.
