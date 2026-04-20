# Feature: Content Agent

## Scenario 1: Generate content candidate from prompt and campaign context
```gherkin
Given a user has an active campaign and prompt variant
When Content Agent generates content
Then output.body is not empty
And output.category is a valid category
And output.rationale is present
```

## Scenario 2: Avoid repeating recent content wording
```gherkin
Given recent posts contain repeated phrase patterns
When Content Agent generates new content
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
When Content Agent generates content
Then generation uses default prompt profile
And output is still valid structured content
```

## Scenario 5: Never attempt direct publishing
```gherkin
Given Content Agent has generated output
When agent run completes
Then no external publish action is invoked by the agent
```

## Scenario 6: Apply style profile during generation
```gherkin
Given a style profile exists for the user
When Content Agent generates content
Then output includes style_profile_version
And output.style_match_score is numeric
And output wording follows style profile constraints
```

## Scenario 7: Fallback when style profile is missing
```gherkin
Given no style profile exists for the user
When Content Agent generates content
Then generation uses conservative fallback style
And output indicates low confidence style match
```
