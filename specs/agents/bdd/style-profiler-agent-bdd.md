# Feature: Style Profiler Agent

## Scenario 1: Build style profile from imported tweets
```gherkin
Given a user has imported tweets
When Style Profiler Agent runs
Then output includes hook patterns, CTA patterns, and tone markers
And output.style_profile_version is present
```

## Scenario 2: Increment version on rebuild
```gherkin
Given a style profile already exists for a user
When Style Profiler Agent rebuilds the profile
Then style_profile_version increments
And updated profile is persisted
```

## Scenario 3: Fallback on low sample size
```gherkin
Given imported tweet sample size is below minimum threshold
When Style Profiler Agent runs
Then output.confidence is low
And fallback style rules are returned
```
