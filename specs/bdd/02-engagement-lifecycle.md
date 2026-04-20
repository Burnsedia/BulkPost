# Feature: Engagement Lifecycle

Goal: discover relevant posts, qualify leads, generate replies, and track activity.

Qualification rule for DM eligibility:
- Only `reply`, `mention`, and `follow` interactions count.
- Likes are excluded from DM qualification.

## Scenario 1: Discover candidate reply targets

```gherkin
Given an authenticated user has engagement enabled in GrowthPolicy
When the Engagement Agent runs discovery
Then candidate tweets are evaluated
And at least one ReplyTarget is created with status "new" when relevant
And each ReplyTarget is scoped to the current user
```

## Scenario 2: Qualify target into lead

```gherkin
Given a ReplyTarget exists with status "new"
When qualification score is above threshold
Then the ReplyTarget status becomes "queued"
And a Lead is created or updated for the source handle
And Lead.status is "qualified"
And Lead.score is evaluated for DM eligibility threshold
```

## Scenario 3: Generate reply draft for qualified target

```gherkin
Given a ReplyTarget exists with status "queued"
When the Reply Writer generates a response
Then a Reply is created with status "pending"
And Reply.target references the ReplyTarget
And Reply.text is not empty
```

## Scenario 4: Post reply and record activity

```gherkin
Given a Reply exists with status "pending"
When execution service posts it successfully
Then Reply.status becomes "posted"
And Reply.posted_at is set
And ReplyTarget.status becomes "replied"
And an Activity record of type "reply_sent" is created for the related Lead
```

## Scenario 5: Ignore low quality target

```gherkin
Given a candidate tweet is discovered
When qualification score is below threshold
Then no Reply is created
And ReplyTarget status becomes "dismissed" or is not persisted
And no Lead is created from that candidate
```

## Scenario 6: Prevent duplicate target per user

```gherkin
Given a ReplyTarget already exists for user and source_tweet_id
When discovery sees the same source_tweet_id again
Then no duplicate ReplyTarget is created
And the existing target may be updated in place
```

## Scenario 7: Exclude likes from DM qualification

```gherkin
Given a lead only liked a post without reply, mention, or follow
When lead qualification runs
Then the lead is not marked DM eligible
And no offer DM is queued
```
