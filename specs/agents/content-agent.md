# Content Agent Spec

## Role
Generates social content drafts aligned with campaign goals and tone constraints.

## Phase
MVP

## Objective
Produce high-quality publishable draft candidates for queueing.

## Inputs
- Prompt/SystemPrompt variant
- Campaign context (goal, audience)
- Recent posts summary (for dedupe)
- Brand/tone constraints

## Output Contract
```json
{
  "body": "string",
  "category": "value | engagement | authority | contrast | transformation",
  "hooks": ["string"],
  "estimated_risk": 0.0,
  "rationale": "string"
}
```

## Rules
1. Avoid repeating recent phrasing.
2. Keep concise, platform-ready language.
3. Return one primary draft per run.
4. Include rationale for traceability.

## Tools
- `get_prompt_variants(user_id)`
- `get_campaign_context(campaign_id)`
- `get_recent_posts(user_id, limit)`
- `retrieve_knowledge(query)`

## Safety Constraints
- No direct publish.
- No unsupported claims or deceptive language.
- Must be passable to Safety Agent.

## Failure Handling
- If prompt context missing: fallback to default prompt profile.
- If generation quality low: request retry once, else return low-confidence draft.

## Acceptance Criteria
- Draft non-empty, categorized, and policy-compatible for safety review.
