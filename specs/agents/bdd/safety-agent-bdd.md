# Feature: Safety Agent

## Scenario 1: Block high-risk content
```gherkin
Given candidate content contains high-risk signals
When Safety Agent evaluates the content
Then output.should_post is false
And output.severity is "high"
And output.flags includes at least one risk flag
```

## Scenario 2: Allow low-risk content
```gherkin
Given candidate content has no meaningful risk signals
When Safety Agent evaluates the content
Then output.should_post is true
And output.severity is "low" or "medium"
```

## Scenario 3: Require explanation and flags for every result
```gherkin
Given Safety Agent evaluates any content
When output is returned
Then output.reason is not empty
And output.flags is present
And output.risk_score is numeric
```

## Scenario 4: Default-safe behavior on evaluation failure
```gherkin
Given Safety Agent cannot complete evaluation due to internal error
When fallback behavior is applied
Then output.should_post is false
And output.reason indicates diagnostic failure
```

## Scenario 5: Detect duplicate/cadence risk
```gherkin
Given recent posts or replies show near-duplicate content and high frequency
When Safety Agent evaluates a new candidate
Then output.flags includes duplicate_risk or spam_risk
```
