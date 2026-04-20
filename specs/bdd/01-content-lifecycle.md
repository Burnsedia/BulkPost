# Feature: Autonomous Content Lifecycle

Goal: run content end-to-end without manual drafting or approval.

## Scenario 1: Generate content candidate from campaign context

```gherkin
Given an authenticated user with an active Campaign
And Prompt, SystemPrompt, and StyleProfile exist
When Autopilot triggers the Content Agent
Then a ContentItem is created with status "generated"
And the item is linked to campaign and prompt context
And content body is not empty
```

## Scenario 2: Safety check auto-queues low-risk content

```gherkin
Given a ContentItem exists with status "generated"
When Safety Agent returns should_post=true
Then ContentItem status becomes "queued"
And a Post queue item is created with status "pending"
```

## Scenario 3: Safety check blocks risky content automatically

```gherkin
Given a ContentItem exists with status "generated"
When Safety Agent returns should_post=false
Then ContentItem status becomes "blocked"
And no Post queue item is created
And block reason is recorded in logs
```

## Scenario 4: Publish queued post successfully

```gherkin
Given a queued Post exists with status "pending"
And the execution service is running
When the scheduler reaches the execution window
And the platform API returns success
Then Post status becomes "posted"
And posted_at is set
And twitter_id is stored
And linked ContentItem status becomes "published"
```

## Scenario 5: Handle publish failure without duplicate posting

```gherkin
Given a queued Post exists with status "pending"
When execution attempts to publish and the platform API fails
Then Post status becomes "failed"
And Post.error contains a failure reason
And no duplicate Post is created
And linked ContentItem does not become "published"
```
