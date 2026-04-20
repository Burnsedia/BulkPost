# Feature: Strategy Agent

## Scenario 1: Build weekly plan from trend and optimization inputs
```gherkin
Given Trend Agent and Optimization Agent outputs are available
When Strategy Agent creates a plan
Then output.weekly_plan contains day, topic, angle, and hook entries
And plan items align to provided campaign constraints
```

## Scenario 2: Produce executable hooks and angles
```gherkin
Given Strategy Agent processes selected topics
When output is returned
Then output.angles and output.hooks are non-empty
And entries are specific enough for Content Agent to execute
```

## Scenario 3: Prioritize according to campaign goal
```gherkin
Given campaign goal is lead generation
When Strategy Agent produces a plan
Then weekly plan favors topics and angles with higher lead fit
```

## Scenario 4: Return structured contract
```gherkin
Given Strategy Agent completes any run
When output is returned
Then output contains topics, angles, hooks, and weekly_plan arrays
```
