# Content Agent Spec

## Role
Generates social content candidates aligned with campaign goals and tone constraints.

## Phase
MVP

## Objective
Produce high-quality publishable content candidates for autonomous queueing.

## Inputs
- Prompt/SystemPrompt variant
- Campaign context (goal, audience)
- Recent posts summary (for dedupe)
- Brand/tone constraints
- StyleProfile (voice, hook, CTA, phrase constraints)

## Output Contract
```json
{
  "body": "string",
  "category": "value | engagement | authority | contrast | transformation",
  "hooks": ["string"],
  "style_profile_version": 0,
  "style_match_score": 0.0,
  "estimated_risk": 0.0,
  "rationale": "string"
}
```

## Rules
1. Avoid repeating recent phrasing.
2. Keep concise, platform-ready language.
3. Return one primary content candidate per run.
4. Include rationale for traceability.
5. Conform to StyleProfile constraints and avoid banned phrases.

## Tools
- `get_prompt_variants(user_id)`
- `get_campaign_context(campaign_id)`
- `get_recent_posts(user_id, limit)`
- `get_style_profile(user_id)`
- `retrieve_knowledge(query)`

## Safety Constraints
- No direct publish.
- No unsupported claims or deceptive language.
- Must be passable to Safety Agent.

## Failure Handling
- If prompt context missing: fallback to default prompt profile.
- If style profile is stale or missing: fallback to conservative house style and include low confidence.
- If generation quality is low: request retry once, else return low-confidence candidate.

## Acceptance Criteria
- Candidate content is non-empty, categorized, and policy-compatible for safety checks.
- Output includes style profile trace fields (`style_profile_version`, `style_match_score`).
