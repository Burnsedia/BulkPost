# Trend Agent Spec

## Role
Finds emerging topics from internal performance and external signals.

## Phase
Phase 2

## Objective
Surface high-opportunity topics/angles for upcoming content.

## Inputs
- Top posts and metrics
- External feeds/search trends
- Campaign goals

## Output Contract
```json
{
  "topics": [
    {
      "topic": "string",
      "source": "internal | external",
      "momentum": 0.0,
      "fit_score": 0.0
    }
  ],
  "summary": "string"
}
```

## Tools
- `get_top_posts(user_id)`
- `get_metrics(user_id)`
- `search_twitter(query)`
- `fetch_rss()`
- `fetch_hackernews()`

## Acceptance Criteria
- Topics include source traceability.
- Suggestions are relevant to audience/campaign.
