# Feature: Policy and Safety Controls

Goal: enforce usage limits, timing rules, and content safety before external actions.

## Scenario 1: Daily tweet cap enforcement

```gherkin
Given GrowthPolicy.target_tweets_per_day is 5
And DailyUsage.tweets_posted is 5 for today
When Autopilot evaluates action
Then action is "skip"
And reason mentions daily tweet cap reached
```

## Scenario 2: Daily reply cap enforcement

```gherkin
Given GrowthPolicy.target_replies_per_day is 20
And DailyUsage.replies_posted is 20 for today
When Autopilot evaluates engagement
Then action is "skip"
And no Reply is queued
```

## Scenario 3: Minimum posting interval enforcement

```gherkin
Given user has a recent posted Post within min_post_interval_minutes
When scheduler attempts next post
Then publish is deferred
And Post remains "pending" until allowed time
```

## Scenario 4: Kill switch hard stop

```gherkin
Given GrowthPolicy.kill_switch is true
When scheduler and execution services run
Then no Post or Reply is published
And actions are logged as skipped due to kill switch
```

## Scenario 5: Safety blocks risky content

```gherkin
Given Content Agent generated text
When Safety Agent returns should_post=false
Then no publish action occurs
And content remains in review or rejected state
And block reason is stored in logs
```

## Scenario 6: High risk requires manual review

```gherkin
Given GrowthPolicy.review_high_risk_only is true
And Safety Agent returns high risk score
When user has not approved the item
Then status does not advance to scheduled publish
And user review is required
```
