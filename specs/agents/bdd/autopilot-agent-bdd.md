# Feature: Autopilot Agent

## Scenario 1: Skip when kill switch is enabled
```gherkin
Given a user GrowthPolicy has kill_switch set to true
When Autopilot evaluates the next action
Then output.action is "skip"
And output.reason mentions kill switch
```

## Scenario 2: Skip when daily tweet cap is reached
```gherkin
Given target_tweets_per_day is 5
And DailyUsage.tweets_posted is 5
When Autopilot evaluates the next action
Then output.action is "skip"
And output.reason mentions daily cap reached
```

## Scenario 3: Prefer posting when posting quota remains
```gherkin
Given kill_switch is false
And post quota remains for today
And min_post_interval has elapsed
When Autopilot evaluates the next action
Then output.action is "post"
```

## Scenario 4: Prefer engagement when replies are available and posting is not prioritized
```gherkin
Given posting quota is met or posting interval has not elapsed
And reply quota remains
And pending reply targets exist
When Autopilot evaluates the next action
Then output.action is "engage"
```

## Scenario 5: Prefer DM offer when qualified candidates are waiting
```gherkin
Given post and reply priorities are satisfied
And qualified DM candidates are available
And DM policy limits allow sending
When Autopilot evaluates the next action
Then output.action is "dm_offer"
```

## Scenario 6: Return structured decision contract
```gherkin
Given Autopilot evaluates any valid state
When it returns a decision
Then output has fields action, reason, priority, cooldown_minutes
And action is one of post, engage, dm_offer, skip
```
