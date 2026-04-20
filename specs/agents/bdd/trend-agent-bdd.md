# Feature: Trend Agent

## Scenario 1: Combine internal and external signals
```gherkin
Given internal top-post metrics and external feeds are available
When Trend Agent runs
Then output.topics includes entries from internal or external sources
And each topic has source, momentum, and fit_score
```

## Scenario 2: Rank by momentum and fit
```gherkin
Given multiple candidate topics exist
When Trend Agent scores topics
Then higher momentum and higher fit topics rank above weaker topics
```

## Scenario 3: Ensure traceability
```gherkin
Given Trend Agent returns topic recommendations
When output is returned
Then each topic includes a source label
And output.summary explains why top topics were selected
```

## Scenario 4: Handle weak data gracefully
```gherkin
Given external sources are unavailable and internal data is sparse
When Trend Agent runs
Then output is still valid
And summary indicates low-confidence trend detection
```
