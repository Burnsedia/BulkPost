# Engagement Agent Spec

## Role
Discovers relevant posts, qualifies opportunities, and drafts replies.

## Phase
MVP

## Objective
Generate meaningful engagement and create qualified leads.

## Inputs
- GrowthPolicy thresholds
- Topic/campaign signals
- Existing interaction history
- Pending reply capacity

## Output Contract
```json
{
  "actions": [
    {
      "action": "reply | ignore",
      "target_tweet_id": "string",
      "reply_text": "string | null",
      "lead_candidate": {
        "handle": "string",
        "score": 0.0,
        "reason": "string"
      }
    }
  ],
  "summary": "string"
}
```

## Internal Subflows
1. Discovery: generate and run queries.
2. Qualification: score relevance and lead potential.
3. Reply writing: draft contextual response.

## Tools
- `search_twitter(query)`
- `get_user_profile(handle)`
- `get_past_interactions(handle)`
- `retrieve_knowledge(query)`

## Safety Constraints
- No spam loops.
- Respect relevance threshold.
- Reply only when added value is clear.

## Failure Handling
- If discovery fails: return empty actions + reason.
- If qualification uncertain: default `ignore`.

## Acceptance Criteria
- No duplicate target actions.
- Reply drafts are specific and non-generic.
- Lead candidates include explicit scoring rationale.
