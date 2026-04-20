# Feature: Optimization Agent

## Scenario 1: Identify best and underperforming variants
```gherkin
Given prompt variants with performance history exist
When Optimization Agent analyzes metrics
Then output.best_variants is not empty when winners exist
And output.underperforming_variants includes weak performers
```

## Scenario 2: Suggest measurable improvements
```gherkin
Given sufficient post and reply metrics are available
When Optimization Agent generates recommendations
Then output.suggestions contains actionable items
And each suggestion maps to observed metric behavior
```

## Scenario 3: Return confidence score
```gherkin
Given Optimization Agent completes analysis
When output is returned
Then output.confidence is a numeric value between 0 and 1
```

## Scenario 4: Avoid destructive automatic changes
```gherkin
Given Optimization Agent suggests updates
When run completes
Then no prompt variants are modified directly by the agent
And changes require explicit service or user action
```
