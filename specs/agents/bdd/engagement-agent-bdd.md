# Feature: Engagement Agent

## Scenario 1: Discover and qualify targets
```gherkin
Given topic signals and search tools are available
When Engagement Agent runs discovery and qualification
Then output.actions contains reply or ignore decisions
And each action contains target_tweet_id
```

## Scenario 2: Draft reply for qualified target
```gherkin
Given a target has score above relevance threshold
When Engagement Agent generates action
Then action is "reply"
And reply_text is not empty
And lead_candidate includes handle, score, reason
```

## Scenario 3: Ignore low relevance target
```gherkin
Given a target has score below relevance threshold
When Engagement Agent generates action
Then action is "ignore"
And reply_text is null or omitted
```

## Scenario 4: Prevent duplicate action for same target in one run
```gherkin
Given a target_tweet_id appears multiple times in discovery results
When Engagement Agent builds actions
Then only one action exists for that target_tweet_id
```

## Scenario 5: Return summary with structured actions
```gherkin
Given Engagement Agent completes a run
When output is returned
Then output.summary is present
And output.actions is an array of structured action objects
```

## Scenario 6: Exclude likes from DM qualification
```gherkin
Given an interaction is a like only
When Engagement Agent scores DM eligibility
Then the candidate is not DM eligible
And no DM candidate action is emitted
```

## Scenario 7: Qualify DM candidates from reply, mention, or follow
```gherkin
Given interactions include reply, mention, or follow signals
When Engagement Agent scores candidates
Then candidates above threshold are marked DM eligible
And threshold uses the configured score floor
```
