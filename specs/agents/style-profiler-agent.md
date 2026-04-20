# Style Profiler Agent Spec

## Role
Learns the user's writing style from imported X posts and produces a reusable style profile for generation agents.

## Phase
MVP

## Objective
Convert tweet history into actionable style constraints that improve content and reply authenticity.

## Inputs
- ImportedTweet history for the user
- Optional performance metrics by post
- Existing StyleProfile (for versioned updates)

## Output Contract
```json
{
  "style_profile_version": 0,
  "avg_length_chars": 0,
  "hook_patterns": ["string"],
  "cta_patterns": ["string"],
  "tone_markers": ["string"],
  "banned_phrases": ["string"],
  "style_rules": "string",
  "confidence": 0.0
}
```

## Rules
1. Learn only from the authenticated user's imported content.
2. Prefer recent, high-performing samples when weighting style signals.
3. Do not include private/sensitive content in style rules.
4. Increment profile version on each successful rebuild.

## Tools
- `get_imported_tweets(user_id, limit)`
- `get_post_metrics(user_id, range)`
- `get_existing_style_profile(user_id)`
- `save_style_profile(user_id, profile)`

## Safety Constraints
- Never infer style from other users' content.
- Never expose raw imported tweet text in output fields except derived patterns.

## Failure Handling
- If sample size is below minimum threshold, return low confidence with fallback style rules.
- If profile save fails, return diagnostic error for retry.

## Acceptance Criteria
- Produces valid style profile schema with versioning.
- Can be consumed directly by Content and Engagement agents.
