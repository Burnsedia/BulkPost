# Feature: Content Agent

## Scenario 1: Generate draft from prompt and campaign context
```gherkin
Given a user has an active campaign and prompt variant
When Content Agent generates a draft
Then output.body is not empty
And output.category is a valid category
And output.rationale is present
```

## Scenario 2: Avoid repeating recent content wording
```gherkin
Given recent posts contain repeated phrase patterns
When Content Agent generates a new draft
Then output.body does not copy recent phrasing verbatim
```

## Scenario 3: Return hooks and estimated risk
```gherkin
Given Content Agent completes generation
When output is produced
Then output.hooks is present
And output.estimated_risk is a numeric value
```

## Scenario 4: Fallback when prompt variant is missing
```gherkin
Given no prompt variant is available for the user
When Content Agent generates a draft
Then generation uses default prompt profile
And output is still valid structured content
```

## Scenario 5: Never attempt direct publishing
```gherkin
Given Content Agent has generated output
When agent run completes
Then no external publish action is invoked by the agent
```
